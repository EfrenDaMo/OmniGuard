import sys
import mysql.connector
from mysql.connector.types import RowItemType, RowType

from modules.config import Configuracion
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

from modules.logging import Logs


class BasedeDatos:
    """Maneja la conexión con la Base de Datos implementado los métodos CRUD."""

    def __init__(self) -> None:
        """Crea un nuevo objeto de la conexión y la inica."""
        self.__logs = Logs()
        self.__cursor: MySQLCursorAbstract | None = None
        self.__conexion: MySQLConnectionAbstract | None = None
        self.__config: dict[str, str | int] = Configuracion().obtener_config_bd()

    def conectar(self) -> None:
        """Crea una nueva conexión a la base de datos y activa el cursor."""
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
        """
        Método para ejecutar consultas SQL.

        :param consulta: La consulta que se ejecutará
        :param params: Parámetros de la consulta (Opcional)
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
        """
        Crear un nuevo registro.

        :param tabla: Nombre de la tabla
        :param datos: Diccionario con pares de campo:valor
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
        """
        Leer registro de la tabla.

        :param tabla: Nombre de la tabla
        :param condiciones: Diccionario opcional que contiene las condiciones de lectura
        :param campos: Campos a seleccionar, todos por defecto
        :return: Lista de los registros
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
        """
        Actualizar registro(s).

        :param tabla: Nombre de la tabla
        :param datos: Diccionario de campos a actualizar
        :param condiciones: Condiciones para la actualización
        :return: Número de registros actualizados
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
        """
        Eliminar registro(s).

        :param tabla: Nombre de la tabla
        :param condiciones: Condiciones para la eliminación
        :return: Numero de registros eliminados
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
        """Confirma la transacción actual"""
        if self.__conexion:
            self.__conexion.commit()
            self.__logs.info("Se confirmo la transacción")

    def revertir(self) -> None:
        """Revierte la transacción actual"""
        if self.__conexion:
            self.__conexion.rollback()
            self.__logs.info("Se revirtio la transacción")
