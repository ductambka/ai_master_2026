# L04 — Mini autograd

## Mục tiêu

Xây dựng trực giác về reverse-mode automatic differentiation bằng một graph
chỉ chứa scalar. Mỗi `Value` giữ giá trị xuôi, gradient và hàm đạo hàm cục bộ;
`backward()` duyệt graph theo thứ tự topo đảo.

## Chạy

Từ thư mục gốc repository:

```bash
pytest -q tests/test_autograd.py
python -m compileall src
```

## Phạm vi và ví dụ

Engine hỗ trợ `+`, `-`, `*`, `/`, lũy thừa với số, `exp` và `log` (cả dạng
phương thức lẫn hàm). Graph có nhánh được xử lý bằng cách cộng dồn gradient
khi một node được dùng nhiều lần. `log(x)` yêu cầu `x > 0` và ném `ValueError`
ngoài miền xác định.

Mỗi lần gọi `backward()` sẽ đặt lại gradient của các node trong graph trước
khi lan truyền ngược; vì vậy gọi lại trên cùng output cho cùng kết quả, còn
các nhánh dùng chung trong một lần chạy vẫn được cộng dồn đúng.

```python
from ai_master.autograd import Value, exp, log

x = Value(0.7)
y = log(exp(x) + x * x)
y.backward()
print(y.data, x.grad)
```

## Kết quả thực nghiệm

- Seed: không dùng số ngẫu nhiên; kiểm thử xác định.
- Gradient check: sai số tuyệt đối tối đa được assertion ở `1e-5` so với sai
  phân hữu hạn trung tâm.
- Threats to validity: chỉ scalar, không tối ưu cho production, không có
  tensor/broadcasting, và không kiểm tra floating-point cực trị.
- Rollback: xóa `src/ai_master/autograd.py`, test tương ứng và thư mục lab;
  hoặc forward-fix nếu API được mở rộng.
