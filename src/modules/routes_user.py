from flask import Blueprint, jsonify, session

from modules.database import BasedeDatos
from modules.routes import require_login
from modules.services_auth import ServicioAutenticacion


usuarios_bp = Blueprint("usuarios", __name__)

bd = BasedeDatos()
serv_auth = ServicioAutenticacion(bd)


@usuarios_bp.route("/api/users", methods=["GET"])
@require_login
def obtener_usuarios():
    """Endpoint para obtener todos los usuarios."""
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401

    try:
        datos_usuarios = serv_auth.obtener_datos_del_usuario()

        respuesta = jsonify({"success": True, "usuarios": datos_usuarios})

        respuesta.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        respuesta.headers["Pragma"] = "no-cache"
        respuesta.headers["Expires"] = "0"

        return respuesta

    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 500


@usuarios_bp.route("/api/users/decrypt-password/<int:id_usuario>", methods=["POST"])
@require_login
def desencriptar_password(id_usuario: int):
    """Endpoint para desencriptar contraseña"""
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401

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
            return jsonify({"success": False, "message": "Usuario no encotrado"}), 404

        decriptado = serv_auth.decriptar_password(str(usuario_clave["password"]))
        return jsonify({"success": True, "password": decriptado})

    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 500
