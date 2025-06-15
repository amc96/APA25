"""
Script simples para extrair vetores Animal_1 e Animal_2 do arquivo CSV.
"""

import pandas as pd
import sys

def extrair_vetores(arquivo_csv):
    """
    Extrai vetores Animal_1 e Animal_2 do arquivo CSV.
    
    Args:
        arquivo_csv: Caminho para o arquivo CSV
    """
    try:
        # Carregar o arquivo CSV
        print(f"Carregando arquivo: {arquivo_csv}")
        df = pd.read_csv(arquivo_csv)
        
        # Extrair vetores únicos
        animal1 = df['Animal_1'].unique().tolist()
        animal2 = df['Animal_2'].unique().tolist()
        
        # Salvar vetores em arquivos separados
        pd.DataFrame(animal1, columns=['Animal_1']).to_csv('vetor_animal1.csv', index=False)
        pd.DataFrame(animal2, columns=['Animal_2']).to_csv('vetor_animal2.csv', index=False)
        
        # Exibir informações
        print(f"Vetores extraídos com sucesso:")
        print(f"- Animal_1: {len(animal1)} valores únicos")
        print(f"- Animal_2: {len(animal2)} valores únicos")
        print(f"Arquivos salvos: vetor_animal1.csv, vetor_animal2.csv")
        
        # Exibir amostras
        print("\nPrimeiros 5 valores de Animal_1:")
        for i, val in enumerate(animal1[:5]):
            print(f"  {i+1}. {val}")
            
        print("\nPrimeiros 5 valores de Animal_2:")
        for i, val in enumerate(animal2[:5]):
            print(f"  {i+1}. {val}")
        
        return animal1, animal2
        
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        return None, None

# Execução principal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extrair_vetores_simples.py <arquivo_csv>")
        sys.exit(1)
        
    arquivo_csv = sys.argv[1]
    extrair_vetores(arquivo_csv)