import pytest
from werkzeug.wrappers import response
from omni.app import Applicacion


@pytest.fixture
def cliente():
    app = Applicacion()
    app.flask_app.config["TESTING"] = True
    return app.flask_app.test_client()


def test_login_invalido(cliente):
    response = cliente.post(
        "/api/login", json={"nombre": "usuario_valido", "password": "contra_bien"}
    )

    assert response.status_code == 401


def test_login_exitoso(cliente):
    response = cliente.post(
        "/api/login", json={"nombre": "Jose", "password": "12345678910"}
    )

    assert response.status_code == 200
