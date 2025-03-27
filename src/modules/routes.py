from functools import wraps
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_from_directory,
    session,
    url_for,
)

omni_bp = Blueprint("omni", __name__, template_folder="../templates/")


def require_login(func):
    """Decorador para requerir autenticación."""

    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("omni.login"))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@omni_bp.route("/")
def home():
    """Redirige inmediatamente a la página de login."""
    # TODO: Implementa sistema de sesion duradera y redirigir a dashboard si esta activa
    return redirect(url_for("omni.login"))


@omni_bp.route("/login")
def login():
    """Muestra la página de login."""
    return render_template("login.html", titulo="Login")


@omni_bp.route("/dashboard")
@require_login
def dashboard():
    """Muestra el dashboard principal."""
    nombre_usuario = session.get("usuario_nombre", "Usuario")
    return render_template("dashboard.html", titulo="Dashboard", nombre=nombre_usuario)


@omni_bp.route("/create-user")
@require_login
def create_user():
    """Muestra la página de creación de usuarios."""
    return render_template("create-user.html", titulo="Usuario Nuevo")


@omni_bp.route("/static/<path:filename>")
def serve_static(filename: str):
    """Sirve archivos estáticos con tipo MIME adecuado"""
    mimetype = "application/javascript" if filename.endswith(".js") else None
    return send_from_directory(
        directory=str(current_app.static_folder),
        path=filename,
        mimetype=mimetype,
    )
