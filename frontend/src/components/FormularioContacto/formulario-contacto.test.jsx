import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { FormularioContacto } from "./formulario-contacto";

describe("FormularioContactoComponent", () => {
    it("muestra los tres campos y el botón de enviar", () => {
        // Arrange
        const onEnviar = () => {}

        // Act
        render(<FormularioContacto onEnviar={onEnviar} />);

        // Assert
        expect(screen.getByAltText("")).toBeInTheDocument();

        expect(screen.getByLabelText("Nombre")).toBeInTheDocument();
        expect(screen.getByLabelText("Email")).toBeInTheDocument();
        expect(screen.getByLabelText("Mensaje")).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Enviar"})).toBeInTheDocument();
    });

    it("muestra un error si se envía el formulario vacío", () => {
        // Arrange
        const user = userEvent.setup()
        render(<FormularioContacto onEnviar={() => {}} />)

        // Act
        await user.click(screen.getByRole("button", { name: "Enviar"}))

        // Assert
        expect(screen.getByRole("alert")
            .toHaveTextContent("Todos los campos son obligatorios"))
    });

    it.todo("llama a onEnviar con los datos rellenados");

    it.todo("muestra un error si el email no tiene arroba");
});
