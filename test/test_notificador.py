import pytest
from unittest.mock import patch, MagicMock

from src.notificador import enviar_notificacion

@patch("src.notificador.requests.post")
def test_enviar_notificacion_exitoso(mock_post):
    mock_post.return_value = MagicMock(
        status_code=200, json=lambda: {"ok": True}
    )

    resultado = enviar_notificacion(
        "https://slack.com/webhook", 
        "Mensaje de prueba", 
        canal="test"
    )

    assert resultado == {"ok": True}
    mock_post.assert_called_once()


@patch("src.notificador.requests.post")
def test_enviar_notifacion_canal_default(mock_post):
    mock_post.return_value = MagicMock(
        status_code=200, json=lambda: {"ok": True}
    )

    resultado = enviar_notificacion(
        "https://slack.com/webhook", 
        "Mensaje de prueba"
    )

    assert resultado == {"ok": True}
    mock_post.assert_called_with(
        "https://slack.com/webhook", 
        json={"text": "Mensaje de prueba", "channel": "general"},
        timeout=5
    )