import pytest
from fastapi import HTTPException

@pytest.fixture()
def crear_pedido(client):
    """Fixture que crea un pedido y devuelve su id."""
    ENDPOINT = "/pedidos"
    PAYLOAD = {"cliente": "Ana", "total": 49.90}
    respuesta = client.post(ENDPOINT, json=PAYLOAD)
    assert respuesta.status_code == 201
    return respuesta.json()["id"]


def test_crear_pedido(client):
    ENDPOINT = "/pedidos"
    PAYLOAD = {"cliente": "Ana", "total": 49.90}
    JSON_RESPUESTA_ESPERADA = {
        "id": 1,
        "cliente": "Ana",
        "total": 49.90,
        "estado": "pendiente"
    }
    
    respuesta = client.post(ENDPOINT, json=PAYLOAD)

    assert respuesta.status_code == 201
    data = respuesta.json()
    assert data == JSON_RESPUESTA_ESPERADA

def test_crear_pedido_total_invalido(client):
    ENDPOINT = "/pedidos"
    PAYLOAD = {"cliente": "Ana", "total": -10}

    respuesta = client.post(ENDPOINT, json=PAYLOAD)

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "El total debe ser mayor que 0"}

def test_obtener_pedido_no_existe(client):
    ENDPOINT = "/pedidos/999"

    respuesta = client.get(ENDPOINT)

    assert respuesta.status_code == 404


def test_obtener_pedido_existente(client, crear_pedido):
    # Arrange
    id_pedido = crear_pedido(client)

    # Act
    ENDPOINT_OBTENER = f"/pedidos/{id_pedido}"
    respuesta_obtener = client.get(ENDPOINT_OBTENER)

    # Assert
    assert respuesta_obtener.status_code == 200
    assert respuesta_obtener.json()["id"] == id_pedido
    assert respuesta_obtener.json()["cliente"] == "Ana"


def test_confirmar_pedido(client, crear_pedido):
    # Arrange
    id_pedido = crear_pedido(client)

    id_pedido = respuesta_crear.json()["id"]

    # Act
    ENDPOINT_CONFIRMAR = f"/pedidos/{id_pedido}/confirmar"
    respuesta_confirmar = client.post(ENDPOINT_CONFIRMAR)

    # Assert
    assert respuesta_confirmar.status_code == 200
    assert respuesta_confirmar.json()["estado"] == "confirmado"

def test_confirmar_pedido_ya_confirmado(client, crear_pedido):
    # Arrange
    id_pedido = crear_pedido(client)

    # Act
    ENDPOINT_CONFIRMAR = f"/pedidos/{id_pedido}/confirmar"
    respuesta_confirmar_1 = client.post(ENDPOINT_CONFIRMAR)
    respuesta_confirmar_2 = client.post(ENDPOINT_CONFIRMAR)

    # Assert
    assert respuesta_confirmar_1.status_code == 200
    assert respuesta_confirmar_1.json()["estado"] == "confirmado"
    assert respuesta_confirmar_2.status_code == 400
    assert respuesta_confirmar_2.json() == {"detail": "No se puede confirmar un pedido en estado 'confirmado'"} 
    assert False, "TODO: Implementar test para confirmar pedido ya confirmado"