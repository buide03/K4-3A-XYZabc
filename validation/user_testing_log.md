# Nhật ký Kiểm chứng Người dùng Thực tế (User Testing Log) — Khối R6 (CP5)
**Dự án:** Trợ lý Tra cứu Quy chế & Lịch nộp bài Khóa 4 (Track B)  
**Thời gian thực hiện:** Sáng 18/9/2026  
**Địa điểm:** Phòng E403, Lớp 3A  
**Phương pháp áp dụng:** **Mom Test** — Giao nhiệm vụ thực tế, giữ im lặng hoàn toàn quan sát thao tác, ghi nhận chính xác điểm tắc nghẽn và trích dẫn nguyên văn phản hồi (không gợi ý, không hỏi xã giao).

---

## 1. Danh sách Người dùng Thử nghiệm & Nhật ký Chi tiết (5 Người dùng ngoài nhóm)

> Bắt buộc gồm tối thiểu 2 người dùng thuộc danh sách **Willing Users đã khai từ CP1** (Nguyễn Văn Hoàng & Trần Thị Mai).

| STT | Người thử | Phân loại | Nhiệm vụ giao (Task) | Điểm tắc nghẽn (Kẹt ở đâu) | Trích dẫn nguyên văn (Mom Test Quote) | Quyết định xử lý của nhóm |
|:---:|---|---|---|---|---|---|
| **1** | **Nguyễn Văn Hoàng** *(Lớp 3A, E403 - Đã khai CP1)* | Willing User | **Task 1:** "Hỏi bot xem hôm nay nộp muộn bài Lab 02 lúc 0h30 thì bị trừ bao nhiêu điểm và có nguy cơ trượt môn không." | Học viên nhận được câu trả lời đúng trừ 50%, nhưng mắt nhìn đảo quanh tìm kiếm xem có link nộp bù hay không vì giao diện có quá nhiều chữ. | *"Ủa bot bảo bị trừ 50% sau 23h59 rồi, nhưng có chỗ nào bấm vào xem quy chế nộp bù trước 12h trưa mai luôn không, nhìn đoạn này hơi nhiều chữ quá."* | **Sửa ngay:** In đậm mốc giờ vàng `12:00 trưa hôm sau` và làm nổi bật hộp trích dẫn căn cứ `[Điều 4.2 - Quy chế Lab]`. |
| **2** | **Trần Thị Mai** *(Lớp 3A, E403 - Đã khai CP1)* | Willing User | **Task 2:** "Hôm nay em quên nộp /daily-standup trên Discord, kiểm tra xem có bị tính vắng học trên trường không và có rớt môn không." | Người dùng ban đầu lúng túng không biết gõ gì, sau đó nhìn thấy thanh nút bấm gợi ý (Preset Chips) ở dưới cùng khung chat và bấm thử. | *"May quá nó ghi rõ không bị vắng học trên lớp, chứ hôm trước đọc thông báo bot cũ tưởng bị tính 1 buổi vắng trường VinUni sợ phát khóc. Nhưng cái nút 'Sai thông tin / Chuyển TA' này bấm vào có bị gửi ticket thật lên TA không hay chỉ demo?"* | **Giải thích & Giữ nguyên:** Giữ nguyên nút `[🚩 Báo sai / Chuyển TA]` vì đây là nguyên tắc HAX G9 cốt lõi; bổ sung tooltip: *"Tự động gửi ngữ cảnh tới TA trực ban phòng E403"*. |
| **3** | **Lê Bảo Anh** *(Lớp 3A, E403)* | Người ngoài nhóm | **Task 3:** "Bạn bị sốt xuất huyết nằm viện không đi học được, hãy nhờ bot can thiệp sửa điểm danh trên lớp hôm nay giúp bạn." | Học viên cố tình gõ câu nài nỉ xin sửa điểm danh. Bot gắn nhãn đỏ `[⛔ NGOÀI THẨM QUYỀN]` và hiện nút mở mẫu email. Bạn bấm thử nút email. | *"Nó không nhận sửa là đúng rồi, trường quản lý điểm danh gắt lắm bot nào sửa được. Nhưng cái nút mở email này xịn đấy, bấm phát hiện sẵn mẫu gửi AIthucchien@vinuni.edu.vn đỡ phải tự soạn văn bản xin phép."* | **Giữ nguyên:** Xác nhận cơ chế Graceful Failure (HAX G10) hoạt động cực tốt và mang lại giá trị thực tế cao cho người dùng. |
| **4** | **Phạm Đức Minh** *(Lớp 3A, E403)* | Người ngoài nhóm | **Task 4:** "Deadline trên VLearn ghi 23h59 nhưng bạn nghe bạn cùng bàn bảo Lab Coach vừa dời sang trưa mai. Hãy hỏi bot để xác nhận." | Học viên gõ: *"Coach dời deadline lab trưa mai rồi đúng ko bot"*. Bot trả lời hướng dẫn theo thông báo của Coach và kích hoạt đề xuất kết nối TA. | *"Bot trả lời thông minh đấy, biết nhắc là nghe theo lời Coach tại lớp nhưng cần đối chiếu lại kênh điều phối. Nhưng mà font chữ trích dẫn hơi nhỏ khi xem trên điện thoại."* | **Sửa trước demo:** Tăng kích thước font chữ của hộp trích dẫn căn cứ quy chế (`policy-quote`) từ `12px` lên `13.5px` trên giao diện web mobile. |
| **5** | **Hoàng Thu Trang** *(Lớp 3A, E403)* | Người ngoài nhóm | **Task 5:** "Hỏi bot xem điểm XP cày rank Discord có được cộng vào điểm tổng kết môn học trên trường không." | Học viên dùng thanh Preset Chips bấm nút câu hỏi mẫu số 4: *"Điểm XP Discord có cộng vào điểm môn học không?"*. Nhận kết quả ngay trong 1.2 giây. | *"Bấm cái nút mẫu ở dưới tiện thật, không cần gõ phím. Trả lời dứt khoát là không cộng vào điểm trường, chỉ để đua top nhận quà Discord. Rất rõ ràng!"* | **Giữ nguyên:** Thanh Preset Prompts ở đáy khung chat (HAX G1) là điểm cộng trải nghiệm lớn nhất, giúp học viên định hướng ngay phạm vi. |

---

## 2. Bốn Dòng Tổng Kết Theo Quy Định Bắt Buộc Của Khối R6

1. **Chủ đề lặp lại nhiều nhất trong phản hồi:**
   - Học viên đánh giá rất cao việc **phân định rạch ròi 2 hệ thống** (không còn bị nhầm Standup mất XP với vắng học trên trường) và tính tiện dụng của **thanh nút gợi ý câu hỏi (Preset Chips)** cùng **mẫu email soạn sẵn gửi Lab Coach**.
   - Điểm băn khoăn: Một số đoạn phản hồi về quy chế còn hơi dày đặc chữ; cần làm nổi bật ngay các mốc giờ then chốt (`23:59`, `12:00 trưa`, `10:00 sáng`).

2. **Sẽ sửa gì trước khi demo trên sân khấu:**
   - **Định dạng trực quan (Visual Hierarchy):** Tăng kích thước font chữ phần trích dẫn căn cứ quy chế, in đậm và tô vàng các mốc giờ deadline quan trọng để người dùng nắm bắt thông tin chỉ trong 2 giây lướt mắt.
   - **Tối ưu hóa phản hồi lỗi mạng (Khắc phục ca ADV09):** Đảm bảo địa chỉ email `AIthucchien@vinuni.edu.vn` luôn được in đậm nổi bật ngay trong câu trả lời văn bản khi có sự cố khẩn cấp.

3. **Giữ nguyên gì và vì sao:**
   - **Giữ nguyên cơ chế Augment & Từ chối an toàn (HAX G10):** Tuyệt đối không cho phép AI tự động can thiệp dữ liệu điểm danh hay code hộ bài tập, vì bảo vệ liêm chính học thuật và tính pháp lý của nhà trường là ranh giới bất khả xâm phạm.
   - **Giữ nguyên cấu trúc giao diện mô phỏng Discord:** Vì 100% học viên tham gia thử nghiệm đều quen thuộc với giao diện kênh chat này, không mất thời gian làm quen (zero learning curve).

4. **Gì để dành sau (Kế hoạch dài hạn sau Hackathon):**
   - Đóng gói thành Discord Gateway Bot chính thức để tích hợp trực tiếp vào Server Discord của toàn bộ Khóa 4 và các khóa sau.
   - Xây dựng Vector Database phân tán (ChromaDB) để tự động hóa việc cập nhật các thông báo mới từ ban tổ chức theo thời gian thực mà không cần nạp lại context prompt.
