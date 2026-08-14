import { useState } from "react";

/**
 * Formulario de contacto controlado, para la práctica guiada de RTL.
 * Deliberadamente simple: nombre, email, mensaje, y validación básica
 * al enviar.
 */
export default function FormularioContacto({ onEnviar }) {
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!nombre.trim() || !email.trim() || !mensaje.trim()) {
      setError("Todos los campos son obligatorios");
      return;
    }
    if (!email.includes("@")) {
      setError("El email no es válido");
      return;
    }
    setError("");
    onEnviar({ nombre, email, mensaje });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="nombre">Nombre</label>
      <input id="nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} />

      <label htmlFor="email">Email</label>
      <input id="email" value={email} onChange={(e) => setEmail(e.target.value)} />

      <label htmlFor="mensaje">Mensaje</label>
      <textarea id="mensaje" value={mensaje} onChange={(e) => setMensaje(e.target.value)} />

      {error && <p role="alert">{error}</p>}

      <button type="submit" name="Enviar">Enviar</button>
    </form>
  );
}
