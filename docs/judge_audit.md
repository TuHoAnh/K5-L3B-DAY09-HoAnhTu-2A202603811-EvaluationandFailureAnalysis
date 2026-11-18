# Judge audit

Lệnh replay: `python -m lab9.judge --csv data/eval/<file> --audit 5`. FLOORS: κ ≥ 0.6, precision ≥ 0.8, recall ≥ 0.7.

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS? | Quyết định |
|---|---:|---:|---:|---:|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | Dùng cho giọng điệu, với rubric được rà soát |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | Loại khỏi gate |

`tone_ok` vượt cả ba floor và phù hợp để đánh giá sắc thái giao tiếp. `helpful` có recall thấp: judge bỏ sót 21/30 nhãn FAIL, gồm các ca reply báo số tiền sai. Judge replay không được xem ledger nên không thể xác nhận số tiền; đánh giá helpful còn thiên về độ dài và lời xin lỗi. Dùng code grader `reply_amount_matches_ledger` cho FM-08 thay vì đưa helpful vào gate.

## 8 case bất đồng để audit thủ công

| # | Case | Human | Judge | Ai đúng? | Hành động với rubric/nhãn |
|---:|---|---|---|---|---|
| 1 | H-008 | FAIL | PASS | Human có cơ sở: xưng “em”, “anh”, “nha” quá suồng sã | Bổ sung ví dụ xưng hô không phù hợp vào rubric tone; giữ nhãn FAIL. |
| 2 | H-029 | FAIL | PASS | Cần rà soát: câu “đang xử lý” có thể là cập nhật hữu ích nhưng không giải quyết yêu cầu | Làm rõ rubric phân biệt trạng thái xử lý với câu trả lời hoàn tất; xác nhận nhãn với reviewer. |
| 3 | H-042 | PASS | FAIL | Human có vẻ đúng về tone; judge có thể nhầm nội dung ngắn/trung tính với không helpful | Tách rubric tone khỏi độ dài; giữ nhãn tone PASS sau xác nhận. |
| 4 | H-051 | PASS | FAIL | Human có vẻ đúng về tone; cách dùng “refund” là vấn đề ngôn ngữ/nhất quán, không nhất thiết tone FAIL | Thêm tiêu chí ngôn ngữ riêng, không phạt tone; xác nhận nhãn. |
| 5 | H-070 | FAIL | PASS | Human có cơ sở: emoji cười trong thông báo refund không phù hợp ngữ cảnh | Bổ sung emoji và ngữ cảnh nhạy cảm vào rubric; giữ nhãn FAIL. |
| 6 | H-081 | PASS | FAIL | Human có vẻ đúng về tone; câu từ chối lịch sự, judge có thể nhầm từ chối với không helpful | Rubric yêu cầu chấm cách diễn đạt độc lập với việc có refund hay không; xác nhận nhãn PASS. |
| 7 | HL-016 | FAIL | PASS | Không thể xác nhận chỉ từ CSV; reply dài, xin lỗi nhưng có thể sai số tiền | Reviewer đối chiếu ledger rồi giữ/sửa human label; helpful judge không được quyền suy ra tiền từ độ dài. |
| 8 | HL-028 | FAIL | PASS | Không thể xác nhận chỉ từ CSV; cùng dạng reply dài/xin lỗi, thiếu ledger trong đầu vào judge | Đối chiếu ledger và sửa nhãn nếu cần; chuyển kiểm tra số tiền sang code grader FM-08. |

## Kết luận

- Dùng `tone_ok` trong phạm vi đánh giá giọng điệu, tiếp tục audit các bất đồng để tăng độ rõ của rubric.
- Loại `helpful` khỏi release gate: recall 0.300 và κ 0.375 không đạt floor; judge không có ledger và bị nhiễu bởi độ dài/lời xin lỗi.
- Các CSV là replay công khai, không phải held-out human evaluation. Những phán định “có vẻ đúng” phía trên là ưu tiên rà soát, không thay thế xác minh với ngữ cảnh/ledger gốc.
