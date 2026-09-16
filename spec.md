# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 17/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — [Tên lát cắt] · Nhóm [XX] · Zone [X]
Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tối ưu tính năng có sẵn  [ ] Tính năng mới

## §1. User & Job
- Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ):
Học viên khóa 4 (giai đoạn Onboarding, đang bị ngợp bởi các quy định).
Workflow hiện tại: Quên deadline/quy chế -> Nhắn tin public tag Bot để hỏi nhanh -> Nhận câu trả lời từ Bot -> Tin tưởng làm theo -> Làm sai quy chế -> Khiếu nại với TA/Mod.
- Core JTBD (không tên sản phẩm/AI trong câu):
Cần tra cứu nhanh chóng và chính xác các mốc thời gian (deadline) và quy chế nộp bài của từng loại nhiệm vụ khác nhau, mà không cần phải tự lội lại hàng trăm tin nhắn thông báo cũ.
- Problem statement (KHÔNG chữ AI):
Học viên nhận thông tin sai lệch hoặc "râu ông nọ cắm cằm bà kia" về quy chế, thời hạn nộp bài từ hệ thống giải đáp tự động. Điều này dẫn đến rủi ro nộp sai hạn, mất điểm bài tập, và làm tăng đột biến khối lượng công việc xử lý khiếu nại cho đội ngũ quản lý (TA/Mod).
- Evidence (chuẩn A và/hoặc B — log đầy đủ trong repo):
  - Số liệu mining / kết quả khảo sát (n = ?, % xác nhận):
  Khai phá tệp k4_messages.csv (1.092 tin) và thực hiện khảo sát trên lớp. Trong 313 tin nhắn của bot, có tới ~10% tin nhắn trả lời sai ngữ cảnh hoàn toàn (nhầm lẫn các loại hình bài tập) hoặc rơi vào vòng lặp "bắt người dùng chọn menu nhưng cuối cùng vẫn từ chối trả lời".
  - ≥5 quote/ví dụ nguyên văn + nguồn:
  (Sai rủi ro cao - Nhầm bài Lab với báo cáo Daily) - M75012: [@BOT] nộp lab muộn trừ bao nhiêu điểm -> Bot (M77155): Nộp daily muộn hơn 10h sáng vẫn ghi nhận nhưng không tính +XP nhé.

(Chối bỏ thông tin lõi) - M07416: Hạn nộp Lab02 [@BOT] -> Bot (M28485): ...hiện tại mình không có thông tin về ngày giờ cụ thể cho hạn nộp Lab02 trong dữ liệu hiện tại.

(Vòng lặp menu vô dụng) - M20574: [@BOT] muộn sau 23h59 -> Bot đưa menu 3 lựa chọn -> M87457: [@BOT] 1 -> Bot (M03540): Phần này mình chưa chắc lắm... xin phép nhờ đội ngũ Mod hỗ trợ bạn ạ!.

(Chỉ sai luồng kênh) - M35641: [@BOT] tớ muốn dùng tính năng branch protection... -> Bot (M25518): Khuyên học viên gõ lệnh tạo ticket tại kênh [#?-hỏi-trợ-lý-kute] (Thực tế kênh này dùng để gõ bot command, không phải ticket).

(Đoán mò quy chế đội nhóm) - M10708: Hỏi về cách tạo team -> Bot (M25574/M9617): Lúng túng bắt chọn menu, sau đó user M10708 phải tự đính chính: bro đọc lại hướng dẫn sử dụng đi, tạo team là có lời mời từ bot vào org....
(Lỗi sai deadline nghiêm trọng - Hậu quả trực tiếp)
Hôm làm Lab day 4, deadline thực tế là 12h trưa hôm sau nhưng bot lại thông báo 24h đêm nay phải nộp bài. Bọn mình rất hoang mang, cuối cùng TA phải nhắn tin đính chính là 'kệ thông báo của bot'. Tốn hơn 1 tiếng đồng hồ và TA phải vào hỗ trợ trực tiếp để dập lửa." — Học viên A (Khảo sát trực tiếp)
(Bot bất lực trước xung đột thông tin)
Chương trình gửi 2 thời khóa biểu khác nhau qua mail làm mình không biết chọn cái nào mới đúng. Tốn 3-5 phút lên hỏi bot Discord để đối chiếu thì bot không hỗ trợ được, toàn bắt chọn 1, 2, 3 máy móc. Cuối cùng vẫn phải đi tìm Lab Coach hỏi trực tiếp." — Học viên B & E (Khảo sát trực tiếp)
(Nhầm lẫn quy chế lõi - Bot giải thích kém)
Mình bị nhầm lẫn loạn xạ giữa việc nộp /daily-standup trên Discord với điểm danh offline, tưởng nộp muộn standup là bị tính vắng học trên trường. Lên hỏi bot thì bot xả ra cả một đoạn văn siêu dài nhưng không trúng trọng tâm, đọc xong vẫn không biết luật thực tế là gì." — Học viên C (Khảo sát trực tiếp)
(Mơ hồ công cụ và giới hạn vắng mặt)
"Lớp yêu cầu quét mã QR Microsoft Form để điểm danh nhưng lên app MyVinUni tìm lịch sử thì không thấy. Mình cũng không rõ nghỉ Workshop online có bị tính vào giới hạn vắng tối đa 4 buổi của trường không. Bot toàn đưa thông tin chung chung, có khi còn bịa lệnh hoặc nhầm lẫn." — Học viên D (Khảo sát trực tiếp)

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):

[Ứng viên 1] Trả lời sai luật, nhầm deadline bài tập (VD: Nhầm Lab thành Daily).

1.000 học viên · 1-2 lần/tuần/người · Tốn: Điểm số của học viên (Fail bài), tốn thời gian TA đi xử lý sự cố đính chính · Khả thi: Cao (RAG giới hạn nguồn).

[Ứng viên 2] Trải nghiệm (UX) kém: Bắt người dùng chọn Menu 1-2-3 rồi từ chối trả lời.

1.000 học viên · 5-7 lần/tuần/người · Tốn: Tốn 3 lượt chat thừa, gây bực bội nhưng không chết người · Khả thi: Cao (Tối ưu Prompt).

[Ứng viên 3] Không nhận diện được câu hỏi ngoài phạm vi khóa học (Tán gẫu).

~100 học viên · Rất ít · Tốn: Không tốn gì, bot học tập không cần bắt buộc phải biết tán gẫu · Khả thi: Dễ.
- Ứng viên ĐÃ LOẠI + vì sao:
Đã loại Ứng viên 2 và Ứng viên 3.
Vì hai vấn đề này chỉ dừng lại ở mức "Phiền toái trải nghiệm" (Nice-to-have). Người dùng bực mình vì phải gõ số 1-2-3, nhưng cuối cùng họ vẫn sẽ hỏi Mod và nhận được câu trả lời. Hậu quả không định lượng được thành thiệt hại thực tế.

- Ứng viên CHỌN + vì sao (bằng số):
Vì đây là "Nỗi đau trí mạng". Nếu 1.000 học viên, chỉ cần 5% (50 người) tin vào câu trả lời M77155 của Bot ("nộp Lab muộn chỉ không được cộng XP"), 50 học viên này sẽ trễ hạn bài Lab và bị trừ điểm đánh giá khóa học trực tiếp.
Kéo theo đó, TA/Mod sẽ phải tốn 50 người x 10 phút = 500 phút (hơn 8 tiếng) chỉ để xử lý khiếu nại xin mở lại cổng nộp bài và giải thích rằng "Bot nói sai". Tối ưu lát cắt này là cứu lấy điểm số của học viên và quỹ thời gian của đội ngũ vận hành.
## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
Học viên Khóa 4 cần tra cứu nhanh và chính xác thời hạn nộp bài (deadline) cùng quy chế tương ứng của từng loại nhiệm vụ (Lab, Daily Standup, Workshop, Điểm danh) mà không bị nhầm lẫn giữa các loại hình, nhờ hệ thống AI tự động phân loại đúng ngữ cảnh nhiệm vụ và trích xuất nguyên văn căn cứ quy định chính thức để học viên tự tin nộp đúng hạn, bảo toàn điểm số.
- Non-goals (≥3 thứ KHÔNG build):
  1. Không build tính năng tán gẫu / trò chuyện ngoài phạm vi khóa học (chitchat).
  2. Không build hệ thống tự động giải bài tập hay viết mã nguồn hộ học viên (giữ vững liêm chính học thuật).
  3. Không thay thế hoàn toàn vai trò của Trợ giảng (TA/Mod) trong việc xử lý các trường hợp ngoại lệ hoặc đơn xin gia hạn đặc biệt.
- Mức prototype nhắm tới: [ ] Sketch [x] Mock [ ] Working — phần nào mock, phần nào thật:
  - **Mức nhắm tới:** Mock (Bản mẫu tương tác giao diện và luồng nghiệp vụ trên nền tảng web mô phỏng Discord).
  - **Phần chạy giả lập (Mock):** Giả lập việc truy vấn Vector DB (RAG) và tính toán điểm tự tin (Confidence score) thông qua các kịch bản mẫu có sẵn đã được cấu hình chặt chẽ.
  - **Phần chạy thực tế:** Toàn bộ luồng tương tác người dùng (Interactive Chat UI), cơ chế phân tách ngữ cảnh bằng nút bấm nhanh (Disambiguation chips), modal can thiệp sửa đổi trực tiếp từ người dùng (Human-in-the-loop Correction), và cơ chế chuyển tiếp ngoại lệ tới kênh Trợ giảng (TA escalation). (Tại CP3 sẽ tích hợp tối thiểu 1 lời gọi AI API thực tế).
- Automation: [x] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
  - **Chọn: Augment (Hỗ trợ con người ra quyết định).**
  - **Lý do theo cost-of-error:** Chi phí sai sót trong bài toán này là **cực kỳ cao (Trí mạng)**. Nếu hệ thống tự động hóa hoàn toàn và trả lời sai deadline bài Lab (ví dụ nhầm sang luật Daily như tin nhắn M77155), học viên sẽ bị trừ 50% đến 100% điểm bài tập, dẫn đến nguy cơ trượt môn; đồng thời làm tiêu tốn hàng chục giờ của TA để xử lý khiếu nại. Do đó, AI chỉ đóng vai trò hỗ trợ (Augment): bắt buộc luôn trích dẫn nguồn văn bản quy định cụ thể kèm nhãn độ tin cậy để học viên tự kiểm chứng trước khi hành động, và luôn có cơ chế cho con người can thiệp sửa sai tức thì.
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **HAX G1: Make clear what system can do** *(Làm rõ năng lực & phạm vi hệ thống)* | Banner tiêu đề kênh `#?-hỏi-trợ-lý-quy-chế` nêu rõ nhiệm vụ phân định 2 hệ thống (Offline VinUni vs Online Discord), kèm thanh nút gợi ý 4 câu hỏi thường gặp (Preset Prompts) ở đáy khung chat giúp học viên định hình rõ phạm vi hỗ trợ. |
  | **HAX G2: Make clear how well system can do** *(Minh bạch nguồn căn cứ & độ tin cậy)* | Mỗi câu trả lời đều gắn nhãn màu phân định rõ hệ thống (`[📘 HỌC VỤ OFFLINE — TRƯỜNG VINUNI]` màu xanh dương hoặc `[🟣 BUILD PHASE ONLINE — DISCORD]` màu tím) kèm hộp trích dẫn căn cứ quy chế chính thức (`Ma trận quy chế`). |
  | **HAX G9: Support efficient correction** *(Hỗ trợ người dùng sửa sai & can thiệp)* | Nút `[🚩 Sai thông tin / Chuyển cho TA]` gắn dưới mỗi câu trả lời, cho phép 1-click kích hoạt hệ thống `TA-Bridge` tạo ticket kèm tóm tắt hội thoại để Trợ giảng vào cuộc hỗ trợ; đồng thời các chip lựa chọn ngữ cảnh (`🏫 Buổi học trên lớp` / `💻 Buổi Workshop online`) giúp học viên điều hướng ngay khi câu hỏi bị hiểu nhầm. |
  | **HAX G10: Scope of services / Graceful failure** *(Thoái lui nhã nhặn, không vượt quyền)* | Khi học viên yêu cầu các việc ngoài thẩm quyền (nhờ sửa điểm danh, xin nghỉ ốm), bot gắn nhãn `[⛔ NGOÀI THẨM QUYỀN CỦA BOT]`, từ chối can thiệp và cung cấp ngay **Mẫu email soạn sẵn gửi Lab Coach** (`AIthucchien@vinuni.edu.vn`) cùng lệnh mở Ticket Discord. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- **Happy path:**
  - *Tình huống:* Học viên hỏi câu hỏi cụ thể về điểm danh lớp: *"Lịch sử điểm danh trên lớp xem ở đâu?"*
  - *Xử lý:* AI phân loại chính xác phạm vi Offline VinUni. Bot trả lời rõ: điểm danh qua mã QR Microsoft Form tại phòng học, chưa đồng bộ MyVinUni, vắng quá 4 buổi sẽ rớt môn; đồng thời cảnh báo phân định: đây KHÔNG PHẢI điểm XP cày rank trên Discord. Kèm nhãn `[📘 HỌC VỤ OFFLINE — TRƯỜNG VINUNI]` và trích dẫn mục "Điểm danh / Chuyên cần".
- **Low-confidence (②):**
  - *Tình huống:* Học viên hỏi câu mơ hồ, chưa rõ hệ thống nào: *"Nghỉ có bị trừ điểm / rớt môn không?"*
  - *Xử lý:* AI nhận diện câu hỏi có thể thuộc 2 hệ thống với chế tài hoàn toàn khác nhau. Thay vì đoán mò, bot hiển thị thông báo làm rõ và đưa ra 2 nút bấm lựa chọn nhanh: `[🏫 Buổi học trên lớp]` (vắng >4 buổi rớt môn) và `[💻 Buổi Workshop online]` (điểm danh tự động qua Zoom, chỉ tích lũy XP, không ảnh hưởng số buổi nghỉ trên lớp).
- **Failure/không căn cứ (①):**
  - *Tình huống:* Học viên hỏi câu ngoài lề hoặc yêu cầu vượt thẩm quyền: *"Hôm nay em xin nghỉ ốm, sửa điểm danh giúp em"* hoặc hỏi tán gẫu.
  - *Xử lý:* Bot nhận diện hành động ngoài thẩm quyền/ngoài phạm vi, gắn nhãn `[⛔ NGOÀI THẨM QUYỀN CỦA BOT]`, giải thích minh bạch bot không có quyền sửa điểm danh thay trường, đồng thời mở lối thoát: cung cấp nút `[📧 Mở mẫu email gửi IT/Lab Coach]` (có sẵn nội dung chuẩn gửi `AIthucchien@vinuni.edu.vn`) và nút `[🎫 Lệnh mở Ticket Discord]`.
- **Correction (user sửa):**
  - *Tình huống:* Học viên phát hiện câu trả lời chưa đúng ý hoặc thông tin thực tế trên lớp có cập nhật mới (ví dụ dời hạn Lab).
  - *Xử lý:* Dưới mỗi phản hồi luôn có nút `[🚩 Sai thông tin / Chuyển cho TA]`. Khi bấm nút, hệ thống `TA-Bridge` tự động tạo ticket gửi thông báo kèm tóm tắt ngữ cảnh hội thoại cho Trợ giảng trực ban dập lửa; đồng thời cho phép học viên bấm chip chọn lại ngữ cảnh để bot cung cấp đúng thông tin mong muốn.
- **Khi bị đòi ngoài phạm vi (③):**
  - *Tình huống:* Học viên nhờ bot can thiệp sửa điểm danh hoặc giải bài tập hộ: *"Sửa điểm danh giúp em"* / *"Giải hộ bài Lab"*.
  - *Xử lý:* Bot từ chối lịch sự, nêu rõ giới hạn thẩm quyền và chuyển hướng sang đúng kênh tiếp nhận (kênh ticket hoặc email bộ phận học vụ).
- **Case đặc thù domain (④):**
  - *Tình huống:* **Nhầm lẫn tai hại giữa Daily Standup trên Discord và Điểm danh Offline trên lớp** (Case kinh điển M77155): Học viên lo sợ nộp muộn standup bị tính vắng học trên trường.
  - *Xử lý:* Khi phát hiện câu hỏi chứa "standup" hoặc "điểm danh", bot lập tức giải thích sự tách biệt độc lập: Nộp `/daily-standup` muộn (sau 10h sáng) chỉ không được cộng XP cày rank Discord, hoàn toàn KHÔNG bị tính vắng học trên lớp và KHÔNG bị rớt môn. Giúp dập tắt ngay sự hoang mang của học viên.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
```