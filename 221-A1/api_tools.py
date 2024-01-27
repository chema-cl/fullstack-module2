# -*- coding: utf-8 -*-
"""
    Módulo que para hacer peticiones a una API
"""
import json
import requests


def get_resource(url, timeout):
    """
    Método para hacer llamadas GET a una API

    :param url(str): Url de la API
    :param timeout(int): timeout de la petición

    :return
        response (str) en formato json
        status_response (str) en formato json

    """
    response = requests.get(url, timeout=timeout)
    return response.json(), prepare_response_status(response)


def create_resource(url, json_data, timeout):
    """
    Método para hacer llamadas POST a una API

    :param url(str): Url de la API
    :param json_data(str): JSON con el recurso a crear
    :param timeout(int): timeout de la petición

    :return
        response (str) en formato json
        status_response (str) en formato json

    """
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url, data=json.dumps(json_data), headers=headers, timeout=timeout
    )
    return response.json(), prepare_response_status(response)


def update_resource(url, json_data, timeout):
    """
    Método para hacer llamadas PUT a una API

    :param url(str): Url de la API
    :param json_data(str): JSON con el recurso a actualizar
    :param timeout(int): timeout de la petición

    :return
        response (str) en formato json
        status_response (str) en formato json

    """
    headers = {"Content-Type": "application/json"}
    response = requests.put(
        url, data=json.dumps(json_data), headers=headers, timeout=timeout
    )
    return response.json(), prepare_response_status(response)


def delete_resource(url, timeout):
    """
    Método para hacer llamadas DELETE a una API

    :param url(str): Url de la API
    :param timeout(int): timeout de la petición

    :return
        status_response (str) en formato json

    """
    response = requests.delete(url, timeout=timeout)
    return {},prepare_response_status(response)


def prepare_response_status(response):
    """
    Función que formatea la respuesta en formato json

    :param response(Response)

    :return
        json (str): la respuesta formateada en json

    """
    return {
        "method": response.request.method,
        "url": response.request.url,
        "status": response.status_code,
        "content-type": response.headers.get("Content-Type"),
        "encoding": response.encoding,
    }
