# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=W0718
# pylint: disable=R0801
"""
    Módulo API REST almacen
"""
import argparse
from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from almacen_tools import AlmacenTools
from parameter_tools import ParameterTools

app = Flask(__name__)

SWAGGER_URL = "/api/docs"
API_URL = "/services/spec"
API_YML = "api_doc.yml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"almacen": "API Almacén"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# Ruta para servir el contenido del fichero api_doc.yaml
@app.route(API_URL)
def api_spec():
    """
    indicamos al servidor de swagger dónde esta nuestro fichero yml
    """
    return send_from_directory(".", API_YML, as_attachment=True)


# Servicios CRUD básicos para administración de artículos
@app.route("/api/articulos", methods=["GET"])
def obtener_articulos():
    """
    Método get para obtención de articulos
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not AlmacenTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        # Posibles parámetros que se puede recibir para la query
        parametros_request = {
            "codigo": str,
            "activo": bool,
        }
        # Carga los parámetros recibidos en la llamada
        parametros = ParameterTools().carga_parametros_request(
            parametros_request, request
        )
        # Buscamos en base de datos
        results = AlmacenTools().select_articulos(parametros)
        # Devolvemos el resultado en un json
        return jsonify({"articulos": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/articulos/<codigo>", methods=["GET"])
def obtener_articulo(codigo):
    """
    Método get para obtención de un artículo concreto

    :param codigo(str) identificador del ártículo a devolver
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not AlmacenTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        # inicializa el parámetro de la query
        parametros = {}
        parametros["codigo"] = codigo
        # Lanza la búsqueda
        results = AlmacenTools().select_articulos(parametros)
        # Devuelve el resultado en JSON
        return jsonify({"articulos": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/articulos", methods=["POST"])
def crear_articulo():
    """
    Método POST para la creación de un artículo
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not AlmacenTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401
        # Creamos el artículo
        results = AlmacenTools().crea_articulo(request.json)

        # Devolvemos mensaje de éxito
        return jsonify({"articulos": results}), 201

    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/articulos/<codigo>", methods=["PUT"])
def actualizar_articulo(codigo):
    """
    Método PUT para actualizar de un artículo concreto

    :param codigo(str) identificador del ártículo a actualizar
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not AlmacenTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401
        # Lanza la actualización en base de datos
        results = AlmacenTools().actualiza_articulo(request.json, codigo)
        # Devuelve el resultado en JSON
        return jsonify({"articulos": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/articulos/<codigo>", methods=["DELETE"])
def borrar_articulo(codigo):
    """
    Método PUT para borrar de un artículo concreto

    :param codigo(str) identificador del ártículo a actualizar
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not AlmacenTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401
        # Lanza la actualización en base de datos
        AlmacenTools().borrar_articulo(codigo)
        # Devuelve el resultado en JSON
        return jsonify({"articulos": {}})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


# Otros servicios para simular la recepción y salida de artículos
@app.route("/api/articulos/recepcion", methods=["PUT"])
def recibir_articulo():
    """
    Método get para incrementar el stock de un artículo
    """
    print("recibir_articulo")
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not AlmacenTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        parametros_request = {
            "codigo": str,
            "cantidad": int,
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
        results = AlmacenTools().actualiza_entrada_stock(
            parametros["codigo"], parametros["cantidad"]
        )
        # Devuelve el resultado en JSON
        return jsonify({"articulos": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/articulos/salida", methods=["PUT"])
def vender_articulo():
    """
    Método get para decrementar el stock de un artículo
    """

    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not AlmacenTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        parametros_request = {
            "codigo": str,
            "cantidad": int,
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
        results = AlmacenTools().actualiza_salida_stock(
            parametros["codigo"], parametros["cantidad"]
        )
        # Devuelve el resultado en JSON
        return jsonify({"articulos": results})
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
        "--puerto", type=int, default=5000, help="Puerto donde se expondrá el API."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Ruta y nombre del fichero de configuración de la aplicación.",
    )
    parser.parse_args()

    args = parser.parse_args()

    # Inicializar la base de datos al arrancar la aplicación
    almacen_tools = AlmacenTools()

    almacen_tools.inicializar_almacen(args.config)

    app.run(host=args.servidor, port=args.puerto, debug=True)
