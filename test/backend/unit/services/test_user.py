import pytest
from unittest.mock import Mock, call
from omni.modules.services_user import ServicioUsuario
from omni.modules.models import Usuario


@pytest.fixture
def mock_db():
    db = Mock()
    db.leer.return_value = [
        {"id": 1, "nombre": "admin", "password": "hash1"},
        {"id": 2, "nombre": "user1", "password": "hash2"},
    ]
    db.actualizar.return_value = 1
    db.eliminar.return_value = 1
    return db


def test_obtener_usuarios(mock_db):
    servicio = ServicioUsuario(mock_db)
    usuarios = servicio.obtener_usuarios()

    assert len(usuarios) == 2
    assert isinstance(usuarios[0], Usuario)
    mock_db.leer.assert_called_once_with("usuario")


def test_actualizar_usuario_exitoso(mock_db):
    servicio = ServicioUsuario(mock_db)
    filas_afectadas = servicio.actualizar_usuario("admin", {"password": "new_hash"})

    assert filas_afectadas == 1
    mock_db.actualizar.assert_called_once_with(
        "usuario", {"password": "new_hash"}, {"nombre": "admin"}
    )


def test_borrar_usuario_exitoso(mock_db):
    servicio = ServicioUsuario(mock_db)
    filas_afectadas = servicio.borrar_usuario("user1")

    assert filas_afectadas == 1
    mock_db.eliminar.assert_called_once_with("usuario", {"nombre": "user1"})
