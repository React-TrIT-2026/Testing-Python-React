import { useState } from "react";
import Carrito from "./components/Carrito";
import FormularioContacto from "./components/FormularioContacto";

export default function App() {
  const [mensajes, setMensajes] = useState([]);

  return (
    <main className="app">
      <header>
        <h1>Tienda</h1>
        <p className="subtitulo">Demo de la academia de testing</p>
      </header>

      <Carrito email="ana@ejemplo.com" />

      <section className="tarjeta">
        <h2>¿Alguna duda?</h2>
        <FormularioContacto
          onEnviar={(datos) => setMensajes((previos) => [...previos, datos])}
        />
        {mensajes.length > 0 && (
          <p role="status">
            Gracias, {mensajes[mensajes.length - 1].nombre}. Te respondemos en 24 h.
          </p>
        )}
      </section>
    </main>
  );
}
