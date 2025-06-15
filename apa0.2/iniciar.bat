@echo off
REM Script para executar o processador de matriz em Windows
REM Verifica se o Python está instalado

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado. Por favor, instale o Python 3.x.
    echo Visite: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Instala as dependências necessárias
echo Instalando dependencias...
pip install pandas numpy

REM Executa o script
echo ========================================
echo PROCESSADOR DE MATRIZ DE PARENTESCO
echo ========================================
echo.
echo Escolha uma opcao:
echo 1. Criar matriz a partir do CSV
echo 2. Extrair vetores do CSV
echo 3. Remover duplicados dos vetores
echo.
set /p opcao="Digite o numero da opcao: "

if "%opcao%"=="1" (
    set /p arquivo="Digite o caminho do arquivo CSV: "
    set /p saida="Digite o nome do arquivo de saida (ou Enter para padrao): "
    
    if "%saida%"=="" (
        python csv_to_matrix.py matriz "%arquivo%"
    ) else (
        python csv_to_matrix.py matriz "%arquivo%" "%saida%"
    )
) else if "%opcao%"=="2" (
    set /p arquivo="Digite o caminho do arquivo CSV: "
    python csv_to_matrix.py vetores "%arquivo%"
) else if "%opcao%"=="3" (
    python csv_to_matrix.py limpar
) else (
    echo Opcao invalida.
)

echo.
echo Processo concluido.
pause