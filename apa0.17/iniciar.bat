@echo off
echo ========================================
echo    Aplicativo de Analise de Parentesco
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.11 ou superior.
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Instalando dependencias...
pip install flask pandas werkzeug numpy
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo Dependencias instaladas com sucesso!
echo.

echo Criando pasta de uploads...
if not exist "uploads" mkdir uploads

echo.
echo Iniciando o aplicativo...
echo Acesse: http://localhost:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python app.py

pause