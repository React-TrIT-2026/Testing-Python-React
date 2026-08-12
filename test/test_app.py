from fastapi import HTTPException

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

# TODO para completar en directo con el grupo

def test_obtener_pedido_existente():
    assert False, "TODO: Implementar test para obtener pedido existente"

def test_confirmar_pedido():
    assert False, "TODO: Implementar test para confirmar pedido"

def test_confirmar_pedido_ya_confirmado():
    assert False, "TODO: Implementar test para confirmar pedido ya confirmado"