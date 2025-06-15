"""
Script para criar uma matriz a partir dos vetores de Animal_1 e Animal_2.
"""

import pandas as pd
import numpy as np
import sys

def criar_matriz_com_vetores(arquivo_csv, arquivo_saida='matriz_parentesco.csv'):
    """
    Cria uma matriz de parentesco usando os vetores únicos de Animal_1 e Animal_2.
    
    Args:
        arquivo_csv: Caminho para o arquivo CSV original
        arquivo_saida: Caminho para salvar a matriz resultante
    """
    try:
        # Carregar o arquivo CSV original
        print(f"Carregando arquivo: {arquivo_csv}")
        df = pd.read_csv(arquivo_csv)
        print(f"Arquivo carregado: {len(df)} linhas")
        
        # Obter todos os animais únicos (combinando Animal_1 e Animal_2)
        animais = sorted(list(set(df['Animal_1']).union(set(df['Animal_2']))))
        total_animais = len(animais)
        print(f"Total de animais únicos: {total_animais}")
        
        # Criar matriz vazia preenchida com zeros
        print(f"Criando matriz {total_animais}x{total_animais}...")
        matriz = pd.DataFrame(0.0, index=animais, columns=animais)
        
        # Diagonal principal = 1.0 (parentesco do animal consigo mesmo)
        for animal in animais:
            matriz.loc[animal, animal] = 1.0
        
        # Preencher valores de parentesco do CSV
        print("Preenchendo matriz com valores de parentesco...")
        contador = 0
        for _, row in df.iterrows():
            animal1 = row['Animal_1']
            animal2 = row['Animal_2']
            coef = row['Coef']
            
            # Verificar se ambos os animais estão na lista
            if animal1 in animais and animal2 in animais:
                # Preencher em ambas as direções para manter simetria
                matriz.loc[animal1, animal2] = coef
                matriz.loc[animal2, animal1] = coef
                contador += 1
                
                # Mostrar progresso
                if contador % 10000 == 0:
                    print(f"  Processadas {contador} relações...")
        
        print(f"Total de relações processadas: {contador}")
        
        # Salvar a matriz
        print(f"Salvando matriz em: {arquivo_saida}")
        matriz.to_csv(arquivo_saida)
        
        # Analisar a matriz
        valores = matriz.values
        valores_nao_zeros = np.sum(valores > 0)
        valores_zeros = np.sum(valores == 0)
        densidade = (valores_nao_zeros / (total_animais * total_animais)) * 100
        
        print("\nEstatísticas da matriz:")
        print(f"- Dimensões: {total_animais}x{total_animais}")
        print(f"- Total de células: {total_animais * total_animais}")
        print(f"- Células com valor zero: {valores_zeros}")
        print(f"- Células com valor não-zero: {valores_nao_zeros}")
        print(f"- Densidade: {densidade:.2f}%")
        
        # Valores não-zero e não-diagonais
        valores_nao_diag = valores[~np.eye(total_animais, dtype=bool)]
        valores_parentesco = valores_nao_diag[valores_nao_diag > 0]
        
        if len(valores_parentesco) > 0:
            print("\nEstatísticas dos coeficientes de parentesco (excluindo diagonal):")
            print(f"- Total: {len(valores_parentesco)}")
            print(f"- Mínimo: {np.min(valores_parentesco)}")
            print(f"- Máximo: {np.max(valores_parentesco)}")
            print(f"- Média: {np.mean(valores_parentesco):.4f}")
            
            # Distribuição dos valores
            faixas = [
                (0, 0.1, "0-0.1"),
                (0.1, 0.2, "0.1-0.2"),
                (0.2, 0.3, "0.2-0.3"),
                (0.3, 0.4, "0.3-0.4"),
                (0.4, 1.0, "0.4-1.0")
            ]
            
            print("\nDistribuição dos coeficientes de parentesco:")
            for min_val, max_val, label in faixas:
                count = np.sum((valores_parentesco > min_val) & (valores_parentesco <= max_val))
                if count > 0:
                    percentual = (count / len(valores_parentesco)) * 100
                    print(f"- {label}: {count} ({percentual:.2f}%)")
        
        return matriz
        
    except Exception as e:
        print(f"Erro ao processar: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python criar_matriz_com_vetores.py <arquivo_csv> [arquivo_saida]")
        sys.exit(1)
        
    arquivo_csv = sys.argv[1]
    arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else 'matriz_parentesco.csv'
    
    matriz = criar_matriz_com_vetores(arquivo_csv, arquivo_saida)