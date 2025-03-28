import logging
from typing import Any
from modules.config import Configuracion


class Logs:
    """Systema central para hacer logging en la applicacion"""

    def __init__(self) -> None:
        self.__config = Configuracion().obtener_config_log()
        self.logger: logging.Logger = logging.getLogger("OmniGuard")
        self.logger.setLevel(self.__config["Level"])

        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(module)s:%(funcName)s:%(lineno)d = %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
        )

        # Manejador de Archivo
        manejador_archivo = logging.FileHandler(
            filename=self.__config["File"],
            encoding="utf-8",
        )
        manejador_archivo.setLevel(logging.DEBUG)
        manejador_archivo.setFormatter(formato)

        self.logger.addHandler(manejador_archivo)

    def debug(self, mensaje: str, **kwargs: Any) -> None:
        """Mensaje Debug Log"""
        self.logger.debug(mensaje, extra=kwargs)

    def info(self, mensaje: str, **kwargs: Any) -> None:
        """Mensaje Info Log"""
        self.logger.info(mensaje, extra=kwargs)

    def warning(self, mensaje: str, **kwargs: Any) -> None:
        """Mensaje Aviso Log"""
        self.logger.warning(mensaje, extra=kwargs)

    def error(self, mensaje: str, **kwargs: Any) -> None:
        """Mensaje Error Log"""
        self.logger.error(mensaje, extra=kwargs)

    def critical(self, mensaje: str, **kwargs: Any) -> None:
        """Mensaje Critico Log"""
        self.logger.critical(mensaje, extra=kwargs)

    def excepcion(self, mensaje: str, **kwargs: Any) -> None:
        """Excepcion Log con stack trace"""
        self.logger.exception(mensaje, extra=kwargs)
