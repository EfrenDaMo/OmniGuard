from omni.modules.logging import Logs
from omni.modules.models import Usuario
from omni.modules.database import BasedeDatos


class ServicioUsuario:
    """Servicio para gestión de usuarios en la base de datos.

    Dependencias:
        - BasedeDatos: Para ejecutar operaciones CRUD
        - Modelo Usuario: Para estructura de datos

    Métodos Principales:
        crear_usuario(): Inserta nuevo usuario
        obtener_usuarios(): Lista todos los usuarios
        actualizar_usuario(): Modifica datos de usuario

    Attributes:
        bd (BasedeDatos): Instancia de conexión a DB
    """

    def __init__(self, bd: BasedeDatos) -> None:
        """Inicializa el servicio de usuario con una base de datos y un logger"""
        self.bd: BasedeDatos = bd
        self.__logs = Logs()
        self.__logs.debug("Servicio de usuarios inicializado")

    def crear_usuario(self, usuario: Usuario):
        """Crea un nuevo usuario en la base de datos.

        Args:
            usuario (Usuario): Objeto Usuario con datos requeridos

        Flujo:
            1. Valida estructura del objeto
            2. Ejecuta INSERT en la base de datos
            3. Registra operación en logs

        Raises:
            ValueError: Si faltan campos obligatorios
            DatabaseError: Si falla la operación SQL
        """
        self.__logs.info("Se esta creando un nuevo usuario:", nombre=usuario.nombre)
        datos_usuario = {
            "nombre": usuario.nombre,
            "password": usuario.password,
        }
        self.bd.crear("usuario", datos_usuario)
        self.__logs.info("Se creo el usuario exitosamente", id=usuario.id)

    def obtener_usuarios(self) -> list[Usuario]:
        """Obtiene todos los usuarios registrados

        Recupera una lista de todos los usuarios existentes en la base de datos.

        Returns:
            list[Usuario]|list: Lista de objetos Usuario. Retorna lista vacía si no hay registros.

        Raises:
            DatabaseError: Si ocurre un error durante la consulta

        Ejemplo:
            usuarios = servicio.obtener_usuarios()
        """
        self.__logs.info("Se esta consiguiendo los usuarios")
        resultados = self.bd.leer("usuario")

        if not resultados:
            self.__logs.error("No se pudo conseguir los usuarios del sistema")
            return []

        usuarios: list[Usuario] = []

        for resultado in resultados:
            if isinstance(resultado, dict):
                usuarios.append(
                    Usuario(
                        id=int(str(resultado["id"])),
                        nombre=str(resultado["nombre"]),
                        password=str(resultado["password"]),
                    )
                )

        self.__logs.info("Se obtuvieron exitosamente los usuarios")
        return usuarios or []

    def obtener_usuarios_con_nombre(self, nombre: str) -> Usuario | None:
        """Busca usuario por nombre exacto.

        Args:
            nombre (str): Nombre a buscar (case-sensitive)

        Retorna:
            Usuario | None: Objeto Usuario si se encuentra, None en caso contrario

        Ejemplo:
            obtener_usuarios_con_nombre("admin")
        """
        self.__logs.info("Se esta consiguiendo el usuario", nombre=nombre)
        resultados = self.bd.leer("usuario", {"nombre": nombre})

        if not resultados:
            self.__logs.error("No se pudo conseguir el usuario", nombre=nombre)
            return None

        resultado = resultados[0]

        if isinstance(resultado, dict):
            self.__logs.info("Se logro conseguir el usuario", nombre=nombre)
            return Usuario(
                id=int(str(resultado["id"])),
                nombre=str(resultado["nombre"]),
                password=str(resultado["password"]),
            )

        self.__logs.error("No se pudo conseguir el usuario", nombre=nombre)
        return None

    def actualizar_usuario(
        self, nombre: str, datos_actualizados: dict[str, str]
    ) -> int:
        """Actualiza los datos de un usuario existente

        Modifica los campos especificados de un usuario en la base de datos.

        Args:
            nombre (str): Nombre del usuario a actualizar
            datos_actualizados (dict[str, str]): Campos y valores nuevos a modificar

        Returns:
            int: Número de registros actualizados. 0 si no se realizaron cambios.

        Raises:
            DatabaseError: Si falla la operación de actualización

        Ejemplo:
            servicio.actualizar_usuario("admin", {"password": "nueva_clave"})
        """
        self.__logs.info("se esta intentando actualizar el usuario", nombre=nombre)
        usuario = self.obtener_usuarios_con_nombre(nombre)

        if not usuario:
            return 0

        return self.bd.actualizar("usuario", datos_actualizados, {"nombre": nombre})

    def borrar_usuario(self, nombre: str) -> int:
        """Elimina un usuario del sistema

        Borra permanentemente el registro del usuario especificado.

        Args:
            nombre (str): Nombre del usuario a eliminar

        Returns:
            int: Número de registros eliminados. 0 si no se realizaron cambios.

        Raises:
            DatabaseError: Si falla la operación de eliminación

        Ejemplo:
            servicio.borrar_usuario("usuario_inactivo")
        """
        self.__logs.info("Se logro eliminar el usuario", nombre=nombre)
        return self.bd.eliminar("usuario", {"nombre": nombre})
