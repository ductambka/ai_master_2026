# Sổ tay sử dụng theo tuần

Tài liệu này là checklist thao tác cho toàn bộ 36 tuần. Đọc cùng
[bản đồ chương trình](curriculum-map.md), [sổ tay module](module-handbooks.md)
và [giáo án](weekly-lesson-plans.md). Mỗi tuần tạo một thư mục artifact có tên
`W##-short-name-vN`; không ghi secret, PII hay dữ liệu production.

## Quy trình chung

1. Tạo issue ghi câu hỏi, hypothesis, dataset/split và tiêu chí falsify.
2. Chạy smoke test với dữ liệu nhỏ trước khi chạy đầy đủ.
3. Lưu command, exit code, seed, môi trường, metric, failure log và checksum.
4. Review chéo: một người chạy lại, một người kiểm tra metric, một người đọc
   threat model.
5. Chỉ đánh dấu DONE khi artifact có README, test và hướng dẫn tái lập.

Lệnh khởi tạo dùng cho mọi tuần:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
```

## Checklist 36 tuần

Mỗi mục gồm: **mục tiêu**, **thao tác**, **xác minh**, **nộp** và **lỗi cần
quan sát**.

### M0 — Nền tảng toán, Python và engineering

#### Tuần 1 — Vector, ma trận, đạo hàm

- **Mục tiêu:** tính dot product, norm và gradient; giải thích chain rule.
- **Thao tác:** viết notebook phép tính tay và finite-difference gradient cho
  một hàm vô hướng; lưu seed nếu có dùng random.
- **Xác minh:** so sánh gradient giải tích với gradient số ở ít nhất 3 điểm;
  ghi sai số tuyệt đối và dấu của từng thành phần.
- **Nộp:** `W01-foundations-v1/README.md`, notebook, bảng sai số, failure log.
- **Lỗi cần quan sát:** step finite difference quá lớn/nhỏ, nhầm shape hoặc
  nhầm dấu đạo hàm.

#### Tuần 2 — Xác suất và tối ưu

- **Mục tiêu:** nối likelihood với loss và chọn learning rate/stopping rule.
- **Thao tác:** tối ưu hàm lồi với ít nhất 3 learning rate; ghi config và
  đường cong loss.
- **Xác minh:** loss giảm theo tiêu chí định trước; chạy lại cùng seed cho kết
  quả tương đương trong tolerance.
- **Nộp:** config, plot/table loss, manifest và ghi chú vì sao chọn stopping rule.
- **Lỗi cần quan sát:** learning rate làm loss phân kỳ, dừng do hết bước nhưng
  chưa hội tụ, hoặc chỉ báo cáo lần chạy tốt nhất.

#### Tuần 3 — Python và engineering

- **Mục tiêu:** chuyển notebook thành package có typing, test, CLI và README.
- **Thao tác:** chạy `python -m compileall -q src service`; thêm một test biên
  và một lỗi đầu vào có thông báo hành động được.
- **Xác minh:** `pytest -q` và quickstart chạy từ repository root.
- **Nộp:** package nhỏ, test, CLI help, README và manifest môi trường.
- **Lỗi cần quan sát:** import phụ thuộc working directory, exception bị nuốt,
  test chỉ kiểm tra đường chạy thành công.

### M1 — Dữ liệu và causal thinking

#### Tuần 4 — Schema và data contract

- **Mục tiêu:** mô tả schema, missingness và provenance.
- **Thao tác:** tạo validator cho dữ liệu tổng hợp và data card; thử input thiếu
  cột, sai kiểu và giá trị ngoài miền.
- **Xác minh:** mỗi input sai bị từ chối với lỗi chỉ rõ trường và cách sửa.
- **Nộp:** schema, validator, fixture hợp lệ/không hợp lệ và data card.
- **Lỗi cần quan sát:** tự động điền missing làm thay đổi semantics hoặc không
  lưu version/checksum của dữ liệu.

#### Tuần 5 — Split và leakage

- **Mục tiêu:** phân biệt random, group và temporal split; nhận diện leakage.
- **Thao tác:** dựng leakage có chủ ý, đo metric, sau đó khóa split đúng.
- **Xác minh:** báo cáo metric trước/sau leakage trong hai bảng riêng; không
  dùng test set để chọn feature.
- **Nộp:** split script, data card cập nhật, leakage report và checksum.
- **Lỗi cần quan sát:** duplicate giữa các split, preprocessing fit trên toàn bộ
  dữ liệu hoặc random seed không được ghi lại.

#### Tuần 6 — Labeling và causal thinking

- **Mục tiêu:** ghi nhận label noise, sampling, confounding và giới hạn nhân quả.
- **Thao tác:** viết guideline; audit tối thiểu 30 mẫu; biểu diễn một DAG.
- **Xác minh:** có agreement, ví dụ bất đồng, sampling rationale và limitation.
- **Nộp:** guideline, audit table, DAG và data card bất biến.
- **Lỗi cần quan sát:** biến hậu quả bị dùng làm feature hoặc kết luận causal từ
  tương quan quan sát.

### M2 — Machine learning cổ điển

#### Tuần 7 — Regression và calibration

- **Mục tiêu:** hiểu loss, regularization và xác suất dự đoán.
- **Thao tác:** làm L01 logistic regression từ đầu; lưu history và prediction.
- **Xác minh:** `pytest -q`; loss giảm; báo cáo accuracy và calibration trên
  cùng split.
- **Nộp:** model, test, metric table và error analysis.
- **Lỗi cần quan sát:** accuracy cao do imbalance, threshold mặc định không có
  lý do, hoặc fit scaler trên test.

#### Tuần 8 — Trees và feature engineering

- **Mục tiêu:** so sánh inductive bias của ít nhất ba baseline.
- **Thao tác:** giữ nguyên split; ghi rõ feature transform, missing-value policy
  và hyperparameter.
- **Xác minh:** confusion matrix và metric của ba baseline dùng cùng dữ liệu.
- **Nộp:** benchmark table, config và phân tích trade-off.
- **Lỗi cần quan sát:** thay đổi split giữa các model hoặc feature engineering
  làm rò rỉ nhãn.

#### Tuần 9 — Imbalance và threshold

- **Mục tiêu:** chọn operating point theo chi phí false positive/negative.
- **Thao tác:** threshold sweep, PR/ROC và error buckets theo subgroup.
- **Xác minh:** threshold cuối có rationale, metric chính/phụ và chi phí giả định.
- **Nộp:** sweep table/plot, confusion matrix và quyết định operating point.
- **Lỗi cần quan sát:** dùng ROC-AUC thay cho quyết định threshold hoặc bỏ qua
  subgroup nhỏ.

#### Tuần 10 — Thống kê thực nghiệm

- **Mục tiêu:** dùng bootstrap, CI, paired comparison và ablation.
- **Thao tác:** chạy L03 trên nhiều seed đã định trước; lưu toàn bộ kết quả.
- **Xác minh:** `pytest -q`; CI/độ phân tán được báo cáo; không cherry-pick seed.
- **Nộp:** benchmark report, raw results, CI và threat-to-validity section.
- **Lỗi cần quan sát:** số lần thử không được ghi, CI tính trên test đã dùng để
  chọn model, hoặc diễn giải chênh lệch nhỏ như chắc chắn.

### M3 — Deep learning và training loop

#### Tuần 11 — Computation graph

- **Mục tiêu:** hiểu forward/backward và reverse-mode autodiff.
- **Thao tác:** hoàn thành L04; kiểm tra graph có nhánh và miền `log`.
- **Xác minh:** `pytest -q tests/test_autograd.py`; sai số gradient tuyệt đối
  `< 1e-5`.
- **Nộp:** engine, gradient-check report và failure log.
- **Lỗi cần quan sát:** không cộng gradient ở node dùng nhiều lần hoặc không
  chặn input ngoài miền xác định.

#### Tuần 12 — Neural network

- **Mục tiêu:** hiểu activation, initialization, batch và loss.
- **Thao tác:** xây MLP toy; cố ý overfit một batch để kiểm tra pipeline.
- **Xác minh:** forward/backward test đạt; loss trên sample nhỏ giảm theo ngưỡng.
- **Nộp:** model, config, plot loss và ghi chú vì sao overfit hữu ích.
- **Lỗi cần quan sát:** shape mismatch, activation bão hòa, hoặc dùng overfit
  như bằng chứng generalization.

#### Tuần 13 — Optimizer và regularization

- **Mục tiêu:** so sánh SGD/momentum/Adam, dropout, weight decay và checkpoint.
- **Thao tác:** chạy controlled comparison; lưu checkpoint và resume command.
- **Xác minh:** resume cho kết quả tương đương trong tolerance định trước.
- **Nộp:** trainer, config, checkpoint manifest và comparison table.
- **Lỗi cần quan sát:** checkpoint thiếu optimizer state, seed không khôi phục,
  hoặc thay đổi nhiều biến cùng lúc.

#### Tuần 14 — Reproducibility

- **Mục tiêu:** tạo trainer và artifact có thể chạy lại.
- **Thao tác:** hoàn thành L05; chạy từ README trong môi trường mới.
- **Xác minh:** reviewer khác chạy được; manifest chứa version, config, seed,
  input/output checksum.
- **Nộp:** trainer, README, manifest, test và failure log.
- **Lỗi cần quan sát:** timestamp/đường dẫn tuyệt đối làm artifact không ổn định.

### M4 — Representation learning

#### Tuần 15 — Convolution

- **Mục tiêu:** giải thích receptive field, padding, pooling và inductive bias.
- **Thao tác:** xây CNN encoder toy; ablation kernel và pooling.
- **Xác minh:** shape test và bảng ablation đạt; phân biệt metric train/test.
- **Nộp:** encoder, ablation và error analysis.
- **Lỗi cần quan sát:** so sánh ablation khác budget hoặc thay đổi preprocessing.

#### Tuần 16 — Sequence models

- **Mục tiêu:** xử lý sequence, padding, recurrence và masking.
- **Thao tác:** classifier toy; chia lỗi theo độ dài sequence.
- **Xác minh:** có error buckets theo độ dài và test padding/mask.
- **Nộp:** model, fixture, metric table và failure cases.
- **Lỗi cần quan sát:** padding được coi là token thật hoặc truncate không được ghi.

#### Tuần 17 — Attention

- **Mục tiêu:** hiểu Q/K/V, softmax, causal mask và complexity.
- **Thao tác:** cài attention tối giản; tạo fixture chứng minh token tương lai bị
  chặn.
- **Xác minh:** test shape và causal-mask đều đạt; đổi token tương lai không làm
  thay đổi output vị trí hiện tại.
- **Nộp:** implementation, tests và giải thích complexity.
- **Lỗi cần quan sát:** mask ngược chiều, NaN sau softmax hoặc leak qua cache.

#### Tuần 18 — Embeddings và retrieval

- **Mục tiêu:** hiểu cosine, normalization và giới hạn của probing.
- **Thao tác:** hoàn thành L06; đo recall@k trên gold set và chạy failure queries.
- **Xác minh:** lưu k, gold version, query set và danh sách case không tìm thấy.
- **Nộp:** index, top-k API, recall report và ablation normalization.
- **Lỗi cần quan sát:** nhầm similarity với hiểu ngữ nghĩa hoặc đánh giá trên
  query đã dùng để xây index.

### M5 — LLM, retrieval và RAG

#### Tuần 19 — Tokenization và LLM

- **Mục tiêu:** hiểu token budget, context window, pretraining và instruction.
- **Thao tác:** tokenizer toy; lập prompt matrix với budget cố định.
- **Xác minh:** mọi run ghi token count; trường hợp vượt budget bị từ chối hoặc
  truncate theo policy đã ghi.
- **Nộp:** tokenizer, prompt matrix và budget policy.
- **Lỗi cần quan sát:** silent truncation hoặc so sánh prompt khác budget.

#### Tuần 20 — Prompting và structured output

- **Mục tiêu:** coi prompt và schema là contract có version.
- **Thao tác:** parser/schema; fixture output thiếu trường, sai kiểu và refusal.
- **Xác minh:** output lỗi bị bắt; không chuyển dữ liệu không hợp lệ thành side
  effect.
- **Nộp:** prompt contract, schema, parser tests và rejection examples.
- **Lỗi cần quan sát:** parser quá dễ dãi hoặc prompt injection được coi là dữ liệu.

#### Tuần 21 — Retrieval

- **Mục tiêu:** so sánh lexical/vector retrieval, chunking và reranking.
- **Thao tác:** tạo fixture top-k; ablation chunk size và query khó.
- **Xác minh:** recall@k và failure cases được lưu; query không có evidence có
  trạng thái abstain/empty rõ ràng.
- **Nộp:** index, fixture, metric table và chunking rationale.
- **Lỗi cần quan sát:** chunk overlap làm duplicate evidence hoặc reranker nhìn
  đáp án gold.

#### Tuần 22 — RAG evaluation

- **Mục tiêu:** đo groundedness, citation và unsupported claim.
- **Thao tác:** hoàn thành L07:
  `python -m ai_master.cli evaluate --gold docs/labs/L07/fixtures/gold.jsonl --predictions docs/labs/L07/fixtures/predictions.jsonl --output /tmp/l07-evaluation.json --k 2 --seed 7`.
- **Xác minh:** output có checksum, recall@k, citation coverage và
  unsupported-claim rate; `pytest -q` đạt.
- **Nộp:** evaluation JSON, report, claim/citation examples và limitation.
- **Lỗi cần quan sát:** coi lexical metric là truth hoặc citation đúng nhưng
  không entail claim.

### M6 — Agents và tools

#### Tuần 23 — Agent loop

- **Mục tiêu:** quản lý state, observe-act, termination, timeout và budget.
- **Thao tác:** chạy loop trên tool giả lập; tạo case timeout và budget exhausted.
- **Xác minh:** mọi trajectory có termination reason; không retry vô hạn.
- **Nộp:** state diagram, runner, replay log và cost summary.
- **Lỗi cần quan sát:** state không bất biến, loop nuốt lỗi hoặc retry làm nhân
  đôi side effect.

#### Tuần 24 — Tool contract

- **Mục tiêu:** dùng schema, allowlist, sandbox, permission và idempotency.
- **Thao tác:** hoàn thành L08; gọi tool hợp lệ, tool lạ và input sai.
- **Xác minh:** tool ngoài allowlist bị chặn fail-closed; schema lỗi không tới
  executor.
- **Nộp:** registry, policy, tests và audit log.
- **Lỗi cần quan sát:** kiểm tra quyền sau khi gọi tool hoặc allowlist theo tên
  hiển thị thay vì định danh ổn định.

#### Tuần 25 — Memory và human-in-loop

- **Mục tiêu:** đặt approval gate trước hành động rủi ro.
- **Thao tác:** giả lập side effect; kiểm tra pause/resume và escalation.
- **Xác minh:** khi chưa approve không có side effect; resume không lặp hành động.
- **Nộp:** policy, state transition, replay và risk notes.
- **Lỗi cần quan sát:** approval giả, memory ghi secret hoặc resume dùng state cũ.

#### Tuần 26 — Agent evaluation

- **Mục tiêu:** đo task success cùng trajectory, cost và safety.
- **Thao tác:** tạo replay set và taxonomy planning/tool/safety failure.
- **Xác minh:** report không chỉ có success rate; mỗi failure có reproduction.
- **Nộp:** replay fixture, evaluator, taxonomy và report.
- **Lỗi cần quan sát:** chấm trajectory khác nhau như cùng một task hoặc loại bỏ
  failure vì “model vẫn hoàn thành”.

### M7 — Production AI và vận hành

#### Tuần 27 — Serving

- **Mục tiêu:** thiết kế HTTP contract, health/readiness và timeout.
- **Thao tác:** xây L09 adapter; test request hợp lệ, schema lỗi và dependency
  chưa sẵn sàng.
- **Xác minh:** health không nhầm readiness; timeout có status/error contract.
- **Nộp:** adapter, schema tests, health/readiness evidence.
- **Lỗi cần quan sát:** health gọi dependency nặng hoặc retry request không idempotent.

#### Tuần 28 — Observability

- **Mục tiêu:** nối logs, metrics, traces và correlation ID.
- **Thao tác:** hoàn thành L10 trace một request end-to-end.
- **Xác minh:** tìm được request bằng correlation ID; log không chứa token, cookie
  hay PII.
- **Nộp:** sample trace, redaction tests và dashboard/table tối thiểu.
- **Lỗi cần quan sát:** log raw prompt, cardinality metrics quá cao hoặc trace
  mất khi qua queue.

#### Tuần 29 — Reliability và cost

- **Mục tiêu:** hiểu load, queue, retry, rate limit, SLO và budget.
- **Thao tác:** load test nhỏ; lập cost worksheet; mô phỏng quá budget.
- **Xác minh:** ghi throughput/latency/error rate và hành vi fail-fast khi vượt
  limit.
- **Nộp:** load result, SLO, budget policy và incident notes.
- **Lỗi cần quan sát:** retry storm, đo p50 nhưng bỏ p95/p99 hoặc cost không
  tính token/queue/storage.

#### Tuần 30 — Release và rollback

- **Mục tiêu:** thực hiện deploy rehearsal, migration và rollback có điều kiện.
- **Thao tác:** dùng reference service; viết runbook trước khi diễn tập.
- **Xác minh:** rollback drill có command, evidence, owner và stop condition.
- **Nộp:** runbook, CI evidence, rollback log và risk register.
- **Lỗi cần quan sát:** migration một chiều, rollback không tương thích schema,
  hoặc coi local pass là production readiness.

### M8 — Responsible AI, security và governance

#### Tuần 31 — Threat modeling

- **Mục tiêu:** lập asset, actor, attack surface và abuse case.
- **Thao tác:** threat model cho capstone; gán severity, owner và test.
- **Xác minh:** mọi rủi ro cao có reproduction hoặc lý do chưa thể reproduction.
- **Nộp:** threat model, risk register và test plan.
- **Lỗi cần quan sát:** chỉ liệt kê threat chung chung, không có owner hoặc
  nhầm mitigation trên giấy với control đã kiểm thử.

#### Tuần 32 — Red team và privacy

- **Mục tiêu:** kiểm tra prompt injection, exfiltration, PII và retention.
- **Thao tác:** hoàn thành L11; chạy attack set trên fixture an toàn.
- **Xác minh:** mỗi attack có reproduction, severity, mitigation và residual risk.
- **Nộp:** attack report, redaction/retention evidence và quyết định containment.
- **Lỗi cần quan sát:** gửi dữ liệu nhạy cảm ra evaluator hoặc lưu payload tấn
  công chưa được làm sạch.

#### Tuần 33 — Fairness và governance

- **Mục tiêu:** đo subgroup metrics, calibration và quyết định go/no-go.
- **Thao tác:** cập nhật system/model card; review risk register cùng owner.
- **Xác minh:** nêu rõ trade-off, ngưỡng chấp nhận và điều kiện triển khai.
- **Nộp:** subgroup report, cards, risk register và decision record.
- **Lỗi cần quan sát:** subgroup quá nhỏ để kết luận, hoặc dùng một fairness
  metric như tiêu chuẩn duy nhất.

### M9 — Capstone và research

#### Tuần 34 — Replication protocol

- **Mục tiêu:** khóa claim, protocol, split, baseline và validity threats.
- **Thao tác:** chọn paper; hoàn thành preregistration nội bộ và L12 skeleton.
- **Xác minh:** reviewer duyệt protocol trước khi xem kết quả extension.
- **Nộp:** protocol, dataset card, baseline plan và threat model.
- **Lỗi cần quan sát:** đổi metric/split sau khi thấy kết quả hoặc HARKing.

#### Tuần 35 — Extension và paper draft

- **Mục tiêu:** chạy một extension có giả thuyết, ablation và negative result.
- **Thao tác:** chạy baseline trước; lưu raw results; viết report theo IMRaD.
- **Xác minh:** có failure analysis, limitation và review chéo theo evidence.
- **Nộp:** code, results, ablation, draft paper và reproducibility notes.
- **Lỗi cần quan sát:** claim mới không được tách khỏi replication hoặc loại bỏ
  negative result.

#### Tuần 36 — Defense và handoff

- **Mục tiêu:** bảo vệ evidence, giới hạn và khả năng tái lập.
- **Thao tác:** hoàn thành L12; chạy demo offline và quickstart từ đầu.
- **Xác minh:** reviewer mới chạy được artifact; trả lời được “what would
  falsify this?”; có containment/rollback và owner.
- **Nộp:** code/artifact, paper, demo, viva notes và final manifest.
- **Lỗi cần quan sát:** demo phụ thuộc mạng/secret, output không deterministic,
  hoặc kết luận vượt quá evidence.

## Mẫu README cho artifact tuần

```text
Week / module:
Question / hypothesis:
Dataset, version, split, checksum:
Theory covered:
Smoke-test command and exit code:
Full command and exit code:
Baseline and metric:
Seed / environment:
Result and confidence interval:
Failure analysis:
Threats to validity:
Rollback or containment:
What would falsify this result?
Next experiment:
```
