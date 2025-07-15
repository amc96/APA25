# Análise de Complexidade - Aplicativo GRASPE

## 1. Análise de Complexidade das Funções

### 1.1 Módulo `csv_to_matrix.py`

#### Função `csv_to_matrix(arquivo_csv)`
- **Complexidade de Tempo**: O(n + m × p)
  - n = número de linhas no CSV
  - m = número de animais únicos em Animal_1
  - p = número de animais únicos em Animal_2
  - Leitura do CSV: O(n)
  - Criação da matriz: O(m × p)
  - Preenchimento da matriz: O(n)
- **Complexidade de Espaço**: O(m × p)
  - Matriz m × p para armazenar os coeficientes

#### Função `get_matrix_statistics(matriz)`
- **Complexidade de Tempo**: O(m × p)
  - m = número de linhas da matriz
  - p = número de colunas da matriz
  - Percorre todos os elementos da matriz uma vez
- **Complexidade de Espaço**: O(1)
  - Apenas variáveis auxiliares

#### Função `contagem_animais(arquivo_csv)`
- **Complexidade de Tempo**: O(n)
  - n = número de linhas no CSV
  - Leitura do CSV e contagem de valores únicos
- **Complexidade de Espaço**: O(k)
  - k = número de animais únicos (para armazenar os conjuntos)

### 1.2 Módulo `graspe.py`

#### Função `f_objetivo(solucao)`
- **Complexidade de Tempo**: O(s)
  - s = número de pares na solução
  - Soma os coeficientes de todos os pares
- **Complexidade de Espaço**: O(1)

#### Função `calcular_media_cruzamentos(solucao)`
- **Complexidade de Tempo**: O(s)
  - s = número de pares na solução
  - Soma os coeficientes e divide pelo tamanho
- **Complexidade de Espaço**: O(1)

#### Função `construir_solucao_rcl_adaptativa(matriz, tamanho_rcl, descartar_valor)`
- **Complexidade de Tempo**: O(p × m × log(m))
  - p = número de colunas (Animal_2)
  - m = número de linhas (Animal_1)
  - Para cada Animal_2, cria lista de candidatos O(m)
  - Ordenação dos candidatos O(m × log(m))
- **Complexidade de Espaço**: O(m × p)
  - Lista de candidatos e estruturas auxiliares

#### Função `busca_local(solucao, matriz)`
- **Complexidade de Tempo**: O(s²)
  - s = número de pares na solução
  - Teste de todas as trocas possíveis entre pares
- **Complexidade de Espaço**: O(s)
  - Cópia da solução atual

#### Função `grasp_cruzamentos(matriz, iteracoes, rcl_tamanho, indice_execucao)`
- **Complexidade de Tempo**: O(i × (p × m × log(m) + s²))
  - i = número de iterações
  - p × m × log(m) = construção da solução
  - s² = busca local
- **Complexidade de Espaço**: O(m × p + s)
  - Matriz e estruturas da solução

#### Função `grasp_multiplas_execucoes(matriz, num_execucoes, pasta_saida)`
- **Complexidade de Tempo**: O(e × i × (p × m × log(m) + s²))
  - e = número de execuções
  - i = número de iterações por execução
  - p × m × log(m) + s² = complexidade do GRASP individual
- **Complexidade de Espaço**: O(e × s + m × p)
  - Armazena resultados de todas as execuções

### 1.3 Módulo `app.py`

#### Função `allowed_file(filename)`
- **Complexidade de Tempo**: O(1)
  - Verificação simples de extensão
- **Complexidade de Espaço**: O(1)

#### Rota `index()` (POST)
- **Complexidade de Tempo**: O(e × i × (p × m × log(m) + s²))
  - Dominada pela execução do GRASP múltiplas vezes
- **Complexidade de Espaço**: O(e × s + m × p)
  - Armazenamento dos resultados

#### Rota `visualizar_matriz(filename)`
- **Complexidade de Tempo**: O(e × i × (p × m × log(m) + s²))
  - Executa GRASP múltiplas vezes
- **Complexidade de Espaço**: O(m × p + e × s)
  - Matriz e resultados das execuções

## 2. Análise de Complexidade do Algoritmo GRASPE

### 2.1 Algoritmo GRASP Individual

O algoritmo GRASP (Greedy Randomized Adaptive Search Procedure) implementado possui:

**Fase Construtiva (construir_solucao_rcl_adaptativa):**
- **Complexidade**: O(p × m × log(m))
- **Justificativa**: 
  - Para cada animal da coluna (p animais)
  - Cria lista de candidatos (m animais)
  - Ordena candidatos por coeficiente (m × log(m))

**Fase de Busca Local (busca_local):**
- **Complexidade**: O(s²)
- **Justificativa**:
  - Testa todas as trocas possíveis entre s pares
  - s × (s-1) / 2 ≈ O(s²)

**Algoritmo GRASP Completo:**
- **Complexidade**: O(i × (p × m × log(m) + s²))
- **Onde**:
  - i = número de iterações
  - p = número de colunas na matriz
  - m = número de linhas na matriz
  - s = número de pares na solução (s ≤ min(m, p))

### 2.2 Algoritmo GRASP Múltiplas Execuções

**Complexidade Total**: O(e × i × (p × m × log(m) + s²))

**Onde**:
- e = número de execuções
- i = número de iterações por execução
- p = número de colunas na matriz
- m = número de linhas na matriz
- s = número de pares na solução

### 2.3 Análise Prática

**Cenário Típico**:
- Matriz 100×100 (m = p = 100)
- 5 execuções (e = 5)
- 100 iterações por execução (i = 100)
- 50 pares na solução (s = 50)

**Complexidade Estimada**:
- Fase construtiva: 100 × 100 × log(100) ≈ 66.400 operações
- Busca local: 50² = 2.500 operações
- Por iteração: ~69.000 operações
- Por execução: 100 × 69.000 = 6.900.000 operações
- Total: 5 × 6.900.000 = 34.500.000 operações

## 3. Otimizações Implementadas

### 3.1 RCL Adaptativa
- **Benefício**: Reduz o espaço de busca mantendo diversidade
- **Impacto**: Melhora a qualidade das soluções sem aumentar significativamente a complexidade

### 3.2 Busca Local Limitada
- **Benefício**: Evita busca exaustiva em soluções muito grandes
- **Impacto**: Complexidade O(s²) em vez de O(s!)

### 3.3 Paralelização Potencial
- **Oportunidade**: Múltiplas execuções podem ser paralelizadas
- **Benefício**: Redução do tempo de execução de O(e × ...) para O(...)

## 4. Limitações e Considerações

### 4.1 Limitações de Memória
- **Matriz**: O(m × p) pode ser limitante para matrizes muito grandes
- **Soluções**: Armazenamento de múltiplas execuções pode consumir memória

### 4.2 Limitações de Tempo
- **Crescimento**: Complexidade quadrática na busca local
- **Mitigação**: Implementar timeout ou limite de movimentos

### 4.3 Qualidade da Solução
- **Trade-off**: Mais iterações/execuções vs. tempo de processamento
- **Balanceamento**: Parâmetros RCL afetam diversidade vs. qualidade

## 5. Recomendações para Escalabilidade

### 5.1 Para Matrizes Grandes (>1000×1000)
- Implementar paralelização das execuções
- Considerar algoritmos aproximados para busca local
- Usar técnicas de amostragem para reduzir espaço de busca

### 5.2 Para Tempo Real
- Implementar timeout configurável
- Usar cache para soluções similares
- Considerar algoritmos online/incremental

### 5.3 Para Qualidade
- Ajustar parâmetros RCL dinamicamente
- Implementar reinicialização adaptativa
- Usar técnicas de intensificação/diversificação

## 6. Conclusão

O algoritmo GRASPE implementado possui complexidade polinomial O(e × i × (p × m × log(m) + s²)), sendo adequado para problemas de médio porte. A implementação inclui otimizações importantes como RCL adaptativa e busca local eficiente, proporcionando um bom balance entre qualidade de solução e tempo de execução.