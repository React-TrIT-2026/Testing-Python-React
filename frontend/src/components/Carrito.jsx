import { useState } from "react";
import {
  formatearPrecio,
  calcularTotalCarrito,
  aplicarCuponDescuento,
} from "../utils/formato";
import { confirmarCompra } from "../services/compra";

const ARTICULOS_INICIALES = [
  { id: 1, nombre: "Camiseta técnica", precio: 24.95, cantidad: 1 },
  { id: 2, nombre: "Mallas de entreno", precio: 39.5, cantidad: 1 },
  { id: 3, nombre: "Botella 750 ml", precio: 12.0, cantidad: 2 },
];

export default function Carrito({ email }) {
  const [items, setItems] = useState(ARTICULOS_INICIALES);
  const [cupon, setCupon] = useState("");
  const [confirmacion, setConfirmacion] = useState(null);

  const subtotal = calcularTotalCarrito(items);
  const total = aplicarCuponDescuento(subtotal, cupon.trim().toUpperCase());

  function cambiarCantidad(id, delta) {
    setItems((actuales) =>
      actuales
        .map((item) =>
          item.id === id ? { ...item, cantidad: item.cantidad + delta } : item,
        )
        .filter((item) => item.cantidad > 0),
    );
  }

  function handleConfirmar() {
    setConfirmacion(confirmarCompra(email, total));
  }

  return (
    <section className="tarjeta">
      <h2>Tu carrito</h2>

      {items.length === 0 ? (
        <p className="vacio">No hay artículos en el carrito.</p>
      ) : (
        <ul className="lista-items">
          {items.map((item) => (
            <li key={item.id}>
              <span className="nombre">{item.nombre}</span>
              <span className="precio">{formatearPrecio(item.precio)}</span>
              <span className="cantidad">
                <button
                  type="button"
                  onClick={() => cambiarCantidad(item.id, -1)}
                  aria-label={`Quitar una unidad de ${item.nombre}`}
                >
                  −
                </button>
                {item.cantidad}
                <button
                  type="button"
                  onClick={() => cambiarCantidad(item.id, 1)}
                  aria-label={`Añadir una unidad de ${item.nombre}`}
                >
                  +
                </button>
              </span>
            </li>
          ))}
        </ul>
      )}

      <label htmlFor="cupon">Cupón de descuento</label>
      <input
        id="cupon"
        value={cupon}
        placeholder="BIENVENIDA10"
        onChange={(e) => setCupon(e.target.value)}
      />

      <dl className="totales">
        <dt>Subtotal</dt>
        <dd>{formatearPrecio(subtotal)}</dd>
        <dt>Total</dt>
        <dd>{formatearPrecio(total)}</dd>
      </dl>

      <button
        type="button"
        className="primario"
        disabled={items.length === 0}
        onClick={handleConfirmar}
      >
        Confirmar compra
      </button>

      {confirmacion && (
        <p role="status">
          Compra {confirmacion.estado} por {formatearPrecio(confirmacion.total)}.
          Te hemos enviado un email a {confirmacion.email}.
        </p>
      )}
    </section>
  );
}
