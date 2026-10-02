- **原因：** `src/auth.ts:42` の `verifyToken` が独自のヘッダーを読んでいました。新しいクライアントは `Authorization: Bearer <token>` を送ります。
- **修正：** `verifyToken` は `Authorization` ヘッダーを読むようになりました。

**結論：** ログインのテストは成功、決済テスト 1 件は失敗中で原因は未確認です。

**0.完了：** `verifyToken` を修正、`npm test` で 214 件中 213 件が成功。

**2.質問：**
  - **Q1.** マージ前に `payment.spec.ts:88` を確認しますか？
    - `<a>` はい、今確認する。
    - (b) マージ後に確認する。

**4.バックログ：**
  - `payment.spec.ts:88` は失敗中。決済のコードは変更していません。
  - `jsonwebtoken` 8.5.1 は古いので、決済の確認後に更新します。
