# Bản đồ đào tạo 36 tuần

Mỗi tuần gồm 90 phút seminar, 120 phút lab, 60 phút paper clinic và 30 phút review. Các mục “thực hành” là vertical slice đủ nhỏ để chạy được trước khi mở rộng.

| Tuần | Module / chủ đề | Lý thuyết cần nắm | Thực hành và sản phẩm | Kiểm tra cuối tuần |
|---:|---|---|---|---|
| 1 | M0: vector, ma trận, đạo hàm | dot product, norm, Jacobian, chain rule | notebook phép tính + gradient số | giải thích 1 gradient bằng hình và công thức |
| 2 | M0: xác suất và tối ưu | kỳ vọng, Bayes, likelihood, gradient descent | tối ưu hàm lồi với nhiều learning rate | loss giảm, ghi rõ seed và stopping rule |
| 3 | M0: Python/engineering | module, typing, test, CLI, Git | tái cấu trúc notebook thành package nhỏ | `pytest -q` xanh, README chạy được |
| 4 | M1: schema và data contracts | kiểu dữ liệu, missingness, provenance | schema validator + data card | input sai bị từ chối rõ ràng |
| 5 | M1: split và leakage | train/validation/test, temporal split, contamination | L02 phát hiện leakage | so sánh metric trước/sau leakage |
| 6 | M1: labeling và causal thinking | label noise, sampling, confounding, DAG | guideline gán nhãn + audit mẫu | inter-annotator agreement và limitation |
| 7 | M2: regression | linear/logistic regression, regularization, calibration | L01 logistic regression từ đầu | loss, accuracy và calibration baseline |
| 8 | M2: trees và feature engineering | entropy, impurity, interactions, missing values | 3 baseline trên cùng split | bảng metric + confusion matrix |
| 9 | M2: imbalance và threshold | precision/recall, ROC/PR, threshold cost | threshold sweep + error buckets | nêu trade-off và operating point |
| 10 | M2: thống kê thực nghiệm | bootstrap, CI, paired comparison, ablation | L03 benchmark ML cổ điển | báo cáo CI không cherry-pick seed |
| 11 | M3: computation graph | forward/backward, chain rule, numerical check | L04 mini autograd | sai số gradient tuyệt đối < 1e-5 |
| 12 | M3: neural network | activation, initialization, batch, loss | MLP nhỏ trên dataset toy | overfit sample nhỏ có chủ đích |
| 13 | M3: optimizer và regularization | SGD, momentum, Adam, dropout, weight decay | trainer có config và checkpoint | resume cho kết quả tương đương |
| 14 | M3: reproducibility | seed, determinism, artifact manifest | L05 trainer deep learning | người khác chạy lại được từ README |
| 15 | M4: convolution | receptive field, padding, pooling, inductive bias | encoder CNN tối giản | ablation kernel/pooling |
| 16 | M4: sequence models | token sequence, recurrence, masking | classifier sequence toy | phân tích lỗi theo độ dài |
| 17 | M4: attention | Q/K/V, softmax, causal mask, complexity | attention tối giản | test mask không nhìn tương lai |
| 18 | M4: embeddings | cosine, normalization, representation probing | encoder + retrieval baseline | L06 recall@k trên gold set |
| 19 | M5: tokenization và LLM | BPE khái niệm, context, pretraining, instruction | tokenizer toy + prompt matrix | kiểm soát token budget |
| 20 | M5: prompting và structured output | few-shot, decomposition, schema, refusal | prompt contract + parser | output sai schema được xử lý |
| 21 | M5: retrieval | lexical/vector retrieval, chunking, reranking | index top-k có fixture | recall@k và failure cases |
| 22 | M5: RAG evaluation | groundedness, citation, unsupported claim | L07 RAG có citation | unsupported-claim rate được báo cáo |
| 23 | M6: agent loop | state, planning, observe-act, termination | agent loop trên tool giả lập | loop có budget và timeout |
| 24 | M6: tool contract | allowlist, schema, permission, idempotency | L08 tool registry + sandbox | tool ngoài allowlist bị chặn |
| 25 | M6: memory và human-in-loop | short/long memory, approval gate, escalation | policy cho thao tác rủi ro | chứng minh pause/resume an toàn |
| 26 | M6: agent evaluation | task success, trajectory, cost, safety | replay set + failure taxonomy | report không chỉ dùng success rate |
| 27 | M7: serving | HTTP contract, health/readiness, timeout | L09 adapter + schema | health/readiness và schema test |
| 28 | M7: observability | logs, metrics, traces, correlation ID | L10 trace end-to-end | log không chứa secret |
| 29 | M7: reliability và cost | load, queue, retry, rate limit, budget | load test + cost worksheet | nêu SLO và giới hạn |
| 30 | M7: release | CI, image, migration, rollback, runbook | deploy rehearsal reference service | rollback drill có bằng chứng |
| 31 | M8: threat modeling | asset, actor, attack surface, abuse case | threat model capstone | mỗi rủi ro có owner/test |
| 32 | M8: red team và privacy | prompt injection, exfiltration, PII, retention | L11 attack set + report | severity, reproduction, mitigation |
| 33 | M8: fairness và governance | subgroup metrics, calibration, documentation | risk register + model/system card | quyết định go/no-go có điều kiện |
| 34 | M9: replication | claim, protocol, artifact, validity | chọn paper và khóa protocol | preregistration nội bộ |
| 35 | M9: extension | ablation, novelty, negative result, writing | chạy experiment và paper draft | review chéo theo IMRaD |
| 36 | M9: defense | evidence, limitations, reproducibility | L12 replication + demo + viva | artifact chạy được, trả lời phản biện |

## Quy ước sản phẩm

Mỗi tuần nộp một thư mục hoặc archive có `README`, lệnh chạy, test, config/seed, output, ảnh/bảng nếu cần, failure log và mục “what would falsify this result?”. Tên artifact nên có dạng `W##-short-name-vN`.

## Mốc tích hợp

- Tuần 6: data card và split bất biến.
- Tuần 10: benchmark có khoảng tin cậy.
- Tuần 14: trainer tái lập.
- Tuần 22: RAG có đánh giá claim/citation.
- Tuần 30: service có runbook và rollback.
- Tuần 33: risk register được review.
- Tuần 36: capstone package hoàn chỉnh.

