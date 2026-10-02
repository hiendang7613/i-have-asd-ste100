- **原因：** `src/auth.ts:42` 中的 `verifyToken` 读取了自定义请求头。新客户端发送 `Authorization: Bearer <token>`。
- **修复：** `verifyToken` 现在读取 `Authorization` 请求头。
- ✅ **测试：** `npm test` 运行了 214 个测试，213 个通过。
- ❌ `payment.spec.ts:88` 失败。我没有修改支付代码，也没有检查原因。

- 🎯 **结论：** 登录问题已修复；一个支付测试仍然失败，原因未检查。
- 🔑 **需要批准：** 无。
- 👉 **你需要做：** 无。
- ❓ **问题：** 现在检查 `payment.spec.ts:88`（推荐）还是合并之后再检查？
- 📌 **待办：** `jsonwebtoken` 8.5.1 已过时；检查支付测试后我可以更新它。
