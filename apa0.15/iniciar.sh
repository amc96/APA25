#!/bin/bash

echo "========================================"
echo "   Aplicativo de Análise de Parentesco"
echo "========================================"
echo

# Verificar se Python está instalado
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERRO: Python não encontrado!"
        echo "Por favor, instale o Python 3.11 ou superior."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python encontrado: $($PYTHON_CMD --version)"
echo

# Verificar se pip está disponível
echo "Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        echo "ERRO: pip não encontrado!"
        echo "Por favor, instale o pip."
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo "pip encontrado!"
echo

# Instalar dependências
echo "Instalando dependências..."
$PIP_CMD install flask pandas werkzeug numpy

if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências!"
    exit 1
fi

echo
echo "Dependências instaladas com sucesso!"
echo

# Criar pasta de uploads
echo "Criando pasta de uploads..."
mkdir -p uploads

echo
echo "Iniciando o aplicativo..."
echo "Acesse: http://localhost:5000"
echo
echo "Pressione Ctrl+C para parar o servidor"
echo

# Executar o aplicativo
$PYTHON_CMD app.py