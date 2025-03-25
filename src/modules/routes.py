from flask import Blueprint, redirect, render_template, url_for

omni_bp = Blueprint("omni", __name__, template_folder="../templates/")


@omni_bp.route("/")
def home():
    return redirect(url_for("omni.login"))


@omni_bp.route("/login")
def login():
    return render_template("login.html", titulo="Login")


@omni_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", titulo="Dashboard")
