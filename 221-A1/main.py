# -*- coding: utf-8 -*-
"""
    Módulo para llamar a una API REST definida en el fichero config.json no securizada
"""
import argparse
import json
from colorama import Fore, Style
import json_tools
import api_tools


def main():
    """
    Función main utilizada para consumir la API
    """
    parser = argparse.ArgumentParser(
        description="Operaciones CRUD en el API definido en config.json"
    )
    parser.add_argument(
        "--method",
        required=True,
        choices=["GET", "POST", "PUT", "DELETE"],
        help="Método",
    )
    parser.add_argument(
        "--resource", required=True, choices=["posts", "comments"], help="Recurso"
    )
    parser.add_argument("--resource_id", required=False, help="Id recurso")

    args = parser.parse_args()

    if args.method in ["PUT", "DELETE"] and args.resource_id is None:
        parser.error(
            "El parámetro --resource_id es obligatorio para los métodos PUT y DELETE."
        )
    if args.method in ["POST"] and args.resource_id is not None:
        parser.error(
            "El parámetro --resource_id no está permitido para el método POST."
        )

    # Leer configuración
    config = json_tools.read_json_file("config.json", "utf-8")

    # Construir la URL del API
    if args.resource_id is None:
        url = f"{config['url']}{args.resource}"
    else:
        url = f"{config['url']}{args.resource}/{args.resource_id}"

    print(f"{Fore.GREEN}{args.method}{Style.RESET_ALL} {url}")

    # Realizar la llamada al API según el método especificado
    response_data = None
    response_status = None
    if args.method == "GET":
        response_data, response_status = api_tools.get_resource(
            url, config["request_time_out"]
        )
    elif args.method == "POST":
        json_data = json_tools.read_json_file(f"{args.resource}.json", "utf-8")
        response_data, response_status = api_tools.create_resource(
            url, json_data, config["request_time_out"]
        )
    elif args.method == "PUT":
        json_data = json_tools.read_json_file(f"{args.resource}.json", "utf-8")
        response_data, response_status = api_tools.update_resource(
            url, json_data, config["request_time_out"]
        )
    elif args.method == "DELETE":
        response_data, response_status = api_tools.delete_resource(
            url, config["request_time_out"]
        )

    # Guardar la respuesta en los archivos de salida
    json_tools.save_json_file(
        response_status, config["response_status"], response_status["encoding"]
    )
    print(
        f"{Fore.BLUE}Consulte el fichero de estado en:{Style.RESET_ALL} {config['response_status']}"
    )
    print(json.dumps(response_status, indent=4, ensure_ascii=False))

    data_json_api = {}
    self = {}
    self["self"] = url
    data_json_api["links"] = self
    data_json_api["data"] = response_data

    json_tools.save_json_file(
        data_json_api, config["response_data"], response_status["encoding"]
    )
    print(
        f"{Fore.BLUE}Consulte el fichero de datos completo en: {Style.RESET_ALL} "
        + f"{config['response_data']}  {Fore.RED}(*Solo mostraremos los primeros 200 caracteres)"
        + f"{Style.RESET_ALL}"
    )
    print((json.dumps(data_json_api, indent=4, ensure_ascii=False))[0:200] + "\n...")


if __name__ == "__main__":
    main()
