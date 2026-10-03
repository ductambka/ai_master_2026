#!/usr/bin/env python3
"""Run the dependency-free lab template and emit auditable artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    if not isinstance(config.get("name"), str) or not config["name"].strip():
        raise ValueError("config.name must be a non-empty string")
    if not isinstance(config.get("seed"), int) or isinstance(config["seed"], bool):
        raise ValueError("config.seed must be an integer")
    dataset = config.get("dataset")
    if not isinstance(dataset, list) or not dataset:
        raise ValueError("config.dataset must be a non-empty list")
    width = None
    for index, row in enumerate(dataset):
        if not isinstance(row, dict) or not isinstance(row.get("label"), str) or not row["label"].strip():
            raise ValueError(f"config.dataset[{index}] must contain a non-empty string label")
        features = row.get("features")
        if not isinstance(features, list) or not features:
            raise ValueError(f"config.dataset[{index}].features must be a non-empty list")
        if width is None:
            width = len(features)
        if len(features) != width or any(
            isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)
            for value in features
        ):
            raise ValueError("config.dataset features must be finite numeric rows of equal width")
    acceptance = config.get("acceptance")
    minimum = acceptance.get("min_accuracy") if isinstance(acceptance, dict) else None
    if isinstance(minimum, bool) or not isinstance(minimum, (int, float)) or not math.isfinite(minimum) or not 0 <= minimum <= 1:
        raise ValueError("config.acceptance.min_accuracy must be between 0 and 1")
    return config


def nearest_centroid(dataset: list[dict[str, Any]]) -> tuple[list[str], float]:
    labels = sorted({row["label"] for row in dataset})
    centroids = {
        label: [
            sum(row["features"][index] for row in dataset if row["label"] == label)
            / sum(row["label"] == label for row in dataset)
            for index in range(len(dataset[0]["features"]))
        ]
        for label in labels
    }
    predictions = []
    for row in dataset:
        predictions.append(
            min(
                labels,
                key=lambda label: math.dist(row["features"], centroids[label]),
            )
        )
    accuracy = sum(predicted == row["label"] for predicted, row in zip(predictions, dataset)) / len(dataset)
    return predictions, accuracy


def run(config_path: Path, output_dir: Path) -> dict[str, Any]:
    config = load_config(config_path)
    _, accuracy = nearest_centroid(config["dataset"])
    minimum = config["acceptance"]["min_accuracy"]
    metrics = {
        "lab": config["name"],
        "seed": config["seed"],
        "samples": len(config["dataset"]),
        "accuracy": accuracy,
        "min_accuracy": minimum,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(metrics_path.read_bytes()).hexdigest()
    manifest = {
        "schema_version": 1,
        "lab": config["name"],
        "status": "PASS" if accuracy >= minimum else "FAIL",
        "config": config_path.name,
        "seed": config["seed"],
        "artifacts": [{"path": "metrics.json", "sha256": digest}],
        "metrics": metrics,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = run(args.config, args.output_dir)
    print(json.dumps(manifest, sort_keys=True))
    return 0 if manifest["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
