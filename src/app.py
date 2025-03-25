from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html", titulo="Login")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", titulo="Dashboard")


if __name__ == "__main__":
    app.run(debug=True)
