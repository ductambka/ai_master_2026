# Sổ tay giảng viên, đánh giá và capstone

## Nhịp điều phối một tuần

| Phần | Thời lượng | Cách điều phối | Bằng chứng |
|---|---:|---|---|
| Seminar | 90 phút | derivation, trade-off, live reasoning | 3 câu hỏi exit ticket |
| Lab | 120 phút | checkpoint 30/60/100 phút, pair debugging | test/output/failure log |
| Paper clinic | 60 phút | claim–method–evidence–limitation | one-page critique |
| Review | 30 phút | đổi artifact, chạy lại một lệnh | review comment + research log |

Mỗi buổi phải có một “known failure” để học viên thấy cách chẩn đoán, nhưng không cung cấp đáp án bằng cách sửa fixture hoặc bỏ qua test.

## Rubric lab — 100 điểm

- Đúng chức năng: 40 điểm.
- Test và xử lý lỗi: 20 điểm.
- Phân tích metric/failure: 20 điểm.
- Reproducibility: 20 điểm.

Không đạt nếu có secret, không có split/seed khi cần, hoặc claim vượt quá evidence. Có thể đạt điểm kỹ thuật cao nhưng bị giới hạn vì thiếu threat model.

## Rubric midterm system — 100 điểm

- Interface và schema: 20.
- Baseline/offline metric: 20.
- Online/operational evidence: 20.
- Observability và failure analysis: 20.
- Reproducibility và runbook: 20.

## Rubric responsible AI audit — 100 điểm

- Asset/actor/abuse-case coverage: 25.
- Attack reproduction: 25.
- Subgroup/privacy analysis: 20.
- Mitigation test và residual risk: 20.
- Owner, severity, decision record: 10.

## Capstone contract

Đề tài phải có câu hỏi có thể bác bỏ, dataset card, baseline đơn giản, metric chính/phụ, ít nhất một ablation, phân tích lỗi, threat model, ngân sách tài nguyên, giới hạn và kế hoạch tái lập. “Chỉ gọi API rồi demo” không đủ để bảo vệ.

### Checkpoint bắt buộc

- Tuần 34: protocol, split, baseline và threat model được duyệt.
- Tuần 35: có kết quả baseline, extension, ablation và failure analysis.
- Tuần 36: artifact sạch, demo offline, paper và viva.

### Tiêu chí nghiệm thu cuối

Người reviewer mới phải chạy được quickstart; prediction-level output đủ để kiểm tra lỗi; metric có CI hoặc giải thích vì sao không thể; report phân biệt observation/inference; hệ thống có giới hạn, rollback/containment và owner vận hành.

## Quy trình phản hồi

Phản hồi theo mẫu: “evidence → impact → suggested next test”. Không chấm theo độ bóng của demo. Khi kết quả âm tính, ghi nhận nếu protocol đúng và phân tích tốt; không khuyến khích cherry-picking.

