from __future__ import annotations

import json
import logging
import re
import secrets
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

MAX_BODY_BYTES = 64 * 1024
REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
SECRET_KEY_RE = re.compile(r"token|secret|password|passwd|cookie|authorization|api[_-]?key|private[_-]?key", re.I)
SECRET_VALUE_RE = re.compile(r"(?i)(bearer\s+|sk-[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9_]{8,})")


class RequestValidationError(ValueError):
    pass


def _redact(value: Any) -> Any:
    """Return JSON-safe log data with secret-like keys and values removed."""
    if isinstance(value, dict):
        return {key: "[REDACTED]" if SECRET_KEY_RE.search(key) else _redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, str) and SECRET_VALUE_RE.search(value):
        return SECRET_VALUE_RE.sub("[REDACTED]", value)
    return value


def _request_id(header_value: str | None) -> str:
    if header_value and REQUEST_ID_RE.fullmatch(header_value):
        return header_value
    return secrets.token_hex(16)


def _json_body(raw: bytes) -> dict[str, Any]:
    if len(raw) > MAX_BODY_BYTES:
        raise RequestValidationError("request body is too large")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RequestValidationError("body must be valid JSON") from exc
    if not isinstance(value, dict):
        raise RequestValidationError("body must be a JSON object")
    return value


def _validate_request_framing(headers: Any) -> None:
    """Require the single JSON framing mode understood by this service."""
    content_type = headers.get("Content-Type", "")
    media_type = content_type.split(";", 1)[0].strip().lower()
    if media_type != "application/json":
        raise RequestValidationError("Content-Type must be application/json")
    if headers.get("Transfer-Encoding"):
        raise RequestValidationError("Transfer-Encoding is not supported")
    content_lengths = headers.get_all("Content-Length", [])
    if len(content_lengths) != 1:
        raise RequestValidationError("exactly one Content-Length is required")


def _execute_tool(payload: dict[str, Any]) -> dict[str, Any]:
    if set(payload) != {"tool", "input"}:
        raise RequestValidationError("request must contain exactly tool and input")
    tool = payload["tool"]
    tool_input = payload["input"]
    if not isinstance(tool, str) or not isinstance(tool_input, dict):
        raise RequestValidationError("tool must be a string and input must be an object")

    if tool == "course.echo":
        if set(tool_input) != {"message"} or not isinstance(tool_input["message"], str):
            raise RequestValidationError("course.echo input requires only a string message")
        if len(tool_input["message"]) > 1000:
            raise RequestValidationError("message must be at most 1000 characters")
        return {"tool": tool, "result": {"message": tool_input["message"]}}

    if tool == "course.lesson_summary":
        if set(tool_input) != {"lesson_id"} or not isinstance(tool_input["lesson_id"], str):
            raise RequestValidationError("course.lesson_summary input requires only a string lesson_id")
        summaries = {
            "L04": "Scalar autodiff, topological backpropagation, and gradient checking.",
            "L07": "Offline retrieval evaluation with citation coverage and unsupported-claim checks.",
        }
        lesson_id = tool_input["lesson_id"]
        if lesson_id not in summaries:
            raise RequestValidationError("unknown lesson_id")
        return {"tool": tool, "result": {"lesson_id": lesson_id, "summary": summaries[lesson_id]}}

    raise PermissionError("tool is not in the allowlist")


class ServiceHandler(BaseHTTPRequestHandler):
    server_version = "CourseReferenceService/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        # Access logs are emitted as structured records by _log; avoid default plaintext logs.
        return

    def _log(self, event: str, request_id: str, **fields: Any) -> None:
        record = {"event": event, "request_id": request_id, **_redact(fields)}
        logging.getLogger("course_reference_service").info(json.dumps(record, sort_keys=True))

    def _send(self, status: HTTPStatus, body: dict[str, Any], request_id: str) -> None:
        encoded = json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("X-Request-ID", request_id)
        self.send_header("Cache-Control", "no-store")
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        request_id = _request_id(self.headers.get("X-Request-ID"))
        if self.path == "/healthz":
            status = HTTPStatus.OK
            self._send(status, {"status": "ok", "service": "course-reference-service"}, request_id)
        elif self.path == "/readyz":
            status = HTTPStatus.OK
            self._send(status, {"status": "ready", "checks": {"in_process_tools": "ok"}}, request_id)
        else:
            status = HTTPStatus.NOT_FOUND
            self._send(status, {"error": "not_found"}, request_id)
        self._log("http_request", request_id, method="GET", path=self.path, status=status.value)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        request_id = _request_id(self.headers.get("X-Request-ID"))
        if self.path != "/v1/tools/execute":
            # Do not leave an unconsumed body on a persistent connection.
            self.close_connection = True
            self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"}, request_id)
            return
        content_length = self.headers.get("Content-Length")
        try:
            _validate_request_framing(self.headers)
            try:
                length = int(content_length or "-1")
            except (TypeError, ValueError) as exc:
                raise RequestValidationError("invalid or oversized Content-Length") from exc
            if length < 0 or length > MAX_BODY_BYTES:
                raise RequestValidationError("invalid or oversized Content-Length")
            payload = _json_body(self.rfile.read(length))
            result = _execute_tool(payload)
        except PermissionError as exc:
            # Do not leave an unread request body on a persistent connection.
            # Closing the connection prevents the next request from being
            # parsed from attacker-controlled leftovers.
            self.close_connection = True
            self._send(HTTPStatus.FORBIDDEN, {"error": "tool_not_allowed", "detail": str(exc)}, request_id)
            # Log only routing metadata. The rejected tool input is untrusted
            # user data and must not be copied into the audit log.
            self._log(
                "tool_denied",
                request_id,
                method="POST",
                path=self.path,
                tool=payload.get("tool") if "payload" in locals() else None,
            )
            return
        except RequestValidationError as exc:
            self.close_connection = True
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "detail": str(exc)}, request_id)
            self._log("request_rejected", request_id, method="POST", path=self.path, reason=str(exc))
            return
        self._send(HTTPStatus.OK, result, request_id)
        self._log("tool_executed", request_id, method="POST", path=self.path, tool=payload["tool"])


def create_server(host: str = "127.0.0.1", port: int = 8080) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), ServiceHandler)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Safe course reference service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    server = create_server(args.host, args.port)
    print(f"course-reference-service listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
