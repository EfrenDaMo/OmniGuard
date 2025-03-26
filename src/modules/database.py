import sys
import mysql.connector
from modules.config import Configuracion
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract


class BasedeDatos:
    """Maneja la conexion con la Base de Datos implementado los metodos CRUD"""

    def __init__(self) -> None:
        """Crea un nuevo objeto de la conexion y la inica"""
        self.cursor: MySQLCursorAbstract | None = None
        self.conexion: MySQLConnectionAbstract | None = None
        self.__config: dict[str, str | int] = Configuracion().obtener_config_bd()

    def conectar(self) -> None:
        """Crea una nueva conexion a la base de datos y activa el cursor"""
        try:
            conexion = mysql.connector.connect(**self.__config)
            if isinstance(conexion, MySQLConnectionAbstract):
                self.conexion = conexion
                self.cursor = self.conexion.cursor(dictionary=True)
                self.conexion.autocommit = False
                _ = self.conexion.cmd_query(
                    "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"
                )
                print("Conexion Exitosa a la base de datos")
        except mysql.connector.Error as err:
            print(f"Error al conectarse a la base de datos: {err}")
            sys.exit(1)

    def desconectar(self) -> None:
        """Desconecta la conexion activa a la base de datos"""
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.conexion:
            self.conexion.close()
            self.conexion = None

    def __ejecutar_consulta(
        self,
        consulta: str,
        parametros: list[str] | None = None,
    ):
        """
        Metodo para ejecutar consultas SQL
        :param consulta: La consulta que se ejecutara
        :param params: Parametros de la consulta (Opcional)
        """
        if not self.conexion:
            self.conectar()

        try:
            if self.cursor and self.conexion:
                if parametros:
                    self.cursor.execute(consulta, parametros)
                else:
                    self.cursor.execute(consulta)
        except mysql.connector.Error as err:
            print(f"Error ejecutando consulta: {err}")
            raise

    def crear(self, tabla: str, datos: dict[str, str]):
        """
        Crear un nuevo registro

        :param tabla: Nombre de la tabla
        :param datos: Dictionario con pares de campo:valor
        """
        valores = list(datos.values())
        campos = ", ".join(datos.keys())
        marcadores = ", ".join(["%s"] * len(datos))

        consulta = f"INSERT INTO `{tabla}` ({campos}) VALUES ({marcadores})"

        try:
            self.__ejecutar_consulta(consulta, valores)
            self.confirmar()
        except Exception as err:
            self.revertir()
            raise err

    def leer(
        self,
        tabla: str,
        condiciones: dict[str, str] | None = None,
        campos: list[str] | str = "*",
    ):
        """
        Leer registro de la tabla

        :param tabla: Nombre de la tabla
        :param condiciones: Dictionario opcional que contiene las condiciones de lectura
        :param campos: Campos a escoger, se escogen todos por defecto
        :return: Lista de los registros
        """
        if isinstance(campos, list):
            campos = ", ".join(campos)

        if condiciones:
            clausula_where = " AND ".join(
                [f"`{campo}` = %s" for campo in condiciones.keys()]
            )
            consulta = f"SELECT {campos} FROM {tabla} WHERE {clausula_where}"
            valores = list(condiciones.values())

            self.__ejecutar_consulta(consulta, valores)
        else:
            consulta = f"SELECT {campos} FROM {tabla}"
            self.__ejecutar_consulta(consulta)

        if self.cursor:
            return self.cursor.fetchall()

    def actualizar(
        self,
        tabla: str,
        datos: dict[str, str],
        condiciones: dict[str, str],
    ):
        """
        Actualizar registro

        :param tabla: Nombre de la tabla
        :param datos: Dictionario de campos a actualizar
        :param condiciones: Dictionario que contiene las condiciones de actualizacion
        :return: Numero de registros actualizados
        """
        clausula_set = ", ".join([f"`{campo}`=%s" for campo in datos.keys()])
        clausula_where = " AND ".join([f"`{campo}`=%s" for campo in condiciones.keys()])

        valores = list(datos.values()) + list(condiciones.values())

        consulta = f"UPDATE {tabla} SET {clausula_set} WHERE {clausula_where}"

        try:
            self.__ejecutar_consulta(consulta, valores)
            self.confirmar()

            if self.cursor:
                return self.cursor.rowcount
        except Exception as err:
            self.revertir()
            raise err

    def eliminar(self, tabla: str, condiciones: dict[str, str]):
        """
        Eliminar registro

        :param tabla: Nombre de la tabla
        :param condiciones: Dictionario que contiene las condiciones de eliminado
        :return: Numero de registros eliminados o un error en caso de falla
        """
        clausula_where = " AND ".join([f"`{campo}`=%s" for campo in condiciones.keys()])

        consulta = f"DELETE FROM {tabla} WHERE {clausula_where}"
        valores = list(condiciones.values())

        try:
            self.__ejecutar_consulta(consulta, valores)
            self.confirmar()

            if self.cursor:
                return self.cursor.rowcount
        except Exception as err:
            self.revertir()
            raise err

    def confirmar(self):
        """Confirma la transaction actual"""
        if self.conexion:
            self.conexion.commit()

    def revertir(self):
        """Revierte la transaction actual"""
        if self.conexion:
            self.conexion.rollback()
