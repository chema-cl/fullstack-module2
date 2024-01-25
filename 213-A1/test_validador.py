# -*- coding: utf-8 -*-
# pylint: disable=I1101
"""
    Módulo prueba unitaria code_token
"""
import validador

def test_validar_xml():
    """
        Prueba unitaria validar xml
    """
    xml_doc_ini = validador.obtener_documento_parseado("carta.xml")
    xsd_doc_ini = validador.obtener_documento_parseado("carta.xsd")
    result = validador.validar_xml(xml_doc_ini, xsd_doc_ini)
    assert result is True
