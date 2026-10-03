# Sổ tay lý thuyết và thực hành theo module

Tài liệu này là “lesson plan” dùng trong seminar và lab. Giảng viên có thể thay dataset hoặc framework, nhưng không thay đổi contract: baseline, split, metric, test và bằng chứng tái lập.

## M0 — Nền tảng toán, Python và engineering (tuần 1–3)

**Câu hỏi trung tâm:** một phép cập nhật mô hình được suy ra, cài đặt và kiểm chứng thế nào?

**Lý thuyết:** vector/ma trận và hình học; đạo hàm và chain rule; xác suất cơ bản; hàm mất mát và gradient descent; cấu trúc package, typing, exception, test, CLI và Git.

**Thực hành:** notebook gradient số; tối ưu hàm bậc hai với sweep learning rate; chuyển thành module có test; tạo manifest gồm Python version, config và hash output.

**Sản phẩm:** notebook tái lập và package nhỏ. **Đạt khi:** có ít nhất một test biên, giải thích được sai số finite difference, và người khác chạy được từ README.

## M1 — Dữ liệu và causal thinking (tuần 4–6)

**Câu hỏi trung tâm:** dữ liệu này đại diện cho quyết định nào, và bằng chứng nào có thể bị rò rỉ?

**Lý thuyết:** schema/provenance; missing data; sampling; temporal/group split; leakage và contamination; label noise; confounding, DAG và giới hạn suy luận nhân quả.

**Thực hành:** viết data card; validator cho schema; dựng một ví dụ leakage có chủ ý; so sánh random split với group/temporal split; audit 30 mẫu và ghi disagreement.

**Sản phẩm:** data card, split script, labeling guideline. **Đạt khi:** split được khóa, có checksum/version, metric leakage được trình bày riêng và không tuyên bố nhân quả từ tương quan.

## M2 — Machine learning cổ điển (tuần 7–10)

**Câu hỏi trung tâm:** baseline rẻ nhất có thể bác bỏ giả thuyết nào?

**Lý thuyết:** regression, regularization, cây quyết định, feature engineering, calibration, class imbalance, threshold, bootstrap và confidence interval.

**Thực hành:** L01 logistic regression; ba baseline trên cùng split; confusion matrix theo subgroup; threshold sweep; L03 benchmark có CI và error analysis.

**Sản phẩm:** benchmark report. **Đạt khi:** nêu metric chính/phụ, operating point, khoảng tin cậy và trường hợp metric có thể gây hiểu lầm.

## M3 — Deep learning và training loop (tuần 11–14)

**Câu hỏi trung tâm:** gradient đúng và training ổn định được chứng minh ra sao?

**Lý thuyết:** computation graph, backprop, activation, initialization, batching, SGD/momentum/Adam, regularization, checkpoint và determinism.

**Thực hành:** L04 mini autograd; MLP toy; overfit một batch để debug; checkpoint/resume; L05 trainer. Không tối ưu tốc độ trước khi có gradient check và test.

**Sản phẩm:** trainer có config. **Đạt khi:** gradient check < `1e-5`, resume không làm thay đổi đáng kể kết quả, và có failure log cho một lần chạy hỏng.

## M4 — Representation learning (tuần 15–18)

**Câu hỏi trung tâm:** representation tốt cho tác vụ nào và hỏng ở đâu?

**Lý thuyết:** convolution/inductive bias; sequence/masking; attention Q-K-V; embedding geometry; cosine similarity; probing và retrieval.

**Thực hành:** CNN encoder toy; sequence classifier theo độ dài; attention causal mask; L06 index và recall@k; ablation normalization/chunk size.

**Sản phẩm:** encoder + ablation report. **Đạt khi:** tách rõ metric downstream và metric representation, có failure cases và không suy ra “hiểu” chỉ từ cosine score.

## M5 — LLM, retrieval và RAG (tuần 19–22)

**Câu hỏi trung tâm:** câu trả lời có được hỗ trợ bởi nguồn và có thể kiểm toán không?

**Lý thuyết:** token/context; prompting; structured output; lexical/vector retrieval; chunking/reranking; groundedness; citation; unsupported claim; offline evaluation.

**Thực hành:** prompt matrix; parser/schema; retrieval fixture; L07 RAG với gold/prediction JSONL; đo recall@k, citation coverage và unsupported-claim rate.

**Sản phẩm:** RAG service hoặc notebook. **Đạt khi:** câu trả lời thiếu bằng chứng bị đánh dấu hoặc abstain, output có citation, metric lexical được ghi rõ là proxy chứ không thay thế human eval.

## M6 — Agents và tools (tuần 23–26)

**Câu hỏi trung tâm:** agent được phép làm gì, dừng khi nào và ai phê duyệt hành động rủi ro?

**Lý thuyết:** state machine, planning, tool schema, allowlist, sandbox, idempotency, memory, approval gate, trajectory evaluation và budget.

**Thực hành:** loop có timeout/step budget; L08 tool registry; tool giả lập có side effect; policy deny; replay trajectory; phân loại failure theo planning/tool/safety.

**Sản phẩm:** agent có policy. **Đạt khi:** tool lạ bị từ chối fail-closed, thao tác rủi ro cần approval, và mọi trajectory có request ID/cost/termination reason.

## M7 — Production AI và vận hành (tuần 27–30)

**Câu hỏi trung tâm:** hệ thống có đáng tin, quan sát được và hoàn tác được không?

**Lý thuyết:** API/schema, health/readiness, timeout/retry, logs/metrics/traces, SLO, load, cost, CI/CD, image, migration và rollback.

**Thực hành:** L09 HTTP adapter; L10 observability; load test nhỏ; cost worksheet; deploy rehearsal với reference service; rollback drill.

**Sản phẩm:** service + runbook. **Đạt khi:** health/readiness phân biệt đúng, log đã khử secret, có rate/budget limit, và rollback được mô tả bằng lệnh cùng điều kiện dừng.

## M8 — Responsible AI, security và governance (tuần 31–33)

**Câu hỏi trung tâm:** ai có thể bị hại, bằng đường nào, và bằng chứng giảm thiểu là gì?

**Lý thuyết:** threat modeling; prompt injection/exfiltration; privacy/retention; subgroup metrics; fairness trade-off; model/system card; risk acceptance.

**Thực hành:** L11 red-team attack set; threat model; privacy review; subgroup evaluation; risk register có owner, severity, likelihood, test và mitigation.

**Sản phẩm:** audit package. **Đạt khi:** mỗi rủi ro quan trọng tái hiện được, có quyết định go/no-go, và không gửi dữ liệu nhạy cảm ra ngoài.

## M9 — Capstone và research (tuần 34–36)

**Câu hỏi trung tâm:** claim có thể bác bỏ, tái lập và mở rộng thế nào?

**Lý thuyết:** IMRaD; protocol/preregistration; baseline; ablation; negative result; threat to validity; artifact review và viva.

**Thực hành:** L12 replication; khóa dataset/split; chạy baseline; một extension có giả thuyết; viết report; demo offline; rehearsal phản biện.

**Sản phẩm:** code/artifact, paper, demo và viva. **Đạt khi:** người khác chạy được, report tách evidence khỏi inference, có giới hạn và kế hoạch forward-fix/rollback.

