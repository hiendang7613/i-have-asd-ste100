- **Causa:** `verifyToken` en `src/auth.ts:42` leía el token de una cabecera propia. El cliente nuevo envía `Authorization: Bearer <token>`.
- **Corrección:** `verifyToken` ahora lee la cabecera `Authorization`.

**Conclusion:** La prueba de login ya pasa; una prueba de pagos sigue fallando y no revisé la causa.

0. **Done:**
   - **Login:** `verifyToken` lee la cabecera correcta; `npm test` ejecutó 214 pruebas y pasan 213.
1. **InProgress:**
2. **Pending:**
3. **Questions:**
   - **Q1.** ¿Reviso `payment.spec.ts:88` antes de fusionar este cambio?
     - `<a>` Sí, ahora.
     - (b) Después de fusionar.
4. **Todos:**
   - **Prueba de pagos:** buscar por qué falla `payment.spec.ts:88`; no cambié el código de pagos.
5. **Backlog:**
6. **Risks:**
   - **R1.** `jsonwebtoken` 8.5.1 es anterior a la versión de seguridad 9.0.0.
     - `<a>` actualizarlo en un cambio aparte | (b) omitir | (c) más tarde
7. **AIIdeas:**
   - **I1.** Añadir una prueba que envíe `Authorization: Bearer <token>`, para que este error no vuelva.
     - `<a>` planificarlo | (b) omitir | (c) más tarde
