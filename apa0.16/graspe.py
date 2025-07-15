import random
import time
import pandas as pd
import os

def f_objetivo(solucao):
    """Função objetivo: minimizar a soma dos coeficientes"""
    return sum(pair['Coeficiente'] for pair in solucao)

def calcular_media_cruzamentos(solucao):
    """Calcula a média dos coeficientes dos melhores cruzamentos"""
    if not solucao:
        return 0.0
    return sum(pair['Coeficiente'] for pair in solucao) / len(solucao)

def construir_solucao_rcl_adaptativa(matriz, tamanho_rcl=0.3, descartar_valor=-1):
    """
    Constrói solução com RCL adaptativa, onde a lista de candidatos e seus coeficientes são atualizados a cada passo.
    tamanho_rcl pode ser float (proporção) ou inteiro (fixo).
    """

    cruzamentos = []
    contador_1 = {}
    max_cruz = int(len(matriz.columns) / len(matriz.index)) + 1

    animais2_disponiveis = list(matriz.columns)

    while animais2_disponiveis:
        animal2 = animais2_disponiveis.pop(0)

        candidatos = []
        for animal1 in matriz.index:
            coef = matriz.loc[animal1, animal2]
            if coef == descartar_valor or coef == 1.0:
                continue
            if contador_1.get(animal1, 0) >= max_cruz:
                continue
            if any(c['Animal_2'] == animal2 for c in cruzamentos):
                candidatos = []
                break
            candidatos.append({'Animal_1': animal1, 'Animal_2': animal2, 'Coeficiente': float(coef)})

        if not candidatos:
            print(f"  Nenhum candidato válido para animal2={animal2}, pulando.")
            continue

        candidatos.sort(key=lambda x: x['Coeficiente'])

        if isinstance(tamanho_rcl, float):
            rcl_size = max(1, int(tamanho_rcl * len(candidatos)))
        else:
            rcl_size = min(tamanho_rcl, len(candidatos))

        rcl = candidatos[:rcl_size]
        escolhido = random.choice(rcl)

        cruzamentos.append(escolhido)
        contador_1[escolhido['Animal_1']] = contador_1.get(escolhido['Animal_1'], 0) + 1

    return cruzamentos

def busca_local(solucao, matriz):
    """Busca local simples que tenta melhorar solução trocando pares"""
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

def grasp_cruzamentos(matriz, iteracoes, rcl_tamanho, indice_execucao=None):
    """
    GRASP com busca construtiva adaptativa.
    Salva as soluções encontradas em arquivos separados por execução.
    """
    print(f"Executando GRASP com {iteracoes} iterações e rcl_tamanho={rcl_tamanho}")

    melhor_solucao = None
    melhor_valor = float('inf')

    # Define o nome do arquivo com base no índice da execução
    if indice_execucao is None:
        indice_execucao = "unica"
    pasta_saida = "resultados_grasp"
    os.makedirs(pasta_saida, exist_ok=True)
    nome_arquivo = f"solucoes_execucao_{indice_execucao}.csv"
    caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

    # Inicia o arquivo
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write("iteracao,valor_objetivo,media_coeficientes,total_cruzamentos\n")

    for i in range(1, iteracoes + 1):
        s = construir_solucao_rcl_adaptativa(matriz, rcl_tamanho)
        s_local = busca_local(s, matriz)
        v = f_objetivo(s_local)
        media_coeficientes = calcular_media_cruzamentos(s_local)
        print(f"  -> solução encontrada (valor {v:.6f})")

        # Salva no arquivo correspondente
        with open(caminho_arquivo, 'a', encoding='utf-8') as f:
            f.write(f"{i},{v:.6f},{media_coeficientes:.6f},{len(s_local)}\n")

        if v < melhor_valor:
            melhor_valor = v
            melhor_solucao = s_local
            print(f"  -> Nova melhor solução encontrada (valor {melhor_valor:.6f})")

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

    print("GRASP finalizado.\n")
    return resultado


def grasp_multiplas_execucoes(matriz, num_execucoes, pasta_saida='resultados_grasp'):
    os.makedirs(pasta_saida, exist_ok=True)

    print(f"Iniciando {num_execucoes} execuções do GRASP com RCL adaptativa...\n")
    
    todas_execucoes = []
    melhor_solucao_global = None
    melhor_valor_global = float('inf')
    todas_medias = []
    tempos_execucao = []
    valores_objetivo = []

    for execucao in range(num_execucoes):
        iteracoes = len(matriz.columns) if hasattr(matriz, 'columns') else len(matriz[0])
        rcl_tamanho_aleatorio = round(random.uniform(0.75, 0.95), 2)

        print(f"Execução {execucao + 1}/{num_execucoes} - Iterações: {iteracoes}, RCL proporcional: {rcl_tamanho_aleatorio:.2f}")

        inicio = time.time()
        resultado = grasp_cruzamentos(
                    matriz,
                    iteracoes,
                    rcl_tamanho_aleatorio,
                    indice_execucao=execucao + 1  
        )
        duracao = time.time() - inicio

        resultado['execucao'] = execucao + 1
        resultado['parametros'] = {
            'iteracoes': iteracoes,
            'rcl_tamanho_proporcional': rcl_tamanho_aleatorio
        }
        resultado['tempo_execucao'] = duracao

        todas_execucoes.append(resultado)
        todas_medias.append(resultado['media_coeficientes'])
        tempos_execucao.append(duracao)
        valores_objetivo.append(resultado['valor_objetivo'])

        if resultado['valor_objetivo'] < melhor_valor_global:
            melhor_valor_global = resultado['valor_objetivo']
            melhor_solucao_global = resultado.copy()

        print(f"Execução {execucao + 1} finalizada em {duracao:.2f} segundos. Melhor valor até agora: {melhor_valor_global:.6f}\n")

    media_das_medias = sum(todas_medias) / len(todas_medias) if todas_medias else 0
    melhor_media = min(todas_medias) if todas_medias else 0
    pior_media = max(todas_medias) if todas_medias else 0
    tempo_total = sum(tempos_execucao)

    print("\n=== RESUMO DE EXECUÇÕES ===")
    print(f"Média das médias: {media_das_medias:.6f}")
    print(f"Melhor média encontrada: {melhor_media:.6f}")
    print(f"Pior média encontrada: {pior_media:.6f}")
    print(f"Melhor valor objetivo global: {melhor_valor_global:.6f}")
    print(f"Tempo total de execução: {tempo_total:.2f} segundos\n")

        
    # Criar DataFrame com os resultados
    df_resultados = pd.DataFrame(melhor_solucao_global['cruzamentos'])
        
    # Salvar CSV temporário
    csv_filename = 'resultado.csv'
    csv_filepath = os.path.join("uploads", csv_filename)
    df_resultados.to_csv(csv_filepath, index=False, encoding='utf-8')
    
    return {
        'execucoes': todas_execucoes,
        'melhor_solucao_global': melhor_solucao_global,
        'estatisticas': {
            'media_das_medias': media_das_medias,
            'melhor_media': melhor_media,
            'pior_media': pior_media,
            'todas_medias': todas_medias,
            'valores_objetivo': valores_objetivo,
            'tempos_execucao': tempos_execucao,
            'tempo_total': tempo_total,
            'num_execucoes': num_execucoes
        }
    }
