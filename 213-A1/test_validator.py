# -*- coding: utf-8 -*-
# pylint: disable=I1101
"""
    Módulo prueba unitaria code_token
"""
import unittest
import validador
from unittest.mock import patch
from io import StringIO
import sys
import os
from lxml import etree

class TestCodeToken(unittest.TestCase):
    """
    Prueba unitaria módulo code_token
    """
    def test_validar_xml(self):
        """
            Prueba unitaria validar xml
        """
        xml_doc = etree.fromstring("<root></root>")
        xsd_doc = etree.fromstring("<xs:schema></xs:schema>")
        with patch("builtins.print") as mock_print:
            validador.validar_xml(xml_doc, xsd_doc)
            mock_print.assert_called_with(
                "    El documento XML es válido según el esquema XSD."
            )

    def test_obtener_valores_xml(self):
        """
            Prueba unitaria obtener valor de un xml
        """
        xml_doc = etree.fromstring("<root><element>value</element></root>")
        xpath = "//element"
        with patch("builtins.print") as mock_print:
            validador.obtener_valores_xml(xml_doc, xpath)
            mock_print.assert_called_with("    > element: value")

    def test_xml_a_json(self):
        """
            Prueba unitaria xml a json
        """
        xml_doc = etree.fromstring("<root><element>value</element></root>")
        with patch("builtins.print") as mock_print, patch(
            "builtins.open", create=True
        ) as mock_open:
            validador.xml_a_json(xml_doc)
            mock_print.assert_called_with("- Convirtiendo a JSON: ")
            mock_open.assert_called_with("salida.json", "w", encoding="utf-8")
            mock_open.return_value.__enter__.return_value.write.assert_called()


if __name__ == "__main__":
    unittest.main()
