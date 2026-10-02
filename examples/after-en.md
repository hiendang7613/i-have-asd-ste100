- **Cause:** `verifyToken` in `src/auth.ts:42` read the token from a custom header. The new client sends `Authorization: Bearer <token>`.
- **Fix:** `verifyToken` now reads the `Authorization` header.

**Conclusion:** The login test passes now; one payment test still fails, and I did not check why.

0. **Done:**
   - **Login fix:** `verifyToken` reads the right header; `npm test` ran 214 tests and 213 pass.
1. **InProgress:**
2. **Pending:**
3. **Questions:**
   - **Q1.** Check `payment.spec.ts:88` before this change is merged?
     - `<a>` Yes, check it now.
     - (b) After the merge.
4. **Todos:**
   - **Payment test:** find why `payment.spec.ts:88` fails; I did not change payment code.
5. **Backlog:**
6. **Risks:**
   - **R1.** `jsonwebtoken` 8.5.1 is older than the 9.0.0 security release.
     - `<a>` update it in a separate change | (b) skip | (c) later
7. **AIIdeas:**
   - **I1.** Add a test that sends `Authorization: Bearer <token>`, so this bug cannot come back.
     - `<a>` plan it | (b) skip | (c) later
