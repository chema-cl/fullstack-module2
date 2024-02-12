# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=W0718
# pylint: disable=R0801
"""
    Módulo API REST tienda
"""
import argparse
from flask import Flask, request, jsonify
from tienda_tools import TiendaTools
from parameter_tools import ParameterTools

app = Flask(__name__)


# Servicios CRUD básicos para administración de productos
@app.route("/api/productos", methods=["GET"])
def obtener_productos():
    """
    Método get para obtención de productos
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        # Posibles parámetros que se puede recibir para la query
        parametros_request = {"codigo": str, "activo": bool}
        # Carga los parámetros recibidos en la llamada
        parametros = ParameterTools().carga_parametros_request(
            parametros_request, request
        )
        # Buscamos en base de datos
        results = TiendaTools().select_productos(parametros)
        # Devolvemos el resultado en un json
        return jsonify({"productos": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos/<codigo>", methods=["GET"])
def obtener_producto(codigo):
    """
    Método get para obtención de un producto concreto

    :param codigo(str) identificador del ártículo a devolver
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        # inicializa el parámetro de la query
        parametros = {}
        parametros["codigo"] = codigo
        # Lanza la búsqueda
        results = TiendaTools().select_productos(parametros)
        # Devuelve el resultado en JSON
        return jsonify({"productos": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos", methods=["POST"])
def crear_producto():
    """
    Método POST para la creación de un producto
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401
        # Creamos el producto
        results = TiendaTools().crea_producto(request.json)

        # Devolvemos mensaje de éxito
        return jsonify({"productos": results}), 201

    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos/<codigo>", methods=["PUT"])
def actualizar_producto(codigo):
    """
    Método PUT para actualizar de un producto concreto

    :param codigo(str) identificador del ártículo a actualizar
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401
        # Lanza la actualización en base de datos
        results = TiendaTools().actualiza_producto(request.json, codigo)
        # Devuelve el resultado en JSON
        return jsonify({"productos": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos/<codigo>", methods=["DELETE"])
def borrar_producto(codigo):
    """
    Método PUT para borrar de un producto concreto

    :param codigo(str) identificador del ártículo a actualizar
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401
        # Lanza la actualización en base de datos
        TiendaTools().borrar_producto(codigo)
        # Devuelve el resultado en JSON
        return jsonify({"productos": {}})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos/reponer", methods=["PUT"])
def reponer_producto_almacen():
    """
    Método solicitar productos al almacen
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        parametros_request = {
            "codigo": str,
            "cantidad": int,
            "adapta_a_disponibilidad": bool,
        }
        # Carga los parámetros recibidos en la llamada
        parametros = ParameterTools().carga_parametros_request(
            parametros_request, request
        )
        if parametros.get("codigo") is None or parametros.get("cantidad") is None:
            return (
                jsonify({"ERROR": "Parámetros codigo y cantidad no recibidos"}),
                401,
            )

        # Lanza la actualización en base de datos
        results = TiendaTools().reponer_producto_almacen(
            parametros["codigo"],
            parametros["cantidad"],
            parametros["adapta_a_disponibilidad"],
        )

        return jsonify({"productos": results})

    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos/venta", methods=["PUT"])
def vender_productos():
    """
    Método put para vender productos
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        # Posibles parámetros que se puede recibir para la query
        parametros_request = {"codigo": str, "cantidad": int}
        # Carga los parámetros recibidos en la llamada
        parametros = ParameterTools().carga_parametros_request(
            parametros_request, request
        )
        if parametros.get("codigo") is None or parametros.get("cantidad") is None:
            return (
                jsonify({"ERROR": "Parámetros codigo y cantidad no recibidos"}),
                401,
            )

        # Lanza la actualización en base de datos
        results = TiendaTools().vender_productos(
            parametros["codigo"], parametros["cantidad"]
        )
        # Devolvemos el resultado en un json
        return jsonify({"mensaje": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Aplicación Almacén")
    parser.add_argument(
        "--servidor",
        default="localhost",
        help="IP o nombre del servidor donde se inicia la aplicación.",
    )
    parser.add_argument(
        "--puerto", type=int, default=6000, help="Puerto donde se expondrá el API."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Ruta y nombre del fichero de configuración de la aplicación.",
    )
    parser.add_argument(
        "--key",
        required=True,
        help="API Key del almacén.",
    )
    parser.parse_args()

    args = parser.parse_args()

    # Inicializar la base de datos al arrancar la aplicación
    TiendaTools.inicializar_tienda(args.config, args.key)

    app.run(host=args.servidor, port=args.puerto, debug=True)
