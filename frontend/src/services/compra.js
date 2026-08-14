import { enviarEmail } from "./notificaciones";

export function confirmarCompra(email, total) {
  if (total <= 0) {
    throw new Error("El total debe ser mayor que 0");
  }
  enviarEmail(email, `Compra confirmada: ${total.toFixed(2)}€`);
  return { email, total, estado: "confirmada" };
}
