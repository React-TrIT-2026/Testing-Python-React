import pytest

from src.descuentos import calcular_descuento, descuento_por_franja, precio_final_con_envio


@pytest.mark.parametrize(
    "precio, porcentaje, resultado_esperado",
    [
        (100, 10, 90),
        (200, 20, 160),
        (50, 5, 47.5),
    ],
)
def test_calcular_descuento_basico(precio, porcentaje, resultado_esperado):
    resultado = calcular_descuento(precio, porcentaje)

    assert resultado == resultado_esperado

@pytest.mark.parametrize(
    "precio, porcentaje",
    [
        (100, -10),
        (100, 150)
    ],
)
def test_calcular_descuento_porcentaje_invalido(precio, porcentaje):
    with pytest.raises(ValueError):
        calcular_descuento(precio, porcentaje)