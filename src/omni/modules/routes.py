from omni.modules.logging import Logs
from functools import wraps
from flask import (
    Blueprint,
    current_app,
    jsonify,
    redirect,
    render_template,
    send_from_directory,
    session,
    url_for,
)

omni_bp = Blueprint("omni", __name__, template_folder="../templates/")

logs = Logs()


def require_login(func):
    """Decorador para requerir autenticación."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return jsonify({"success": False, "message": "No autorizado"}), 401
        return func(*args, **kwargs)

    return wrapper


@omni_bp.route("/")
def home():
    """Redirige inmediatamente a la página de login."""
    logs.info("Se redirecciono al usuario a la pagina login")
    return redirect(url_for("omni.login"))


@omni_bp.route("/login")
def login():
    """Muestra la página de login.

    Retorna:
        render_template: Plantilla HTML del login con contexto:
            - titulo (str): Título de la página
    """
    logs.info("Pagina Login fue accedida")
    return render_template("login.html", titulo="Login")


@omni_bp.route("/dashboard")
@require_login
def dashboard():
    """Muestra el dashboard principal del usuario autenticado.

    Requisitos:
        - Sesión activa (cookie de usuario válida)

    Retorna:
        render_template: Plantilla HTML del dashboard con contexto:
            - titulo (str): Título de la página
            - nombre (str): Nombre del usuario desde la sesión

    Errores:
        401: Si no hay sesión activa (manejado por @require_login)
    """
    logs.info(
        "Pagina dashboard fue accedida por el usuario",
        user_id=session.get("usuario_id"),
    )
    nombre_usuario = session.get("usuario_nombre", "Usuario")
    return render_template("dashboard.html", titulo="Dashboard", nombre=nombre_usuario)


@omni_bp.route("/create-user")
@require_login
def create_user():
    """Muestra el formulario de creación de usuarios.

    Requisitos:
        - Sesión activa con privilegios de administrador

    Retorna:
        render_template: Template HTML con el formulario

    Errores:
        401: Si no hay sesión activa
        403: Si el usuario no tiene permisos suficientes
    """
    logs.info("Pagina crear usuario fue accedida")
    return render_template("create-user.html", titulo="Usuario Nuevo")


@omni_bp.route("/edit-user")
@require_login
def edit_user():
    """Muestra el formulario de creación de usuarios.

    Requisitos:
        - Sesión activa con privilegios de administrador

    Retorna:
        render_template: Template HTML con el formulario

    Errores:
        401: Si no hay sesión activa
        403: Si el usuario no tiene permisos suficientes
    """
    logs.info("Pagina editar usuario fue accedida")
    return render_template("edit-user.html", titulo="Editar Usuario")


@omni_bp.route("/static/<path:filename>")
def serve_static(filename: str):
    """Sirve archivos estáticos del sistema.

    Parámetros:
        filename (str): Ruta relativa al directorio /static

    Retorna:
        Response: Archivo solicitado con headers adecuados

    Ejemplos:
        /static/js/app.js → Sirve archivo JavaScript
        /static/css/style.css → Sirve archivo CSS

    Notas:
        - Configura automáticamente el MIME type
        - Cache control desactivado para desarrollo
    """
    logs.info("Se sirvio un script estatico")
    mimetype = "application/javascript" if filename.endswith(".js") else None
    return send_from_directory(
        directory=str(current_app.static_folder),
        path=filename,
        mimetype=mimetype,
    )
