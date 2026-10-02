- **Causa:** `verifyToken` en `src/auth.ts:42` leía el token de una cabecera propia. El cliente nuevo envía `Authorization: Bearer <token>`.
- **Corrección:** `verifyToken` ahora lee la cabecera `Authorization`.

**Conclusión:** La prueba de login ya pasa; una prueba de pagos sigue fallando y no revisé la causa.

0. **Hecho:** Corrección en `verifyToken`; `npm test` ejecutó 214 pruebas y pasan 213.
1. **En curso:** Ninguno.
2. **Preguntas:**
   - **Q1.** ¿Reviso `payment.spec.ts:88` antes de fusionar este cambio?
     - `<a>` Sí, ahora.
     - (b) Después de fusionar.
3. **Por hacer:** Buscar por qué falla `payment.spec.ts:88`; no cambié el código de pagos.
4. **Pendiente:** Ninguno.
5. **Más adelante:** `jsonwebtoken` 8.5.1 está desactualizado; actualizarlo en un cambio aparte.
