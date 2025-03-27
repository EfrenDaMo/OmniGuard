import os
from dotenv import load_dotenv


class Configuracion:
    """Maneja la configuración de la applicación con variables de entornó"""

    def __init__(self) -> None:
        if not load_dotenv():
            return

        # Configuración de la base de datos
        self.DB_USER: str = os.getenv("DB_USER", "")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
        self.DB_HOST: str = os.getenv("DB_HOST", "localhost")
        self.DB_NAME: str = os.getenv("DB_NAME", "OmniGuard")
        self.DB_PORT: int = int(os.getenv("DB_PORT", "3306"))

        # Configuración de la applicación
        self.APP_SECRET: str = os.getenv("APP_SECRET", "")
        self.APP_DEBUG: bool = bool(os.getenv("APP_DEBUG", "False"))
        self.APP_KEY: str = os.getenv("APP_KEY", "")

    def obtener_config_bd(self) -> dict[str, str | int]:
        """
        Obtiene la configuración de solo la base de datos.
        Esto para evitar la interacción con otras configuraciones.
        """
        return {
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
            "database": self.DB_NAME,
        }

    def obtener_config_app(self) -> dict[str, bool | str]:
        """
        Obtiene la configuración de solo la applicación
        Esto para evitar la interacción con otras configuraciones.
        """
        return {
            "Key": self.APP_KEY,
            "Debug": self.APP_DEBUG,
            "Secret": self.APP_SECRET,
        }
