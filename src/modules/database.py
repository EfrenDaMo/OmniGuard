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

    def ejecutar_consulta(self, consulta: str, parametros: list[str] | None = None):
        """
        Metodo para ejecutar consultas SQL
        :param consulta: La consulta que se ejecutara
        :param parametros: Parametros de la consulta (Opcional)
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

    def confirmar(self):
        """Confirma la transaction actual"""
        if self.conexion:
            self.conexion.commit()

    def revertir(self):
        """Revierte la transaction actual"""
        if self.conexion:
            self.conexion.rollback()
