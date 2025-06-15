import pandas as pd
import numpy as np


def csv_to_matrix(arquivo_csv):
    """
    Função para converter um arquivo CSV em uma matriz.
    O CSV deve conter colunas Animal_1, Animal_2 e Coef.
    Cria uma matriz onde as linhas e colunas são os animais e 
    os valores são os coeficientes.
    
    Parâmetros:
    arquivo_csv (str): Caminho para o arquivo CSV
    
    Retorno:
    DataFrame: Matriz convertida do CSV
    """
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(arquivo_csv)

        # Verificar se as colunas necessárias existem
        colunas_necessarias = ['Animal_1', 'Animal_2']
        if 'Coef' in df.columns:
            colunas_necessarias.append('Coef')

        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise ValueError(
                    f"A coluna {coluna} não está presente no arquivo CSV")

        # Obter listas separadas de Animal_1 e Animal_2
        animais_1 = sorted(df['Animal_1'].unique())  # Linhas
        animais_2 = sorted(df['Animal_2'].unique())  # Colunas

        # Criar uma matriz com Animal_1 nas linhas e Animal_2 nas colunas
        # Usar float como tipo para evitar avisos de incompatibilidade de tipo
        matriz = pd.DataFrame(0.0, index=animais_1, columns=animais_2)

        # Preencher a matriz com os coeficientes
        if 'Coef' in df.columns:
            # Usar o valor do coeficiente no arquivo
            for _, row in df.iterrows():
                animal1 = row['Animal_1']
                animal2 = row['Animal_2']
                coef = float(row['Coef'])  # Converter para float
                matriz.loc[animal1, animal2] = coef
        else:
            # Se não houver coluna Coef, usar valor 1 para preenchimento
            for _, row in df.iterrows():
                animal1 = row['Animal_1']
                animal2 = row['Animal_2']
                matriz.loc[animal1, animal2] = 1.0

        # Adicionar contagem de Animal_1 e Animal_2 como atributos da matriz
        # Usar dicionário para armazenar atributos, pois DataFrame não possui attrs em algumas versões
        if not hasattr(matriz, 'attrs'):
            matriz.attrs = {}
        matriz.attrs['contagem_animal_1'] = len(animais_1)
        matriz.attrs['contagem_animal_2'] = len(animais_2)
        matriz.attrs['total_animais'] = len(animais_1) + len(animais_2)

        return matriz

    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo_csv} não foi encontrado.")
        raise
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        raise


def get_matrix_statistics(matriz):
    """
    Função para obter estatísticas da matriz
    
    Parâmetros:
    matriz (DataFrame): Matriz de dados
    
    Retorno:
    dict: Dicionário com estatísticas da matriz
    """
    estatisticas = {
        'linhas': matriz.shape[0],
        'colunas': matriz.shape[1],
    }

    # Adicionar contagem de Animal_1 e Animal_2 às estatísticas
    if hasattr(matriz, 'attrs') and 'contagem_animal_1' in matriz.attrs:
        estatisticas['contagem_animal_1'] = matriz.attrs['contagem_animal_1']

    if hasattr(matriz, 'attrs') and 'contagem_animal_2' in matriz.attrs:
        estatisticas['contagem_animal_2'] = matriz.attrs['contagem_animal_2']

    # Adicionar estatísticas adicionais
    # Valores não zero (excluindo a diagonal)
    non_zero = 0
    valores_soma = 0
    valores_min = float('inf')
    valores_max = 0
    
    for i in matriz.index:
        for j in matriz.columns:
            if i != j and matriz.loc[i, j] > 0:  # Exclui diagonal e zeros
                non_zero += 1
                valores_soma += matriz.loc[i, j]
                valores_min = min(valores_min, matriz.loc[i, j])
                valores_max = max(valores_max, matriz.loc[i, j])
    
    estatisticas['non_zero_values'] = non_zero
    if non_zero > 0:
        estatisticas['avg_coefficient'] = valores_soma / non_zero
        estatisticas['min_coefficient'] = valores_min if valores_min != float('inf') else 0
        estatisticas['max_coefficient'] = valores_max

    return estatisticas


def contagem_animais(arquivo_csv):
    """
    Função para ler um arquivo CSV e contar quantos animais distintos existem 
    nas colunas Animal_1 e Animal_2
    
    Parâmetros:
    arquivo_csv (str): Caminho para o arquivo CSV
    
    Retorno:
    dict: Dicionário com a contagem de animais distintos em Animal_1 e Animal_2
    """
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(arquivo_csv)

        # Verificar se as colunas necessárias existem
        colunas_necessarias = ["Animal_1", "Animal_2"]
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                print(f"Erro: A coluna {coluna} não existe no arquivo CSV.")
                return None

        # Contagem de animais únicos em cada coluna
        contagem = {
            "Animal_1": {
                "Total de animais distintos": len(df["Animal_1"].unique())
            },
            "Animal_2": {
                "Total de animais distintos": len(df["Animal_2"].unique())
            }
        }

        # Lista de animais únicos em cada coluna (para referência)
        contagem["Animal_1"]["Animais únicos"] = len(df["Animal_1"].unique())
        contagem["Animal_2"]["Animais únicos"] = len(df["Animal_2"].unique())

        return contagem

    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo_csv} não foi encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None


# Importamos as funções GRASPE do módulo dedicado
from graspe import analisar_cruzamentos_graspe, ordenar_cruzamentos_por_coeficiente, filtrar_cruzamentos_inviaveis


# Exemplo de uso se executado diretamente
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        arquivo_csv = sys.argv[1]
        try:
            matriz = csv_to_matrix(arquivo_csv)
            estatisticas = get_matrix_statistics(matriz)

            print("\n=== Estatísticas da Matriz ===")
            for chave, valor in estatisticas.items():
                if chave == 'contagem_animal_1':
                    print("\nContagem de Animal_1:")
                    for animal, qtd in valor.items():
                        print(f"  {animal}: {qtd}")
                elif chave == 'contagem_animal_2':
                    print("\nContagem de Animal_2:")
                    for animal, qtd in valor.items():
                        print(f"  {animal}: {qtd}")
                else:
                    print(f"{chave}: {valor}")
                    
            # Analisar os melhores cruzamentos
            melhores_cruzamentos = analisar_cruzamentos_graspe(matriz)
            
            print("\n=== Melhores Combinações de Cruzamento (Método GRASPE) ===")
            print(f"Combinações ordenadas priorizando coeficiente 0, depois valores crescentes")
            for i, comb in enumerate(melhores_cruzamentos, 1):
                print(f"{i}. {comb['Animal_1']} x {comb['Animal_2']} - Coeficiente: {comb['Coeficiente']:.4f}")
            
        except Exception as e:
            print(f"Erro: {e}")
    else:
        print("Uso: python csv_to_matrix.py [caminho_para_arquivo_csv]")
