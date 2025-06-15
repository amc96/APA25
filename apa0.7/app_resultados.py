#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aplicação web para apresentar os resultados da análise de parentesco de produtos.
Mostra os melhores cruzamentos de acordo com o método GRASPE.
"""

from flask import Flask, render_template, send_file, request, redirect, url_for
import pandas as pd
import os
import time

app = Flask(__name__)

# Configuração
RESULTADOS_FILE = 'melhores_cruzamentos.csv'
ARQUIVO_ENTRADA = './uploads/parentesco_produtos (1).csv'

@app.route('/')
def index():
    """Rota principal que carrega e apresenta os resultados da análise."""
    try:
        # Verificar se o arquivo de resultados existe
        if not os.path.exists(RESULTADOS_FILE):
            return render_template('error.html', 
                                  mensagem="Arquivo de resultados não encontrado. Execute a análise primeiro.")
        
        # Carregar os melhores cruzamentos
        df_resultados = pd.read_csv(RESULTADOS_FILE)
        
        # Contar quantos registros foram analisados no arquivo de entrada
        total_registros = 0
        if os.path.exists(ARQUIVO_ENTRADA):
            with open(ARQUIVO_ENTRADA, 'r') as f:
                total_registros = sum(1 for _ in f) - 1  # -1 para o cabeçalho
        
        # Preparar dados para o template
        melhores_cruzamentos = []
        for _, row in df_resultados.iterrows():
            melhores_cruzamentos.append({
                'Animal_1': row['Animal_1'],
                'Animal_2': row['Animal_2'],
                'Coeficiente': row['Coeficiente']
            })
        
        # Extrair e contar os animais utilizados nos cruzamentos
        animais_1_utilizados = set()
        animais_2_utilizados = set()
        
        for cruzamento in melhores_cruzamentos:
            animais_1_utilizados.add(cruzamento['Animal_1'])
            animais_2_utilizados.add(cruzamento['Animal_2'])
        
        # Contar animais únicos no arquivo original (se disponível)
        total_animais_1_unicos = 0
        total_animais_2_unicos = 0
        
        if os.path.exists(ARQUIVO_ENTRADA):
            try:
                df_original = pd.read_csv(ARQUIVO_ENTRADA)
                total_animais_1_unicos = len(df_original['Animal_1'].unique())
                total_animais_2_unicos = len(df_original['Animal_2'].unique())
            except Exception as e:
                print(f"Erro ao contar animais únicos: {str(e)}")
        
        # Informações para exibição
        nome_arquivo = os.path.basename(ARQUIVO_ENTRADA)
        limite_cruzamentos = len(melhores_cruzamentos)
        total_cruzamentos = total_registros
        tempo_processamento = "2.61"  # Atualizado com o valor do último processamento
        
        # Estatísticas de animais utilizados
        total_animais_1 = len(animais_1_utilizados)
        total_animais_2 = len(animais_2_utilizados)
        porcentagem_animal1 = (total_animais_1 / total_animais_1_unicos * 100) if total_animais_1_unicos > 0 else 0
        porcentagem_animal2 = (total_animais_2 / total_animais_2_unicos * 100) if total_animais_2_unicos > 0 else 0
        
        return render_template('resultados.html',
                              melhores_cruzamentos=melhores_cruzamentos,
                              nome_arquivo=nome_arquivo,
                              total_registros=total_registros,
                              tempo_processamento=tempo_processamento,
                              total_cruzamentos=total_cruzamentos,
                              limite_cruzamentos=limite_cruzamentos,
                              total_animais_1=total_animais_1,
                              total_animais_2=total_animais_2,
                              total_animais_1_unicos=total_animais_1_unicos,
                              total_animais_2_unicos=total_animais_2_unicos,
                              porcentagem_animal1=porcentagem_animal1,
                              porcentagem_animal2=porcentagem_animal2)
    
    except Exception as e:
        return render_template('error.html', 
                              mensagem=f"Erro ao carregar os resultados: {str(e)}")

@app.route('/download')
def download_resultados():
    """Rota para baixar o arquivo de resultados."""
    try:
        return send_file(RESULTADOS_FILE, 
                        as_attachment=True,
                        download_name='melhores_cruzamentos.csv')
    except Exception as e:
        return render_template('error.html', 
                              mensagem=f"Erro ao baixar o arquivo: {str(e)}")

if __name__ == '__main__':
    # Criar a pasta uploads se não existir
    os.makedirs('./uploads', exist_ok=True)
    
    # Iniciar o servidor
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)