from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from modules.config import Configuracion

from modules.logging import Logs
from modules.routes import omni_bp
from modules.routes_auth import auth_bp
from modules.routes_user import usuarios_bp


class Applicacion:
    """Clase principal de configuración y ejecución de la aplicación Flask.

    Responsabilidades:
        - Carga configuración desde .env
        - Inicializa componentes principales
        - Registra blueprints (rutas)
        - Configura seguridad y CORS
        - Maneja errores globales

    Uso:
        app = Applicacion()
        app.ejecutar()
    """

    def __init__(self) -> None:
        """Constructor que inicializa todos los componentes."""
        # Obtiene la configuración para la applicación
        self.__config: dict[str, str | bool | int] = (
            Configuracion().obtener_config_app()
        )

        # Inicializar el logger
        self.logger: Logs = Logs()
        self.logger.info("Applicación Inicializada")

        # Inicializa la applicación como un objeto con una sub ruta estatica
        self.flask_app: Flask = Flask(__name__, static_folder="static")

        # Habilita CORS para todas las rutas
        self.__cors = CORS(
            self.flask_app, supports_credentials=True, origins=["http://localhost:5000"]
        )

        # Configura partes de la applicación
        self.flask_app.debug = bool(self.__config["Debug"])
        self.flask_app.secret_key = self.__config["Secret"]

        # Se configuran cookies
        self.flask_app.config.update(
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE="Lax",
        )

        # Inicializar limitador
        self.limiter = Limiter(
            app=self.flask_app,
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"],
            storage_uri="memory://",
        )

        # Registra los blueprints generados en otros modulos
        self.flask_app.register_blueprint(omni_bp)
        self.flask_app.register_blueprint(auth_bp)
        self.flask_app.register_blueprint(usuarios_bp)

        @self.flask_app.errorhandler(500)
        def manejar_500(_):
            self.logger.critical("Error interno de servidor", stack_info=True)
            return jsonify({"success": False, "message": "Error interno de servidor"})

    def ejecutar(self) -> None:
        """Inicia el servidor web con la configuración cargada."""
        self.limiter.init_app(self.flask_app)
        self.logger.info(
            "Iniciando el servidor de applicación",
            host=self.__config["Host"],
            port=self.__config["Port"],
        )
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
