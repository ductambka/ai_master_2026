# Bộ tài liệu đào tạo AI thực chiến

Bộ tài liệu này là hướng dẫn vận hành đầy đủ cho chương trình 36 tuần. Nó nối chương trình tổng quan với việc học hằng tuần: học gì, làm gì, nộp gì, chạy lệnh nào và đánh giá ra sao.

## Lộ trình đọc

1. [Bản đồ 36 tuần](curriculum-map.md): mục tiêu, chủ đề, seminar, lab và sản phẩm của từng tuần.
2. [Giáo án theo tuần](weekly-lesson-plans.md): mục tiêu, hoạt động seminar/lab, sản phẩm và lệnh xác minh cho đủ 36 tuần.
3. [Sổ tay module](module-handbooks.md): lý thuyết cốt lõi, bài thực hành và tiêu chí hoàn thành cho từng module.
4. [Sổ tay sử dụng](learner-handbook.md): cách cài đặt, chạy lab, lưu artifact, xử lý lỗi và làm việc nhóm.
5. [Đánh giá và giảng dạy](instructor-assessment.md): nhịp lớp, rubric, checkpoint, phản hồi và capstone.
6. [Sổ tay theo tuần](weekly-user-guide.md): checklist thao tác, lệnh xác minh,
   artifact và lỗi cần quan sát cho từng tuần 1–36.

## Chuẩn bị một tuần học

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
```

Mỗi tuần học theo chu trình:

```text
Đọc trước → seminar → lab nhỏ → kiểm thử → phân tích lỗi → paper clinic → review → research log
```

Học viên phải lưu tối thiểu: câu hỏi, giả thuyết, dataset/split, baseline, metric, seed, môi trường, kết quả, lỗi, giới hạn và bước tiếp theo. Không dùng secret, dữ liệu cá nhân hoặc dữ liệu production trong lab.

## Quan hệ với tài liệu hiện có

- [Chương trình tổng quan](../program.md) giữ chuẩn đầu ra và tỷ trọng điểm.
- [Lab book](../labs.md) là danh mục lab chuẩn L01–L12.
- [Engineering playbook](../engineering-playbook.md) là định nghĩa DONE và checklist kỹ thuật.
- [Reference service](../course-reference-service.md) là mẫu để capstone học cách healthcheck, audit và policy.
