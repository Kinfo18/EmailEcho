#!/bin/bash

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "Python3 no está instalado. Por favor, instale Python3 y vuelva a intentarlo."
    exit 1
fi

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar requerimientos
pip install -r requirements.txt

# Configurar contraseña de correo
python3 -c "from src.config_manager import ConfigManager; ConfigManager('config/config.json').set_password(input('Ingrese su contraseña de correo: '))"

echo "Instalación completa. Puede iniciar el programa ejecutando 'python src/main.py'"