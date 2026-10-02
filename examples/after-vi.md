- **Nguyên nhân:** `verifyToken` trong `src/auth.ts:42` đọc token từ một header riêng. Client mới gửi `Authorization: Bearer <token>`.
- **Cách sửa:** `verifyToken` nay đọc header `Authorization`.

**Kết luận:** Test đăng nhập đã đạt; còn một test thanh toán lỗi, chưa kiểm tra nguyên nhân.

**0.Đã xong:** Sửa `verifyToken`; `npm test` chạy 214 test, 213 test đạt.

**1.Đang làm:** Không có.

**2.Câu hỏi:**
  - **Q1.** Kiểm tra `payment.spec.ts:88` trước khi gộp thay đổi này?
    - `<a>` Có, kiểm tra ngay.
    - (b) Sau khi gộp.

**3.Việc cần làm:** Tìm nguyên nhân `payment.spec.ts:88` lỗi; tôi không sửa mã thanh toán.

**5.Tồn đọng:** `jsonwebtoken` 8.5.1 đã cũ; cập nhật trong một thay đổi riêng.
