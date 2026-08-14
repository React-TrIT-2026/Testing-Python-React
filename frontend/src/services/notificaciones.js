/**
 * Envío de notificaciones al cliente. En producción esto sería una
 * llamada de red; aquí se simula, y en los tests se sustituye entero
 * con `jest.mock()`.
 */

export function enviarEmail(destinatario, asunto) {
  console.log(`Enviando email a ${destinatario}: ${asunto}`);
  return true;
}
