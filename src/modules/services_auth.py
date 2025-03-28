from flask import session

from modules.logging import Logs
from modules.models import Usuario
from modules.config import Configuracion
from modules.database import BasedeDatos
from modules.services_user import ServicioUsuario

from cryptography.fernet import Fernet


class ServicioAutenticacion:
    """Servicio para gestión de autenticación y seguridad.

    Dependencias:
        - ServicioUsuario: Para operaciones CRUD de usuarios
        - Fernet: Para cifrado simétrico (debe reemplazarse por hashing)

    Métodos Clave:
        registrar_usuario(): Crea nuevos usuarios
        iniciar_sesion(): Maneja el login
        verificar_sesion(): Comprueba sesión activa

    Attributes:
        cypher (Fernet): Instancia para cifrado/descifrado
    """

    def __init__(self, bd: BasedeDatos) -> None:
        """Inicializa el servicio de autenticación con un logger, configuracion y servicio usuario"""
        self.__logs: Logs = Logs()
        self.__logs.debug("Servicio Auth inicializado")
        self.__config = Configuracion().obtener_config_app()
        self.servicio_usuario: ServicioUsuario = ServicioUsuario(bd)

        self.key: str = str(self.__config["Key"])
        self.cypher: Fernet = Fernet(self.key.encode())

    def registrar_usuario(self, nombre: str, password: str) -> dict[str, str | bool]:
        """Registra un nuevo usuario en el sistema.

        Flujo:
            1. Verifica si el usuario existe
            2. Cifra la contraseña
            3. Crea registro en la base de datos

        Args:
            nombre (str): Nombre único de usuario
            password (str): Contraseña en texto plano

        Retorna:
            dict: Resultado con formato:
                {"success": bool, "message": str}

        Códigos de estado:
            201: Registro exitoso
            400: Datos inválidos
            409: Usuario ya existe
        """
        usuario_existente = self.servicio_usuario.obtener_usuarios_con_nombre(nombre)

        if usuario_existente:
            return {"success": False, "message": "El usuario ya existe"}

        password_encriptado = self.cypher.encrypt(password.encode()).decode()
        usuario_nuevo = Usuario(nombre=nombre, password=password_encriptado)

        try:
            self.servicio_usuario.crear_usuario(usuario_nuevo)
            self.__logs.info("Se registro un nuevo usuario")
            return {"success": True, "message": "Usuario registrado correctamente"}
        except Exception as err:
            self.__logs.error("Fallo registrar un nuevo usuario")
            return {"success": False, "message": str(err)}

    def iniciar_sesion(self, nombre: str, password: str) -> dict[str, str | bool]:
        """Valida credenciales y establece sesión de usuario.

        Flujo:
            1. Busca usuario por nombre
            2. Compara contraseña descifrada
            3. Establece cookies de sesión

        Args:
            nombre (str): Nombre de usuario
            password (str): Contraseña en texto plano

        Retorna:
            dict: Resultado de la operación con formato estandarizado
        """
        self.__logs.info("Intento de ingreso", nombre=nombre)
        usuario = self.servicio_usuario.obtener_usuarios_con_nombre(nombre)

        # Verifica que el usuario no exista en el registro
        if not usuario:
            self.__logs.warning("No se encontro el usuario")
            return {"success": False, "message": "Usuario no encontrado"}

        # Verifica que la Contraseña ingresada y del usuario sean igual
        if self.descifrar_password(usuario.password) != password:
            self.__logs.error("Se fallo el intento de ingreso")
            return {"success": False, "message": "Contraseña incorrecta"}

        # Inicia la sesión para el usuario
        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.nombre

        return {"success": True, "message": "Inicio se sesión exitosa"}

    def cerrar_sesion(self) -> dict[str, str | bool]:
        """Termina la sesión actual del usuario.

        Acciones:
            - Limpia todas las variables de sesión
            - Invalida cookies relacionadas

        Retorna:
            dict: Siempre {"success": True, "message": str}
        """
        session.clear()
        self.__logs.info("Se cerro la session de usuario")
        return {"success": True, "message": "Sesión cerrada exitosa"}

    def verificar_sesion(self) -> dict[str, bool | str | dict[str, int | str]]:
        """Verifica la existencia de una sesión de usuario activa

        Comprueba si las variables de sesión contienen datos de autenticación válidos.

        Returns:
            dict: Resultado con:
                - success (bool): Estado de la operación
                - message (str): Mensaje descriptivo
                - usuario (dict, opcional): Datos del usuario si la sesión está activa

        Ejemplo:
            resultado = servicio.verificar_sesion()
        """
        if "usuario_id" in session:
            return {
                "success": True,
                "message": "Sesión activa",
                "usuario": {
                    "id": session["usuario_id"],
                    "nombre": session["usuario_nombre"],
                },
            }

        self.__logs.info("Se verifico la sesión de usuario")
        return {"success": False, "message": "No hay sesión activa"}

    def obtener_datos_del_usuario(self) -> list[dict[str, str | int | None]] | None:
        """Recupera información detallada de todos los usuarios registrados

        Obtiene datos sensibles como contraseñas cifradas (uso interno restringido).

        Returns:
            list[dict]|None: Lista de diccionarios con datos de usuarios. None si hay errores.

        Raises:
            DatabaseError: Si falla la consulta a la base de datos

        Ejemplo:
            datos_usuarios = servicio.obtener_datos_del_usuario()
        """
        self.__logs.info("Se esta intentando conseguir los datos de usuario")
        usuarios = self.servicio_usuario.obtener_usuarios()

        if not usuarios:
            self.__logs.error("No se encontro los usuarios")
            return None

        datos_usaurios: list[dict[str, str | int | None]] = []

        for usuario in usuarios:
            datos_usaurio: dict[str, str | int | None] = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "password": usuario.password,
            }
            datos_usaurios.append(datos_usaurio)

        self.__logs.info("Se obtuvieron los datos de los usuarios")
        return datos_usaurios

    def descifrar_password(self, password_encriptado: str) -> str:
        """Convierte una contraseña cifrada a texto legible

        Utiliza la clave simétrica configurada para realizar el descifrado.

        Args:
            password_encriptado (str): Contraseña encriptada con Fernet

        Returns:
            str: Contraseña descifrada en texto plano

        Raises:
            cryptography.fernet.InvalidToken: Si el token es inválido o la clave incorrecta

        Ejemplo:
            password_original = servicio.descifrar_password(token_cifrado)
        """
        self.__logs.info("Se esta descifrando la contraseña")
        return self.cypher.decrypt(password_encriptado.encode()).decode()
