"""
Módulo para conversão de CSV de relações entre animais em uma matriz.

Este módulo converte dados de relacionamento entre animais de um arquivo CSV 
em uma matriz onde as linhas e colunas são os animais.
"""

import pandas as pd
import numpy as np
import sys
import os

def csv_to_matrix(csv_path: str, output_path: str = "matriz_final.csv") -> pd.DataFrame:
    """
    Converte um arquivo CSV de relacionamentos em uma matriz.
    
    Args:
        csv_path (str): Caminho para o arquivo CSV.
        output_path (str): Caminho para salvar a matriz resultante.
        
    Returns:
        pd.DataFrame: DataFrame contendo a matriz de coeficientes.
    """
    try:
        # Carregar o arquivo CSV
        print(f"Carregando arquivo: {csv_path}")
        df = pd.read_csv(csv_path)
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
        print(f"Salvando matriz em: {output_path}")
        matriz.to_csv(output_path)
        
        return matriz
    
    except Exception as e:
        print(f"Erro ao processar: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def get_matrix_statistics(matrix: pd.DataFrame) -> dict:
    """
    Calcula estatísticas básicas sobre a matriz.
    
    Args:
        matrix (pd.DataFrame): Matriz de coeficientes.
        
    Returns:
        dict: Dicionário com várias estatísticas da matriz.
    """
    try:
        # Obter dimensões
        total_animais = matrix.shape[0]
        
        # Analisar a matriz
        valores = matrix.values
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
        
        stats = {
            "dimensoes": f"{total_animais}x{total_animais}",
            "total_celulas": int(total_animais * total_animais),
            "valores_zero": int(valores_zeros),
            "valores_nao_zero": int(valores_nao_zeros),
            "densidade": float(f"{densidade:.2f}"),
        }
        
        if len(valores_parentesco) > 0:
            print("\nEstatísticas dos coeficientes de parentesco (excluindo diagonal):")
            print(f"- Total: {len(valores_parentesco)}")
            print(f"- Mínimo: {np.min(valores_parentesco)}")
            print(f"- Máximo: {np.max(valores_parentesco)}")
            print(f"- Média: {np.mean(valores_parentesco):.4f}")
            
            stats["estatisticas_parentesco"] = {
                "total": int(len(valores_parentesco)),
                "minimo": float(np.min(valores_parentesco)),
                "maximo": float(np.max(valores_parentesco)),
                "media": float(f"{np.mean(valores_parentesco):.4f}")
            }
            
            # Distribuição dos valores
            faixas = [
                (0, 0.1, "0-0.1"),
                (0.1, 0.2, "0.1-0.2"),
                (0.2, 0.3, "0.2-0.3"),
                (0.3, 0.4, "0.3-0.4"),
                (0.4, 1.0, "0.4-1.0")
            ]
            
            distribuicao = {}
            print("\nDistribuição dos coeficientes de parentesco:")
            for min_val, max_val, label in faixas:
                count = np.sum((valores_parentesco > min_val) & (valores_parentesco <= max_val))
                if count > 0:
                    percentual = (count / len(valores_parentesco)) * 100
                    print(f"- {label}: {count} ({percentual:.2f}%)")
                    distribuicao[label] = {
                        "contagem": int(count),
                        "percentual": float(f"{percentual:.2f}")
                    }
            
            stats["distribuicao"] = distribuicao
        
        return stats
        
    except Exception as e:
        print(f"Erro ao calcular estatísticas: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}

def extract_vectors(csv_path: str, vector1_path: str = "vetor_animal1.csv", 
                   vector2_path: str = "vetor_animal2.csv") -> tuple:
    """
    Extrai vetores Animal_1 e Animal_2 do arquivo CSV.
    
    Args:
        csv_path (str): Caminho para o arquivo CSV
        vector1_path (str): Caminho para salvar o vetor Animal_1
        vector2_path (str): Caminho para salvar o vetor Animal_2
        
    Returns:
        tuple: Tupla contendo os dois vetores (animal1, animal2)
    """
    try:
        # Carregar o arquivo CSV
        print(f"Carregando arquivo: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Extrair vetores únicos
        animal1 = df['Animal_1'].unique().tolist()
        animal2 = df['Animal_2'].unique().tolist()
        
        # Salvar vetores em arquivos separados
        pd.DataFrame(animal1, columns=['Animal_1']).to_csv(vector1_path, index=False)
        pd.DataFrame(animal2, columns=['Animal_2']).to_csv(vector2_path, index=False)
        
        # Exibir informações
        print(f"Vetores extraídos com sucesso:")
        print(f"- Animal_1: {len(animal1)} valores únicos")
        print(f"- Animal_2: {len(animal2)} valores únicos")
        print(f"Arquivos salvos: {vector1_path}, {vector2_path}")
        
        return animal1, animal2
        
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        return None, None

def remove_duplicates(vector1_path: str = "vetor_animal1.csv", 
                     vector2_path: str = "vetor_animal2.csv",
                     output_path: str = "vetor_animal2_sem_duplicados.csv") -> list:
    """
    Remove duplicidades entre os vetores Animal_1 e Animal_2.
    
    Args:
        vector1_path (str): Caminho para o arquivo do vetor Animal_1
        vector2_path (str): Caminho para o arquivo do vetor Animal_2
        output_path (str): Caminho para salvar o novo vetor Animal_2 sem duplicados
        
    Returns:
        list: Lista de animais únicos no vetor Animal_2
    """
    try:
        # Carregar os vetores
        print("Carregando vetores existentes...")
        df_animal1 = pd.read_csv(vector1_path)
        df_animal2 = pd.read_csv(vector2_path)
        
        # Obter listas de animais
        animal1 = df_animal1['Animal_1'].tolist()
        animal2 = df_animal2['Animal_2'].tolist()
        
        print(f"Vetor Animal_1: {len(animal1)} animais")
        print(f"Vetor Animal_2: {len(animal2)} animais")
        
        # Encontrar animais duplicados (presentes em ambos vetores)
        set_animal1 = set(animal1)
        set_animal2 = set(animal2)
        
        duplicados = set_animal1.intersection(set_animal2)
        unicos_animal2 = set_animal2 - set_animal1
        
        print(f"\nAnálise de duplicidade:")
        print(f"- Animais presentes em ambos vetores: {len(duplicados)}")
        print(f"- Animais exclusivos do vetor Animal_2: {len(unicos_animal2)}")
        
        # Se houver duplicados, removê-los do vetor_animal2
        if duplicados:
            print(f"\nRemovendo {len(duplicados)} animais duplicados do vetor Animal_2...")
            
            # Criar novo vetor Animal_2 sem os duplicados
            animal2_sem_duplicados = sorted(list(unicos_animal2))
            
            # Salvar o novo vetor Animal_2
            df_animal2_novo = pd.DataFrame(animal2_sem_duplicados, columns=['Animal_2'])
            df_animal2_novo.to_csv(output_path, index=False)
            
            print(f"Novo vetor Animal_2 criado: {len(animal2_sem_duplicados)} animais")
            print(f"Salvo em: {output_path}")
            
            return animal2_sem_duplicados
        else:
            print("\nNão foram encontrados animais duplicados entre os vetores.")
            return animal2
        
    except Exception as e:
        print(f"Erro ao processar vetores: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  Para criar matriz: python csv_to_matrix.py matriz <arquivo_csv> [arquivo_saida]")
        print("  Para extrair vetores: python csv_to_matrix.py vetores <arquivo_csv>")
        print("  Para remover duplicados: python csv_to_matrix.py limpar")
        sys.exit(1)
    
    comando = sys.argv[1].lower()
    
    if comando == "matriz":
        if len(sys.argv) < 3:
            print("Erro: Forneça o caminho para o arquivo CSV")
            sys.exit(1)
            
        arquivo_csv = sys.argv[2]
        arquivo_saida = sys.argv[3] if len(sys.argv) > 3 else "matriz_final.csv"
        
        matriz = csv_to_matrix(arquivo_csv, arquivo_saida)
        if matriz is not None:
            get_matrix_statistics(matriz)
            
    elif comando == "vetores":
        if len(sys.argv) < 3:
            print("Erro: Forneça o caminho para o arquivo CSV")
            sys.exit(1)
            
        arquivo_csv = sys.argv[2]
        extract_vectors(arquivo_csv)
        
    elif comando == "limpar":
        remove_duplicates()
        
    else:
        print(f"Comando desconhecido: {comando}")
        print("Comandos válidos: matriz, vetores, limpar")
        sys.exit(1)