#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arquivo: analisar_parentesco.py
Descrição: Script para analisar o arquivo de parentesco de produtos e gerar um arquivo 
           com os melhores cruzamentos usando o método GRASPE.
"""

import pandas as pd
import numpy as np
import os
import time

def analisar_parentesco_direto(arquivo_entrada, arquivo_saida, limite_combinacoes=100, valor_descarte=-1):
    """
    Analisa o arquivo de parentesco de produtos diretamente, sem criar uma matriz completa,
    e gera um arquivo com os melhores cruzamentos.
    
    Esta função é otimizada para arquivos grandes e garante que todos os produtos Animal_2
    sejam incluídos nos cruzamentos, mesmo que isso exija repetir produtos Animal_1.
    
    Parâmetros:
    arquivo_entrada (str): Caminho para o arquivo CSV de entrada com os dados de parentesco
    arquivo_saida (str): Caminho para o arquivo CSV de saída com os melhores cruzamentos
    limite_combinacoes (int): Número máximo de combinações a retornar
    valor_descarte (float): Valor de coeficiente a ser descartado
    """
    print(f"Analisando arquivo: {arquivo_entrada}")
    inicio = time.time()
    
    # Lendo o arquivo CSV diretamente para um DataFrame
    print("Lendo arquivo CSV...")
    df = pd.read_csv(arquivo_entrada)
    print(f"Arquivo lido com sucesso. {len(df)} linhas encontradas.")
    
    # Verificar as colunas necessárias
    colunas_necessarias = ['Animal_1', 'Animal_2', 'Coef']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"A coluna {coluna} não está presente no arquivo CSV")
    
    # Filtrar cruzamentos inviáveis e coeficientes 1
    print("Filtrando cruzamentos inviáveis e valores extremos...")
    # Remover coeficientes -1 (valor de descarte)
    df = df[df['Coef'] != valor_descarte]
    # Remover coeficientes 1 (parentesco total)
    df = df[df['Coef'] != 1.0]
    
    # Obter a lista de todos os animais únicos em Animal_2 - precisamos garantir que todos estejam nos resultados
    todos_animal2 = df['Animal_2'].unique()
    print(f"Total de produtos/animais únicos em Animal_2: {len(todos_animal2)}")
    
    # Ordenar cruzamentos conforme método GRASPE
    print("Ordenando cruzamentos...")
    # Priorizamos coeficiente 0, depois usamos os coeficientes mais baixos
    # Não precisamos de coluna auxiliar, ordenamos diretamente pelo coeficiente
    df = df.sort_values(by=['Coef'], ascending=[True])
    
    # Isso garantirá que os coeficientes 0 venham primeiro, seguidos pelos próximos mais baixos em ordem crescente
    
    # Calcular distribuição ideal de cruzamentos
    todos_animal1 = df['Animal_1'].unique()
    total_animal1 = len(todos_animal1)
    total_animal2 = len(todos_animal2)
    
    # Definir o limite máximo de cruzamentos por Animal_1
    # Baseado na proporção Animal_2/Animal_1, arredondado para cima
    # Adicionamos um fator de segurança para garantir que todos os Animal_2 sejam incluídos
    import math
    fator_seguranca = 4  # Multiplicador para garantir que haja espaço suficiente
    max_cruzamentos_por_animal1 = math.ceil(total_animal2 / total_animal1 * fator_seguranca)
    print(f"Número máximo de cruzamentos por Animal_1: {max_cruzamentos_por_animal1}")
    
    # Remover duplicatas sem perder pares importantes
    print("Selecionando os melhores cruzamentos para cada Animal_2...")
    animal2_incluidos = set()  # Controla quais Animal_2 já foram incluídos
    contagem_animal1 = {}      # Contador de uso de cada Animal_1
    linhas_selecionadas = []   # Índices das linhas que serão mantidas
    
    # Primeiro passamos pelo dataframe ordenado para pegar os melhores cruzamentos para cada Animal_2
    for idx, row in df.iterrows():
        animal1 = row['Animal_1']
        animal2 = row['Animal_2']
        
        # Se este Animal_2 ainda não foi incluído
        if animal2 not in animal2_incluidos:
            # Verificamos se o Animal_1 já atingiu seu limite de cruzamentos
            contagem_atual = contagem_animal1.get(animal1, 0)
            
            if contagem_atual < max_cruzamentos_por_animal1:
                animal2_incluidos.add(animal2)
                contagem_animal1[animal1] = contagem_atual + 1
                linhas_selecionadas.append(idx)
                
                # Se já incluímos todos os Animal_2, podemos parar
                if len(animal2_incluidos) >= len(todos_animal2):
                    break
    
    # Se não conseguimos incluir todos os Animal_2, emitimos um aviso
    animal2_faltantes = set(todos_animal2) - animal2_incluidos
    if animal2_faltantes:
        print(f"AVISO: Não foi possível incluir {len(animal2_faltantes)} produtos Animal_2 nos cruzamentos.")
    
    # Agora adicionamos mais cruzamentos até atingir o limite, evitando duplicatas
    pares_vistos = set()
    for idx, row in df.iterrows():
        if len(linhas_selecionadas) >= limite_combinacoes:
            break
            
        # Verificamos se este cruzamento já não foi selecionado
        if idx not in linhas_selecionadas:
            animal1 = row['Animal_1']
            animal2 = row['Animal_2']
            par = tuple(sorted([animal1, animal2]))
            
            # Só adicionamos se não for o mesmo animal e se o par ainda não foi visto
            if animal1 != animal2 and par not in pares_vistos:
                pares_vistos.add(par)
                linhas_selecionadas.append(idx)
    
    # Manter apenas as linhas selecionadas e renomear a coluna de coeficiente
    df_resultado = df.loc[linhas_selecionadas].copy()
    df_resultado = df_resultado.rename(columns={'Coef': 'Coeficiente'})
    
    # Calcular estatísticas de uso dos Animal_1
    estatisticas_animal1 = {}
    for _, row in df_resultado.iterrows():
        animal1 = row['Animal_1']
        estatisticas_animal1[animal1] = estatisticas_animal1.get(animal1, 0) + 1
    
    # Adicionar estatísticas como metadados ao arquivo de resultados
    df_estatisticas = pd.DataFrame([
        {"tipo": "estatistica", "chave": "max_cruzamentos_por_animal1", "valor": max_cruzamentos_por_animal1},
        {"tipo": "estatistica", "chave": "total_animal1_utilizados", "valor": len(estatisticas_animal1)},
        {"tipo": "estatistica", "chave": "total_animal1_possiveis", "valor": total_animal1},
        {"tipo": "estatistica", "chave": "total_animal2_utilizados", "valor": len(animal2_incluidos)},
        {"tipo": "estatistica", "chave": "total_animal2_possiveis", "valor": total_animal2}
    ])
    
    # Salvar os resultados e estatísticas em arquivos CSV
    df_resultado.to_csv(arquivo_saida, index=False)
    df_estatisticas.to_csv(arquivo_saida.replace(".csv", "_estatisticas.csv"), index=False)
    
    fim = time.time()
    tempo_total = fim - inicio
    
    # Calcular estatísticas de distribuição
    utilizacao_animal1 = [count for animal, count in estatisticas_animal1.items()]
    media_utilizacao = sum(utilizacao_animal1) / len(utilizacao_animal1) if utilizacao_animal1 else 0
    
    print(f"\nEstatísticas de utilização de Animal_1:")
    print(f"- Animal_1 utilizados: {len(estatisticas_animal1)} de {total_animal1} ({len(estatisticas_animal1)/total_animal1*100:.1f}%)")
    print(f"- Média de cruzamentos por Animal_1: {media_utilizacao:.2f}")
    print(f"- Máximo de cruzamentos permitidos por Animal_1: {max_cruzamentos_por_animal1}")
    
    print(f"\nProcessamento concluído em {tempo_total:.2f} segundos.")
    print(f"Total de produtos Animal_2 incluídos: {len(animal2_incluidos)} de {len(todos_animal2)}")
    print(f"Resultados salvos em: {arquivo_saida}")
    
    # Mostrar os 10 primeiros resultados
    print("\n=== Melhores Cruzamentos (Top 10) ===")
    for i, (_, row) in enumerate(df_resultado.head(10).iterrows(), 1):
        print(f"{i}. {row['Animal_1']} × {row['Animal_2']} - Coeficiente: {row['Coeficiente']:.4f}")
    
    return df_resultado

if __name__ == "__main__":
    # Definir caminhos dos arquivos
    arquivo_entrada = "./uploads/parentesco_produtos (1).csv"
    arquivo_saida = "./melhores_cruzamentos.csv"
    
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo {arquivo_entrada} não foi encontrado.")
    else:
        # Analisar o arquivo e gerar os resultados - usando método otimizado
        df_melhores = analisar_parentesco_direto(arquivo_entrada, arquivo_saida, limite_combinacoes=100)