# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=W0718
# pylint: disable=R0801
"""
    Módulo API REST tienda
"""
import argparse
import secrets
from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from tienda_tools import TiendaTools
from parameter_tools import ParameterTools

app = Flask(__name__)

SWAGGER_URL = "/api/docs"
API_URL = "/services/spec"
API_YML = "api_doc.yml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"tienda": "API Almacén"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# Ruta para servir el contenido del fichero api_doc.yaml
@app.route(API_URL)
def api_spec():
    """
    indicamos al servidor de swagger dónde esta nuestro fichero yml
    """
    return send_from_directory(".", API_YML, as_attachment=True)


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


@app.route("/api/consumidores", methods=["POST"])
def crear_consumidor():
    """
    Método POST para la creación de un producto
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        # recogemos los parámetros
        consumidor = request.args.get("consumidor")
        if consumidor is None:
            return (
                jsonify({"ERROR": "Parámetro consumidor no recibido"}),
                401,
            )
        # Creamos consumidor
        parametros = {}
        parametros["codigo"] = str(secrets.token_hex(20))
        parametros["descripcion"] = consumidor
        parametros["activo"] = True
        print(parametros)

        results = TiendaTools().crear_consumidor(parametros)

        # Devolvemos mensaje de éxito
        return jsonify({"consumidores": results}), 201

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

        # recogemos los parámetros
        cantidad = request.args.get("cantidad")
        codigo = request.args.get("codigo")
        adapta_a_disponibilidad = request.args.get("adapta_a_disponibilidad")
        if codigo is None or cantidad is None:
            return (
                jsonify({"ERROR": "Parámetros codigo y cantidad no recibidos"}),
                401,
            )

        # Lanza la actualización en base de datos
        results = TiendaTools().reponer_producto_almacen_por_codigo(
            codigo,
            cantidad,
            adapta_a_disponibilidad,
        )

        return jsonify({"productos": results})

    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos/vender", methods=["PUT"])
def vender_productos():
    """
    Método put para vender productos
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401

        # recogemos los parámetros
        cantidad = request.args.get("cantidad")
        codigo = request.args.get("codigo")
        if codigo is None or cantidad is None:
            return (
                jsonify({"ERROR": "Parámetros codigo y cantidad no recibidos"}),
                401,
            )
        cantidad=int(cantidad)
        # Lanza la actualización en base de datos
        results = TiendaTools().vender_productos(codigo, cantidad)
        # Devolvemos el resultado en un json
        return jsonify({"mensaje": results})
    except Exception as error:
        return jsonify({"ERROR": f"{error.args[0]}"}), 400


@app.route("/api/productos/precio", methods=["PUT"])
def actualizar_precio():
    """
    Método PUT para modificar el precio
    """
    try:
        # Verifica la clave de API
        api_key = request.headers.get("X-API-Key")
        if not TiendaTools().check_consumidor_valido(api_key):
            return jsonify({"ERROR": "Clave de API inválida"}), 401
        # Lanza la actualización en base de datos

        # recogemos los parámetros
        codigo = request.args.get("codigo")
        precio = request.args.get("precio")
        activo = request.args.get("activo")
        if precio is None or codigo is None:
            return (
                jsonify({"ERROR": "Los parámetros precio y codigo son obligatorios"}),
                401,
            )
        parametros_update = {}
        parametros_update["precio"] = precio
        if activo is not None:
            parametros_update["activo"] = activo

        results = TiendaTools().actualiza_producto_parametros(codigo, parametros_update)
        # Devuelve el resultado en JSON
        return jsonify({"productos": results})
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
        "--puerto", type=int, default=7000, help="Puerto donde se expondrá el API."
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
