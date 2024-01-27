# -*- coding: utf-8 -*-
"""
    Módulo para invocar la documentación de la api con Flask y la librería flask_swagger_ui. 
"""
from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Ruta al fichero api_doc.yaml generado
API_SPEC_PATH = "/ruta/a/tu/api_doc.yaml"

# Configuración para la documentación Swagger UI
SWAGGER_URL = "/api/docs"
API_URL = "/services/spec"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "API Documentation"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Ruta para servir el contenido del fichero api_doc.yaml
@app.route(API_URL)
def api_spec():
    """
        indicamos al servidor de swagger dónde esta nuestro fichero yml
    """
    return send_from_directory(".", "api_doc.yaml", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
