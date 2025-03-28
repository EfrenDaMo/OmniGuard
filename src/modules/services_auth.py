from flask import session

from modules.logging import Logs
from modules.models import Usuario
from modules.config import Configuracion
from modules.database import BasedeDatos
from modules.services_user import ServicioUsuario

from cryptography.fernet import Fernet


class ServicioAutenticacion:
    """Servicio para manejar la autenticación de usuarios"""

    def __init__(self, bd: BasedeDatos) -> None:
        self.__logs: Logs = Logs()
        self.__logs.debug("Servicio Auth inicializado")
        self.__config = Configuracion().obtener_config_app()
        self.servicio_usuario: ServicioUsuario = ServicioUsuario(bd)

        self.key: str = str(self.__config["Key"])
        self.cypher: Fernet = Fernet(self.key.encode())

    def registrar_usuario(self, nombre: str, password: str) -> dict[str, str | bool]:
        """Crea el registro de un nuevo usuario"""
        usuario_existente = self.servicio_usuario.obtener_usuarios_con_nombre(nombre)

        if usuario_existente:
            return {"success": False, "message": "El usuario ya existe"}

        password_encriptado = self.cypher.encrypt(password.encode()).decode()
        usuario_nuevo = Usuario(nombre=nombre, password=password_encriptado)

        try:
            self.servicio_usuario.crear_usuario(usuario_nuevo)
            self.__logs.info("Se registro un nuevo usuario")
            return {"success": True, "message": "Usuario registrado correctamente"}
        except Exception as err:
            self.__logs.error("Fallo registrar un nuevo usuario")
            return {"success": False, "message": str(err)}

    def iniciar_sesion(self, nombre: str, password: str) -> dict[str, str | bool]:
        """Inicia la sesión para un usuario"""
        self.__logs.info("Intento de ingreso", nombre=nombre)
        usuario = self.servicio_usuario.obtener_usuarios_con_nombre(nombre)

        # Verifica que el usuario no exista en el registro
        if not usuario:
            self.__logs.warning("No se encontro el usuario")
            return {"success": False, "message": "Usuario no encontrado"}

        # Verifica que la Contraseña ingresada y del usuario sean igual
        if self.descifrar_password(usuario.password) != password:
            self.__logs.error("Se fallo el intento de ingreso")
            return {"success": False, "message": "Contraseña incorrecta"}

        # Inicia la sesión para el usuario
        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.nombre

        return {"success": True, "message": "Inicio se sesión exitosa"}

    def cerrar_sesion(self) -> dict[str, str | bool]:
        """Cierra la sesión actual."""
        session.clear()
        self.__logs.info("Se cerro la session de usuario")
        return {"success": True, "message": "Sesión cerrada exitosa"}

    def verificar_sesion(self) -> dict[str, bool | str | dict[str, int | str]]:
        """Verifica si hay una sesión activa."""
        if "usuario_id" in session:
            return {
                "success": True,
                "message": "Sesión activa",
                "usuario": {
                    "id": session["usuario_id"],
                    "nombre": session["usuario_nombre"],
                },
            }

        self.__logs.info("Se verifico la sesión de usuario")
        return {"success": False, "message": "No hay sesión activa"}

    def obtener_datos_del_usuario(self) -> list[dict[str, str | int | None]] | None:
        """Obtiene datos de todos los usuarios."""
        self.__logs.info("Se esta intentando conseguir los datos de usuario")
        usuarios = self.servicio_usuario.obtener_usuarios()

        if not usuarios:
            self.__logs.error("No se encontro los usuarios")
            return None

        datos_usaurios: list[dict[str, str | int | None]] = []

        for usuario in usuarios:
            datos_usaurio: dict[str, str | int | None] = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "password": usuario.password,
            }
            datos_usaurios.append(datos_usaurio)

        self.__logs.info("Se obtuvieron los datos de los usuarios")
        return datos_usaurios

    def descifrar_password(self, password_encriptado: str) -> str:
        """Descifra una contraseña encriptada."""
        self.__logs.info("Se esta descifrando la contraseña")
        return self.cypher.decrypt(password_encriptado.encode()).decode()
