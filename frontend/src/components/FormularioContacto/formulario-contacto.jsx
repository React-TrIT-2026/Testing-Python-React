import { useState } from "react";

export const ERROR_CAMPOS_OBLIGATORIOS = "Todos los campos son obligatorios";
export const ERROR_EMAIL_INVALIDO = "El email no es válido";

export default function FormularioContacto({ onEnviar }) {
  const [nombre, setNombre] = useState("");
  const [email, setEmail] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!nombre.trim() || !email.trim() || !mensaje.trim()) {
      setError(ERROR_CAMPOS_OBLIGATORIOS);
      return;
    }
    if (!email.includes("@")) {
      setError(ERROR_EMAIL_INVALIDO);
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
