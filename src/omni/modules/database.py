import sys
import mysql.connector
from mysql.connector.types import RowItemType, RowType

from omni.modules.config import Configuracion
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

from omni.modules.logging import Logs


class BasedeDatos:
    """Gestor de operaciones CRUD para MySQL con manejo de transacciones.

    Atributos:
        __cursor (MySQLCursorAbstract): Cursor para ejecutar consultas
        __conexion (MySQLConnectionAbstract): Conexión activa a la DB

    Features:
        - Reconexión automática
        - Transacciones ACID
        - Logging integrado

    Ejemplo:
        bd = BasedeDatos()
        bd.conectar()
        usuarios = bd.leer("usuarios")
    """

    def __init__(self) -> None:
        """Crea un nuevo objeto de la conexión y la inica."""
        self.__logs = Logs()
        self.__cursor: MySQLCursorAbstract | None = None
        self.__conexion: MySQLConnectionAbstract | None = None
        self.__config: dict[str, str | int] = Configuracion().obtener_config_bd()

    def conectar(self) -> None:
        """Establece conexión con la base de datos.

        Acciones:
            - Crea nueva conexión usando parámetros de Configuracion
            - Configura isolation level a READ COMMITTED
            - Habilita cursor con retorno de diccionarios

        Raises:
            mysql.connector.Error: Error de conexión
            RuntimeError: Configuración faltante
        """
        try:
            self.__logs.info("Intentando conectarse a la base de datos")
            conexion = mysql.connector.connect(**self.__config)
            if isinstance(conexion, MySQLConnectionAbstract):
                self.__conexion = conexion
                self.__cursor = self.__conexion.cursor(dictionary=True)
                self.__conexion.autocommit = False
                _ = self.__conexion.cmd_query(
                    "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"
                )
                self.__logs.info("Conexion Exitosa a la base de datos")
        except mysql.connector.Error as err:
            self.__logs.critical(f"Error al conectarse a la base de datos: {err}")
            sys.exit(1)

    def desconectar(self) -> None:
        """Desconecta la conexión activa a la base de datos."""
        if self.__cursor:
            self.__cursor.close()
            self.__cursor = None

        if self.__conexion:
            self.__conexion.close()
            self.__conexion = None

        self.__logs.info("Desconexion exitosa.")

    def __ejecutar_consulta(
        self,
        consulta: str,
        parametros: list[str] | None = None,
    ) -> None:
        """Ejecuta una consulta SQL genérica

        Método interno para ejecutar operaciones SQL con manejo de errores y reconexión automática.

        Args:
            consulta (str): Consulta SQL a ejecutar
            parametros (list[str]|None): Parámetros para la consulta (opcional)

        Raises:
            mysql.connector.Error: Si ocurre un error en la ejecución
            RuntimeError: Si no hay conexión establecida
        """
        if not self.__conexion:
            self.conectar()

        try:
            if self.__cursor and self.__conexion:
                if parametros:
                    self.__cursor.execute(consulta, parametros)
                else:
                    self.__cursor.execute(consulta)
        except mysql.connector.Error as err:
            self.__logs.error(f"Error ejecutando consulta: {err}")
            raise

    def crear(self, tabla: str, datos: dict[str, str]) -> None:
        """Inserta un nuevo registro en la tabla especificada.

        Args:
            tabla (str): Nombre de la tabla
            datos (dict): Pares campo-valor para la inserción

        Ejemplo:
            crear("usuarios", {"nombre": "Ana", "password": "***"})

        Raises:
            mysql.connector.Error: Error de sintaxis SQL
            KeyError: Campos inválidos
        """
        valores = list(datos.values())
        campos = ", ".join(datos.keys())
        marcadores = ", ".join(["%s"] * len(datos))

        consulta = f"INSERT INTO `{tabla}` ({campos}) VALUES ({marcadores})"

        try:
            self.__ejecutar_consulta(consulta, valores)
            self.confirmar()

            self.__logs.info("Registro fue creado", tabla=tabla)
        except Exception as err:
            self.revertir()
            self.__logs.info("Operación de creación fallo", error=str(err))
            raise err
        finally:
            self.desconectar()

    def leer(
        self,
        tabla: str,
        condiciones: dict[str, str] | None = None,
        campos: list[str] | str = "*",
    ) -> list[RowType | dict[str, RowItemType]]:
        """Obtiene registros de una tabla con filtros opcionales.

        Args:
            tabla (str): Nombre de la tabla
            condiciones (dict): Filtros WHERE como pares clave-valor
            campos (list|str): Campos a seleccionar (default: todos)

        Retorna:
            list: Lista de registros como diccionarios

        Ejemplo:
            bd.leer("usuarios", {"id": 5}, ["nombre", "email"])
        """
        try:
            if isinstance(campos, list):
                campos = ", ".join(campos)

            if condiciones:
                clausula_where = " AND ".join(
                    [f"`{campo}` = %s" for campo in condiciones.keys()]
                )
                consulta = f"SELECT {campos} FROM `{tabla}` WHERE {clausula_where}"
                valores = list(condiciones.values())

                self.__ejecutar_consulta(consulta, valores)
            else:
                consulta = f"SELECT {campos} FROM `{tabla}`"
                self.__ejecutar_consulta(consulta)

            self.__logs.info("De leyeron los registros", tabla=tabla)
            return self.__cursor.fetchall() if self.__cursor else []
        finally:
            self.desconectar()

    def actualizar(
        self,
        tabla: str,
        datos: dict[str, str],
        condiciones: dict[str, str],
    ) -> int:
        """Actualiza registros en la base de datos

        Modifica campos específicos de registros que cumplan con las condiciones.

        Args:
            tabla (str): Nombre de la tabla objetivo
            datos (dict[str, str]): Campos y valores a actualizar
            condiciones (dict[str, str]): Condiciones para filtrar registros

        Returns:
            int: Número de filas afectadas. 0 si no hay cambios.

        Raises:
            mysql.connector.Error: Si la consulta es inválida

        Ejemplo:
            filas_afectadas = bd.actualizar("usuarios", {"rol": "admin"}, {"id": 5})
        """
        clausula_set = ", ".join([f"`{campo}`=%s" for campo in datos.keys()])
        clausula_where = " AND ".join([f"`{campo}`=%s" for campo in condiciones.keys()])

        valores = list(datos.values()) + list(condiciones.values())
        consulta = f"UPDATE `{tabla}` SET {clausula_set} WHERE {clausula_where}"

        try:
            self.__ejecutar_consulta(consulta, valores)
            self.confirmar()

            self.__logs.info("Se actualizaron registros", tabla=tabla)
            return self.__cursor.rowcount if self.__cursor else 0
        except Exception as err:
            self.revertir()
            self.__logs.info("Operación de actualización fallo", error=str(err))
            raise err
        finally:
            self.desconectar()

    def eliminar(self, tabla: str, condiciones: dict[str, str]) -> int:
        """Elimina registros de la base de datos

        Borra permanentemente registros que cumplan con las condiciones especificadas.

        Args:
            tabla (str): Nombre de la tabla objetivo
            condiciones (dict[str, str]): Condiciones para filtrar registros

        Returns:
            int: Número de filas eliminadas. 0 si no hay coincidencias.

        Raises:
            mysql.connector.Error: Si la consulta es inválida

        Ejemplo:
            filas_eliminadas = bd.eliminar("logs", {"fecha": "2022-01-01"})
        """
        clausula_where = " AND ".join([f"`{campo}`=%s" for campo in condiciones.keys()])

        consulta = f"DELETE FROM `{tabla}` WHERE {clausula_where}"
        valores = list(condiciones.values())

        try:
            self.__ejecutar_consulta(consulta, valores)
            self.confirmar()

            self.__logs.info("Se eliminaron registros", tabla=tabla)
            return self.__cursor.rowcount if self.__cursor else 0
        except Exception as err:
            self.revertir()
            self.__logs.info("Operación de eliminación fallo", error=str(err))
            raise err
        finally:
            self.desconectar()

    def confirmar(self) -> None:
        """Confirma la transacción actual.

        Acciones:
            - Ejecuta COMMIT
            - Registra confirmación en logs

        Uso típico:
            Después de operaciones de escritura exitosas
        """
        if self.__conexion:
            self.__conexion.commit()
            self.__logs.info("Se confirmo la transacción")

    def revertir(self) -> None:
        """Revierte la transacción actual

        Acciones:
            - Ejecuta ROLLBACK
            - Registra reversión logs

        Uso típico:
            Después de operaciones de escritura no exitosas
        """
        if self.__conexion:
            self.__conexion.rollback()
            self.__logs.info("Se revirtio la transacción")
