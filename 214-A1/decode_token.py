# -*- coding: utf-8 -*-
"""
    Módulo para decodificar un token JWT
"""
import argparse
import json
import jwt
from colorama import Fore, Style

def decodificar_token(token, secret, field=None):
    """
    Decodifica un token y lo muestra por pantalla

    :param token (str): token necesario para decodificar el token
    :param secret (str): secreto con el que se ha codificado el token
    :param field (str): campo que queremos devover por pantalla, 
                        si no se recibe se decodificará el token entero

    """
    try:
        # Decodificamos el token
        payload = jwt.decode(token, secret, algorithms=["HS256"])

        # Si viene relleno el campo field,
        # lo buscamos y lo imprimimos
        if field:
            field_value = payload.get(field)
            if field_value is None:
                print(
                    f"{Style.BRIGHT}{field}{Style.RESET_ALL}: " +
                    f"{Fore.RED}No encontrado{Style.RESET_ALL} "
                )
            else:
                print(
                    f"{Style.BRIGHT}{field}{Style.RESET_ALL}: " +
                    f"{Fore.BLUE}{field_value}{Style.RESET_ALL} "
                )
        else:
            # No viene indicado el campo field
            # Impriomimos el payload completo
            print(
                f"{Style.BRIGHT}" +
                f"- Contenido completo del cuerpo del token:{Style.RESET_ALL}"
            )
            #Imprimimos el payload completo formateado para que se vea bien
            print(json.dumps(payload, indent=4, ensure_ascii=False))
    except jwt.ExpiredSignatureError:
        print(f"    {Fore.RED}Error:{Style.RESET_ALL} Token expirado.")
    except jwt.InvalidSignatureError:
        print(f"    {Fore.RED}Error:{Style.RESET_ALL} Firma incorrecta.")
    except jwt.InvalidTokenError:
        print(f"    {Fore.RED}Error:{Style.RESET_ALL} Token no válido.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decodificador de tokens JWT")
    parser.add_argument("--token", required=True, help="Token JWT a decodificar")
    parser.add_argument("--secret", required=True, help="Secreto de la firma del token")
    parser.add_argument(
        "--field", required=False, help="Nombre de un campo del token"
    )

    args = parser.parse_args()

    # Decodificamos el token y mostramos la información por consola
    decodificar_token(args.token, args.secret, args.field)
