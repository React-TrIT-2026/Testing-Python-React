import pytest
from unittest.mock import patch, MagicMock

from src.notificador import enviar_notificacion, ErrorDeNotificacion

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

# @pytest.mark.parametrize(
#     "status_code, expected_exception",
#     [
#         (400, "El servicio respondió con 400: Bad Request"),
#     ]
# )
# @patch("src.notificador.requests.post")
# def test_enviar_notifacion_canal_default(mock_post, status_code, expected_exception):
#     mock_post.return_value = MagicMock(
#         status_code=status_code, json=lambda: {"ok": False}
#     )

#     resultado = enviar_notificacion(
#         "https://slack.com/webhook", 
#         "Mensaje de prueba"
#     )

#     with pytest.raises(ErrorDeNotificacion):
#         enviar_notificacion(
#             "https://slack.com/webhook", 
#             "Mensaje de prueba"
#         )

#         # Testear el mensaje de error
#         assert str(exc.value) == expected_exception

