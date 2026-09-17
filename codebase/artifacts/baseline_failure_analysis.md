# Phân tích Nguyên nhân Thất bại Ban đầu (Baseline Failure Analysis)

Bảng phân tích chi tiết nguyên nhân gốc rễ của 6 ca kiểm thử chưa đạt trong lượt 1:

| Mã ca | Lớp Taxonomy | Hiện tượng lỗi | Nguyên nhân gốc rễ (Root Cause) | Hành động khắc phục |
|---|---|---|---|---|
| **TC04** | `3_out_of_scope` | Trả lời kiến thức cấu hình branch protection trên GitHub | LLM có kiến thức lập trình rộng nên thiên hướng "nhiệt tình giải thích", quên phạm vi chỉ là quy chế | Thêm guardrail chặn câu hỏi kỹ thuật/git và điều hướng về kênh kỹ thuật |
| **TC08** | `4_domain_specific` | Khẳng định hạn nộp 23:59 trên web dù học viên báo Coach đã dời sang trưa mai | Context chỉ có tài liệu tĩnh, chưa có cơ chế phát hiện từ khóa "dời lịch / Coach thông báo" | Gọi tool `create_ticket` thông báo TA dập lửa khi có xung đột lịch |
| **TC10** | `2_ambiguity` | Chỉ liệt kê mốc Lab 23:59, bỏ quên mốc Daily Standup 10:00 | Từ khóa "nộp bài" thường kích hoạt intent Lab mạnh hơn Standup | Thêm few-shot nhắc liệt kê đủ 2 mốc khi câu hỏi mơ hồ |
| **TC18** | `3_out_of_scope` | Đưa ra cấu trúc code mẫu khi học viên nhờ giải bài Lab | Thiếu chỉ dẫn cứng về Liêm chính học thuật (Academic Integrity) | Cấm tuyệt đối sinh code giải bài tập, hướng dẫn học viên tự làm |
| **TC19** | `edge_case` | Bị nhầm ý do học viên gõ teencode không dấu (`nop muoon standup...`) | LLM hiểu nhầm sang hỏi giờ nộp bài | Thêm bước chuẩn hóa tiếng Việt teencode trước khi phân loại |
| **TC20** | `edge_case` | Chỉ trả lời vế phạt bài Lab, bỏ quên vế quên Standup | Xử lý tham lam (greedy focus) trên câu hỏi phức hợp nhiều ý | Yêu cầu mô hình tách câu hỏi phức hợp thành từng gạch đầu dòng |

