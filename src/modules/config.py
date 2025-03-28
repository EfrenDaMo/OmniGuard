import os
from dotenv import load_dotenv


class Configuracion:
    """Gestor centralizado de configuración de la aplicación.

    Carga y valida variables de entorno desde un archivo .env.
    Proporciona configuraciones estructuradas para diferentes módulos.

    Atributos:
        DB_USER (str): Usuario de la base de datos
        DB_PASSWORD (str): Contraseña de la base de datos
        LOG_FILE (str): Ruta del archivo de logs
        APP_SECRET (str): Clave secreta para sesiones Flask

    Métodos:
        obtener_config_bd(): Retorna configuración para MySQL
        obtener_config_app(): Retorna configuración para Flask
        obtener_config_log(): Retorna configuración para logging

    Raises:
        RuntimeError: Si falta el archivo .env
    """

    def __init__(self) -> None:
        """Inicializa y valida la configuración desde variables de entorno."""
        if not load_dotenv():
            raise RuntimeError("No se encontro un archivo .env")

        # Configuración de la base de datos
        self.DB_USER: str = os.getenv("DB_USER", "")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
        self.DB_HOST: str = os.getenv("DB_HOST", "localhost")
        self.DB_NAME: str = os.getenv("DB_NAME", "OmniGuard")
        self.DB_PORT: int = int(os.getenv("DB_PORT", "3306"))

        # Configuración de la applicación
        self.APP_KEY: str = os.getenv("APP_KEY", "")
        self.APP_HOST: str = os.getenv("APP_HOST", "localhost")
        self.APP_PORT: int = int(os.getenv("APP_PORT", "5000"))
        self.APP_DEBUG: bool = bool(os.getenv("APP_DEBUG", "False"))
        self.APP_SECRET: str = os.getenv("APP_SECRET", "")

        # Configuración del logger
        self.LOG_FILE: str = os.getenv("LOG_FILE", "omniguard.log")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def obtener_config_bd(self) -> dict[str, str | int]:
        """Configuración para conexión a MySQL.

        Retorna:
            dict: Parámetros de conexión con estructura:
                {
                    "user": str,
                    "password": str,
                    "host": str,
                    "port": int,
                    "database": str
                }

        Ejemplo:
            {'user': 'admin', 'password': 'secret', ...}
        """
        return {
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
            "database": self.DB_NAME,
        }

    def obtener_config_app(self) -> dict[str, bool | str | int]:
        """Configuración principal de la aplicación Flask.

        Retorna:
            dict: Parámetros críticos para el funcionamiento:
                {
                    "Key": str,
                    "Port": int,
                    "Host": str,
                    "Debug": bool,
                    "Secret": str
                }
        Ejemplo:
            {'key': 'key', 'host': 'localhost', ...}
        """
        return {
            "Key": self.APP_KEY,
            "Port": self.APP_PORT,
            "Host": self.APP_HOST,
            "Debug": self.APP_DEBUG,
            "Secret": self.APP_SECRET,
        }

    def obtener_config_log(self) -> dict[str, str]:
        """Configuración para el sistema de registros

        Retorna:
            dict: Parámetros críticos para el funcionamiento:
                {
                    "File": str,
                    "Level": str,
                }
        Ejemplo:
            {'file': 'log.log', 'level': 'Debug', ...}
        """
        return {
            "File": self.LOG_FILE,
            "Level": self.LOG_LEVEL,
        }
