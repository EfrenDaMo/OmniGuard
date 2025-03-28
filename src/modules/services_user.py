from modules.models import Usuario
from modules.database import BasedeDatos


class ServicioUsuario:
    """Nivel de servicio para las operaciones relacionadas a usuarios."""

    def __init__(self, bd: BasedeDatos) -> None:
        self.bd: BasedeDatos = bd

    def crear_usuario(self, usuario: Usuario):
        """Crea un nuevo usuario."""
        datos_usuario = {
            "nombre": usuario.nombre,
            "password": usuario.password,
        }
        self.bd.crear("usuario", datos_usuario)

    def obtener_usuarios(self) -> list[Usuario]:
        """Obtiene todos los usuarios."""
        resultados = self.bd.leer("usuario")

        if not resultados:
            return []

        usuarios: list[Usuario] = []

        for resultado in resultados:
            if isinstance(resultado, dict):
                usuarios.append(
                    Usuario(
                        id=int(str(resultado["id"])),
                        nombre=str(resultado["nombre"]),
                        password=str(resultado["password"]),
                    )
                )

        return usuarios or []

    def obtener_usuarios_con_nombre(self, nombre: str) -> Usuario | None:
        """Obtiene un usario por su nombre."""
        resultados = self.bd.leer("usuario", {"nombre": nombre})

        if not resultados:
            return None

        resultado = resultados[0]

        if isinstance(resultado, dict):
            return Usuario(
                id=int(str(resultado["id"])),
                nombre=str(resultado["nombre"]),
                password=str(resultado["password"]),
            )

        return None

    def actualizar_usuario(
        self, nombre: str, datos_actualizados: dict[str, str]
    ) -> int:
        """Actualiza un usuario existente."""
        return self.bd.actualizar("usuario", datos_actualizados, {"nombre": nombre})

    def borrar_usuario(self, nombre: str) -> int:
        """Elimina un usuario existente."""
        return self.bd.eliminar("usuario", {"nombre": nombre})
