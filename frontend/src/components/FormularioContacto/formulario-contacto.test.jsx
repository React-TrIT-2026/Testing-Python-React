import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { 
    FormularioContacto, 
    ERROR_CAMPOS_OBLIGATORIOS, 
    ERROR_EMAIL_INVALIDO 
} from "./formulario-contacto";

describe("FormularioContactoComponent", async () => {
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

    it("muestra un error si se envía el formulario vacío", async () => {
        // Arrange
        const user = userEvent.setup()
        render(<FormularioContacto onEnviar={() => {}} />)

        // Act
        await user.click(screen.getByRole("button", { name: "Enviar"}))

        // Assert
        expect(screen.getByRole("alert")
            .toHaveTextContent(ERROR_CAMPOS_OBLIGATORIOS))
    });

    it("llama a onEnviar con los datos rellenados", async () => {
        // Arrange
        const NOMBRE = "Manuel S. Lemos"
        const EMAIL = "mlemos@ferrumox.com"
        const MENSAJE = "Esto es un mensaje"

        const onEnviarMock = jest.fn()

        const user = userEvent.setup()
        render(<FormularioContacto onEnviar={onEnviarMock} />);

        // Act
        await user.type(screen.getByLabelText("Nombre"), NOMBRE)
        await user.type(screen.getByLabelText("Email"), EMAIL)
        await user.type(screen.getByLabelText("Mensaje"), MENSAJE)

        await user.click(screen.getByRole("button", { name: "Enviar"}))

        // Assert
        expect(onEnviarMock).toHaveBeenCalledWith({ NOMBRE, EMAIL, MENSAJE })
    });

    it("muestra un error si el email no tiene arroba", async () => {
        // Arrange
        const NOMBRE = "Manuel S. Lemos"
        const EMAIL = "mlemos.ferrumox.com"
        const MENSAJE = "Esto es un mensaje"

        const user = userEvent.setup()
        render(<FormularioContacto onEnviar={() => {}} />);

        // Act
        await user.type(screen.getByLabelText("Nombre"), NOMBRE)
        await user.type(screen.getByLabelText("Email"), EMAIL)
        await user.type(screen.getByLabelText("Mensaje"), MENSAJE)

        await user.click(screen.getByRole("button", { name: "Enviar"}))

        // Assert
        expect(screen.getByRole("alert")
            .toHaveTextContent(ERROR_EMAIL_INVALIDO))
    });
});
