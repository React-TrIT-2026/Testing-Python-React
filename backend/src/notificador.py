"""
Módulo de notificaciones para la práctica guiada de mocking (11:00-11:40).

Llama a un servicio externo (webhook) por HTTP. En la práctica, jamás
queremos golpear el servicio real en un test -- por eso mockeamos
`requests.post`.
"""

import requests


class ErrorDeNotificacion(Exception):
    pass


def enviar_notificacion(webhook_url, mensaje, canal="general"):
    """Envía un mensaje a un webhook (estilo Slack/Discord).

    Lanza ErrorDeNotificacion si el servicio responde con un código >= 400.
    Devuelve el JSON de la respuesta si todo va bien.
    """

    payload = {"text": mensaje, "channel": canal}
    respuesta = requests.post(webhook_url, json=payload, timeout=5)

    if respuesta.status_code >= 400:
        raise ErrorDeNotificacion(
            f"El servicio respondió con {respuesta.status_code}: {respuesta.text}"
        )

    return respuesta.json()


def notificar_pedido_confirmado(webhook_url, id_pedido, total):
    mensaje = f"Pedido {id_pedido} confirmado por {total}€"
    return enviar_notificacion(webhook_url, mensaje, canal="pedidos")
