# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:** baseline `E-swarm-20261118-e9f6`; fixed PR `E-fixed-20261118-e9f6`; seeded regression PR `E-seeded_regression-20261118-e9f6`. Eval set SHA: `e9f6fdb66124`.
- **Phiên bản:** eval set v1, metric spec 1.0, seeds 11/22/33/44/55; model backend MockLLM.
- **Eval set:** 14 item × 5 seed, nguồn `lab8_public`; nhãn tách riêng trong `labels_v1.json`.
- **Metric baseline:** `approval_bypass=0`, `secret_leak=0`, `db_fact_kept=0.9857`, `refund_amount_correct=0.9857`, `pass_rate=0.9857`, `reply_amount_matches_ledger=1.0`, `pass_5=0.9286`, `cost_per_success=49.567` simulated VND.
- **Gate fixed:** exit 0. So với baseline, `refund_amount_correct` Δ +0.014, CI [+0.000, +0.043]; `pass_rate` Δ +0.014, CI [+0.000, +0.043]. Các metric blocking đạt.
- **Gate seeded regression:** exit 1, blocked `refund_amount_correct`, `pass_rate`, `reply_amount_matches_ledger`. `pass_rate`=0.7143, Δ -0.271, CI [-0.500, -0.057]. `reply_amount_matches_ledger`=0.7857.
- **Judge:** `tone_ok` đạt FLOORS; `helpful` bị loại vì κ ≈ 0.375, recall 0.300; judge không thấy ledger và có thiên lệch độ dài. Chi tiết/audit mẫu: `docs/judge_audit.md`.
- **Trace case:** [docs/trace_case.md](trace_case.md), regression test `src/tests/test_lab9_trace_case_regression.py`.
- **Gate owner:** Eval owner trực CI xử lý gate exit 1; chỉ merge sau khi điều tra regression hoặc có waiver được Product và Eval owner phê duyệt, ghi lý do trong PR.
- **Phạm vi pilot:** yêu cầu refund đơn hàng trong world state mô phỏng, với policy, approval, dữ kiện đơn và ledger được kiểm soát; không bao gồm tranh chấp pháp lý hoặc nhiều đơn trong cùng claim.
- **Giới hạn / bằng chứng còn thiếu:** MockLLM không đại diện model thật; 14 item × 5 seed khó phát hiện lỗi hiếm (ví dụ lỗi chỉ xuất hiện 1/3 seed); judge chỉ replay CSV công khai, chưa có held-out human labels; không đo trên người dùng thật.
- **Khi nào tăng eval-set version:** thêm/đổi item hoặc nhãn thì tăng `eval_set_version`, sinh lại và tạo baseline mới. Thay metric/ngưỡng trên cùng tập thì tăng `metric_spec_version`, ghi lý do và giữ ratchet không nới ngưỡng.
