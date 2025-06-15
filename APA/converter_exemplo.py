"""
Exemplo de uso do módulo csv_to_matrix para converter arquivo CSV em matriz.
"""

import pandas as pd
import matplotlib.pyplot as plt
from csv_to_matrix import csv_to_matrix, get_matrix_statistics, filter_matrix_by_coefficient

# Caminho do arquivo CSV - usando o arquivo enviado
arquivo_csv = "parentesco_produtos.csv"

# Converte o CSV em matriz
print("Convertendo CSV em matriz...")
matriz = csv_to_matrix(arquivo_csv)

# Exibe estatísticas da matriz
stats = get_matrix_statistics(matriz)
print(f"\nEstatísticas da matriz:")
print(f"Dimensões: {stats['rows']} linhas x {stats['columns']} colunas")
print(f"Valores não-zero: {stats['non_zero_values']}")
print(f"Coeficiente médio: {stats['avg_coefficient']:.4f}")
print(f"Coeficiente máximo: {stats['max_coefficient']:.4f}")
print(f"Coeficiente mínimo: {stats['min_coefficient']:.4f}")

# Exibe os primeiros 5x5 elementos da matriz
print("\nAmostra da matriz (5x5 primeiros elementos):")
print(matriz.iloc[:5, :5])

# Filtra a matriz para mostrar apenas coeficientes acima de 0.2
matriz_filtrada = filter_matrix_by_coefficient(matriz, min_coef=0.2)
valores_nao_zero = (matriz_filtrada > 0).sum().sum()
print(f"\nMatriz filtrada (coef >= 0.2) tem {valores_nao_zero} valores não-zero")

# Salva a matriz em um arquivo CSV
arquivo_saida = "matriz_resultado.csv"
matriz.to_csv(arquivo_saida)
print(f"\nMatriz salva em: {arquivo_saida}")

# Opcional: Cria uma visualização da matriz (apenas para uma amostra pequena)
if min(matriz.shape) <= 50:  # Apenas se a matriz for pequena
    # Cria uma amostra da matriz para visualização
    plt.figure(figsize=(10, 8))
    plt.imshow(matriz.values, cmap='viridis')
    plt.colorbar(label='Coeficiente')
    plt.title('Matriz de Coeficientes de Relacionamento entre Animais')
    plt.tight_layout()
    plt.savefig('matriz_visualizacao.png')
    print("Visualização da matriz salva em: matriz_visualizacao.png")
else:
    # Se a matriz for grande, cria uma amostra
    amostra_linhas = min(30, matriz.shape[0])
    amostra_colunas = min(30, matriz.shape[1])
    amostra = matriz.iloc[:amostra_linhas, :amostra_colunas]
    
    plt.figure(figsize=(12, 10))
    plt.imshow(amostra.values, cmap='viridis')
    plt.colorbar(label='Coeficiente')
    plt.title(f'Amostra da Matriz de Coeficientes ({amostra_linhas}x{amostra_colunas})')
    plt.tight_layout()
    plt.savefig('matriz_amostra_visualizacao.png')
    print("Visualização da amostra da matriz salva em: matriz_amostra_visualizacao.png")