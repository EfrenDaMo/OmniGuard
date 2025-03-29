import pytest
from omni.app import Applicacion
from unittest.mock import patch


@pytest.fixture
def client():
    app = Applicacion()
    app.flask_app.config["TESTING"] = True
    return app.flask_app.test_client()


@patch("omni.modules.services_auth.ServicioAutenticacion")
def test_obtener_usuarios_no_autorizado(mock_auth, client):
    mock_auth.verificar_sesion.return_value = {"success": False}

    response = client.get("/api/users")

    assert response.status_code == 401
    assert b"No autorizado" in response.data


@patch("omni.modules.services_user.ServicioUsuario")
def test_eliminar_usuario_error(mock_service, client):
    with patch(
        "omni.modules.services_auth.ServicioAutenticacion.verificar_sesion"
    ) as mock_verificar:
        response = client.post(
            "/api/login", json={"nombre": "Jose", "password": "12345678910"}
        )
        mock_verificar.return_value = {"success": True}
        mock_service.return_value.borrar_usuario.return_value = 0

        response = client.delete("/api/users/delete/999")

        assert response.status_code == 500
