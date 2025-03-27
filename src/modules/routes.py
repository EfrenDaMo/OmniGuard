import os
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_file,
    send_from_directory,
    session,
    url_for,
)

omni_bp = Blueprint("omni", __name__, template_folder="../templates/")


def require_login(func):
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("omni.login"))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@omni_bp.route("/")
def home():
    return redirect(url_for("omni.login"))


@omni_bp.route("/login")
def login():
    return render_template("login.html", titulo="Login")


@omni_bp.route("/dashboard")
@require_login
def dashboard():
    nombre_usuario = session.get("usuario_nombre", "Usuario")
    return render_template("dashboard.html", titulo="Dashboard", nombre=nombre_usuario)


@omni_bp.route("/create-user")
@require_login
def create_user():
    return render_template("create-user.html", titulo="Usuario Nuevo")


@omni_bp.route("/static/<path:filename>")
def serve_static(filename: str):
    mimetype = "application/javascript" if filename.endswith(".js") else None
    return send_from_directory(
        directory=str(current_app.static_folder),
        path=filename,
        mimetype=mimetype,
    )
