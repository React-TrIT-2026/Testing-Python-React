import {
    formatearPrecio
} from "./formato";

describe("formatearPrecio", () => { 
    // Happy Path: precio válido y moneda por defecto
    it("formatea un precio en euros por defecto", () => {
        // Arrange
        const PRECIO = 19.9;
        const MONEDA = "EUR";
        const RESULTADO_ESPERADO = "19.90€";

        // Act
        const RESULTADO = formatearPrecio(PRECIO, MONEDA);

        // Assert
        expect(RESULTADO).toBe(RESULTADO_ESPERADO);
    });

    // Cornel Case: precio válido y moneda indicada
    it("formatea un precio en la moneda indicada", () => {
        // Arrange
        const PRECIO = 19.9;
        const MONEDA = "USD";
        const RESULTADO_ESPERADO = "19.90$";

        // Act
        const RESULTADO = formatearPrecio(PRECIO, MONEDA);

        // Assert
        expect(RESULTADO).toBe(RESULTADO_ESPERADO);
    });

    // Error Path: precio no es un número
    it("lanza un error si el precio no es un número", () => {
        // Arrange
        const PRECIO = "19.9";
        const MONEDA = "EUR";

        // Act & Assert
        expect(() => formatearPrecio(PRECIO, MONEDA))
            .toThrow("El precio debe ser un número");
    });
});

describe("esEmailValido", () => { });

describe("calcularTotalCarrito", () => { });

describe("aplicarCuponDescuento", () => { });