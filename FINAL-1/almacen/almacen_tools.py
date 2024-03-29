# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=R0801
"""
    Módulo de operaciones en el alamacen   
"""
import os
import yaml

# import database_tools
from database_tools import DatabaseTools
from parameter_tools import ParameterTools


class AlmacenTools:
    """
    Clase que agrupa herramientas para trabajar con el almacen
    """

    # Inicializar la base de datos
    def inicializar_almacen(self, config_file):
        """
        Inicializa la base de datos, si no existe la crea
        Inicializa la tabla articulos, si no existe la crea

        :param config_file (str): Ruta del fichero de configuración
        """
        try:
            config = None
            if config_file is not None:
                with open(config_file, "r", encoding="utf-8") as file:
                    config = yaml.safe_load(file)

            database_path = config["basedatos"]["path"]
            DatabaseTools.init_database_path(database_path)

            if not os.path.exists(database_path):

                db_operations = DatabaseTools()

                query_crea_tabla_articulos = (
                    "CREATE TABLE IF NOT EXISTS articulos ("
                    "id TEXT PRIMARY KEY,"
                    "codigo TEXT UNIQUE NOT NULL,"
                    "descripcion TEXT,"
                    "stock INTEGER,"
                    "activo BOOLEAN )"
                )

                db_operations.execute_query(query_crea_tabla_articulos)

                # Recorre la lista de articulos
                for articulo in config["basedatos"]["articulos"]:
                    parametros = {}
                    parametros["codigo"] = articulo["codigo"]
                    parametros["descripcion"] = articulo["descripcion"]
                    parametros["stock"] = articulo["stock"]
                    parametros["activo"] = articulo["activo"]
                    db_operations.insert_into_table("articulos", parametros)

                query_crea_consumidores = (
                    "CREATE TABLE IF NOT EXISTS consumidores ("
                    "id TEXT PRIMARY KEY,"
                    "codigo TEXT UNIQUE NOT NULL,"
                    "descripcion TEXT,"
                    "activo BOOLEAN )"
                )

                db_operations.execute_query(query_crea_consumidores)

                parametros = {}
                parametros["codigo"] = config["basedatos"]["consumidor_almacen_key"]
                parametros["descripcion"] = config["basedatos"]["consumidor_almacen"]
                parametros["activo"] = True

                db_operations.insert_into_table("consumidores", parametros)
        except Exception as error:
            raise error

    def select_articulos(self, parametros):
        """
        Realiza un select de artículos dados unso parámetros

        :param parametros(lista clave calor) parámetros del select
        """
        try:
            # Construir la consulta SQL dinámicamente
            table = "articulos"
            return DatabaseTools().select_from_table(table, parametros)
        except Exception as error:
            raise error

    def crea_articulo(self, json):
        """
        Crea un artículo dado un json

        :param json(json) json con el artículo
        """
        try:
            parametros_create = {
                "codigo": str,
                "descripcion": str,
                "stock": int,
                "activo": bool,
            }
            parametros = ParameterTools().carga_parametros_json(parametros_create, json)
            return DatabaseTools().insert_into_table("articulos", parametros)
        except Exception as error:
            raise error

    def actualiza_articulo(self, json, codigo_articulo):
        """
        Actualiza un artículo dado su código

        :param json(json) datos del artículo
        :param codigo_articulo(codigo_articulo) identificador único del artículo
        """
        try:
            parametros_actualizacion = {
                "descripcion": str,
                "stock": int,
                "activo": bool,
            }
            parametros_update = ParameterTools().carga_parametros_json(
                parametros_actualizacion, json
            )
            parametros_where = {}
            parametros_where["codigo"] = codigo_articulo
            return DatabaseTools().update_table(
                "articulos", parametros_update, parametros_where
            )
        except Exception as error:
            raise error

    @classmethod
    def borrar_articulo(cls, codigo):
        """
        Borra un artículo dado su código

        :param json_entrada(json) datos del artículo
        :param codigo(codigo) identificador único del artículo
        """
        try:
            parametros_where = {}
            parametros_where["codigo"] = codigo
            DatabaseTools().delete_table("articulos", parametros_where)
        except Exception as e:
            raise e

    def actualiza_entrada_stock(self, codigo, cantidad):
        """
        Actualiza entrada de stock de un artículo

        :param codigo(str): código de artículo
        :param cantidad(int): cantidad que entra
        """
        try:
            parametro_set = "stock = stock + " + str(cantidad)
            parametros_where = {}
            parametros_where["codigo"] = codigo
            return DatabaseTools().update_table_set_string(
                "articulos", parametro_set, parametros_where
            )
        except Exception as error:
            raise error

    def actualiza_salida_stock(self, codigo, cantidad):
        """
        Actualiza salida de stock de un artículo

        :param codigo(str): código de artículo
        :param cantidad(int): cantidad que entra
        """
        try:
            parametros_where = {}
            parametros_where["codigo"] = codigo

            # Aquí deberías obtener el artículo de alguna manera
            # Por ejemplo, utilizando alguna función como select_articulos
            articulos = self.select_articulos(parametros_where)

            if not articulos:
                raise ValueError(
                    "El artículo solicitado no está registrado en nuestro almacen"
                )

            if int(articulos[0]["stock"]) < int(cantidad):
                stock = articulos[0]["stock"]
                raise ValueError(
                    "No disponemos de stock suficiente para atender su petición, "
                    + f"stock disponible {stock}"
                )
            if bool(articulos[0]["activo"]) is False:
                raise ValueError(
                    "En estos momentos no tenemos activo el artículo solicitado"
                )

            parametro_set = f"stock = stock - {cantidad}"
            return DatabaseTools().update_table_set_string(
                "articulos", parametro_set, parametros_where
            )

        except Exception as error:
            raise error

    def check_consumidor_valido(self, consumidor_key):
        """
        Comprueba si el código de un consumidor api_key es válido

        :param consumidor_key(str) api_key consumidor
        """
        try:
            parametros = {}
            parametros["codigo"] = consumidor_key
            parametros["activo"] = True
            table = "consumidores"
            consumidor = DatabaseTools().select_from_table(table, parametros)
            if not consumidor:
                return False
            return True
        except Exception as error:
            raise error

    @classmethod
    def crear_consumidor(cls, parametros):
        """
        Crear un consumidor de la tienda
        """
        try:
            return DatabaseTools().insert_into_table("consumidores", parametros)
        except Exception as e:
            raise e
