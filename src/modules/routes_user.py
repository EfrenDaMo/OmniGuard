from flask import Blueprint, jsonify

from modules.database import BasedeDatos
from modules.logging import Logs
from modules.routes import require_login
from modules.services_auth import ServicioAutenticacion


usuarios_bp = Blueprint("usuarios", __name__)

bd = BasedeDatos()
serv_auth = ServicioAutenticacion(bd)

logs = Logs()


@usuarios_bp.route("/api/users", methods=["GET"])
@require_login
def obtener_usuarios():
    """Obtiene lista completa de usuarios registrados.

    Método: POST
    Requiere:
        - Sesión activa con privilegios de administrador

    Respuestas:
        200 (éxito):
            {"success": True, "usuarios": [lista_de_usuarios]}
        401 (error):
            {"success": False, "message": "No autorizado"}
        500 (error):
            {"success": False, "message": "Error del servidor"}

    Cabeceras:
        - Cache-Control: no-store (previene almacenamiento en caché)
    """
    logs.debug("Peticion para conseguir usuarios")

    try:
        logs.info("Usuarios fueron conseguidos")
        datos_usuarios = serv_auth.obtener_datos_del_usuario()

        respuesta = jsonify({"success": True, "usuarios": datos_usuarios})

        respuesta.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        respuesta.headers["Pragma"] = "no-cache"
        respuesta.headers["Expires"] = "0"

        return respuesta

    except Exception as err:
        logs.error("Fallo conseguir los usuarios", error=str(err), stack_info=True)
        return jsonify({"success": False, "message": str(err)}), 500


@usuarios_bp.route("/api/users/decrypt-password/<int:id_usuario>", methods=["POST"])
@require_login
def desencriptar_password(id_usuario: int):
    """Endpoint para desencriptar contraseña

    Método: POST
    Parámetros:
        id_usuario (int): ID del usuario objetivo

    Respuestas:
        200 (éxito):
            {"success": True, "password": "contraseña_desencriptada"}
        404 (error):
            {"success": False, "message": "Usuario no encontrado"}
        500 (error):
            {"success": False, "message": "Error de desencriptación"}

    """
    logs.debug("Peticion para desencriptar la contraseña")

    try:
        usuarios = serv_auth.obtener_datos_del_usuario()

        usuario_clave = (
            next(
                (usuario for usuario in usuarios if usuario["id"] == id_usuario),
                None,
            )
            if usuarios
            else None
        )

        if not usuario_clave:
            logs.warning("No se encontro el usuario que se buscaba")
            return jsonify({"success": False, "message": "Usuario no encotrado"}), 404

        decriptado = serv_auth.descifrar_password(str(usuario_clave["password"]))

        logs.info("Se logro conseguir la contraseña desencriptada")
        return jsonify({"success": True, "password": decriptado})

    except Exception as err:
        logs.error("Fallo desencriptar la contraseña", error=str(err), stack_info=True)
        return jsonify({"success": False, "message": str(err)}), 500
