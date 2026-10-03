# Sổ tay sử dụng cho học viên

## 1. Cài đặt và kiểm tra môi trường

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python -m compileall -q src service
pytest -q
```

Nếu `pytest` không chạy, kiểm tra đang dùng đúng Python bằng `which python` và `python --version`; không sửa code để che lỗi môi trường. Lab cơ bản không cần GPU, API key hay mạng.

## 2. Chạy một lab

```bash
./tooling/run_lab_template.sh
python -m ai_master.cli demo
python -m ai_master.cli train --epochs 25
```

Đọc `README` của lab trước khi chạy. Ghi lại command nguyên văn, exit code, thời gian, seed và đường dẫn output. Không sửa fixture gold để làm test xanh.

## 3. Contract của artifact

```text
Question / Hypothesis
Dataset, version, split, checksum
Baseline và metric chính/phụ
Seed, Python/dependency, command
Result và confidence interval
Error analysis / failure log
Threats to validity
Rollback hoặc containment
What would falsify this result?
Next experiment
```

Artifact tối thiểu phải có `README`, `config`, `tests`, `output/manifest.json` và kết quả. Dùng dữ liệu tổng hợp hoặc dữ liệu công khai đã được phép; xóa secret trước khi commit.

## 4. Cách đọc paper

Trả lời theo thứ tự: claim là gì; baseline nào; split và metric nào; evidence có đủ không; failure/limitation nào; thử nghiệm nào có thể bác bỏ claim. Mỗi paper clinic nộp một trang, không chép abstract thay cho phân tích.

## 5. Quy tắc debug

1. Tái hiện bằng sample nhỏ và seed cố định.
2. Kiểm tra input/schema/split trước model.
3. Viết test tái hiện lỗi trước khi sửa.
4. So sánh với baseline rẻ nhất.
5. Lưu failure log và cập nhật research log.

Không retry vô hạn, không log token/cookie/PII, không dùng production data và không kết luận chất lượng chỉ từ một seed.

## 6. Làm việc nhóm và review

Mỗi PR/artefact cần một người chạy lại command, một người review metric và một người đọc threat model. Review phải ghi bằng chứng cụ thể: file, command, output và câu hỏi còn mở. Khi thay đổi lớn đã test thành công, maintainer commit và push; thay đổi chưa đủ bằng chứng phải để ở trạng thái draft.

