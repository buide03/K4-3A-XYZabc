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
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

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