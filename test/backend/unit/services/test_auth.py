import pytest
from unittest.mock import Mock
from omni.modules.models import Usuario
from omni.modules.services_auth import ServicioAutenticacion


@pytest.fixture
def mock_bd():
    bd = Mock()
    bd.leer.return_value = []
    return bd


def test_registro_usuario_exitoso(mock_bd):
    servicio = ServicioAutenticacion(mock_bd)
    result = servicio.registrar_usuario("usuario_test", "ContraSegura")

    assert result["success"] is True
    assert "registrado correctamente" in str(result["message"])


def test_registro_usuario_duplicado(mock_bd):
    mock_bd.leer.return_value = [
        {"id": 1, "nombre": "usuario_test", "password": "hashed"}
    ]

    servicio = ServicioAutenticacion(mock_bd)
    result = servicio.registrar_usuario("usuario_test", "ContraNUEVA")

    assert result["success"] is False
    assert "ya existe" in str(result["message"])
