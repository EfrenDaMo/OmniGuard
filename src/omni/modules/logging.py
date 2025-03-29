import logging
from typing import Any
from omni.modules.config import Configuracion


class Logs:
    """Sistema centralizado de logging para la aplicación.

    Configura y gestiona los registros de la aplicación usando el módulo logging.
    Crea un logger principal con manejo de archivos y formato estructurado.

    Atributos:
        logger (logging.Logger): Instancia del logger configurado.

    Ejemplo de uso:
        logs = Logs()
        logs.info("Mensaje informativo", user_id=123)
    """

    def __init__(self) -> None:
        """Inicializa el logger con configuración desde el archivo .env."""
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
        """Registra un mensaje de nivel DEBUG.

        Args:
            mensaje (str): Texto descriptivo del evento
            **kwargs: Campos adicionales para el registro (ej: user_id=45)
        """
        self.logger.debug(mensaje, extra=kwargs)

    def info(self, mensaje: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel INFO.

        Args:
            mensaje (str): Texto descriptivo del evento
            **kwargs: Campos adicionales para el registro (ej: user_id=45)
        """
        self.logger.info(mensaje, extra=kwargs)

    def warning(self, mensaje: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel WARNING.

        Args:
            mensaje (str): Texto descriptivo del evento
            **kwargs: Campos adicionales para el registro (ej: user_id=45)
        """
        self.logger.warning(mensaje, extra=kwargs)

    def error(self, mensaje: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel ERROR.

        Args:
            mensaje (str): Texto descriptivo del evento
            **kwargs: Campos adicionales para el registro (ej: user_id=45)
        """
        self.logger.error(mensaje, extra=kwargs)

    def critical(self, mensaje: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel CRITICAL.

        Args:
            mensaje (str): Texto descriptivo del evento
            **kwargs: Campos adicionales para el registro (ej: user_id=45)
        """
        self.logger.critical(mensaje, extra=kwargs)

    def exception(self, mensaje: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel Exception.

        Args:
            mensaje (str): Texto descriptivo del evento
            **kwargs: Campos adicionales para el registro (ej: user_id=45)
        """
        self.logger.exception(mensaje, extra=kwargs)
