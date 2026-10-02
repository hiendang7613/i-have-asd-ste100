- **Cause:** `verifyToken` in `src/auth.ts:42` read a custom header. The new client sends `Authorization: Bearer <token>`.
- **Fix:** `verifyToken` now reads the `Authorization` header.

**Conclusion:** Login is fixed and on staging; one payment test still fails, cause not checked.

0. **Done:** Login fix; `npm test` ran 214 tests and 213 pass; staging is deployed.
1. **InProgress:**
2. **Questions:**
   - **Q1.** Approve: deploy the login fix to production?
     - `<a>` Yes, after I check `payment.spec.ts:88`.
     - (b) Yes, now.
3. **Todos:** Check why `payment.spec.ts:88` fails; I did not change payment code.
4. **Pending:**
5. **Backlog:** `jsonwebtoken` 8.5.1 is old; update it after the deploy.
