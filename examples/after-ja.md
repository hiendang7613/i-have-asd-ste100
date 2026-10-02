- **原因：** `src/auth.ts:42` の `verifyToken` が独自のヘッダーを読んでいました。新しいクライアントは `Authorization: Bearer <token>` を送ります。
- **修正：** `verifyToken` は `Authorization` ヘッダーを読むようになりました。

**Conclusion:** ログインのテストは成功、決済テスト 1 件は失敗中で原因は未確認です。

0. **Done:**
   - **ログイン修正：** `verifyToken` が正しいヘッダーを読む。`npm test` で 214 件中 213 件が成功。
1. **InProgress:**
2. **Pending:**
3. **Questions:**
   - **Q1.** マージ前に `payment.spec.ts:88` を確認しますか？
     - `<a>` はい、今確認する。
     - (b) マージ後に確認する。
4. **Todos:**
   - **決済テスト：** `payment.spec.ts:88` の失敗原因を調べる。決済のコードは変更していません。
5. **Backlog:**
6. **Risks:**
   - **R1.** `jsonwebtoken` 8.5.1 は、セキュリティ修正を含む 9.0.0 より古い版です。
     - `<a>` 別の変更で更新する | (b) 見送る | (c) 後で
7. **AIIdeas:**
   - **I1.** `Authorization: Bearer <token>` を送るテストを追加し、この不具合の再発を防ぐ。
     - `<a>` 計画する | (b) 見送る | (c) 後で
