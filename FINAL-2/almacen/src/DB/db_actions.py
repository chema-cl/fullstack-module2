import sqlite3


class StorehouseDB:
    _instance = None
    # DB of the Strorehouse.

    def __new__(cls, conf, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StorehouseDB, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, conf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Engaging the embedded database')
        self._conf = conf

    def create_tables(self):
        try:
            print(self._conf['basedatos']['-path'])
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            tables = []
            product_table = """
                    CREATE TABLE IF NOT EXISTS products(
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                        name VARCHAR(150),
                        description VARCHAR(250),
                        quantity INTEGER DEFAULT 0,
                        available BOOLEAN DEFAULT true
                    );
                 """
            consumer_table = """ 
                    CREATE TABLE IF NOT EXISTS consumers(
                        key VARCHAR(150) PRIMARY KEY NOT NULL, 
                        consumer_name VARCHAR(150)
                    );
                """
            tables.append(product_table)
            tables.append(consumer_table)
            for table in tables:
                cursor.execute(table)
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def insert_product(self, name, description, quantity):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            insert_sql = "INSERT INTO products (name, description, quantity) VALUES ('{}', '{}', {})"\
                .format(str(name), str(description), quantity)
            print("insert_sql", insert_sql)
            cursor.execute(insert_sql)
            bd.commit()
            return 'ok'
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def get_all_products(self):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            get_all_sql = "SELECT * FROM products;"
            cursor.execute(get_all_sql)
            products = cursor.fetchall()
            return products
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def get_one_product(self, product_id):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            get_one_sql = "SELECT * FROM products where id = {}".format(product_id)
            cursor.execute(get_one_sql)
            product = cursor.fetchone()
            return product
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def delete_product(self, product_id):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            delete_sql = "DELETE FROM products WHERE id = {}".format(product_id)
            cursor.execute(delete_sql)
            bd.commit()
            return 'ok'
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def update_product(self, product_id, name, description, quantity, available):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            update_sql = "UPDATE products SET name = '{}', description = '{}', quantity = {}, available = {} WHERE id = {};"\
                .format(str(name), str(description), quantity, available, product_id)
            cursor.execute(update_sql)
            bd.commit()
            return 'ok'
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def increase_quantity(self, product_id, quantity_to_increase):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            increase_string = "quantity + {}".format(quantity_to_increase)
            update_sql = "UPDATE products SET quantity = {} WHERE id = {};"\
                .format(increase_string, product_id)
            cursor.execute(update_sql)
            bd.commit()
            return 'ok'
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def decrease_quantity(self, product_id, quantity_to_decrease):
        try:
            product_to_decrease = self.get_one_product(product_id)
            op = product_to_decrease[3] - quantity_to_decrease
            if op >= 0:
                bd = sqlite3.connect(self._conf['basedatos']['-path'])
                cursor = bd.cursor()
                increase_string = "quantity - {}".format(quantity_to_decrease)
                update_sql = "UPDATE products SET quantity = {} WHERE id = {};"\
                    .format(increase_string, product_id)
                cursor.execute(update_sql)
                bd.commit()
                return 'ok'
            else:
                return 'This product has less quantity than required'
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def insert_consumer(self, key, consumer_name):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            insert_sql = "INSERT OR IGNORE INTO consumers (key, consumer_name) VALUES ('{}', '{}')"\
                .format(str(key), str(consumer_name))
            print("insert_sql", insert_sql)
            cursor.execute(insert_sql)
            bd.commit()
            return 'ok'
        except sqlite3.OperationalError as error:
            print("Error:", error)

    def get_consumer(self, api_key):
        try:
            bd = sqlite3.connect(self._conf['basedatos']['-path'])
            cursor = bd.cursor()
            get_one_sql = "SELECT * FROM consumers where key = {}".format(api_key)
            cursor.execute(get_one_sql)
            consumer = cursor.fetchone()
            print("con", consumer)
            return consumer
        except sqlite3.OperationalError as error:
            print("Error:", error)
