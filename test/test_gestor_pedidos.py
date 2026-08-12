import pytest

from src.gestor_pedidos import Pedido

class TestPedido:
    pass

class TestCalcularEnvio:
    pass

class TestAplicarDescuentoPorVolumen:
    pass

        pedido = Pedido(
            id_pedido=4,
            items=[{"precio": 20, "cantidad": 5}],
            cliente_vip=False
        )
        pedido.cancelar_pedido()
        assert pedido.estado == "cancelado"