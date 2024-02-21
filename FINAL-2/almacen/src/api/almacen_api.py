from flask import Flask, request, Response, send_from_directory
import json
from flask_expects_json import expects_json
from DB import db_actions
from schemas import new_product, schema_update_product, schema_consumer
from flask_swagger_ui import get_swaggerui_blueprint
from api import config
import os

config = config

app = Flask("storehouse - REST services")
API_URL = '/services/spec'
SWAGGER_URL = '/api/docs/'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
database = db_actions.StorehouseDB(config)


def authenticate_api_key(api_key):
    print("apu", api_key)
    ok_api_key = database.get_consumer(api_key)
    if ok_api_key is not None:
        return api_key
    return None


# Swagger Route
@app.route(API_URL)
def specs():
    return send_from_directory(os.getcwd(), "api_doc.yaml")


# Check the request to extract api-key
@app.before_request
def before_request():
    print(SWAGGER_URL)
    print("request", request.url )
    if SWAGGER_URL not in request.url and API_URL not in request.url:
        api_key = request.headers.get('Api-key')
        if not api_key or not authenticate_api_key(api_key):
            return Response(json.dumps({'error': 'Unauthorized'}), status=401)


# Get all products of the DB
@app.route('/storehouse/services/products', methods=['GET'])
def srv_get_all_products():
    list_products = database.get_all_products()
    json_l = []
    status = 200
    if list_products is not None and len(list_products) > 0:
        for row in list_products:
            availability = True
            if row[4] == 1:
                availability = True
            elif row[4] == 0:
                availability = False
            product = {'id': row[0], 'name': row[1], 'description': row[2], 'quantity': row[3],
                       'available': availability}
            json_l.append(product)
    else:
        json_l.append("There are no products in the database")
        status = 404
    return Response(json.dumps(json_l), mimetype='application/json', status=status)


# Get one product of the DB with the product_id
@app.route('/storehouse/services/product/<product_id>', methods=['GET'])
def srv_one_product(product_id):
    response = database.get_one_product(product_id)
    status = 200
    if response is not None:
        availability = True
        if response[4] == 1:
            availability = True
        elif response[4] == 0:
            availability = False
        product = {'id': response[0], 'name': response[1], 'description': response[2], 'quantity': response[3],
                   'available': availability}
        return Response(json.dumps(product), mimetype='application/json', status=status)
    else:
        product = "The prodcut don't exist"
        status = 404
        return Response(json.dumps(product), status=status)


# Create a new product in the DB
@app.route('/storehouse/services/product', methods=['POST'])
@expects_json(new_product.new_product)
def srv_new_product():
    product = request.json
    name = product['name']
    description = product['description']
    quantity = product['quantity']
    response = database.insert_product(name, description, quantity)
    status = 201
    if response != 'ok':
        status = 400
    return Response(json.dumps(response), mimetype='text/json', status=status)


# Update one product in the DB with the product_id
@app.route('/storehouse/services/product/<product_id>', methods=['PUT'])
@expects_json(schema_update_product.update_product)
def srv_update_product(product_id):
    product = request.json
    name = product['name']
    description = product['description']
    quantity = product['quantity']
    available = product['available']
    response = database.update_product(product_id, name, description, quantity, available)
    status = 200
    if response != 'ok':
        status = 400
    return Response(json.dumps(response), mimetype='text/json', status=status)


# Delete one product in the DB with the product_id
@app.route('/storehouse/services/product/<product_id>', methods=['DELETE'])
def srv_delete_product(product_id):
    response = database.delete_product(product_id)
    status = 201
    if response != 'ok':
        response = "The prodcut don't exist"
        status = 404
    return Response(json.dumps(response), mimetype='text/json', status=status)


# Increase the quantity of one product in the DB with the product_id. Product receipt
@app.route('/storehouse/services/product/<product_id>/increase', methods=['PUT'])
@expects_json()
def srv_increase_quantity(product_id):
    product = request.json
    quantity_to_increase = product['increase_quantity']
    response = database.increase_quantity(product_id, quantity_to_increase)
    status = 200
    if response != 'ok':
        status = 404
        response = "The prodcut don't exist"
    return Response(json.dumps(response), mimetype='text/json', status=status)


# Decrease the quantity of one product in the DB with the product_id. Product output
@app.route('/storehouse/services/product/<product_id>/decrease', methods=['PUT'])
@expects_json()
def srv_decrease_quantity(product_id):
    product = request.json
    quantity_to_decrease = product['decrease_quantity']
    response = database.decrease_quantity(product_id, quantity_to_decrease)
    status = 200
    if response != 'ok':
        status = 404
        if response != 'This product has less quantity than required':
            status = 400
            response = "The prodcut don't exist"
    return Response(json.dumps(response), mimetype='text/json', status=status)


# Create a new consumer
@app.route('/storehouse/services/consumer', methods=['POST'])
@expects_json(schema_consumer.consumer)
def srv_create_consumer():
    consumer = request.json
    consumer_name = consumer['consumer_name']
    key = consumer['consumer_key']
    response = database.insert_consumer(key, consumer_name)
    status = 200
    if response != 'ok':
        status = 400
    return Response(json.dumps(response), mimetype='text/json', status=status)
