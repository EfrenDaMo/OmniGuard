import os
from dotenv import load_dotenv


class Configuracion:
    def __init__(self) -> None:
        _ = load_dotenv()
        self.DB_USER: str = os.getenv("DB_USER", "")
        self.DB_PORT: int = int(os.getenv("DB_PORT", 3306))
        self.DB_HOST: str = os.getenv("DB_HOST", "localhost")
        self.DB_NAME: str = os.getenv("DB_NAME", "OmniGuard")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

        self.APP_DEBUG: bool = bool(os.getenv("APP_DEBUG", "False") == "True")
        self.APP_SECRET: str = os.getenv("APP_SECRET", "")

    def obtener_config_bd(self) -> dict[str, str | int]:
        return {
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
            "database": self.DB_NAME,
        }

    def obtener_config_app(self) -> dict[str, bool | str]:
        return {
            "Debug": self.APP_DEBUG,
            "Secret": self.APP_SECRET,
        }
