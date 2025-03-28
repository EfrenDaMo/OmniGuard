from flask import Flask, jsonify
from flask_cors import CORS

from modules.limiter import limiter
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
        """Inicializa la aplicación con configuración base

        Acciones:
            - Carga configuración desde el módulo Configuracion
            - Crea instancia de Flask con carpeta estática
            - Registra blueprints y manejadores de errores
        """
        # Obtiene la configuración para la applicación
        self.__config: dict[str, str | bool | int] = (
            Configuracion().obtener_config_app()
        )

        # Inicializar el logger
        self.logger: Logs = Logs()
        self.logger.info("Applicación Inicializada")

        # Inicializa la applicación como un objeto con una sub ruta estatica
        self.flask_app: Flask = Flask(__name__, static_folder="static")

        # Configuración modular
        self.__registrar_bp()
        self.__configurar_app()
        self.__registrar_manejador_errores()

    def __configurar_app(self) -> None:
        """Configura parámetros críticos de la aplicación Flask

        Acciones:
            - Habilita modo debug según configuración
            - Establece clave secreta
            - Inicializa limitador de tasas
            - Configura políticas de cookies seguras
            - Habilita CORS con credenciales y orígenes permitidos
        """
        # Configura partes de la applicación
        self.flask_app.debug = bool(self.__config["Debug"])
        self.flask_app.secret_key = self.__config["Secret"]

        # Inicializar limitador
        limiter.init_app(self.flask_app)

        # Se configuran cookies
        self.flask_app.config.update(
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE="Lax",
        )

        # Habilita CORS para todas las rutas
        self.__cors = CORS(
            self.flask_app,
            supports_credentials=True,
            origins=["http://localhost:5000"],
        )

    def __registrar_bp(self) -> None:
        """Registra blueprints en la aplicación

        Blueprints incluidos:
            - omni_bp: Rutas generales
            - auth_bp: Rutas de autenticación
            - usuarios_bp: Rutas de gestión de usuarios
        """
        # Registra los blueprints generados en otros modulos
        self.flask_app.register_blueprint(omni_bp)
        self.flask_app.register_blueprint(auth_bp)
        self.flask_app.register_blueprint(usuarios_bp)

    def __registrar_manejador_errores(self) -> None:
        """Registra manejadores globales para errores HTTP

        Errores manejados:
            - 500 (Internal Server Error): Registra en logs y retorna respuesta JSON
        """

        @self.flask_app.errorhandler(500)
        def manejar_500(_):
            """Maneja errores internos del servidor

            Actions:
                - Registra evento crítico en logs
                - Retorna respuesta JSON estandarizada
            """
            self.logger.critical("Error interno de servidor", stack_info=True)
            return jsonify({"success": False, "message": "Error interno de servidor"})

    def ejecutar(self) -> None:
        """Inicia el servidor web con la configuración cargada

        Detalles:
            - Utiliza host y puerto definidos en la configuración
            - Habilita modo debug según configuración
        """
        self.logger.info(
            "Iniciando el servidor de applicación",
            host=self.__config["Host"],
            port=self.__config["Port"],
        )
        # Ejecuta la applicación
        self.flask_app.run(
            host=str(self.__config["Host"]), port=int(self.__config["Port"])
        )


def main() -> None:
    """Punto de entrada principal de la aplicación
    Copy

    Flujo:
        1. Crea instancia de Applicacion
        2. Ejecuta el servidor web
    """
    app = Applicacion()
    app.ejecutar()


if __name__ == "__main__":
    """Ejecuta la aplicación en modo standalone"""
    main()
