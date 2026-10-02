- **原因：** `src/auth.ts:42` の `verifyToken` が独自のヘッダーを読んでいました。新しいクライアントは `Authorization: Bearer <token>` を送ります。
- **修正：** `verifyToken` は `Authorization` ヘッダーを読むようになりました。

**Conclusion:** ログインのテストは成功、決済テスト 1 件は失敗中で原因は未確認です。

0. **Done:** `verifyToken` を修正、`npm test` で 214 件中 213 件が成功。
1. **InProgress:**
2. **Questions:**
   - **Q1.** マージ前に `payment.spec.ts:88` を確認しますか？
     - `<a>` はい、今確認する。
     - (b) マージ後に確認する。
3. **Todos:** `payment.spec.ts:88` の失敗原因を調べる。決済のコードは変更していません。
4. **Pending:**
5. **Backlog:** `jsonwebtoken` 8.5.1 は古いので、別の変更で更新します。
