# Giáo án triển khai theo tuần

Tài liệu này là checklist thực thi cho 36 tuần. Mỗi tuần gồm bốn phần: seminar
lý thuyết, lab xây dựng, paper clinic và review. Giảng viên có thể đổi dataset
hoặc framework, nhưng phải giữ nguyên bằng chứng tối thiểu: baseline, split,
metric, test, seed/config và failure analysis.

## Cách dùng

Trước buổi học, học viên đọc mục lý thuyết và tạo một issue có câu hỏi/hypothesis.
Trong lab, làm smoke test trước rồi mới chạy đầy đủ. Cuối tuần nộp artifact theo
contract trong [learner handbook](learner-handbook.md). Giảng viên chỉ đánh dấu
hoàn thành khi lệnh xác minh chạy được từ repository root.

## Kế hoạch 36 tuần

| Tuần | Chủ đề và mục tiêu đo được | Seminar / paper clinic | Lab và sản phẩm | Xác minh cuối tuần |
|---:|---|---|---|---|
| 1 | Vector, norm, dot product; giải thích gradient của một hàm vô hướng | Hình học của biểu diễn; đọc phần phương pháp của một paper regression | Notebook tính tay và finite-difference gradient | Có 3 ví dụ đúng dấu và sai số được ghi lại |
| 2 | Kỳ vọng, Bayes, likelihood; chọn learning rate và stopping rule | Từ objective đến evidence | Tối ưu hàm lồi với nhiều learning rate | Loss giảm; seed, config và stopping rule trong manifest |
| 3 | Package, typing, exception, test, CLI và Git | Đọc code thay vì chỉ đọc notebook | Chuyển notebook thành package nhỏ | `pytest -q` và quickstart chạy từ môi trường sạch |
| 4 | Schema, missingness, provenance và data contract | Data card có thể bác bỏ claim nào? | Validator + data card trên dữ liệu tổng hợp | Input sai bị từ chối với lỗi có thể hành động |
| 5 | Random/group/temporal split, leakage và contamination | Phân biệt proxy tốt với leakage | Tạo leakage có chủ ý rồi sửa split | Báo cáo metric trước/sau leakage, không gộp hai kết quả |
| 6 | Label noise, sampling, confounding và DAG | Annotation disagreement và giới hạn nhân quả | Guideline gán nhãn + audit 30 mẫu | Có agreement, ví dụ bất đồng và limitation |
| 7 | Linear/logistic regression, loss và regularization | Baseline rẻ nhất có thể bác bỏ điều gì? | **L01** logistic regression từ đầu | Loss giảm, accuracy và calibration được ghi lại |
| 8 | Cây quyết định, impurity, feature interaction, missing values | So sánh inductive bias | Ba baseline trên cùng split | Bảng metric và confusion matrix cùng một split |
| 9 | Imbalance, threshold, precision/recall, ROC/PR | Metric nào phù hợp với chi phí lỗi? | Threshold sweep + error buckets | Operating point có lý do và trade-off |
| 10 | Bootstrap, CI, paired comparison, ablation | Khi nào chênh lệch là noise? | **L03** benchmark ML cổ điển | CI/độ phân tán và không cherry-pick seed |
| 11 | Computation graph, chain rule, reverse-mode autodiff | Kiểm tra gradient như một scientific instrument | **L04** mini autograd | `pytest -q tests/test_autograd.py` đạt; sai số `< 1e-5` |
| 12 | Activation, initialization, batching, loss | Vì sao overfit một batch hữu ích? | MLP toy, cố ý overfit sample nhỏ | Có test forward/backward và failure log |
| 13 | SGD, momentum, Adam, dropout, weight decay, checkpoint | Optimizer là giả định hay chỉ là tiện ích? | Trainer có config và resume | Resume cho kết quả tương đương trong tolerance định trước |
| 14 | Seed, determinism, artifact manifest | Tái lập khác tái tạo thế nào? | **L05** trainer deep learning | Reviewer mới chạy được README và kiểm tra manifest |
| 15 | Receptive field, padding, pooling, inductive bias | CNN đưa prior vào mô hình ra sao? | CNN encoder toy + kernel/pooling ablation | Bảng ablation và phân tích lỗi |
| 16 | Sequence, recurrence, padding và masking | Metric theo độ dài chuỗi | Classifier sequence toy | Error buckets theo độ dài, không chỉ accuracy tổng |
| 17 | Q/K/V, softmax, causal mask, complexity | Attention có nhìn thấy tương lai không? | Attention tối giản | Test causal mask và test shape đều đạt |
| 18 | Embedding geometry, cosine, normalization, probing | Cosine similarity không đồng nghĩa “hiểu” | **L06** encoder + retrieval | Recall@k trên gold set và failure cases |
| 19 | Tokenization, context window, pretraining, instruction tuning | Token budget là ràng buộc sản phẩm | Tokenizer toy + prompt matrix | Ghi token budget và trường hợp vượt budget |
| 20 | Few-shot, decomposition, structured output, refusal | Prompt là contract có version | Parser/schema + prompt contract | Output sai schema bị bắt và xử lý an toàn |
| 21 | Lexical/vector retrieval, chunking, reranking | Chunk size thay đổi evidence thế nào? | Index top-k có fixture | Recall@k, query khó và case không tìm thấy |
| 22 | Groundedness, citation, unsupported claim, offline eval | Proxy metric và human eval | **L07** RAG có citation | Chạy lệnh evaluate; unsupported-claim rate được báo cáo |
| 23 | Agent state, plan/observe/act, termination | Agent loop hay workflow có state? | Loop có timeout và step budget | Có termination reason, không retry vô hạn |
| 24 | Tool schema, allowlist, sandbox, permission, idempotency | Side effect cần policy nào? | **L08** registry + sandbox | Tool ngoài allowlist bị chặn fail-closed |
| 25 | Memory, approval gate, escalation, pause/resume | Human-in-loop không phải nút “OK” giả | Tool có side effect giả lập + policy | Thao tác rủi ro dừng trước side effect và resume an toàn |
| 26 | Task success, trajectory, cost, safety và failure taxonomy | Đọc trajectory như đọc log thí nghiệm | Replay set + failure report | Báo cáo tách planning/tool/safety failure |
| 27 | HTTP contract, schema, health/readiness, timeout | API contract trước implementation | **L09** adapter serving | Health/readiness và schema test đạt |
| 28 | Logs, metrics, traces, correlation ID | Quan sát được không có nghĩa là log mọi thứ | **L10** trace end-to-end | Trace theo request ID; không có secret/PII |
| 29 | Load, queue, retry, rate limit, SLO, cost | Error budget và chi phí biên | Load test nhỏ + cost worksheet | Nêu SLO, giới hạn và hành vi khi quá budget |
| 30 | CI/CD, image, migration, rollback, runbook | Release rehearsal và điều kiện dừng | Deploy rehearsal reference service | Rollback drill có lệnh, bằng chứng và owner |
| 31 | Asset, actor, attack surface, abuse case | Threat model là artefact sống | Threat model cho capstone | Mỗi rủi ro có severity, owner và test |
| 32 | Prompt injection, exfiltration, PII, retention | Red-team có thể tái hiện | **L11** attack set + report | Attack có reproduction, mitigation và residual risk |
| 33 | Subgroup metrics, calibration, system/model card | Fairness trade-off và risk acceptance | Risk register + governance review | Có quyết định go/no-go có điều kiện |
| 34 | Claim, protocol, artifact, internal validity | Preregistration và chống HARKing | **L12** replication: khóa protocol | Được duyệt dataset, split, baseline, threat model |
| 35 | Ablation, novelty, negative result, IMRaD | Review chéo theo evidence | Chạy extension + paper draft | Có baseline, ablation, failure analysis và giới hạn |
| 36 | Evidence, limitations, reproducibility, defense | Viva rehearsal và phản biện | Demo offline + final artifact + viva | Reviewer mới chạy quickstart; trả lời được “what would falsify?” |

## Template cho từng tuần

```text
Week:
Question / hypothesis:
Required reading:
Theory notes:
Smoke-test command:
Full lab command:
Dataset/version/split:
Baseline and metric:
Expected artifact:
Known failure to reproduce:
Evidence / exit code:
Threats to validity:
What would falsify this result?
Next experiment:
```

## Mapping lệnh với repository

Các lệnh dưới đây là smoke test chuẩn; lệnh đầy đủ của từng lab nằm trong
README tương ứng. Chạy từ thư mục gốc:

```bash
python -m compileall -q src service
pytest -q
./tooling/run_lab_template.sh
python -m ai_master.cli demo
python -m ai_master.cli train --epochs 25
python -m ai_master.cli evaluate \
  --gold docs/labs/L07/fixtures/gold.jsonl \
  --predictions docs/labs/L07/fixtures/predictions.jsonl \
  --output /tmp/l07-evaluation.json --k 2 --seed 7
```

Nếu một tuần dùng framework ngoài repository, vẫn phải lưu command, phiên bản
dependency, seed/config, output checksum và test tối thiểu trong artifact. Không
đưa API key, cookie, PII hoặc dữ liệu production vào artifact hay log.

## Tiêu chí hoàn thành chương trình

- 36 artifact theo format `W##-short-name-vN` hoặc một archive có index.
- 12 lab có test và failure analysis tương ứng.
- Ba mốc tích hợp được ký duyệt ở tuần 14, 22 và 30.
- Responsible AI audit hoàn tất trước khi demo capstone.
- Capstone có code, report, demo, viva, threat model và hướng dẫn tái lập.

