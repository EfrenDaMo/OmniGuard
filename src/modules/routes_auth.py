from flask import Blueprint, jsonify, request

from app import Applicacion
from modules.database import BasedeDatos
from modules.logging import Logs
from modules.services_auth import ServicioAutenticacion


auth_bp = Blueprint("auth", __name__)

bd = BasedeDatos()
serv_auth = ServicioAutenticacion(bd)
logs = Logs()


@auth_bp.route("/api/registro", methods=["POST"])
def registro():
    """Endpoint para registro de nuevos usuarios.

    Método: POST
    Expects (JSON):
        {
            "nombre": "nuevo_usuario",
            "password": "contraseña_segura"
        }

    Respuestas:
        201 (éxito):
            {"success": True, "message": "Usuario registrado correctamente"}
        400 (error):
            {"success": False, "message": "Datos incompletos"}
        409 (error):
            {"success": False, "message": "El usuario ya existe"}

    Acciones:
        - Valida datos de entrada
        - Cifra la contraseña
        - Crea nuevo registro en la base de datos
        - Registra evento en el log

    Errores comunes:
        - Campos faltantes en el JSON
        - Nombre de usuario duplicado
    """
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
@Applicacion().limiter.limit("5 per minute")
def login():
    """Endpoint para autenticación de usuarios.

    Método: POST
    Expects (JSON):
        {
            "nombre": "usuario_existente",
            "password": "contraseña_valida"
        }

    Respuestas:
        200 (éxito):
            {"success": True, "message": "Inicio de sesión exitoso"}
        400 (error):
            {"success": False, "message": "Datos incompletos"}
        401 (error):
            {"success": False, "message": "Credenciales inválidas"}

    Acciones:
        - Establece cookies de sesión (usuario_id, usuario_nombre)
        - Registra intentos fallidos en el log
    """
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
    """Cierra la sesión del usuario actual.

    Método: POST
    Requiere:
        - Sesión activa (cookie válida)

    Respuestas:
        200 (éxito):
            {"success": True, "message": "Sesión cerrada exitosamente"}

    Acciones:
        - Elimina todas las cookies de sesión
        - Registra el evento en el log

    Notas:
        - Funciona incluso sin sesión activa (limpia cookies residuales)
    """
    logs.debug("Se hizo una peticion de cierre de sesión")
    resultado = serv_auth.cerrar_sesion()

    logs.info("Se logro hacer la peticion")
    return jsonify(resultado), 200


@auth_bp.route("/api/session", methods=["POST"])
def verificar_sesion():
    """Verifica si existe una sesión activa.

    Método: POST
    Requiere:
        - Cookies de sesión (opcional)

    Respuestas:
        200 (éxito):
            {
                "success": True,
                "message": "Sesión activa",
                "usuario": {"id": 123, "nombre": "ejemplo"}
            }
        401 (error):
            {"success": False, "message": "No hay sesión activa"}

    Uso típico:
        - Verificar autenticación al cargar la aplicación
        - Mantener sesión persistente en el frontend
    """
    logs.debug("Se hizo una peticion de verificacion de sesión")
    resultado = serv_auth.verificar_sesion()
    codigo_status = 200 if resultado["success"] else 401

    logs.info("Se logro hacer la peticion")
    return jsonify(resultado), codigo_status
