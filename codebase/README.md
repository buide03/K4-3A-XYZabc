# Codebase — CP2 Interactive Flow & Prototype
**Dự án:** Trợ lý Quy chế & Lịch nộp bài Khóa 4 (Track B)  
**Nhóm:** K4-3A-XYZabc

Thư mục này chứa mã nguồn giao diện bản mẫu tương tác và sơ đồ luồng chi tiết phục vụ nghiệm thu mốc **Checkpoint 2 (CP2)**.

---

## 1. Thành phần trong thư mục `codebase/`

| Tệp tin | Định dạng | Nội dung chi tiết |
|---|---|---|
| [`index.html`](file:///c:/Users/Admin/K4-3A-XYZabc/codebase/index.html) | Bản mẫu web tương tác (Clickable Prototype) | Giao diện mô phỏng Discord Dark Theme trực quan. Tích hợp thanh chọn 4 kịch bản (Happy Path, Low-confidence, Failure/No-grounding, Correction) và gắn thẻ các nguyên tắc **HAX G1, G2, G9, G10**. |
| [`FLOWCHART.md`](file:///c:/Users/Admin/K4-3A-XYZabc/codebase/FLOWCHART.md) | Sơ đồ luồng (Flowchart) | Sơ đồ Mermaid biểu diễn chi tiết các bước người dùng nhập liệu, điểm gọi quyết định AI, phân nhánh 4 kịch bản và cơ chế xử lý ngoại lệ. |

---

## 2. Hướng dẫn mở và kiểm thử Bản mẫu tương tác (`index.html`)

1. **Cách mở:**
   * Mở trực tiếp tệp `codebase/index.html` bằng bất kỳ trình duyệt web nào (Chrome, Edge, Firefox). Không cần cài đặt server hay thư viện npm phụ trợ.
2. **Cách kiểm thử 4 kịch bản tại thanh công cụ trên cùng:**
   * **Nút 1 - Happy Path:** Mô phỏng câu hỏi có ngữ cảnh rõ ràng (`Lab 02`), bot phản hồi chính xác kèm trích dẫn văn bản gốc (**HAX G2**).
   * **Nút 2 - Low-Confidence:** Mô phỏng câu hỏi mơ hồ (*"Hôm nay nộp gì?"*), bot đưa ra các chip gợi ý lựa chọn làm rõ ngữ cảnh thay vì đoán mò.
   * **Nút 3 - Failure / No-grounding:** Mô phỏng câu hỏi ngoài phạm vi, bot thoái lui nhã nhặn (**HAX G10**) và cung cấp nút liên hệ Trợ giảng (TA).
   * **Nút 4 - Correction (Sửa sai):** Mở cửa sổ can thiệp nhanh (**HAX G9**) cho phép người dùng đổi loại bài tập hoặc gửi thông báo đính chính.

