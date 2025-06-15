"""
Implementação do método GRASPE para análise de cruzamentos.
Prioriza coeficientes 0 e avança em ordem crescente.
"""

def analisar_cruzamentos_graspe(matriz, limite_combinacoes=50, descartar_valor=-1):
    """
    Análise de cruzamentos usando método GRASPE.
    - Descarta combinações com coeficiente igual ao valor descartado (-1 por padrão)
    - Prioriza coeficientes começando por 0 e avançando em ordem crescente
    - Apresenta as melhores combinações
    
    Parâmetros:
    matriz (DataFrame): Matriz de coeficientes
    limite_combinacoes (int): Número máximo de combinações a retornar
    descartar_valor (float): Valor de coeficiente a ser descartado
    
    Retorno:
    list: Lista de dicionários com as melhores combinações
    """
    # Cria uma lista para armazenar todas as combinações de animais
    combinacoes = []
    
    # Busca todas as combinações possíveis na matriz (exceto a diagonal)
    for animal1 in matriz.index:
        for animal2 in matriz.columns:
            # Ignora a diagonal (mesmo animal) e valores a serem descartados
            if animal1 != animal2 and matriz.loc[animal1, animal2] != descartar_valor:
                combinacoes.append({
                    'Animal_1': animal1,
                    'Animal_2': animal2,
                    'Coeficiente': float(matriz.loc[animal1, animal2])
                })
    
    # Ordena as combinações começando por 0 e avançando em ordem crescente
    # Para isso, usamos um critério de ordenação que coloca 0 primeiro, depois valores positivos crescentes
    combinacoes_ordenadas = sorted(combinacoes, key=lambda x: (
        0 if x['Coeficiente'] == 0 else 1,  # Prioriza 0
        abs(x['Coeficiente'])               # Depois valores crescentes
    ))
    
    # Remove duplicatas (considerando as combinações simétricas)
    combinacoes_unicas = []
    pares_vistos = set()
    
    for comb in combinacoes_ordenadas:
        # Ordena os animais para evitar duplicatas como (A,B) e (B,A)
        par = tuple(sorted([comb['Animal_1'], comb['Animal_2']]))
        if par not in pares_vistos:
            combinacoes_unicas.append(comb)
            pares_vistos.add(par)
    
    # Retorna as melhores combinações (limitadas pelo parâmetro)
    return combinacoes_unicas[:limite_combinacoes]


def ordenar_cruzamentos_por_coeficiente(cruzamentos):
    """
    Ordena uma lista de cruzamentos segundo o método GRASPE.
    
    Parâmetros:
    cruzamentos (list): Lista de dicionários com pares de animais e seus coeficientes
    
    Retorno:
    list: Lista ordenada de acordo com o método GRASPE
    """
    return sorted(cruzamentos, key=lambda x: (
        0 if x['Coeficiente'] == 0 else 1,  # Prioriza 0
        abs(x['Coeficiente'])               # Depois valores crescentes
    ))


def filtrar_cruzamentos_inviaveis(cruzamentos, valor_descarte=-1):
    """
    Filtra cruzamentos inviáveis da lista (com coeficiente igual ao valor de descarte).
    
    Parâmetros:
    cruzamentos (list): Lista de dicionários com pares de animais e seus coeficientes
    valor_descarte (float): Valor de coeficiente a ser descartado
    
    Retorno:
    list: Lista filtrada sem os cruzamentos inviáveis
    """
    return [comb for comb in cruzamentos if comb['Coeficiente'] != valor_descarte]


# Exemplo de uso se executado diretamente
if __name__ == "__main__":
    import pandas as pd
    
    # Exemplo de matriz
    data = {
        'Touro1': {'Vaca1': 0.0, 'Vaca2': 0.125, 'Vaca3': 0.25, 'Vaca4': 0.5},
        'Touro2': {'Vaca1': 0.0, 'Vaca2': 0.25, 'Vaca3': 0.375, 'Vaca4': 0.0}
    }
    
    matriz = pd.DataFrame(data)
    
    # Analisar cruzamentos
    melhores = analisar_cruzamentos_graspe(matriz, limite_combinacoes=5)
    
    # Imprimir resultados
    print("Melhores cruzamentos segundo método GRASPE:")
    for i, comb in enumerate(melhores, 1):
        print(f"{i}. {comb['Animal_1']} × {comb['Animal_2']} - Coeficiente: {comb['Coeficiente']:.4f}")