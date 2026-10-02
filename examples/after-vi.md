- Nguyên nhân: `verifyToken` trong `src/auth.ts:42` đọc token từ một header riêng. Client mới gửi `Authorization: Bearer <token>`.
- Cách sửa: `verifyToken` nay đọc header `Authorization`.
- Test: `npm test` chạy 214 test, 213 test đạt.
- `payment.spec.ts:88` lỗi. Tôi không sửa mã thanh toán và chưa kiểm tra nguyên nhân.

Chốt: Test đăng nhập đã đạt; còn một test thanh toán lỗi, chưa kiểm tra nguyên nhân.
Cần duyệt: Không có.
Bạn cần làm: Không có.
Câu hỏi: Tôi kiểm tra `payment.spec.ts:88` ngay (khuyến nghị) hay sau khi gộp thay đổi này?
Việc còn mở: `jsonwebtoken` 8.5.1 đã cũ; tôi có thể cập nhật sau khi kiểm tra test thanh toán.
