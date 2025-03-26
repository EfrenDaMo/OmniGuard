from flask import Blueprint, jsonify, request, session

from modules.database import BasedeDatos
from modules.auth_service import ServicioAutentificacion


usuarios_bp = Blueprint("usuarios", __name__)

bd = BasedeDatos()
serv_auth = ServicioAutentificacion(bd)


@usuarios_bp.route("/api/usuarios", methods=["GET"])
def obtener_usuarios():
    if "usuario_id" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401

    try:
        datos_usuarios = serv_auth.obtener_datos_del_usuario()

        return jsonify({"success": True, "usuarios": datos_usuarios}), 200
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 500
