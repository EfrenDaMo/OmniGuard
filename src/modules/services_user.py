from modules.logging import Logs
from modules.models import Usuario
from modules.database import BasedeDatos


class ServicioUsuario:
    """Nivel de servicio para las operaciones relacionadas a usuarios."""

    def __init__(self, bd: BasedeDatos) -> None:
        self.bd: BasedeDatos = bd
        self.__logs = Logs()
        self.__logs.debug("Servicio de usuarios inicializado")

    def crear_usuario(self, usuario: Usuario):
        """Crea un nuevo usuario."""
        self.__logs.info("Se esta creando un nuevo usuario:", nombre=usuario.nombre)
        datos_usuario = {
            "nombre": usuario.nombre,
            "password": usuario.password,
        }
        self.bd.crear("usuario", datos_usuario)
        self.__logs.info("Se creo el usario exitosamente", id=usuario.id)

    def obtener_usuarios(self) -> list[Usuario]:
        """Obtiene todos los usuarios."""
        self.__logs.info("Se esta consiguiendo los usuarios")
        resultados = self.bd.leer("usuario")

        if not resultados:
            self.__logs.error("No se pudo conseguir los usuarios del sistema")
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

        self.__logs.info("Se obtubieron exitosamente los usuarios")
        return usuarios or []

    def obtener_usuarios_con_nombre(self, nombre: str) -> Usuario | None:
        """Obtiene un usario por su nombre."""
        self.__logs.info("Se esta consiguiendo el usuario", nombre=nombre)
        resultados = self.bd.leer("usuario", {"nombre": nombre})

        if not resultados:
            self.__logs.error("No se pudo conseguir el usuario", nombre=nombre)
            return None

        resultado = resultados[0]

        if isinstance(resultado, dict):
            self.__logs.info("Se logro conseguir el usuario", nombre=nombre)
            return Usuario(
                id=int(str(resultado["id"])),
                nombre=str(resultado["nombre"]),
                password=str(resultado["password"]),
            )

        self.__logs.error("No se pudo conseguir el usuario", nombre=nombre)
        return None

    def actualizar_usuario(
        self, nombre: str, datos_actualizados: dict[str, str]
    ) -> int:
        """Actualiza un usuario existente."""
        self.__logs.info("Se logro actualizar el usario", nombre=nombre)
        return self.bd.actualizar("usuario", datos_actualizados, {"nombre": nombre})

    def borrar_usuario(self, nombre: str) -> int:
        """Elimina un usuario existente."""
        self.__logs.info("Se logro eliminar el usario", nombre=nombre)
        return self.bd.eliminar("usuario", {"nombre": nombre})
