import json
import logging
import threading
from http.client import HTTPConnection

import pytest

from service import create_server


@pytest.fixture()
def service_server():
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def request(server, method, path, body=None, headers=None):
    connection = HTTPConnection(*server.server_address, timeout=2)
    encoded = json.dumps(body).encode() if body is not None else None
    connection.request(method, path, body=encoded, headers={"Content-Type": "application/json", **(headers or {})})
    response = connection.getresponse()
    result = response.status, response.getheaders(), json.loads(response.read())
    connection.close()
    return result


def test_health_readiness_and_request_id(service_server):
    status, headers, body = request(service_server, "GET", "/healthz", headers={"X-Request-ID": "audit-123"})
    assert status == 200
    assert body["status"] == "ok"
    assert dict(headers)["X-Request-ID"] == "audit-123"
    assert request(service_server, "GET", "/readyz")[2]["status"] == "ready"


def test_allowlisted_tool_returns_safe_result(service_server):
    status, headers, body = request(
        service_server,
        "POST",
        "/v1/tools/execute",
        {"tool": "course.lesson_summary", "input": {"lesson_id": "L07"}},
    )
    assert status == 200
    assert body["result"]["lesson_id"] == "L07"
    assert dict(headers)["X-Request-ID"]


def test_unknown_tool_is_rejected(service_server):
    status, _, body = request(service_server, "POST", "/v1/tools/execute", {"tool": "shell.exec", "input": {"command": "id"}})
    assert status == 403
    assert body["error"] == "tool_not_allowed"


def test_schema_validation_and_redacted_structured_log(service_server, caplog):
    caplog.set_level(logging.INFO, logger="course_reference_service")
    status, _, body = request(
        service_server,
        "POST",
        "/v1/tools/execute",
        {"tool": "course.echo", "input": {"message": "hello", "api_key": "do-not-log"}},
    )
    assert status == 400
    assert body["error"] == "invalid_request"
    assert "do-not-log" not in caplog.text
    assert '"event": "request_rejected"' in caplog.text


def test_oversized_body_and_invalid_request_id_are_rejected_or_replaced(service_server):
    oversized = {"tool": "course.echo", "input": {"message": "x" * 100_000}}
    status, _, body = request(service_server, "POST", "/v1/tools/execute", oversized)
    assert status == 400
    assert body["error"] == "invalid_request"

    status, headers, body = request(
        service_server,
        "GET",
        "/healthz",
        headers={"X-Request-ID": "contains spaces"},
    )
    assert status == 200
    assert body["status"] == "ok"
    assert dict(headers)["X-Request-ID"] != "contains spaces"


def test_non_numeric_content_length_is_rejected_as_bad_request(service_server):
    connection = HTTPConnection(*service_server.server_address, timeout=2)
    connection.request(
        "POST",
        "/v1/tools/execute",
        body=b"{}",
        headers={"Content-Type": "application/json", "Content-Length": "not-a-number"},
    )
    response = connection.getresponse()
    body = json.loads(response.read())
    connection.close()

    assert response.status == 400
    assert body["error"] == "invalid_request"
