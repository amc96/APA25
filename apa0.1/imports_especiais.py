"""
Módulo para importação de formatos especiais de CSV em formato padrão.

Este módulo contém funções para detectar e converter formatos especiais de arquivo CSV,
como matrizes de adjacência e listas de arestas, para o formato padrão utilizado pelo sistema.
"""

import pandas as pd
import numpy as np
import csv
import io

def detectar_formato_csv(arquivo_path):
    """
    Detecta o formato do arquivo CSV e retorna informações sobre ele.
    
    Args:
        arquivo_path (str): Caminho para o arquivo CSV.
        
    Returns:
        dict: Dicionário com informações sobre o formato do arquivo.
    """
    try:
        # Detectar delimitador do arquivo
        with open(arquivo_path, 'r') as f:
            # Lê as primeiras linhas para detectar o delimitador
            sample = f.read(1024)
            dialect = csv.Sniffer().sniff(sample)
            delimitador = dialect.delimiter
        
        # Ler o arquivo com o delimitador detectado
        df = pd.read_csv(arquivo_path, sep=delimitador)
        
        # Verificar formato
        colunas = list(df.columns)
        
        # Verificar se é uma matriz de adjacência (primeira coluna é rótulo e restante são os mesmos valores da primeira coluna)
        if len(colunas) > 2 and colunas[0] not in ['Animal_1', 'origem', 'source'] and all(col not in ['Animal_2', 'destino', 'target', 'Coef', 'peso', 'weight'] for col in colunas[1:]):
            # Verificar se as colunas 1+ são iguais aos valores da primeira coluna em uma matriz de adjacência
            try:
                primeiros_valores = df[colunas[0]].tolist()
                if all(col in primeiros_valores for col in colunas[1:]):
                    return {
                        'formato': 'matriz_adjacencia',
                        'delimitador': delimitador,
                        'colunas': colunas,
                        'linhas': len(df)
                    }
            except:
                pass
        
        # Verificar se é uma lista de arestas
        if len(colunas) >= 3:
            # Tentar encontrar colunas de origem, destino e peso
            colunas_mapeamento = {
                'Animal_1': ['origem', 'source', 'from', 'animal1', 'animal_1'],
                'Animal_2': ['destino', 'target', 'to', 'animal2', 'animal_2'],
                'Coef': ['peso', 'weight', 'coeficiente', 'valor', 'value', 'coef']
            }
            
            mapeamento = {}
            for col_padrao, alternativas in colunas_mapeamento.items():
                for col in colunas:
                    if col.lower() in alternativas or col == col_padrao:
                        mapeamento[col_padrao] = col
                        break
            
            if len(mapeamento) >= 3:
                return {
                    'formato': 'lista_arestas',
                    'delimitador': delimitador,
                    'colunas': colunas,
                    'mapeamento': mapeamento,
                    'linhas': len(df)
                }
        
        # Formato padrão ou não reconhecido
        return {
            'formato': 'padrao' if all(col in df.columns for col in ['Animal_1', 'Animal_2', 'Coef']) else 'desconhecido',
            'delimitador': delimitador,
            'colunas': colunas,
            'linhas': len(df)
        }
    
    except Exception as e:
        return {
            'formato': 'erro',
            'mensagem': str(e)
        }

def converter_matriz_adjacencia(arquivo_path, info_formato):
    """
    Converte uma matriz de adjacência para o formato padrão.
    
    Args:
        arquivo_path (str): Caminho para o arquivo CSV.
        info_formato (dict): Informações sobre o formato do arquivo.
        
    Returns:
        pd.DataFrame: DataFrame no formato padrão (Animal_1, Animal_2, Coef).
    """
    # Ler a matriz de adjacência
    df = pd.read_csv(arquivo_path, sep=info_formato['delimitador'], index_col=0)
    
    # Criar lista de arestas a partir da matriz
    linhas = []
    
    # Iterar pelas linhas e colunas da matriz
    for idx in df.index:
        for col in df.columns:
            # Extrair o valor na célula
            valor = df.loc[idx, col]
            
            # Verificar se o valor é um número válido e maior que zero
            try:
                valor_float = float(valor)
                if not pd.isna(valor) and valor_float > 0:
                    linhas.append({
                        'Animal_1': idx,
                        'Animal_2': col,
                        'Coef': valor_float
                    })
            except (ValueError, TypeError):
                # Ignora valores que não podem ser convertidos para float
                continue
    
    # Criar DataFrame no formato padrão
    return pd.DataFrame(linhas)

def converter_lista_arestas(arquivo_path, info_formato):
    """
    Converte uma lista de arestas para o formato padrão.
    
    Args:
        arquivo_path (str): Caminho para o arquivo CSV.
        info_formato (dict): Informações sobre o formato do arquivo.
        
    Returns:
        pd.DataFrame: DataFrame no formato padrão (Animal_1, Animal_2, Coef).
    """
    # Ler a lista de arestas
    df = pd.read_csv(arquivo_path, sep=info_formato['delimitador'])
    
    # Mapear colunas para o formato padrão
    mapeamento = info_formato['mapeamento']
    
    # Criar um novo DataFrame com as colunas no formato padrão
    df_padrao = df[[mapeamento['Animal_1'], mapeamento['Animal_2'], mapeamento['Coef']]].copy()
    df_padrao.columns = ['Animal_1', 'Animal_2', 'Coef']
    
    return df_padrao

def processar_arquivo_csv(arquivo_path):
    """
    Processa um arquivo CSV e retorna um DataFrame no formato padrão.
    
    Args:
        arquivo_path (str): Caminho para o arquivo CSV.
        
    Returns:
        tuple: (DataFrame no formato padrão, informações sobre o formato detectado)
    """
    # Detectar formato
    info_formato = detectar_formato_csv(arquivo_path)
    
    # Converter com base no formato detectado
    if info_formato['formato'] == 'matriz_adjacencia':
        df = converter_matriz_adjacencia(arquivo_path, info_formato)
    elif info_formato['formato'] == 'lista_arestas':
        df = converter_lista_arestas(arquivo_path, info_formato)
    elif info_formato['formato'] == 'padrao':
        df = pd.read_csv(arquivo_path, sep=info_formato['delimitador'])
    else:
        # Tentar ler o arquivo normalmente se o formato não for reconhecido
        df = pd.read_csv(arquivo_path)
        
        # Verificar se as colunas necessárias existem
        required_columns = ['Animal_1', 'Animal_2', 'Coef']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Formato de arquivo não suportado. Colunas necessárias: {required_columns}")
    
    return df, info_formato