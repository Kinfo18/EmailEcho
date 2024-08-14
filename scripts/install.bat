@echo off

REM Verificar si Python está instalado
python --version 2>NUL
if errorlevel 1 goto errorNoPython

REM Crear entorno virtual
python -m venv venv

REM Activar entorno virtual
call venv\Scripts\activate

REM Instalar requerimientos
pip install -r requirements.txt

REM Configurar contraseña de correo
python -c "from src.config_manager import ConfigManager; ConfigManager('config/config.json').set_password(input('Ingrese su contraseña de correo: '))"

echo Instalación completa. Puede iniciar el programa ejecutando 'python src/main.py'
goto :eof

:errorNoPython
echo.
echo Error: Python no está instalado o no está en el PATH.
echo Instale Python y asegúrese de que esté en el PATH del sistema.