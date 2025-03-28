from flask import Blueprint, jsonify, request

from modules.database import BasedeDatos
from modules.logging import Logs
from modules.services_auth import ServicioAutenticacion


auth_bp = Blueprint("auth", __name__)

bd = BasedeDatos()
serv_auth = ServicioAutenticacion(bd)
logs = Logs()


@auth_bp.route("/api/registro", methods=["POST"])
def registro():
    """Endpoint para el registro de un nuevo usuario."""
    logs.debug("Se hizo una peticion de registro")
    datos = request.json

    if not datos or "nombre" not in datos or "password" not in datos:
        logs.error("Los datos estaban incompletos para la peticion")
        return jsonify({"success": False, "message": "Datos incompletos"}), 400

    nombre: str = datos["nombre"]
    password: str = datos["password"]

    resultado = serv_auth.registrar_usuario(nombre, password)
    codigo_status = 201 if resultado["success"] else 400

    logs.info("Se logro hacer la peticion")
    return jsonify(resultado), codigo_status


@auth_bp.route("/api/login", methods=["POST"])
def login():
    """Endpoint para inicio de sesión."""
    logs.debug("Se hizo una peticion de ingreso")
    datos = request.json

    if not datos or "nombre" not in datos or "password" not in datos:
        logs.error("Los datos estaban incompletos para la peticion")
        return jsonify({"success": False, "message": "Datos incompletos"}), 400

    nombre: str = datos["nombre"]
    password: str = datos["password"]

    resultado = serv_auth.iniciar_sesion(nombre, password)
    codigo_status = 200 if resultado["success"] else 401

    logs.info("Se logro hacer la peticion")
    return jsonify(resultado), codigo_status


@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    """Endpoint para cierre de sesión."""
    logs.debug("Se hizo una peticion de cierre de sesión")
    resultado = serv_auth.cerrar_sesion()

    logs.info("Se logro hacer la peticion")
    return jsonify(resultado), 200


@auth_bp.route("/api/session", methods=["POST"])
def verificar_sesion():
    """Endpoint para verificar sesión activa."""
    logs.debug("Se hizo una peticion de verificacion de sesión")
    resultado = serv_auth.verificar_sesion()
    codigo_status = 200 if resultado["success"] else 401

    logs.info("Se logro hacer la peticion")
    return jsonify(resultado), codigo_status
