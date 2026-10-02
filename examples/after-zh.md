- **原因：** `src/auth.ts:42` 中的 `verifyToken` 读取了自定义请求头。新客户端发送 `Authorization: Bearer <token>`。
- **修复：** `verifyToken` 现在读取 `Authorization` 请求头。

**结论：** 登录测试已通过；一个支付测试仍然失败，原因未检查。

**0.已完成：** 修复了 `verifyToken`；`npm test` 运行 214 个测试，213 个通过。

**1.进行中：** 无。

**2.问题：**
  - **Q1.** 合并前先检查 `payment.spec.ts:88` 吗？
    - `<a>` 是，现在检查。
    - (b) 合并之后再检查。

**3.待办：** 查明 `payment.spec.ts:88` 失败的原因；我没有修改支付代码。

**5.以后再做：** `jsonwebtoken` 8.5.1 已过时；另开一个变更来更新。
