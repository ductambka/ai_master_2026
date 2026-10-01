# Engineering & research playbook

## Definition of done

Một tính năng AI chỉ đạt DONE khi có: interface rõ, unit/contract test, baseline, metric offline, logging không chứa secret, giới hạn tài nguyên, tài liệu vận hành và rollback/forward-fix. Demo xanh không đủ để kết luận mô hình tốt.

## Quy trình thực nghiệm

1. Chốt question và hypothesis trước khi chạy.
2. Tạo baseline rẻ nhất và split bất biến.
3. Chạy smoke test trên sample nhỏ.
4. Chạy full experiment với seed, config và artifact ID.
5. Lưu prediction-level output để phân tích lỗi.
6. Báo cáo mean, độ phân tán hoặc khoảng tin cậy; không cherry-pick seed tốt.
7. Chỉ sau đó mới tối ưu model/infra.

## Rủi ro đặc thù AI

- Leakage, contamination và thay đổi dữ liệu âm thầm.
- Hallucination, prompt injection, data exfiltration, tool abuse.
- Proxy bias, subgroup regression, privacy leakage.
- Non-determinism, dependency drift, cost/latency runaway.

## Checklist review

- Có threat model và người dùng bị ảnh hưởng không?
- Có failure mode cụ thể và test tái hiện không?
- Có metric phản ánh mục tiêu, không chỉ accuracy không?
- Có giới hạn confidence và trường hợp abstain không?
- Có rollback, rate limit, audit log và owner không?

