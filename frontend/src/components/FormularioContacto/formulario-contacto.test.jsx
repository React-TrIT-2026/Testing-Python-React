import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { FormularioContacto } from "./formulario-contacto";

describe("FormularioContactoComponent", () => {
    it.todo("muestra los tres campos y el botón de enviar");

    it.todo("muestra un error si se envía el formulario vacío");

    it.todo("llama a onEnviar con los datos rellenados");

    it.todo("muestra un error si el email no tiene arroba");
});
