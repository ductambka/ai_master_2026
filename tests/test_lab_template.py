import hashlib
import json
import subprocess
import sys
from pathlib import Path


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
