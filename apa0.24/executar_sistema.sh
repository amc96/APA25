#!/bin/bash

# Configurar cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "  Sistema de Otimizacao de Acasalamento"
echo "  Inicializacao Automatica"
echo "========================================"
echo ""

# Função para detectar sistema operacional
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Função para instalar Python no Linux
install_python_linux() {
    echo -e "${YELLOW}Tentando instalar Python...${NC}"
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python python-pip
    else
        echo -e "${RED}Gerenciador de pacotes não suportado. Instale Python3 manualmente.${NC}"
        exit 1
    fi
}

# Função para abrir navegador
open_browser() {
    local os_type=$(detect_os)
    local url="http://localhost:5000"
    
    case $os_type in
        "linux")
            if command -v xdg-open &> /dev/null; then
                xdg-open "$url" &> /dev/null &
            elif command -v gnome-open &> /dev/null; then
                gnome-open "$url" &> /dev/null &
            elif command -v firefox &> /dev/null; then
                firefox "$url" &> /dev/null &
            elif command -v google-chrome &> /dev/null; then
                google-chrome "$url" &> /dev/null &
            else
                echo -e "${YELLOW}Navegador não detectado. Abra manualmente: $url${NC}"
            fi
            ;;
        "macos")
            open "$url" &> /dev/null &
            ;;
        *)
            echo -e "${YELLOW}Sistema não suportado. Abra manualmente: $url${NC}"
            ;;
    esac
}

# [1/5] Verificar Python
echo "[1/5] Verificando Python..."
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 encontrado${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Verificar se é Python 3
    if python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo -e "${GREEN}✓ Python encontrado${NC}"
        PYTHON_CMD="python"
    else
        echo -e "${RED}ERRO: Python 3.8+ necessário${NC}"
        install_python_linux
        PYTHON_CMD="python3"
    fi
else
    echo -e "${RED}ERRO: Python não encontrado${NC}"
    install_python_linux
    PYTHON_CMD="python3"
fi

# [2/5] Verificar ambiente virtual
echo "[2/5] Verificando ambiente virtual..."
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERRO: Falha ao criar ambiente virtual${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "${GREEN}✓ Ambiente virtual já existe${NC}"
fi

# [3/5] Ativar ambiente virtual
echo "[3/5] Ativando ambiente virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERRO: Falha ao ativar ambiente virtual${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Ambiente virtual ativado${NC}"

# [4/5] Verificar e instalar dependências
echo "[4/5] Verificando dependências..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    python -m pip install --upgrade pip
    pip install streamlit pandas numpy plotly
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERRO: Falha ao instalar dependências${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Dependências instaladas${NC}"
else
    echo -e "${GREEN}✓ Dependências já instaladas${NC}"
fi

# [5/5] Iniciar aplicação
echo "[5/5] Iniciando aplicação..."
echo ""
echo -e "${GREEN}✓ Sistema iniciado com sucesso!${NC}"
echo -e "${GREEN}✓ Abrindo navegador em 3 segundos...${NC}"
echo ""
echo "Para parar o sistema, pressione Ctrl+C neste terminal"
echo ""

# Aguardar 3 segundos e abrir navegador
sleep 3
open_browser

# Executar Streamlit
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true