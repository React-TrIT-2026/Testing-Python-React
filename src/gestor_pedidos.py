"""
Módulo de gestión de pedidos de una tienda online.
Sin tests. Para usar en la discusión de "riesgos de un repo sin testear".

Contiene bugs intencionados y deuda técnica para que el grupo los descubra
leyendo el código, sin ejecutar nada todavía.
"""

from datetime import datetime


class Pedido:
    def __init__(self, id_pedido, items, cliente_vip=False):
        self.id_pedido = id_pedido
        self.items = items  # lista de dicts: {"precio": float, "cantidad": int}
        self.cliente_vip = cliente_vip
        self.estado = "pendiente"
        self.fecha_creacion = datetime.now()

    def calcular_total(self):
        total = 0
        for item in self.items:
            total += item["precio"] * item["cantidad"]

        # Descuento del 10% para clientes VIP
        if self.cliente_vip:
            total = total - total * 0.1

        return total

    def aplicar_cupon(self, porcentaje_descuento):
        total = self.calcular_total()
        descuento = total * (porcentaje_descuento / 100)
        return total - descuento

    def confirmar_pedido(self):
        if len(self.items) > 0:
            self.estado = "confirmado"
            return True
        return False

    def cancelar_pedido(self):
        self.estado = "cancelado"


def calcular_envio(peso_kg, distancia_km):
    # Tarifa base + variable
    base = 5.0
    variable = peso_kg * 0.5 + distancia_km * 0.1
    return base + variable


def aplicar_descuento_por_volumen(total, cantidad_items):
    if cantidad_items >= 10:
        return total * 0.85
    elif cantidad_items >= 5:
        return total * 0.95
    return total
