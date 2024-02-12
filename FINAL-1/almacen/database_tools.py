# -*- coding: utf-8 -*-
# pylint: disable=R0801
"""
Módulo motor base de datos
"""
import sqlite3
import uuid


class DatabaseTools:
    """
    Clase para manejar bases de datos
    """

    # Variable de clase para almacenar la ruta de la base de datos
    database_path = None

    def __init__(self):
        self.conn = None

    @classmethod
    def init_database_path(cls, database_path):
        """
        Inicializa el path de la base de datos

        :param database_path: path del fichero de base de datos
        """
        # Asigna la ruta de la base de datos a la variable de clase
        cls.database_path = database_path

    def obtener_conexion(self):
        """
        Método para obtener la conexión a la base de datos
        """
        if not self.database_path:
            raise RuntimeError("El path de la base de datos no ha sido inicializado")
        try:
            self.conn = sqlite3.connect(self.database_path)
            return self.conn
        except sqlite3.Error as error:
            print(error.sqlite_errorcode)
            print(error.sqlite_errorname)
            raise RuntimeError(
                "Error al ejecutar la consulta SQL: " + error.sqlite_errorname
            ) from error

    def select_from_table(self, table, parametros):
        """
        Realiza un select generico, dada una tabla y
        los parámtros de búsqueda

        :param table(str) tabla de la que hay que hacer el select
        :param parametros(lista clave calor) parámetros del select
        """
        try:
            sql_query = "SELECT * FROM "
            sql_query += table
            if parametros:
                sql_query += " WHERE "
                sql_query += " AND ".join([f"{param} = ?" for param in parametros])
                params = tuple(parametros.values())
            else:
                params = ()

            cursor = self.obtener_conexion().cursor()
            cursor.execute(sql_query, params)

            columnas = [
                descripcion[0] for descripcion in cursor.description
            ]  # Obtener nombres de las columnas
            results = [
                dict(zip(columnas, fila)) for fila in cursor.fetchall()
            ]  # Crear un diccionario para cada fila

            return results
        except sqlite3.Error as error:
            raise RuntimeError(
                "Error al ejecutar la consulta SQL: " + error.sqlite_errorname
            ) from error

    def insert_into_table(self, table, parametros):
        """
        Insert genérico para cualquier tabla

        :param table(str) tabla de la que hay que hacer el insert
        :param parametros(lista clave calor) parámetros del insert
        """
        try:
            nuevo_id = str(uuid.uuid4())
            parametros["id"] = nuevo_id
            sql_query = "INSERT INTO "
            sql_query += table
            sql_query += "("
            sql_query += ", ".join(
                parametros.keys()
            )  # Agrega los nombres de las columnas
            sql_query += ") VALUES ("
            sql_query += ", ".join(
                ["?" for _ in parametros]
            )  # Crea placeholders para los valores
            sql_query += ")"

            params = tuple(parametros.values())

            cursor = self.obtener_conexion().cursor()
            cursor.execute(sql_query, params)
            self.conn.commit()

            parametros_select = {}
            parametros_select = {"id": nuevo_id}
            return self.select_from_table(table, parametros_select)
        except sqlite3.Error as error:
            print(error)
            raise RuntimeError(
                "Error al ejecutar la consulta SQL: " + error.sqlite_errorname
            ) from error

    def update_table(self, table, parametros_update, parametros_where):
        """
        Método genérico para actualizar una tabla

        :param table(str) nombre de la tabla
        :param parametros_update(lista clave valor) parámetros a actualizar
        :parametros_where(lista clave valor) parámetros where
        """
        try:
            # Construir la consulta UPDATE con los parámetros de actualización
            # y los parámetros de condición
            sql_query = f"UPDATE {table} SET "
            sql_query += ", ".join(
                [f"{columna} = ?" for columna in parametros_update.keys()]
            )  # Parámetros de actualización
            sql_query += " WHERE "
            sql_query += " AND ".join(
                [f"{columna} = ?" for columna in parametros_where.keys()]
            )  # Parámetros de condición

            # Concatenar los valores de los parámetros para construir la tupla de parámetros
            params = tuple(parametros_update.values()) + tuple(
                parametros_where.values()
            )

            cursor = self.obtener_conexion().cursor()
            cursor.execute(sql_query, params)
            self.conn.commit()

            return self.select_from_table(table, parametros_where)
        except sqlite3.Error as error:
            raise RuntimeError(
                "Error al ejecutar la consulta SQL: " + error.sqlite_errorname
            ) from error

    def update_table_set_string(self, table, set_string, parametros_where):
        """
        Método genérico para actualizar una tabla

        :param table(str) nombre de la tabla
        :param set_string(str) cadena set de la clausula
        :parametros_where(lista clave valor) parámetros where
        """
        try:
            # Construir la consulta UPDATE con los parámetros de actualización
            # y los parámetros de condición
            sql_query = f"UPDATE {table} SET {set_string} "
            sql_query += " WHERE "
            sql_query += " AND ".join(
                [f"{columna} = ?" for columna in parametros_where.keys()]
            )  # Parámetros de condición

            # Concatenar los valores de los parámetros para construir la tupla de parámetros
            params = tuple(parametros_where.values())

            cursor = self.obtener_conexion().cursor()
            cursor.execute(sql_query, params)
            self.conn.commit()

            return self.select_from_table(table, parametros_where)
        except sqlite3.Error as error:
            raise RuntimeError(
                "Error al ejecutar la consulta SQL: " + error.sqlite_errorname
            ) from error

    def execute_query(self, sql_query):
        """
        Método que ejecuta una sentencia sql

        :param sql_query(str) consulta a ejecutar
        """
        try:
            cursor = self.obtener_conexion().cursor()
            cursor.execute(sql_query)
            self.conn.commit()
        except sqlite3.Error as error:
            raise RuntimeError(
                "Error al ejecutar la consulta SQL: " + error.sqlite_errorname
            ) from error
