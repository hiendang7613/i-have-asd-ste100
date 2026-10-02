- Causa: `verifyToken` en `src/auth.ts:42` leía una cabecera propia. El cliente nuevo envía `Authorization: Bearer <token>`.
- Corrección: `verifyToken` ahora lee la cabecera `Authorization`.
- Pruebas: `npm test` ejecutó 214 pruebas. Pasan 213.
- `payment.spec.ts:88` falla. No cambié el código de pagos y no revisé la causa.

Conclusión: El login ya funciona; una prueba de pagos sigue fallando, causa sin revisar.
Aprobar: Ninguno.
Tu acción: Ninguna.
Pregunta: ¿Reviso `payment.spec.ts:88` ahora (recomendado) o después de fusionar este cambio?
Pendiente: `jsonwebtoken` 8.5.1 está desactualizado; puedo actualizarlo después de revisar los pagos.
