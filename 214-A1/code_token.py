# -*- coding: utf-8 -*-
"""
    Módulo para codificar un token JWT
"""
import argparse
import json
import uuid
import jwt
from colorama import Fore, Style


def generar_token(payload_path, secret):
    """
    Generador de token JWT

    :param payload_path (str): ruta del fichero payload, para añadir al token JWT
    :param secret (str): secreto para codificar el token

    """
    try:
        # Leemos el fichero de payload
        with open(payload_path, "r", encoding="utf-8") as file:
            payload_data = json.load(file)

        # Generamos un identificador único
        jwt_id = str(uuid.uuid4())

        # Añadimos el identificador jti al payload
        payload_data["jti"] = jwt_id

        # Generamos el token JWT
        token = jwt.encode(payload_data, secret, algorithm="HS256")

        # Imprimimos el token codificado
        print(token)
    except FileNotFoundError:
        print(
            f"    {Fore.RED}Error:{Style.RESET_ALL} El archivo '{payload_path}' no se encontró."
        )
    except json.JSONDecodeError as e:
        print(
            f"    {Fore.RED}Error:{Style.RESET_ALL} al decodificar el contenido JSON: {e}"
        )
    except jwt.PyJWTError as e:
        print(f"    {Fore.RED}Error:{Style.RESET_ALL} al generar el token JWT: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de tokens JWT")
    parser.add_argument(
        "--payload", required=True, help="Ruta del fichero de payload (payload.json)"
    )
    parser.add_argument("--secret", required=True, help="Secreto para firmar el token")

    args = parser.parse_args()

    # Generamos el token
    generar_token(args.payload, args.secret)
