import pytest

# from src.gestor_pedidos import Pedido

class TestPedido():

    # 1. setup_class
    # 2. setup_method
    # 3. test_crear_pedido
    # 4. teardown_method
    # 5. setup_method
    # 6. test_confirmar_pedido
    # 7. teardown_method
    # 8. teardown_class
    
    def setup_class(self):
        print("setup_class: Inicializando recursos compartidos para todos los tests de la clase TestPedido.")

    def setup_method(self):
        print("setup_method: Inicializando recursos para el test actual.")

    def test_crear_pedido(self):
        print("test_crear_pedido: Ejecutando test para crear un pedido.")

    def teardown_method(self):
        print("teardown_method: Limpiando recursos después del test actual.")

    def teardown_class(self):
        print("teardown_class: Limpiando recursos compartidos después de todos los tests de la clase TestPedido.")


class TestAplicarDescuentoPorVolumen:
    @pytest.fixture(autouse=True, scope="class")
    def conectar_con_autouse(self):
        print("1, 2, 3, 4") # Setup
        yield "Conexión a la base de datos establecida" # Yield
        print("4, 3, 2, 1") # Teardown

    @pytest.fixture(autouse=True, scope="function")
    def conectar_a_base_de_datos(self):
        print("Conectando a la base de datos...") # Setup
        yield "Conexión a la base de datos establecida" # Yield
        print("Cerrando la conexión a la base de datos...") # Teardown


    def test_aplicar_descuento_por_volumen_1(self):
        print("test_aplicar_descuento_por_volumen: Ejecutando test para aplicar descuento")

    def test_aplicar_descuento_por_volumen_2(self):
        print("test_aplicar_descuento_por_volumen: Ejecutando test para aplicar descuento")

    def test_aplicar_descuento_por_volumen(self):
        print("test_aplicar_descuento_por_volumen: Ejecutando test para aplicar descuento")