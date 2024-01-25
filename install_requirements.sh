#!/bin/bash

# Encuentra todos los archivos requirements.txt en el repositorio
requirements_files=$(find . -name 'requirements.txt')

# Instala los requisitos de cada archivo requirements.txt
for file in $requirements_files; do
    echo "Instalando requisitos para $file"
    pip install -r $file
done
