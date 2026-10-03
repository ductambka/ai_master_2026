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


def test_repeated_prediction_claims_do_not_reuse_one_gold_claim():
    gold = [{"id": "q1", "relevant_ids": ["d1"], "claims": [{"text": "A fact", "citation_ids": ["d1"]}]}]
    predictions = [
        {
            "id": "q1",
            "retrieved_ids": ["d1"],
            "claims": [
                {"text": "A fact", "citation_ids": ["d1"]},
                {"text": "A fact", "citation_ids": ["d1"]},
            ],
        }
    ]

    metrics = evaluate_records(gold, predictions)["metrics"]

    assert metrics["citation_coverage"]["exact"] == {"covered": 1, "total": 1, "value": 1.0}
    assert metrics["citation_coverage"]["semantic_lite"]["covered"] == 1
    assert metrics["citation_coverage"]["semantic_lite"]["total"] == 1
    assert metrics["unsupported_claim_rate"] == pytest.approx(0.5)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"k": 0}, "k must be at least 1"),
        ({"k": True}, "k must be at least 1"),
        ({"semantic_threshold": -0.1}, "semantic_threshold must be between 0 and 1"),
        ({"semantic_threshold": True}, "semantic_threshold must be between 0 and 1"),
        ({"semantic_threshold": float("nan")}, "semantic_threshold must be between 0 and 1"),
        ({"semantic_threshold": float("inf")}, "semantic_threshold must be between 0 and 1"),
        ({"seed": True}, "seed must be an integer"),
    ],
)
def test_evaluator_rejects_invalid_metric_parameters(kwargs, message):
    with pytest.raises(EvaluationError, match=message):
        evaluate_records([], [], **kwargs)


def test_cli_rejects_invalid_metric_parameters_without_traceback(tmp_path):
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
            "--k",
            "0",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).parents[1] / "src")},
    )
    assert result.returncode == 2
    assert "must be a positive integer" in result.stderr
    assert "Traceback" not in result.stderr


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
