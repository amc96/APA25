
import random

def f_objetivo(solucao):
    return sum(pair['Coeficiente'] for pair in solucao)

def construir_solucao_rcl(matriz, tamanho_rcl=3, descartar_valor=-1):
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
    melhor_solucao = None
    melhor_valor = float('inf')

    for _ in range(iteracoes):
        s = construir_solucao_rcl(matriz, rcl_tamanho)
        s_local = busca_local(s, matriz)
        v = f_objetivo(s_local)

        if v < melhor_valor:
            melhor_valor = v
            melhor_solucao = s_local

    return melhor_solucao
