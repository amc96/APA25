#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para limpar o projeto, removendo arquivos desnecessários 
e mantendo apenas os essenciais para a apresentação dos resultados.
"""

import os
import shutil

# Lista de arquivos a manter
ARQUIVOS_ESSENCIAIS = [
    'analisar_parentesco.py',     # Script de análise
    'graspe.py',                  # Implementação do método GRASPE
    'app_resultados.py',          # App web para mostrar resultados
    'melhores_cruzamentos.csv',   # Resultados da análise
    'README.md',                  # Documentação do projeto
    'limpar_projeto.py',          # Este script
]

# Lista de pastas a manter
PASTAS_ESSENCIAIS = [
    'templates',                 # Templates HTML
    'uploads',                   # Pasta com arquivos de entrada
    '.git',                      # Controle de versão
    '.pythonlibs',               # Bibliotecas Python instaladas
    '__pycache__',               # Cache Python
]

def limpar_projeto():
    """Remove arquivos desnecessários e mantém apenas os essenciais."""
    print("Iniciando limpeza do projeto...")
    
    # Listar todos os arquivos no diretório atual
    arquivos = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # Remover arquivos que não estão na lista de essenciais
    for arquivo in arquivos:
        if arquivo not in ARQUIVOS_ESSENCIAIS and not arquivo.startswith('.'):
            try:
                os.remove(arquivo)
                print(f"Arquivo removido: {arquivo}")
            except Exception as e:
                print(f"Erro ao remover {arquivo}: {str(e)}")
    
    # Listar todas as pastas no diretório atual
    pastas = [d for d in os.listdir('.') if os.path.isdir(d)]
    
    # Remover pastas que não estão na lista de essenciais
    for pasta in pastas:
        if pasta not in PASTAS_ESSENCIAIS and not pasta.startswith('.'):
            try:
                shutil.rmtree(pasta)
                print(f"Pasta removida: {pasta}")
            except Exception as e:
                print(f"Erro ao remover pasta {pasta}: {str(e)}")
    
    print("Limpeza concluída!")

if __name__ == "__main__":
    # Perguntar ao usuário se deseja continuar
    resposta = input("Esta ação irá remover arquivos desnecessários do projeto. Continuar? (S/N): ")
    
    if resposta.upper() == 'S':
        limpar_projeto()
    else:
        print("Operação cancelada pelo usuário.")