# -*- coding: utf-8 -*-
"""
    Módulo con herramietas para trabajar con ficheros json
"""
import json


def read_json_file(file_path, file_encoding):
    """
    Dada la una ruta de un json, lo devuelve en una variable

    :param file_path (str): Ruta del fichero
    :param file_encoding (str): encoding del fiechero
    """
    with open(file_path, "r", encoding=file_encoding) as file:
        return json.load(file)


def save_json_file(content, file_path, file_encoding):
    """
    Formatea el contenido recibido y lo guarda en un fichero

    :param content (str): Contenido del json
    :param file_path (str): Ruta del fichero
    :param file_encoding (str): encoding del fiechero
    """
    if content is not None:
        with open(file_path, "w", encoding=file_encoding) as file:
            json.dump(content, file, indent=4, ensure_ascii=False)
    else:
        with open(file_path, "w", encoding=file_encoding) as file:
            file.write("")
            file.close()
