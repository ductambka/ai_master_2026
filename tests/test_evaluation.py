import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from ai_master.evaluation import EvaluationError, evaluate_files, evaluate_records


FIXTURE = Path(__file__).parents[1] / "docs" / "labs" / "L07" / "fixtures"


def test_evaluator_computes_provider_independent_metrics_and_checksum():
    result = evaluate_files(FIXTURE / "gold.jsonl", FIXTURE / "predictions.jsonl", k=2, seed=7)
    assert result["version"] == "1.0"
    assert result["seed"] == 7
    assert len(result["input_checksum"]) == 64
    assert result["metrics"]["recall_at_k"]["value"] == pytest.approx(1.0)
    assert result["metrics"]["citation_coverage"]["exact"]["value"] == pytest.approx(0.5)
    assert result["metrics"]["citation_coverage"]["semantic_lite"]["value"] == pytest.approx(2 / 3)
    assert result["metrics"]["unsupported_claim_rate"] == pytest.approx(0.5)


def test_empty_inputs_are_valid_and_return_zero_metrics():
    result = evaluate_records([], [], seed=3)
    assert result["records"] == 0
    assert result["metrics"]["recall_at_k"]["value"] == 0.0
    assert result["metrics"]["unsupported_claim_rate"] == 0.0


def test_malformed_input_is_rejected(tmp_path):
    gold = tmp_path / "gold.jsonl"
    predictions = tmp_path / "predictions.jsonl"
    gold.write_text('{"id":"q1"}\n', encoding="utf-8")
    predictions.write_text("not-json\n", encoding="utf-8")
    with pytest.raises(EvaluationError, match="not valid JSON"):
        evaluate_files(gold, predictions)


def test_cli_output_is_json(tmp_path):
    output = tmp_path / "result.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_master.cli",
            "evaluate",
            "--gold",
            str(FIXTURE / "gold.jsonl"),
            "--predictions",
            str(FIXTURE / "predictions.jsonl"),
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).parents[1] / "src")},
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(output.read_text(encoding="utf-8"))["version"] == "1.0"
