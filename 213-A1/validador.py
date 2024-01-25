# -*- coding: utf-8 -*-
# pylint: disable=I1101
"""
    Módulo para trabajar ficheros XML, XSD y JSON
"""
import argparse
import json
import xmltodict

from lxml import etree
from colorama import Fore, Style


def obtener_documento_parseado(path):
    """
    Devuelve el contenido de un XML parseado, dad su ruta

    :param path (str): Ruta al fichero a parsear.

    :return (str): documento
    """
    try:
        # Cargamos el documento
        return etree.parse(path)
    except etree.XMLSyntaxError as e:
        print("{Fore.RED}Error:{Style.RESET_ALL} El XML proporcionado no es válido.")
        print(e.msg)
        return []


def validar_xml(xml_doc, xsd_doc):
    """
    Valida un documento XML contra un esquema XSD.

    :param xml_doc (str): Documento XML.
    :param xsd_doc (str): Contenido fichero XSD (esquema) de validación.
    
    :return True ok False no Ok
    """
    print("- Comienza la validación")
    # Creamos un validador XML
    xml_validator = etree.XMLSchema(xsd_doc)
    validado = True
    # Validamos el documento XML contra el esquema XSD
    if xml_validator.validate(xml_doc):
        print(
            "    El documento XML "
            + f"{Fore.BLUE}{Style.BRIGHT}es válido{Style.RESET_ALL} según el esquema XSD."
        )
    else:
        validado = False
        print(
            "    El documento XML "
            + f"{Fore.RED}{Style.BRIGHT}no es válido{Style.RESET_ALL} según el esquema XSD."
        )
        print(f"{Fore.RED}{Style.BRIGHT}Errores:{Style.RESET_ALL}")
        for error in xml_validator.error_log:
            print(f"- Linea {error.line}, Columna {error.column}: {error.message}")
    return validado

def obtener_valores_xml(xml_doc, xpath):
    """
    Obtiene los valores de elementos XML utilizando XPath.

    :param xml_doc (str): Documento XML.
    :param xpath (str): Expresión XPath para buscar los valores.
    """
    print("- Comienza la búsqueda")
    try:
        # Utilizar XPath para obtener los valores
        resultados = xml_doc.xpath(xpath)

        # Devolver la lista de resultados
        if resultados:
            print(
                f"    Se han encontrado {Style.BRIGHT}{Fore.BLUE}{len(resultados)} "
                + f"ocurrecncias{Style.RESET_ALL} el fichero XML:"
            )
            for elemento in resultados:
                # Imprimir la información del elemento
                print(f"    > {elemento.tag}: {elemento.text}")
                # Si es un nodo padre, imprimir toda la información dentro del nodo
                for hijo in elemento:
                    print(f"        >{hijo.tag}: {hijo.text}")
        else:
            print(
                "    No se encontraron valores para la expresión XPath proporcionada."
            )
    except etree.XPathEvalError:
        print(
            f"    {Fore.RED}Error:{Style.RESET_ALL} La expresión XPath "
            + f"{Style.DIM}'{xpath}'{Style.RESET_ALL} no es válida."
        )


def xml_a_json(xml_doc):
    """
    Transforma un fichero XML en JSON y escribe el resultado por consola.

    :param xml_doc (str): Documento XML.

    """
    print("- Convirtiendo a JSON: ")
    try:
        xml_str = etree.tostring(xml_doc, pretty_print=True, encoding="utf-8").decode(
            "utf-8"
        )
        json_content = json.dumps(
            xmltodict.parse(xml_str), indent=4, ensure_ascii=False
        )
        print(json_content)
        with open("salida.json", "w", encoding="utf-8") as file:
            file.write(json_content)
    except xmltodict.expat.ExpatError as expat_err:
        print(
            f"    {Fore.RED}Error{Style.RESET_ALL} en el análisis XML con xmltodict: {expat_err}"
        )
    except json.JSONDecodeError as json_err:
        print(f"    {Fore.RED}Error{Style.RESET_ALL} al decodificar JSON: {json_err}")

def str2bool(v):
    """
    Función para convertir cadena en boolean
    """
    return v.lower() in ("true", "1", "yes", "y", "t")


if __name__ == "__main__":
    # Creamos un parser para los argumentos del módulo
    parser = argparse.ArgumentParser(description="Validador de ficheros XML")
    parser.add_argument("--xml", required=True, help="Ruta al fichero XML")
    parser.add_argument("--xsd", required=True, help="Ruta al fichero XSD")
    parser.add_argument("--xpath", required=False, help="XPATH a mostrar")
    parser.add_argument(
        "--json", required=False, default=False, type=str2bool, help="Devuelve JSON"
    )

    # Parseamos los argumentos
    args = parser.parse_args()

    xml_doc_ini = obtener_documento_parseado(args.xml)
    xsd_doc_ini = obtener_documento_parseado(args.xsd)

    # Validamos el XML
    validar_xml(xml_doc_ini, xsd_doc_ini)

    if args.xpath is not None:
        obtener_valores_xml(xml_doc_ini, args.xpath)

    if args.json:
        xml_a_json(xml_doc_ini)
