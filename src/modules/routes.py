from flask import Blueprint, redirect, render_template, session, url_for

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
