# Lab book

Mỗi lab phải lưu `README`, `run.sh` hoặc lệnh chạy, seed, môi trường, kết quả, failure log và một đoạn “what would falsify this result?”.

## Bộ khung lab

[`examples/lab_template`](../examples/lab_template) là template chuẩn để bắt
đầu lab mới. Template có config seed, runner, artifact `metrics.json`,
`manifest.json` và test subprocess. Chạy từ repository root bằng
`./tooling/run_lab_template.sh`; runner chỉ dùng Python standard library và
không yêu cầu secret.

| ID | Đề bài | Deliverable | Nghiệm thu |
|---|---|---|---|
| L01 | Cài logistic regression từ đầu | model + unit tests | loss giảm, accuracy baseline đạt |
| L02 | Phát hiện leakage | data card + split script | chứng minh metric trước/sau leakage |
| L03 | Benchmark ML cổ điển | bảng 3 baseline | CI và confusion matrix |
| L04 | Mini autograd | scalar graph + backward | gradient check sai số < 1e-5 |
| L05 | Trainer deep learning | loop + checkpoint | resume cho kết quả tương đương |
| L06 | Embedding/retrieval | index + top-k API | recall@k trên gold set |
| L07 | RAG có citation | retriever + answerer | unsupported claim bị phát hiện |
| L08 | Agent tool policy | tool registry + sandbox | tool ngoài allowlist bị chặn |
| L09 | Serving | HTTP adapter + schema | health/readiness + load test |
| L10 | Observability | logs/metrics/traces | trace một request end-to-end |
| L11 | Red team | attack set + report | severity, reproduction, mitigation |
| L12 | Replication | paper + artifact | người khác chạy lại được |

## Mẫu báo cáo lab

```text
Question:
Hypothesis:
Dataset/version/split:
Baseline:
Metric + confidence interval:
Seed/environment:
Result:
Error analysis:
Threats to validity:
Rollback or containment:
Next experiment:
```
