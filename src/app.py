from flask import Flask, jsonify
from flask_cors import CORS

from modules.config import Configuracion

from modules.routes import omni_bp
from modules.routes_auth import auth_bp
from modules.routes_user import usuarios_bp


class Applicacion:
    """
    Clase de la applicación principal,
    se usa para inicializarla y ejecutarla
    """

    def __init__(self) -> None:
        # Obtiene la configuración para la applicación
        self.__config: dict[str, str | bool | int] = (
            Configuracion().obtener_config_app()
        )
        # Inicializa la applicación como un objeto con una sub ruta estatica
        self.flask_app: Flask = Flask(__name__, static_folder="static")

        # Habilita CORS para todas las rutas
        self.__cors = CORS(
            self.flask_app, supports_credentials=True, origins=["http://localhost:5000"]
        )

        # Configura partes de la applicación
        self.flask_app.debug = bool(self.__config["Debug"])
        self.flask_app.secret_key = self.__config["Secret"]

        self.flask_app.config.update(
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE="Lax",
        )

        # Registra los blueprints generados en otros modulos
        self.flask_app.register_blueprint(omni_bp)
        self.flask_app.register_blueprint(auth_bp)
        self.flask_app.register_blueprint(usuarios_bp)

        @self.flask_app.errorhandler(500)
        def manejar_500(_):
            return jsonify({"success": False, "message": "Error interno de servidor"})

    def ejecutar(self) -> None:
        """Ejecuta la applicación"""
        self.flask_app.run(
            host=str(self.__config["Host"]), port=int(self.__config["Port"])
        )


def main() -> None:
    """Punto de entrada de la applicación"""
    app = Applicacion()
    app.ejecutar()


if __name__ == "__main__":
    main()
