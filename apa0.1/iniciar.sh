#!/bin/bash

echo "======================================"
echo "Instalando dependências necessárias..."
echo "======================================"
pip install pandas numpy matplotlib flask

echo
echo "==================================================="
echo "Iniciando aplicação web de conversão CSV para Matriz"
echo "==================================================="
python app.py