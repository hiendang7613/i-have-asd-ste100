Next: approve the production deploy, or tell me to check `payment.spec.ts:88` first.

Login works for the new client now: `verifyToken` (`src/auth.ts:42`) reads the `Authorization: Bearer <token>` header instead of a custom one.

1. `npm test`: 213 of 214 pass.
2. `payment.spec.ts:88` fails. I did not change payment code and did not check the cause.
3. Staging is deployed.

Step 3 of 4 done. Production deploy waits for your approval.

Separately: `jsonwebtoken` 8.5.1 is old. Want me to update it after this?

Next: reply "deploy" or "check payment first".
