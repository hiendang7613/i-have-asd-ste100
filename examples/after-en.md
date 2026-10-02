- **Cause:** `verifyToken` in `src/auth.ts:42` read the token from a custom header. The new client sends `Authorization: Bearer <token>`.
- **Fix:** `verifyToken` now reads the `Authorization` header.

**Conclusion:** The login test passes now; one payment test still fails, and I did not check why.

**0.Done:** Login fix in `verifyToken`; `npm test` ran 214 tests and 213 pass.

**2.Questions:**
  - **Q1.** Check `payment.spec.ts:88` before this change is merged?
    - `<a>` Yes, check it now.
    - (b) After the merge.

**3.Todos:** Check why `payment.spec.ts:88` fails; I did not change payment code.

**5.Backlog:** `jsonwebtoken` 8.5.1 is old; update it in a separate change.
