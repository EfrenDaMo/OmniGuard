from flask import Blueprint, jsonify, request

from omni.modules.database import BasedeDatos
from omni.modules.logging import Logs
from omni.modules.routes import require_login
from omni.modules.services_auth import ServicioAutenticacion


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


@usuarios_bp.route("/api/users/update", methods=["PUT"])
@require_login
def actualizar_usuario():
    """Endpoint para actualizar datos de un usuario

    Método: PUT

    Respuestas:
        200 (éxito):
            {"success": True, "password": "Usuario actualizado correctamente"}
        400 (error):
            {"success": False, "message": "Datos incompletos"}
        404 (error):
            {"success": False, "message": "Usuario no encontrado"}
        500 (error):
            {"success": False, "message": "Error de actualizado"}

    """
    logs.debug("Peticion para actualizar usuario")
    datos = request.json

    if not datos or "nombre_actual" not in datos or "nuevo_nombre" not in datos:
        logs.error("Datos incompletos")
        return jsonify({"success": False, "message": "Datos incompletos"}), 400

    nombre_actual: str = datos["nombre_actual"]
    nuevo_nombre: str = datos["nuevo_nombre"]
    nueva_password: str | None = datos.get("nueva_password", "")

    logs.debug(
        f"Nombre actual: {nombre_actual}, Nuevo nombre: {nuevo_nombre}, Nuevo password: {nueva_password}"
    )

    # Prepare update data
    datos_actualizados = {"nombre": nuevo_nombre}

    if nueva_password:
        password_encriptado = serv_auth.cypher.encrypt(nueva_password.encode()).decode()
        datos_actualizados["password"] = password_encriptado
        logs.debug("Se encripto la contraseña")

    logs.debug(
        f"Nombre actual: {datos_actualizados['nombre']}, Nuevo password: {datos_actualizados['password']}"
    )

    try:
        # Update user
        filas_afectadas = serv_auth.servicio_usuario.actualizar_usuario(
            nombre_actual, datos_actualizados
        )
        logs.debug("se logro servicio")
        logs.debug(f"{filas_afectadas}")

        if filas_afectadas > 0:
            logs.debug("Se actualizo el usuario")
            return jsonify(
                {"success": True, "message": "Usuario actualizado correctamente"}, 200
            )

        logs.debug("No se pudo actualizar el usuario")
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
    except Exception as err:
        logs.error("Error al actualizar usuario", error=str(err))
        return jsonify({"success": False, "message": str(err)}), 500


@usuarios_bp.route("/api/users/delete/<int:id_usuario>", methods=["DELETE"])
@require_login
def eliminar_usuario(id_usuario: int):
    """Endpoint para actualizar datos de un usuario

    Método: DELETE

    Respuestas:
        200 (éxito):
            {"success": True, "password": "Usuario eliminado correctamente"}
        404 (error):
            {"success": False, "message": "Usuario no encontrado"}
        500 (error):
            {"success": False, "message": "Error de eliminado"}

    """
    logs.debug("Peticion para eliminar usuario", user_id=id_usuario)

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
            return jsonify({"success": False, "message": "Usuario no encotrado"}), 500

        filas_afectadas = serv_auth.servicio_usuario.borrar_usuario(
            str(usuario_clave["nombre"])
        )

        if filas_afectadas > 0:
            logs.info("Usuario eliminado", user_id=id_usuario)
            return jsonify(
                {"success": True, "message": "Usuario eliminado exitosamente"}
            )

        return jsonify(
            {"success": False, "message": "No se pudo eliminar el usuario"}
        ), 500

    except Exception as err:
        logs.error("Error eliminando usuario", error=str(err))
        return jsonify({"success": False, "message": str(err)}), 500


@usuarios_bp.route("/api/users/decrypt-password/<int:id_usuario>", methods=["GET"])
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
