from flask import session
from modules.models import Usuario
from modules.database import BasedeDatos
from modules.user_service import ServicioUsuario
from werkzeug.security import generate_password_hash, check_password_hash


class ServicioAutentificacion:
    """Servicio para manejar la autentificacion de usuarios"""

    def __init__(self, bd: BasedeDatos) -> None:
        self.servicio_usuario: ServicioUsuario = ServicioUsuario(bd)

    def registrar_usuario(self, nombre: str, password: str):
        usuario_existente = self.servicio_usuario.obtener_usuarios_con_nombre(nombre)
        if usuario_existente:
            return {"success": True, "message": "El usuario ya existe"}

        password_hash = generate_password_hash(password)

        usuario_nuevo = Usuario(nombre=nombre, password=password_hash)

        try:
            self.servicio_usuario.crear_usuario(usuario_nuevo)
            return {"success": True, "message": "Usuario registrado correctamente"}
        except Exception as err:
            return {"success": False, "message": str(err)}

    def iniciar_sesion(self, nombre: str, password: str) -> dict[str, str | bool]:
        """Inicia la session para un usuario"""

        usuario = self.servicio_usuario.obtener_usuarios_con_nombre(nombre)

        # Verifica que el usuario exista en el registro
        if not usuario:
            return {"success": False, "message": "Usuario no encontrado"}

        # Verifica la Contraseña
        if not check_password_hash(usuario.password, password):
            return {"success": False, "message": "Contraseña incorrecta"}

        # Inicia la sesión para el usuario
        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.nombre

        return {"success": True, "message": "Inicio se sesión exitosa"}

    def cerrar_sesion(self) -> dict[str, str | bool]:
        session.clear()
        return {"success": True, "message": "Sesión cerrada exitosa"}

    def verificar_sesion(self) -> dict[str, bool | str | dict[str, int | str]]:
        if "usuario_id" in session:
            return {
                "success": True,
                "message": "Sesion activa",
                "usuario": {
                    "id": session["usuario_id"],
                    "nombre": session["usuario_nombre"],
                },
            }

        return {"success": False, "message": "No hay session activa"}

    def obtener_datos_del_usuario(self) -> list[dict[str, str | int | None]] | None:
        usuarios = self.servicio_usuario.obtener_usuarios()

        if not usuarios:
            return None

        datos_usaurios: list[dict[str, str | int | None]] = []
        for usuario in usuarios:
            datos_usaurio: dict[str, str | int | None] = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "password": usuario.password,
            }
            datos_usaurios.append(datos_usaurio)

        return datos_usaurios
