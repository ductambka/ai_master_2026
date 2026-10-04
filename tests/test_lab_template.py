import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab_template"


def test_lab_template_runs_and_writes_verified_manifest(tmp_path):
    output_dir = tmp_path / "output"
    result = subprocess.run(
        [
            sys.executable,
            str(LAB / "run_lab.py"),
            "--config",
            str(LAB / "config.json"),
            "--output-dir",
            str(output_dir),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    metrics_path = output_dir / "metrics.json"
    assert manifest["status"] == "PASS"
    assert manifest["metrics"]["accuracy"] == 1.0
    assert manifest["artifacts"][0]["sha256"] == hashlib.sha256(metrics_path.read_bytes()).hexdigest()
    assert "secret" not in result.stdout.lower()


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("dataset", [], "non-empty list"),
        ("seed", True, "integer"),
        ("acceptance", {"min_accuracy": 2}, "between 0 and 1"),
    ],
)
def test_lab_config_validation_rejects_invalid_contract(tmp_path, field, value, message):
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("lab_runner", LAB / "run_lab.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    config = json.loads((LAB / "config.json").read_text(encoding="utf-8"))
    config[field] = value
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        module.load_config(path)


def test_lab_cli_reports_invalid_config_without_traceback(tmp_path):
    config = tmp_path / "config.json"
    config.write_text("{not-json\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(LAB / "run_lab.py"),
            "--config",
            str(config),
            "--output-dir",
            str(tmp_path / "output"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "JSONDecodeError" not in result.stderr
    assert "Traceback" not in result.stderr
    assert "Expecting property name" in result.stderr


def test_lab_cli_reports_output_errors_without_traceback(tmp_path):
    output_path = tmp_path / "output"
    output_path.write_text("not-a-directory", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(LAB / "run_lab.py"),
            "--config",
            str(LAB / "config.json"),
            "--output-dir",
            str(output_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert "File exists" in result.stderr
