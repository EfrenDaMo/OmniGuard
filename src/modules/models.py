from dataclasses import asdict, dataclass


@dataclass
class Usuario:
    """Modelo Usuario que representa la tabla de la base de datos."""

    nombre: str
    password: str
    id: int | None = None

    def a_dict(self) -> dict[str, str | int]:
        """Convierte el modelo a un diccionario, excluyendo valores nulos."""
        dict_modelo: dict[str, str | int | None] = asdict(self)
        dict_usuario: dict[str, str | int] = {}

        for campo, valor in dict_modelo.items():
            if valor is not None:
                dict_usuario[campo] = valor

        return dict_usuario
