import pandas as pd


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

        # Obter a lista de todos os animais únicos
        animais = sorted(
            set(df['Animal_1'].unique()) | set(df['Animal_2'].unique()))

        # Criar uma matriz vazia com todos os animais como índices e colunas
        # Usar float como tipo para evitar avisos de incompatibilidade de tipo
        matriz = pd.DataFrame(0.0, index=animais, columns=animais)

        # Preencher a matriz com os coeficientes
        if 'Coef' in df.columns:
            # Usar o valor do coeficiente no arquivo
            for _, row in df.iterrows():
                animal1 = row['Animal_1']
                animal2 = row['Animal_2']
                coef = float(row['Coef'])  # Converter para float
                matriz.loc[animal1, animal2] = coef
                matriz.loc[animal2, animal1] = coef  # A matriz é simétrica
        else:
            # Se não houver coluna Coef, usar valor 1 para preenchimento
            for _, row in df.iterrows():
                animal1 = row['Animal_1']
                animal2 = row['Animal_2']
                matriz.loc[animal1, animal2] = 1.0
                matriz.loc[animal2, animal1] = 1.0  # A matriz é simétrica

        # Preencher a diagonal principal com 1 (um animal tem 100% de relação consigo mesmo)
        for animal in animais:
            matriz.loc[animal, animal] = 1.0

        # Adicionar contagem de Animal_1 e Animal_2 como atributos da matriz
        matriz.attrs['contagem_animal_1'] = len(df['Animal_1'].unique())
        matriz.attrs['contagem_animal_2'] = len(df['Animal_2'].unique())
        matriz.attrs['total_animais'] = len(animais)

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

    # Você pode adicionar mais estatísticas conforme necessário
    # Por exemplo, média, desvio padrão, etc.

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
        contagem = {"Animal_1": {}, "Animal_2": {}}

        # Total de animais distintos
        contagem["Animal_1"]["Total de animais distintos"] = len(
            df["Animal_1"].unique())
        contagem["Animal_2"]["Total de animais distintos"] = len(
            df["Animal_2"].unique())

        # Lista de animais únicos em cada coluna (para referência)
        contagem["Animal_1"]["Lista de animais"] = sorted(
            df["Animal_1"].unique().tolist())
        contagem["Animal_2"]["Lista de animais"] = sorted(
            df["Animal_2"].unique().tolist())

        return contagem

    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo_csv} não foi encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None


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
        except Exception as e:
            print(f"Erro: {e}")
    else:
        print("Uso: python csv_to_matrix.py [caminho_para_arquivo_csv]")
