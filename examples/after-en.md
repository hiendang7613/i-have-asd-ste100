- **Cause:** `verifyToken` in `src/auth.ts:42` read the token from a custom header. The new client sends `Authorization: Bearer <token>`.
- **Fix:** `verifyToken` now reads the `Authorization` header.
- ✅ **Tests:** `npm test` ran 214 tests. 213 pass.
- ❌ `payment.spec.ts:88` fails. I did not change payment code, and I did not check the cause.

- 🎯 **Conclusion:** The login test passes now; one payment test still fails, cause not checked.
- 🔑 **Approve:** None.
- 👉 **Your action:** None.
- ❓ **Question:** Should I check `payment.spec.ts:88` now (recommended) or after this change is merged?
- 📌 **Open:** `jsonwebtoken` 8.5.1 is old; I can update it after the payment check.
