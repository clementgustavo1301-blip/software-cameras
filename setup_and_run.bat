@echo off
echo ==========================================
echo Configurando Retail Analytics System
echo ==========================================

REM Tentar encontrar Python
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :FoundPython
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :FoundPython
)

echo ERRO: Python nao encontrado. Por favor, instale o Python e adicione ao PATH.
echo Voce pode baixar em python.org
pause
exit /b 1

:FoundPython
echo Python encontrado: %PYTHON_CMD%

if not exist venv (
    echo Criando ambiente virtual...
    %PYTHON_CMD% -m venv venv
)

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo ==========================================
echo Iniciando Sistema...
echo Pressione 'q' na janela do video para sair.
echo ==========================================

python main.py

pause
