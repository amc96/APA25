@echo off
title Sistema de Otimizacao de Acasalamento Animal
color 0A

echo ========================================
echo   Sistema de Otimizacao de Acasalamento
echo   Inicializacao Automatica
echo ========================================
echo.

REM Verificar se Python esta instalado
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Opcoes:
    echo 1. Instalar Python manualmente: https://www.python.org/downloads/
    echo 2. Instalar via Microsoft Store: python3
    echo.
    pause
    exit /b 1
)
echo ✓ Python encontrado

REM Verificar se ambiente virtual existe
echo [2/5] Verificando ambiente virtual...
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo ✓ Ambiente virtual criado
) else (
    echo ✓ Ambiente virtual ja existe
)

REM Ativar ambiente virtual
echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)
echo ✓ Ambiente virtual ativado

REM Verificar e instalar dependencias
echo [4/5] Verificando dependencias...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Instalando dependencias...
    python -m pip install --upgrade pip
    pip install streamlit pandas numpy plotly
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
    echo ✓ Dependencias instaladas
) else (
    echo ✓ Dependencias ja instaladas
)

REM Iniciar aplicacao
echo [5/5] Iniciando aplicacao...
echo.
echo ✓ Sistema iniciado com sucesso!
echo ✓ Abrindo navegador em 3 segundos...
echo.
echo Para parar o sistema, pressione Ctrl+C nesta janela
echo.

REM Aguardar 3 segundos e abrir navegador
timeout /t 3 /nobreak >nul
start http://localhost:5000

REM Executar Streamlit
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true

pause