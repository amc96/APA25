"""
Implementação do método GRASPE para análise de cruzamentos.
Prioriza coeficientes 0 e avança em ordem crescente.
"""

def analisar_cruzamentos_graspe(matriz, limite_combinacoes=50, descartar_valor=-1):
    """
    Análise de cruzamentos usando método GRASPE.
    - Animal_1 pode cruzar múltiplas vezes
    - Animal_2 pode cruzar uma única vez
    - Todos os Animal_2 precisam ter um cruzamento
    - Prioriza coeficientes começando por 0 e avançando em ordem crescente
    
    Parâmetros:
    matriz (DataFrame): Matriz de coeficientes
    limite_combinacoes (int): Número máximo de combinações a retornar
    descartar_valor (float): Valor de coeficiente a ser descartado
    
    Retorno:
    list: Lista de dicionários com as melhores combinações
    """
    # Criar lista de todas as combinações válidas
    todas_combinacoes = []
    
    for animal1 in matriz.index:
        for animal2 in matriz.columns:
            coef = matriz.loc[animal1, animal2]
            # Filtrar valores descartados e valores 1.0 (parentesco total)
            if coef != descartar_valor and coef != 1.0:
                todas_combinacoes.append({
                    'Animal_1': animal1,
                    'Animal_2': animal2,
                    'Coeficiente': float(coef)
                })
    
    # Ordenar por coeficiente (prioriza 0, depois valores crescentes)
    todas_combinacoes.sort(key=lambda x: (
        0 if x['Coeficiente'] == 0 else 1,
        x['Coeficiente']
    ))
    
    # Conjunto para controlar Animal_2 já usados (cada Animal_2 só pode cruzar uma vez)
    animal2_usados = set()
    cruzamentos_selecionados = []
    
    # Contador de cruzamentos por Animal_1
    contador_animal1 = {}
    
    # Lista de todos os Animal_2 que precisam ter cruzamento
    todos_animal2 = list(matriz.columns)
    
    # Calcular número máximo de cruzamentos por Animal_1: (Animal_2/Animal_1)+1
    num_animal2 = len(matriz.columns)
    num_animal1 = len(matriz.index)
    max_cruzamentos_por_animal1 = int((num_animal2 / num_animal1) + 1)
    
    print(f"Máximo de cruzamentos por Animal_1: {max_cruzamentos_por_animal1}")
    
    # Garantir que todos os Animal_2 tenham um cruzamento
    for animal2 in todos_animal2:
        if animal2 not in animal2_usados:
            # Buscar o melhor cruzamento para este Animal_2
            melhor_opcao = None
            
            for comb in todas_combinacoes:
                if comb['Animal_2'] == animal2:
                    # Verificar se o Animal_1 ainda pode cruzar mais
                    animal1 = comb['Animal_1']
                    uso_atual = contador_animal1.get(animal1, 0)
                    
                    if uso_atual < max_cruzamentos_por_animal1:
                        melhor_opcao = comb
                        break
            
            if melhor_opcao:
                cruzamentos_selecionados.append(melhor_opcao)
                animal2_usados.add(melhor_opcao['Animal_2'])
                # Incrementar contador do Animal_1
                animal1 = melhor_opcao['Animal_1']
                contador_animal1[animal1] = contador_animal1.get(animal1, 0) + 1
    
    return cruzamentos_selecionados


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