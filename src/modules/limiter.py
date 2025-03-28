from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


class Limitador:
    """Gestor de límites de tasa para endpoints de la aplicación
    Copy

    Dependencias:
        - Flask-Limiter: Para control de tasas de solicitudes
        - Flask: Para integración con la aplicación

    Métodos Clave:
        init_app(): Vincula el limitador con la app Flask
        limit(): Aplica restricciones a rutas específicas

    Attributes:
        _limiter (Limiter): Instancia del limitador de Flask
    """

    def __init__(self) -> None:
        """Inicializa el limitador con configuración base

        Configuración predeterminada:
            - Clave de identificación: Dirección IP del cliente
            - Límites globales: 200 solicitudes/día y 50/hora
            - Almacenamiento en memoria
        """
        self._limiter: Limiter = Limiter(
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"],
            storage_uri="memory://",
        )

    def init_app(self, app: Flask) -> None:
        """Vincula el limitador con la aplicación Flask

        Args:
            app (Flask): Instancia de la aplicación Flask a proteger

        Ejemplo:
            limitador = Limitador()
            limitador.init_app(app)
        """
        self._limiter.init_app(app)

    def limit(self, *args, **kwargs):
        """Aplica restricciones de tasa a un endpoint específico

        Args:
            *args: Límites en formato de cadena (ej: "10/minute")
            **kwargs: Configuraciones adicionales del decorador

        Returns:
            function: Decorador para aplicar a las rutas

        Ejemplo:
            @app.route("/api")
            @limiter.limit("30/minute")
            def endpoint():
                return "OK"
        """
        return self._limiter.limit(*args, **kwargs)


limiter = Limitador()
"""Instancia preconfigurada para uso global en la aplicación

Ejemplo de uso:
from limiter import limiter
limiter.init_app(app)
"""
