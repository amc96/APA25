
import random
import json

def f_objetivo(solucao):
    """Função objetivo: minimizar a soma dos coeficientes"""
    return sum(pair['Coeficiente'] for pair in solucao)

def calcular_media_cruzamentos(solucao):
    """Calcula a média dos coeficientes dos melhores cruzamentos"""
    if not solucao:
        return 0.0
    
    soma_coeficientes = sum(pair['Coeficiente'] for pair in solucao)
    return soma_coeficientes / len(solucao)

def construir_solucao_rcl(matriz, tamanho_rcl=3, descartar_valor=-1):
    """Constrói uma solução usando Restricted Candidate List (RCL)"""
    todas_combinacoes = []

    for animal1 in matriz.index:
        for animal2 in matriz.columns:
            coef = matriz.loc[animal1, animal2]
            if coef != descartar_valor and coef != 1.0:
                todas_combinacoes.append({
                    'Animal_1': animal1,
                    'Animal_2': animal2,
                    'Coeficiente': float(coef)
                })

    # Ordenar por coeficiente (menor primeiro = melhor)
    todas_combinacoes.sort(key=lambda x: x['Coeficiente'])

    cruzamentos = []
    usados_2 = set()
    contador_1 = {}
    max_cruz = int(len(matriz.columns) / len(matriz.index)) + 1

    for animal2 in matriz.columns:
        candidatos = [c for c in todas_combinacoes if c['Animal_2'] == animal2]
        rcl = candidatos[:tamanho_rcl]
        random.shuffle(rcl)

        for c in rcl:
            a1 = c['Animal_1']
            if contador_1.get(a1, 0) < max_cruz:
                cruzamentos.append(c)
                usados_2.add(animal2)
                contador_1[a1] = contador_1.get(a1, 0) + 1
                break

    return cruzamentos

def busca_local(solucao, matriz):
    """Aplica busca local para melhorar a solução"""
    atual = list(solucao)
    melhor = atual[:]
    valor_melhor = f_objetivo(melhor)

    for i in range(len(atual)):
        for j in range(i+1, len(atual)):
            nova = atual[:]
            nova[i], nova[j] = nova[j], nova[i]
            if f_objetivo(nova) < valor_melhor:
                melhor = nova[:]
                valor_melhor = f_objetivo(nova)

    return melhor

def grasp_cruzamentos(matriz, iteracoes=50, rcl_tamanho=3):
    """
    Algoritmo GRASP para encontrar os melhores cruzamentos
    
    Args:
        matriz: DataFrame com a matriz de relacionamentos
        iteracoes: Número de iterações do GRASP (padrão: 50)
        rcl_tamanho: Tamanho da lista de candidatos restritos (padrão: 3)
    
    Returns:
        dict: Dicionário com solução e estatísticas
    """
    melhor_solucao = None
    melhor_valor = float('inf')

    for _ in range(iteracoes):
        s = construir_solucao_rcl(matriz, rcl_tamanho)
        s_local = busca_local(s, matriz)
        v = f_objetivo(s_local)

        if v < melhor_valor:
            melhor_valor = v
            melhor_solucao = s_local

    # Calcular estatísticas
    if melhor_solucao:
        media_coeficientes = calcular_media_cruzamentos(melhor_solucao)
        resultado = {
            'cruzamentos': melhor_solucao,
            'valor_objetivo': melhor_valor,
            'media_coeficientes': media_coeficientes,
            'total_cruzamentos': len(melhor_solucao)
        }
    else:
        resultado = {
            'cruzamentos': [],
            'valor_objetivo': 0,
            'media_coeficientes': 0.0,
            'total_cruzamentos': 0
        }

    return resultado

def grasp_multiplas_execucoes(matriz, num_execucoes=10):
    """
    Executa o algoritmo GRASP múltiplas vezes com parâmetros aleatórios
    Retorna dict com todas as execuções, estatísticas e a melhor solução
    """
    print(f"Iniciando {num_execucoes} execuções do GRASPE com parâmetros aleatórios...")
    
    todas_execucoes = []
    melhor_solucao_global = None
    melhor_valor_global = float('inf')
    todas_medias = []
    
    for execucao in range(num_execucoes):
        # Parâmetros aleatórios para variação na metaheurística GRASP
        n_colunas = len(matriz.columns) if hasattr(matriz, 'columns') else len(matriz[0])
        rcl_tamanho_aleatorio = random.randint(2, 10)   # Variação no tamanho da RCL
        print(f"Execução {execucao + 1}/{num_execucoes} - Iterações: {n_colunas}, RCL: {rcl_tamanho_aleatorio}")
        
        # Executar GRASP com parâmetros aleatórios
        
        resultado = grasp_cruzamentos(matriz, n_colunas, rcl_tamanho_aleatorio)
        
        # Adicionar informações da execução
        resultado['execucao'] = execucao + 1
        resultado['parametros'] = {
            'iteracoes': n_colunas,
            'rcl_tamanho': rcl_tamanho_aleatorio
        }
        
        todas_execucoes.append(resultado)
        todas_medias.append(resultado['media_coeficientes'])
        
        # Verificar se é a melhor solução global
        if resultado['valor_objetivo'] < melhor_valor_global:
            melhor_valor_global = resultado['valor_objetivo']
            melhor_solucao_global = resultado.copy()
    
    # Calcular estatísticas gerais
    media_das_medias = sum(todas_medias) / len(todas_medias) if todas_medias else 0
    melhor_media = min(todas_medias) if todas_medias else 0
    pior_media = max(todas_medias) if todas_medias else 0
    
    print(f"\n=== RESUMO DE {num_execucoes} EXECUÇÕES ===")
    print(f"Média das médias: {media_das_medias:.6f}")
    print(f"Melhor média encontrada: {melhor_media:.6f}")
    print(f"Pior média encontrada: {pior_media:.6f}")
    print(f"Melhor valor objetivo global: {melhor_valor_global:.6f}")
    
    return {
        'execucoes': todas_execucoes,
        'melhor_solucao_global': melhor_solucao_global,
        'estatisticas': {
            'media_das_medias': media_das_medias,
            'melhor_media': melhor_media,
            'pior_media': pior_media,
            'todas_medias': todas_medias,
            'num_execucoes': num_execucoes
        }
    }
