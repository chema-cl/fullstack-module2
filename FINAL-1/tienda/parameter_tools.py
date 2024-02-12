# -*- coding: utf-8 -*-
# pylint: disable=R0801
"""
    Operaciones con parámetros
"""


class ParameterTools:
    """
    Clase para agrupar las operaciones con parámetros
    """

    def carga_parametros_request(self, parametros_request, request):
        """
        Construye la una lista de parámetros extraidos a partir del
        request de una petición

        :param parametros_request(lista clave valor) parámetors, nombre y tipo
        :param request(request) peticón
        """
        try:
            parametros = {}
            for parametro, tipo in parametros_request.items():
                valor = request.args.get(parametro)
                if valor is not None:
                    try:
                        parametros[parametro] = self.calcula_valor(valor, tipo)
                    except ValueError as error:
                        raise error
            return parametros
        except ValueError as error:
            raise error

    def carga_parametros_json(self, parametros_opcionales, json_entrada):
        """
        Construye la una lista de parámetros extraidos a partir de
        un json

        :param parametros_request(lista clave valor) parámetors, nombre y tipo
        :param json_entrada(json) json
        """
        try:
            parametros = {}
            for parametro, tipo in parametros_opcionales.items():
                if parametro in json_entrada:
                    valor = json_entrada[parametro]
                    if valor is not None:
                        try:
                            parametros[parametro] = self.calcula_valor(valor, tipo)
                        except ValueError as error:
                            raise error
            return parametros
        except ValueError as error:
            raise error

    def calcula_valor(self, valor, tipo):
        """
        Devuelve un valor adaptado a su tipo

        :param valor(?) valor del parámetro
        :param tipo(?) tipo del parámetro valor
        """
        try:
            if valor is not None:
                if tipo is bool:
                    if isinstance(valor, bool):
                        return valor
                    if valor == 1 or valor.lower() == "true":
                        return True
                    if valor == 0 or valor.lower() == "false":
                        return False
                    raise ValueError("Valores booleanos solo permite True | False")
                if tipo is int:
                    if isinstance(valor, int):
                        return valor
                    return int(valor)
            return valor
        except ValueError as error:
            raise error
