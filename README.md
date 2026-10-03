# AI Thực chiến — chương trình cấp Thạc sĩ, tiệm cận Tiến sĩ

Kho học liệu này là một chương trình 36 tuần, thiết kế theo mô hình **học qua xây dựng**. Mỗi module có mục tiêu đo được, đọc trước, lab, rubric, artefact và câu hỏi nghiên cứu. Phần code mẫu chạy bằng Python 3.11+ và chỉ dùng thư viện chuẩn để người học có thể bắt đầu ngay.

## Bắt đầu nhanh

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
python -m ai_master.cli demo
python -m ai_master.cli train --epochs 25
```

Không cần GPU, API key hay dữ liệu bí mật. Các lab nâng cao có thể thay backend bằng PyTorch, JAX, vLLM, PostgreSQL/pgvector hoặc cloud sau khi đã hoàn tất baseline.

## Tài liệu chính

- [`docs/program.md`](docs/program.md): chương trình 36 tuần, chuẩn đầu ra, lịch học, rubric và lộ trình nghiên cứu.
- [`docs/training/README.md`](docs/training/README.md): bộ tài liệu đào tạo chi tiết theo tuần, module, chủ đề, thực hành và hướng dẫn sử dụng.
- [`docs/training/weekly-lesson-plans.md`](docs/training/weekly-lesson-plans.md): giáo án triển khai đủ 36 tuần, lệnh smoke test và checklist nghiệm thu.
- [`docs/training/weekly-user-guide.md`](docs/training/weekly-user-guide.md): hướng dẫn sử dụng, xác minh và nộp artifact cho từng tuần.
- [`docs/labs.md`](docs/labs.md): 12 lab có đề bài, deliverable, tiêu chí nghiệm thu và mở rộng.
- [`docs/engineering-playbook.md`](docs/engineering-playbook.md): quy trình reproducibility, đánh giá, an toàn, MLOps và nghiên cứu.
- [`jobs/follow-up-jobs.json`](jobs/follow-up-jobs.json): các job nhỏ có thể thực hiện tuần tự.
- [`src/ai_master`](src/ai_master): ví dụ hồi quy logistic, retrieval TF-IDF, đánh giá và CLI.

## Nguyên tắc học

1. Mỗi tuyên bố về chất lượng phải đi kèm dataset split, metric, seed và baseline.
2. Mọi hệ thống sinh nội dung phải có kiểm thử định lượng, kiểm thử nguy hiểm và cơ chế quan sát.
3. Không dùng dữ liệu cá nhân, bí mật hoặc dữ liệu production trong lab.
4. Tách rõ kết quả thực nghiệm, giả thuyết và suy luận chưa được kiểm chứng.
