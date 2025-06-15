"""
Módulo para conversão de CSV de relações entre animais em uma matriz.

Este módulo converte dados de relacionamento entre animais de um arquivo CSV 
em uma matriz onde as linhas são Animal_2 e as colunas são Animal_1.
"""

import pandas as pd
import numpy as np


def csv_to_matrix(csv_path: str) -> pd.DataFrame:
    """
    Converte um arquivo CSV de relacionamentos em uma matriz.
    
    Args:
        csv_path (str): Caminho para o arquivo CSV.
        
    Returns:
        pd.DataFrame: DataFrame contendo a matriz de coeficientes.
    """
    # Carrega o arquivo CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Erro ao carregar o arquivo CSV: {str(e)}")
    
    # Verifica se o DataFrame tem as colunas necessárias
    required_columns = ['Animal_1', 'Animal_2', 'Coef']
    if not all(col in df.columns for col in required_columns):
        missing = [col for col in required_columns if col not in df.columns]
        raise ValueError(f"O arquivo CSV deve conter as colunas: {required_columns}. Faltando: {missing}")
    
    # Cria a matriz utilizando o pivot_table
    # Animal_1 nas colunas, Animal_2 nas linhas e os valores são os coeficientes
    matrix = df.pivot_table(index='Animal_2', columns='Animal_1', values='Coef', fill_value=-1)
    
    return matrix


def filter_matrix_by_coefficient(matrix: pd.DataFrame, min_coef: float = 0.0) -> pd.DataFrame:
    """
    Filtra a matriz para conter apenas coeficientes acima de um valor mínimo.
    
    Args:
        matrix (pd.DataFrame): Matriz de coeficientes.
        min_coef (float, optional): Valor mínimo do coeficiente. Padrão é 0.0.
        
    Returns:
        pd.DataFrame: Matriz filtrada.
    """
    # Cria uma cópia para não modificar a original
    filtered = matrix.copy()
    
    # Substitui todos os valores abaixo do mínimo por 0
    filtered[filtered < min_coef] = 0
    
    return filtered


def get_matrix_statistics(matrix: pd.DataFrame) -> dict:
    """
    Calcula estatísticas básicas sobre a matriz.
    
    Args:
        matrix (pd.DataFrame): Matriz de coeficientes.
        
    Returns:
        dict: Dicionário com várias estatísticas da matriz.
    """
    # Remove zeros para calcular estatísticas apenas de coeficientes reais
    non_zero = matrix.values[matrix.values > 0]
    
    if len(non_zero) == 0:
        return {
            'rows': matrix.shape[0],
            'columns': matrix.shape[1],
            'non_zero_values': 0,
            'avg_coefficient': 0,
            'max_coefficient': 0,
            'min_coefficient': 0
        }
    
    return {
        'rows': matrix.shape[0],
        'columns': matrix.shape[1],
        'non_zero_values': len(non_zero),
        'avg_coefficient': float(np.mean(non_zero)),
        'max_coefficient': float(np.max(non_zero)),
        'min_coefficient': float(np.min(non_zero))
    }


def export_matrix_to_csv(matrix: pd.DataFrame, output_path: str) -> None:
    """
    Exporta a matriz para um arquivo CSV.
    
    Args:
        matrix (pd.DataFrame): Matriz de coeficientes.
        output_path (str): Caminho para salvar o arquivo CSV.
    """
    matrix.to_csv(output_path)


if __name__ == "__main__":
    # Exemplo de uso do módulo
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python csv_to_matrix.py <caminho_do_arquivo.csv> [caminho_de_saida.csv]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "matriz_resultado.csv"
    
    try:
        print(f"Convertendo {input_file} em matriz...")
        matriz = csv_to_matrix(input_file)
        
        # Imprime informações básicas
        stats = get_matrix_statistics(matriz)
        print(f"Matriz criada com {stats['rows']} linhas e {stats['columns']} colunas")
        print(f"Valores não-zero: {stats['non_zero_values']}")
        print(f"Coeficiente médio: {stats['avg_coefficient']:.4f}")
        
        # Exporta a matriz
        export_matrix_to_csv(matriz, output_file)
        print(f"Matriz exportada para {output_file}")
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)