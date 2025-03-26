from flask import Blueprint, jsonify, session

from modules.database import BasedeDatos
from modules.auth_service import ServicioAutentificacion


usuarios_bp = Blueprint("usuarios", __name__)

bd = BasedeDatos()
serv_auth = ServicioAutentificacion(bd)


@usuarios_bp.route("/api/users", methods=["GET"])
def obtener_usuarios():
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401

    try:
        datos_usuarios = serv_auth.obtener_datos_del_usuario()

        return jsonify({"success": True, "usuarios": datos_usuarios}), 200
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 500


@usuarios_bp.route("/api/users/decrypt-password/<int:id_usuario>", methods=["GET"])
def decriptar_password(id_usuario: int):
    if "usuario_id" not in session:
        return jsonify({"success": False, "messages": "No autorizado"}), 401

    try:
        usuarios = serv_auth.obtener_datos_del_usuario()
        if usuarios:
            usuario_clave = next(
                (usuario for usuario in usuarios if usuario["id"] == id_usuario),
                None,
            )
        else:
            usuario_clave = None

        if not usuario_clave:
            return jsonify({"success": False, "messages": "Usuario no encotrado"}), 404

        decriptado = serv_auth.decriptar_password(str(usuario_clave["password"]))
        return jsonify({"success": True, "password": decriptado})

    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 500
