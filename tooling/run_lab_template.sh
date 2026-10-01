#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
python3 "$repo_root/examples/lab_template/run_lab.py" \
  --config "$repo_root/examples/lab_template/config.json" \
  --output-dir "$repo_root/examples/lab_template/output"
