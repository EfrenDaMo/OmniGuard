from flask import Flask
from modules.routes import omni_bp
from modules.config import Configuracion


class Applicacion:
    def __init__(self) -> None:
        self.__config: dict[str, str | bool] = Configuracion().obtener_config_app()
        self.flask_app: Flask = Flask(__name__)
        self.flask_app.debug = bool(self.__config["Debug"])
        self.flask_app.secret_key = self.__config["Secret"]

        self.flask_app.register_blueprint(omni_bp)

    def ejecutar(self, host: str = "localhost", port: int = 5000):
        self.flask_app.run(host=host, port=port)


def main():
    app = Applicacion()
    app.ejecutar()


if __name__ == "__main__":
    main()
