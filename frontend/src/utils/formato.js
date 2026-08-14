/**
 * Funciones puras de formato y cálculo del carrito.
 * Sin dependencias externas: son el mejor punto de entrada para tests
 * unitarios clásicos (entrada -> salida, sin mocks).
 */

export function formatearPrecio(precio, moneda = "EUR") {
  if (typeof precio !== "number" || Number.isNaN(precio)) {
    throw new Error("El precio debe ser un número");
  }
  const simbolos = { EUR: "€", USD: "$", GBP: "£" };
  const simbolo = simbolos[moneda] || moneda;
  return `${precio.toFixed(2)}${simbolo}`;
}

export function esEmailValido(email) {
  if (typeof email !== "string") return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function calcularTotalCarrito(items) {
  if (!Array.isArray(items)) {
    throw new Error("items debe ser un array");
  }
  return items.reduce((total, item) => total + item.precio * item.cantidad, 0);
}

export function aplicarCuponDescuento(total, cupon) {
  const cupones = {
    BIENVENIDA10: 0.1,
    VERANO20: 0.2,
  };
  const descuento = cupones[cupon];
  if (descuento === undefined) {
    return total; // cupón no reconocido: no se aplica descuento, no se lanza error
  }
  return total * (1 - descuento);
}
