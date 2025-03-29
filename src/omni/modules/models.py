from dataclasses import asdict, dataclass


@dataclass
class Usuario:
    """Modelo de datos para representar usuarios del sistema.

    Campos:
        nombre (str): Nombre único de usuario (requerido)
        password (str): Contraseña cifrada (requerido)
        id (int|None): ID único autogenerado (opcional)

    Métodos:
        a_dict(): Convierte el modelo a diccionario, excluyendo valores nulos
    """

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
