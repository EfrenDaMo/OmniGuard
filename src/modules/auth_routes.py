from flask import Blueprint, jsonify, request

from modules.database import BasedeDatos
from modules.auth_service import ServicioAutentificacion


auth_bp = Blueprint("auth", __name__)

bd = BasedeDatos()
serv_auth = ServicioAutentificacion(bd)


@auth_bp.route("/api/registro", methods=["POST"])
def registro():
    datos = request.json

    if not datos or "nombre" not in datos or "password" not in datos:
        return jsonify({"success": False, "message": "Datos incompletos"}), 400

    resultado = serv_auth.registrar_usuario(datos["nombre"], datos["password"])

    return jsonify(resultado), 200 if resultado["success"] else 400


@auth_bp.route("/api/login", methods=["POST"])
def login():
    datos = request.json

    if not datos or "nombre" not in datos or "password" not in datos:
        return jsonify({"success": False, "message": "Datos incompletos"}), 400

    resultado = serv_auth.iniciar_sesion(datos["nombre"], datos["password"])

    return jsonify(resultado), 200 if resultado["success"] else 401


@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    resultado = serv_auth.cerrar_sesion()

    return jsonify(resultado), 200


@auth_bp.route("/api/session", methods=["GET"])
def verificar_sesion():
    resultado = serv_auth.verificar_sesion()

    return jsonify(resultado), 200 if resultado["success"] else 401
