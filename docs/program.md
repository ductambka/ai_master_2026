# Chương trình AI thực chiến 36 tuần

## Định vị

Đối tượng là kỹ sư, nhà nghiên cứu hoặc giảng viên đã biết Python, đại số tuyến tính cơ bản, xác suất và Git. Chuẩn đầu ra tương đương một chương trình Thạc sĩ thiên về hệ thống, với năng lực đọc bài báo, tái lập thí nghiệm và thiết kế một nghiên cứu nhỏ tiệm cận Tiến sĩ.

## Chuẩn đầu ra (measurable outcomes)

Sau 36 tuần, học viên có thể:

1. Xây và giải thích pipeline dữ liệu → mô hình → đánh giá → triển khai.
2. Tự cài đặt từ đầu các baseline: linear/logistic regression, cây quyết định, embedding retrieval, attention tối giản.
3. Thiết kế split, baseline, ablation, confidence interval và kiểm định phù hợp.
4. Xây RAG/agent có groundedness, citation, guardrail, logging và budget.
5. Đo latency, throughput, cost, drift, robustness, fairness và security.
6. Viết technical report theo cấu trúc IMRaD, kèm artifact đủ để tái lập.

## Lịch học theo học kỳ

| Tuần | Module | Trọng tâm | Sản phẩm |
|---|---|---|---|
| 1–3 | M0 Nền tảng toán & Python | vector, gradient, xác suất, clean code | notebook tái lập |
| 4–6 | M1 Dữ liệu & causal thinking | schema, leakage, sampling, labeling | data card |
| 7–10 | M2 ML cổ điển | regression, trees, calibration, imbalance | benchmark |
| 11–14 | M3 Deep learning | backprop, optimizer, regularization | trainer từ đầu |
| 15–18 | M4 Representation | CNN, sequence, attention, embeddings | encoder + ablation |
| 19–22 | M5 LLM & retrieval | tokenization, prompting, RAG, eval | RAG service |
| 23–26 | M6 Agents & tools | planning, memory, sandbox, human-in-loop | agent có policy |
| 27–30 | M7 Production AI | serving, monitoring, CI/CD, cost | deployed service |
| 31–33 | M8 Responsible AI | privacy, red-team, fairness, governance | risk register |
| 34–36 | Capstone/research | replication + novel extension | paper + demo + viva |

## Nhịp mỗi tuần

- 90 phút seminar: derivation, paper discussion, design trade-off.
- 120 phút lab: xây một vertical slice, test trước khi tối ưu.
- 60 phút paper clinic: đọc theo câu hỏi “claim–method–evidence–limitation”.
- 30 phút review: peer review artefact và cập nhật research log.

## Đánh giá

- Labs: 30% (đúng chức năng 40, test 20, phân tích 20, reproducibility 20).
- Midterm system: 20% (offline/online metrics, failure analysis).
- Responsible AI audit: 10%.
- Capstone: 40% gồm code/artifact 30, report 30, thực nghiệm 25, viva 15.

## Capstone contract

Mỗi đề tài phải có: câu hỏi có thể bác bỏ, dataset card, baseline đơn giản, metric chính/phụ, ít nhất một ablation, phân tích lỗi, threat model, ngân sách tài nguyên, giới hạn và kế hoạch tái lập. Không chấp nhận “chỉ gọi API rồi demo”.

## Danh mục đọc khởi đầu

- Bishop — *Pattern Recognition and Machine Learning*.
- Goodfellow, Bengio, Courville — *Deep Learning*.
- Sutton & Barto — *Reinforcement Learning: An Introduction*.
- Vaswani et al. — *Attention Is All You Need*.
- Papers With Code và tài liệu chính thức của framework được chọn cho từng lab.

