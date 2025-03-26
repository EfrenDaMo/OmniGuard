from flask import Flask

from modules.routes import omni_bp
from modules.auth_routes import auth_bp
from modules.user_routes import usuarios_bp

from modules.config import Configuracion
from flask_cors import CORS


class Applicacion:
    def __init__(self) -> None:
        self.__config: dict[str, str | bool] = Configuracion().obtener_config_app()
        self.flask_app: Flask = Flask(__name__)

        # Enable CORS for all routes
        _ = CORS(self.flask_app, supports_credentials=True)

        # Configure app settings
        self.flask_app.debug = bool(self.__config["Debug"])
        self.flask_app.secret_key = self.__config["Secret"]

        # Register blueprints
        self.flask_app.register_blueprint(omni_bp)
        self.flask_app.register_blueprint(auth_bp)
        self.flask_app.register_blueprint(usuarios_bp)

    def ejecutar(self, host: str = "localhost", port: int = 5000):
        self.flask_app.run(host=host, port=port)


def main():
    app = Applicacion()
    app.ejecutar()


if __name__ == "__main__":
    main()
