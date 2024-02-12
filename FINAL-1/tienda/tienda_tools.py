# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=W0718
"""
    Utilidades para trabajar con la tienda
"""

import os
import json
import yaml
import requests
from database_tools import DatabaseTools
from parameter_tools import ParameterTools


class TiendaTools:
    """
    Clase que encapsula la utilidades dsiponibles para la tienda
    """

    API_KEY_ALMACEN = ""
    API_ALMACEN = ""
    API_ALMACEN_COMPRAR = ""

    ESTRUCTURA_PRODUCTO = {
        "codigo": str,
        "descripcion": str,
        "stock": int,
        "precio": float,
        "vendidos": int,
        "activo": bool,
    }

    @classmethod
    def inicializar_tienda(cls, config_file, api_key_almacen):
        """
        Inicializa la base de datos, si no existe la crea
        Inicializa la tabla productos, si no existe la crea

        :param config_file (str): Ruta del fichero de configuración
        :api_key_almacen (str): API-KEY para acceder los servicios de Almacén
        """
        try:

            cls.API_KEY_ALMACEN = api_key_almacen

            config = None
            if config_file is not None:
                with open(config_file, "r", encoding="utf-8") as file:
                    config = yaml.safe_load(file)

            database_path = config["basedatos"]["path"]
            DatabaseTools.init_database_path(database_path)

            cls.API_ALMACEN = config["api_almacen"]
            cls.API_ALMACEN_COMPRAR = config["api_almacen_comprar"]

            if not os.path.exists(database_path):
                cls._crear_tablas(
                    cls,
                    config["basedatos"]["consumidor_tienda"],
                    config["basedatos"]["consumidor_tienda_key"],
                )

            cls._reponer_tienda_desde_alamcen(2)

        except Exception as error:
            raise error

    def _crear_tablas(self, consumidor_tienda, consumidor_tienda_key):
        """
        Incializa la base de datos y crea las tablas

        :param consumidor_tienda(str) consumidor inicial
        :param consumidor_tienda_key(str) api_key consumidor inicial
        """
        try:
            db_operations = DatabaseTools()

            query_crea_consumidores = (
                "CREATE TABLE IF NOT EXISTS consumidores ("
                "id TEXT PRIMARY KEY,"
                "codigo TEXT UNIQUE NOT NULL,"
                "descripcion TEXT,"
                "activo BOOLEAN )"
            )
            db_operations.execute_query(query_crea_consumidores)

            parametros = {}
            parametros["codigo"] = consumidor_tienda_key
            parametros["descripcion"] = consumidor_tienda
            parametros["activo"] = True

            db_operations.insert_into_table("consumidores", parametros)

            query_crea_tabla_productos = (
                "CREATE TABLE IF NOT EXISTS productos ("
                "id TEXT PRIMARY KEY,"
                "codigo TEXT UNIQUE NOT NULL,"
                "descripcion TEXT,"
                "precio DOUBLE,"
                "stock INTEGER,"
                "vendidos INTEGER,"
                "activo BOOLEAN )"
            )
            db_operations.execute_query(query_crea_tabla_productos)
        except Exception as error:
            raise error

    @classmethod
    def _reponer_tienda_desde_alamcen(cls, min_stock):
        """
        Busca los productos activos del almacen y llama al método encargado
        de cargarlo en la tienda

        :param min_stock(int) stock mínimo de cada producto
        """
        try:
            # Recorre la lista de productos
            my_params = {}
            my_params["activo"] = True

            my_headers = {}
            my_headers["Content-Type"] = "application/json"
            my_headers["X-API-Key"] = cls.API_KEY_ALMACEN

            response = requests.get(
                cls.API_ALMACEN,
                params=my_params,
                headers=my_headers,
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()  # Obtener el contenido JSON de la respuesta
                if "articulos" in data:
                    for articulo in data["articulos"]:
                        cls._check_producto_necesita_reponer(articulo, min_stock)
        except Exception as e:
            print(f"Error al sincronizar productos con almacén: {str(e)}")

    @classmethod
    def _check_producto_necesita_reponer(cls, articulo, min_stock):
        """
        Evalúa si es necesario reponer producto en la base de datos
        
        :param articulo(articulo)
        :param min_stock(int) stock mínmo deseado
        """
        try:
            parametros_producto = {"codigo": articulo["codigo"]}
            productos = cls.select_productos(parametros_producto)

            reponer = min_stock
            if productos:
                producto = productos[0]
                if producto["stock"] <= min_stock:
                    reponer = min_stock - producto["stock"]
                else:
                    reponer = 0

            if reponer > 0:
                cls.reponer_producto_almacen(articulo["codigo"], reponer, True)
        except Exception as e:
            print(f"Error al sicronizar el artículo: {str(e)}")

    @classmethod
    def select_productos(cls, parametros):
        """
        Realiza un select de productos dados unos parámetros

        :param parametros(lista clave calor) parámetros del select
        """
        try:
            # Construir la consulta SQL dinámicamente
            table = "productos"
            return DatabaseTools().select_from_table(table, parametros)
        except Exception as e:
            raise e

    @classmethod
    def crea_producto(cls, json_entrada):
        """
        Crea un artículo dado un json

        :param json_entrada(json) json con el artículo
        """
        try:
            parametros = ParameterTools().carga_parametros_json(
                cls.ESTRUCTURA_PRODUCTO, json_entrada
            )
            return DatabaseTools().insert_into_table("productos", parametros)
        except Exception as e:
            raise e

    @classmethod
    def actualiza_producto(cls, json_entrada, codigo):
        """
        Actualiza un artículo dado su código

        :param json_entrada(json) datos del artículo
        :param codigo(codigo_producto) identificador único del artículo
        """
        try:
            parametros_update = ParameterTools().carga_parametros_json(
                cls.ESTRUCTURA_PRODUCTO, json_entrada
            )
            parametros_where = {}
            parametros_where["codigo"] = codigo
            return DatabaseTools().update_table(
                "productos", parametros_update, parametros_where
            )
        except Exception as e:
            raise e

    @classmethod
    def actualiza_entrada_stock(cls, json_articulo, codigo_articulo, cantidad):
        """
        Actualiza entrada de stock de un artículo

        :parametro cantidad(int)
        """
        try:

            parametros_where = {"codigo": codigo_articulo}
            row_results = cls.select_productos(parametros_where)

            # Si el producto no existe lo creamos no activo y convender_productos precio 0
            if not row_results:
                json_producto = {}
                json_producto["codigo"] = json_articulo["codigo"]
                json_producto["descripcion"] = json_articulo["descripcion"]
                json_producto["stock"] = cantidad
                json_producto["precio"] = 0
                json_producto["vendidos"] = 0
                json_producto["activo"] = False
                return cls.crea_producto(json_producto)

            # Si el producto existe le actualizamos el stock
            parametro_set = "stock = stock + " + str(cantidad)
            parametros_where = {}
            parametros_where["codigo"] = codigo_articulo
            return DatabaseTools().update_table_set_string(
                "productos", parametro_set, parametros_where
            )

        except Exception as e:
            raise e

    @classmethod
    def vender_productos(cls, codigo, cantidad):
        """
        Actualiza entrada de stock de un artículo

        :param codigo(str)
        :param cantidad(int)
        """
        try:

            parametros_where = {"codigo": codigo}
            productos = cls.select_productos(parametros_where)

            # Si el producto no existe lo creamos no activo y con precio 0
            if not productos:
                raise ValueError("El producto indicado no figura en nuestro sistema")
            if productos:
                producto = productos[0]
                if not producto["activo"]:
                    raise ValueError(
                        "El producto seleccionado no está disponible ahora mismo"
                    )
                if producto["stock"] < cantidad:
                    raise ValueError(
                        "No disponemos de stock sufiente para realizar la venta"
                    )
                if producto["precio"] is None or producto["precio"] == 0:
                    raise ValueError(
                        "El producto no dispone de precio de venta, intentelo en otro momento"
                    )

            # Si el producto existe le actualizamos el stock
            parametro_set = (
                f"stock = stock - {str(cantidad)}, "
                + f" vendidos = vendidos + {str(cantidad)}"
            )
            parametros_where = {}
            parametros_where["codigo"] = codigo

            DatabaseTools().update_table_set_string(
                "productos", parametro_set, parametros_where
            )

            return "La venta se ha realizado correctamente"
        except Exception as e:
            raise e

    @classmethod
    def reponer_producto_almacen(cls, codigo, cantidad, adapta_a_disponibilidad):
        """
        Se comunica con la API de almacen para reponer el stock

        :param codigo(str)
        :param cantidad(int)
        :param adapta_a_disponibilidad(bool)
        """
        try:
            my_params = {}
            my_params["codigo"] = codigo

            my_headers = {}
            my_headers["Content-Type"] = "application/json"
            my_headers["X-API-Key"] = cls.API_KEY_ALMACEN

            # Hacemos un get del artículo para comprobar si hay suficiente stock
            response_check = requests.get(
                cls.API_ALMACEN,
                params=my_params,
                headers=my_headers,
                timeout=10,
            )
            stock_disponible = 0
            if response_check.status_code == 200:
                # La solicitud fue exitosa
                data = (
                    response_check.json()
                )  # Obtener el contenido JSON de la respuesta
                if "articulos" in data:
                    for articulo in data["articulos"]:
                        stock_disponible = int(articulo["stock"])
            else:
                raise ValueError(
                    json.loads(response_check.content.decode("unicode_escape"))["ERROR"]
                )

            # Si indicamos que adaptemos la cantidad al stock disponible
            # en caso de que se solicite más stock del disponible
            if stock_disponible < int(cantidad) and adapta_a_disponibilidad:
                cantidad = stock_disponible

            if int(cantidad) > 0:
                # Hacemos la petición de almacen adaptada al stock disponible
                my_params["cantidad"] = cantidad
                response_comprar = requests.put(
                    cls.API_ALMACEN_COMPRAR,
                    params=my_params,
                    headers=my_headers,
                    timeout=10,
                )

                if response_comprar.status_code == 200:
                    # La solicitud fue exitosa
                    data = (
                        response_comprar.json()
                    )  # Obtener el contenido JSON de la respuesta
                    if "articulos" in data:
                        for articulo in data["articulos"]:
                            return cls.actualiza_entrada_stock(
                                articulo, codigo, cantidad
                            )
                raise ValueError(
                    json.loads(response_comprar.content.decode("unicode_escape"))[
                        "ERROR"
                    ]
                )
            raise ValueError("No hay disponible stock en este momento en el almacen")
        except Exception as e:
            raise e

    @classmethod
    def check_consumidor_valido(cls, consumidor_key):
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
        except Exception as e:
            raise e
