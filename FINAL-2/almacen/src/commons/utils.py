from api.almacen_api import app
from DB import db_actions


# Initialize the app and DB, and if it´s necessary create the tables and consumer
def initialize_app(host, port, config):
    database = db_actions.StorehouseDB(config)
    database.create_tables()
    generate_api_key(database, config)
    app.run(host=host, port=port)


# Generate a key por the consumer in the config
def generate_api_key(database, config):
    consumer_key = config['basedatos']['-consumidor_almacen_key']
    consumer_name = config['basedatos']['-consumidor_almacen']
    database.insert_consumer(consumer_key, consumer_name)


