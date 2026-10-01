# Lab template: reproducible baseline

Đây là bộ khung tối thiểu cho một lab có thể chạy lại từ môi trường sạch.
Lab dùng một baseline nearest-centroid trên dataset nhỏ được khai báo trong
[`config.json`](config.json), không cần API key, package ngoài hay dữ liệu
production.

## Cấu trúc

```text
lab_template/
├── README.md
├── config.json       # seed, dataset và ngưỡng nghiệm thu
├── run_lab.py        # runner tạo metrics.json và manifest.json
└── output/           # artifact sinh ra khi chạy (mặc định không commit)
```

## Chạy

Từ thư mục gốc repository:

```bash
./tooling/run_lab_template.sh
```

Hoặc chạy trực tiếp:

```bash
python3 examples/lab_template/run_lab.py \
  --config examples/lab_template/config.json \
  --output-dir examples/lab_template/output
```

Runner tạo:

- `metrics.json`: accuracy, số mẫu và seed.
- `manifest.json`: đường dẫn tương đối, SHA-256 của metrics, cấu hình đã
  dùng, kết quả nghiệm thu và thời điểm UTC.

Lab có thể được mở rộng bằng cách thay `run()` bằng pipeline thật, nhưng vẫn
giữ hợp đồng artifact và manifest. Không đưa secret vào config hoặc artifact.

## Nghiệm thu

Kết quả đạt khi `status` trong manifest là `PASS` và accuracy không thấp hơn
`acceptance.min_accuracy`. Test tương ứng nằm tại
[`tests/test_lab_template.py`](../../tests/test_lab_template.py).

## Báo cáo thí nghiệm

- Question: baseline có phân loại đúng hai cụm điểm hay không?
- Hypothesis: nearest-centroid đạt accuracy 1.0 trên dataset seed.
- Dataset/version/split: dataset tổng hợp trong `config.json`, toàn bộ dữ liệu
  được dùng để kiểm tra tính reproducible của template.
- Threats to validity: dataset rất nhỏ, không đại diện cho bài toán thực tế.
- Rollback: xóa output artifact hoặc revert commit; không có thay đổi API.
