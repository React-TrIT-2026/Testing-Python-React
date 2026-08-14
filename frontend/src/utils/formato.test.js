import {
    formatearPrecio
} from "./formato";

describe("formatearPrecio", () => { 
    // Happy Path: precio válido y moneda por defecto
    it.each([
        { precio: 19.9, moneda: "EUR", resultado: "19.90€" },
        { precio: 19.9, moneda: "USD", resultado: "19.90$" },
        { precio: 19.9, moneda: "GBP", resultado: "19.90£" }
    ])("formatea un precio en %s", ({ precio, moneda, resultado }) => {
        // Act
        const RESULTADO = formatearPrecio(precio, moneda);

        // Assert
        expect(RESULTADO).toBe(resultado);
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

describe("esEmailValido", () => { 
    it("acepta un email con formato correcto", () => {
        // Arrange
        const EMAIL = "test@trainingit.com";

        // Act
        const RESULTADO = esEmailValido(EMAIL);

        // Assert
        expect(RESULTADO).toBe(true);
    
    });

    it("rechaza un email sin arroba", () => { 
        // Arrange
        const EMAIL = "test.trainingit.com";

        // Act
        const RESULTADO = esEmailValido(EMAIL);

        // Assert
        expect(RESULTADO).toBe(false);
    });

    it("rechaza un valor que no es un string", () => { 
        // Arrange
        const EMAIL = 123;

        // Act
        const RESULTADO = esEmailValido(EMAIL);

        // Assert
        expect(RESULTADO).toBe(false);
    });
});

describe("calcularTotalCarrito", () => { 
    // Setup
    beforeAll(() => {});

    beforeEach(() => {});

    // Tests

    it.todo("suma precio * cantidad de cada item");

    it.skip("devuelve 0 si el carrito está vacío");

    it.only("lanza un error si el carrito no es un array"); // pytest -k

    // Teardown
    afterEach(() => {});

    afterAll(() => {});
});

describe("aplicarCuponDescuento", () => { });