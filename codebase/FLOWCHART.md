# CP2 Flow — Trợ lý Quy chế & Lịch nộp bài (Track B)

```mermaid
flowchart TD
    A[Học viên đặt câu hỏi] --> B[Phân tích Intent & Thực thể]
    B --> C{Ngoài phạm vi / Vượt thẩm quyền?}
    C -- Có --> H[HAX G10: Thoái lui + Mẫu Email Lab Coach / Ticket TA]
    C -- Không --> D[Truy xuất quy chế chính thức]
    D --> E{Đủ căn cứ & Rõ ràng?}
    E -- Không / Mơ hồ --> I[HAX G9: Quick chips làm rõ ngữ cảnh Offline vs Online]
    I --> D
    E -- Có --> F{Xung đột thông báo?}
    F -- Có --> J[Cảnh báo xung đột + Chuyển Trợ giảng dập lửa]
    F -- Không --> G[HAX G2: Trả lời + Badge hệ thống + Trích dẫn nguồn]
    G --> K{Phản hồi người dùng}
    K -- Đúng ý --> L[Hoàn thành (Bấm 👍)]
    K -- Sai thông tin --> M[HAX G9: TA-Bridge tạo ticket tự động hỗ trợ]
```

## Diễn giải 4 Kịch bản Trải nghiệm (§6)
* **1. Happy Path (Tự tin cao):** Học viên hỏi xem lịch sử điểm danh lớp $\rightarrow$ Trả lời rõ quy chế quét mã QR form tại lớp, vắng quá 4 buổi rớt môn, phân định không phải điểm XP rank Discord $\rightarrow$ Gắn nhãn `[📘 HỌC VỤ OFFLINE]` + Hộp trích dẫn nguồn quy chế.
* **2. Low-Confidence (Mơ hồ):** Học viên hỏi "Nghỉ có bị trừ điểm / rớt môn không?" $\rightarrow$ AI nhận diện sự mơ hồ giữa 2 hệ thống và đưa ra 2 chip chọn nhanh: `[🏫 Buổi học trên lớp]` (rớt môn) và `[💻 Buổi Workshop online]` (Zoom, tích lũy XP, không tính vắng trên lớp).
* **3. Failure / No-Grounding / Out-of-Scope:** Học viên xin sửa điểm danh hoặc xin nghỉ ốm $\rightarrow$ Bot gắn nhãn `[⛔ NGOÀI THẨM QUYỀN]`, từ chối can thiệp và cung cấp ngay mẫu email soạn sẵn gửi Lab Coach (`AIthucchien@vinuni.edu.vn`) + nút mở Ticket Discord.
* **4. Correction (Sửa sai):** Học viên bấm `[🚩 Sai thông tin / Chuyển cho TA]` $\rightarrow$ Hệ thống `TA-Bridge` tự động tạo ticket kèm tóm tắt hội thoại cho Trợ giảng xử lý ngay lập tức; đồng thời cho phép chọn lại ngữ cảnh.

## Bảng đối chiếu 4 Nguyên tắc HAX Toolkit (§4b)
| Nguyên tắc | Vị trí áp dụng cụ thể trên giao diện |
|---|---|
| **HAX G1 (Năng lực & phạm vi)** | Header kênh `#?-hỏi-trợ-lý-quy-chế` + 4 nút câu hỏi mẫu preset prompts dưới đáy khung chat |
| **HAX G2 (Minh bạch căn cứ)** | Badge màu phân định hệ thống (`Offline VinUni` vs `Online Discord`) + Hộp trích dẫn căn cứ quy chế |
| **HAX G9 (Hỗ trợ sửa lỗi)** | Nút `[🚩 Sai thông tin / Chuyển cho TA]` kích hoạt `TA-Bridge` + Các chip chọn ngữ cảnh |
| **HAX G10 (Thoái lui nhã nhặn)** | Nhãn `[⛔ NGOÀI THẨM QUYỀN]` + Mẫu email soạn sẵn gửi Lab Coach khi câu hỏi vượt thẩm quyền |

## Checklist CP2
- [x] Bản mẫu tương tác bấm thử được (`codebase/index.html`)
- [x] Sơ đồ luồng toàn diện từ đầu vào đến đầu ra (`codebase/FLOWCHART.md`)
- [x] Đủ 4 nhánh trải nghiệm: Happy, Low-confidence, Failure, Correction
- [x] Khai rõ Mock/Real và Cost-of-error trong `spec.md` §4 & §6
- [x] Bảng 4 nguyên tắc HAX Toolkit gắn đúng vị trí trên giao diện
