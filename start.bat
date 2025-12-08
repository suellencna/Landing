@echo off
echo ========================================
echo   Landing Page - Investir e Realizar
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.8 ou superior.
    pause
    exit /b 1
)

echo Verificando dependencias...
pip install -r requirements.txt --quiet

echo.
echo Iniciando servidor...
echo Acesse: http://localhost:5000
echo Pressione Ctrl+C para parar o servidor
echo.

python app.py

pause

