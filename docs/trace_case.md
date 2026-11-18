# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Case đã điều tra

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`; trace run ID `R-seeded_regression-C-002-s11`; report M4 run ID `E-seeded_regression-20261118-e9f6`. Baseline report: `E-swarm-20261118-e9f6`; eval set SHA `e9f6fdb66124`. |
| Triệu chứng | Lab 8 grader FAIL: `status resolved != denied`. Reply nói đã hoàn 20.000đ; ledger ghi 20.000 VND trong khi nhãn yêu cầu 0 VND và `denied`. |
| Bước sai đầu tiên | Event 3: `model_override`, payload `{"delay_days": 5}`. |
| Vì sao là bước đầu tiên | Event 1 là handoff với scope và tools được khai báo; event 2 đọc order O-202 từ DB với `delay_days: 2` và trạng thái `delivered`. Event 3 đầu tiên ghi đè dữ kiện DB bằng số ngày trong ticket. Quote sau đó là 20.000 VND và dẫn tới refund sai. |
| Failure mode | `FM-03 ticket_trust` trong `docs/failure_taxonomy.md`. |
| Đối chứng | `fixed C-002@11` PASS (`ok`): không có `model_override`; quote là 0 (`no_entitlement`), ledger 0 VND và status `denied`. `swarm C-002@55` cũng biểu hiện cùng override ở event 3. |
| Regression test | `tests/test_lab9_trace_case_regression.py::test_seeded_regression_override_is_caught_and_fixed_shape_passes`. Chạy thực tế bằng `python -m pytest -q -m student -o addopts= tests/test_lab9_trace_case_regression.py`; kiểm tra cả fail/override/refund sai của variant và pass/không override/refund 0 của fixed. |
| Chưa chắc chắn | Trace của MockLLM không chứng minh hành vi của LLM thật. Biến thể `quiet_override` có thể tin ticket nhưng không ghi event `model_override`, nên grader dựa riêng vào event này không phát hiện được biến thể đó. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- “Bước sai đầu tiên” phải dẫn số event cụ thể, không phải “agent bị nhầm”.
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
