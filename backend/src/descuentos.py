"""
Módulo simple de cálculo de descuentos para la práctica guiada de pytest.
Código limpio y ya funcional -- el objetivo aquí es escribir tests,
no arreglar bugs (eso ya lo hicieron mentalmente en la práctica de Bloque 1).
"""


def calcular_descuento(precio, porcentaje):
    """Aplica un descuento porcentual a un precio. Lanza ValueError si el
    porcentaje no está entre 0 y 100."""
    if not (0 <= porcentaje <= 100):
        raise ValueError("El porcentaje debe estar entre 0 y 100")
    return precio - (precio * porcentaje / 100)


def descuento_por_franja(precio):
    """Descuento automático según el importe de la compra."""
    if precio >= 200:
        return calcular_descuento(precio, 20)
    elif precio >= 100:
        return calcular_descuento(precio, 10)
    elif precio >= 50:
        return calcular_descuento(precio, 5)
    return precio


def precio_final_con_envio(precio, gastos_envio, envio_gratis_desde=100):
    """Suma gastos de envío salvo que el precio supere el umbral de envío gratis."""
    if precio >= envio_gratis_desde:
        return precio
    return precio + gastos_envio
