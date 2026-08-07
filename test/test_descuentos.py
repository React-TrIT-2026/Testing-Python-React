import pytest

from src.descuentos import calcular_descuento, descuento_por_franja, precio_final_con_envio

@pytest.fixture
def precio_base():
    return 100 


def test_calcular_descuento_basico(precio_base):
    PRECIO_BASE = precio_base
    PORCENTAJE_DESCUENTO = 10
    RESULTADO_ESPERADO = 90

    resultado = calcular_descuento(PRECIO_BASE, PORCENTAJE_DESCUENTO)

    assert resultado == RESULTADO_ESPERADO

def test_calcular_descuento_porcentaje_invalido():
    PRECIO_BASE = 100

    with pytest.raises(ValueError):
        calcular_descuento(PRECIO_BASE, 150)

    with pytest.raises(ValueError):
        calcular_descuento(PRECIO_BASE, -10)

    with pytest.raises(ValueError):
        calcular_descuento(PRECIO_BASE, 0)

    with pytest.raises(ValueError):
        calcular_descuento(PRECIO_BASE, 100)