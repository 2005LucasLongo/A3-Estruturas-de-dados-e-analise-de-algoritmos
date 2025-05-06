@echo off
set VENV_DIR=venv

:: Verifica se a venv já existe
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Criando ambiente virtual...
    python -m venv %VENV_DIR%
    call %VENV_DIR%\Scripts\activate
    echo Instalando dependências...
    pip install -r requirements.txt
    echo.
    echo Dependências instaladas com sucesso!
echo O programa será iniciado em instantes. Por favor, aguarde...
    timeout /t 3 >nul
) else (
    echo Ambiente virtual já existe.
    call %VENV_DIR%\Scripts\activate
)

cls
echo Executando o programa principal...
python main.py
python testes/comparador_testes.py

pause
