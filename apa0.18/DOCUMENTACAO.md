# Documentação Técnica - Aplicativo GRASPE

## Visão Geral

Este aplicativo web implementa análise de parentesco genético utilizando o algoritmo GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement). O sistema converte arquivos CSV em matrizes de relacionamento e executa análises otimizadas para encontrar os melhores pares reprodutivos.

## Arquitetura do Sistema

### Estrutura do Projeto
```
├── app.py                  # Aplicativo Flask principal
├── csv_to_matrix.py        # Conversão de CSV para matriz
├── graspe.py              # Algoritmo GRASPE
├── main.py                # Ponto de entrada
├── templates/             # Interface web
│   ├── index.html         # Página principal
│   ├── resultados.html    # Resultados GRASPE
│   └── visualizar_novo.html # Visualização de matriz
├── uploads/               # Arquivos do usuário
├── resultados_grasp/      # Resultados das execuções
├── COMPLEXIDADE.md        # Análise de complexidade
└── README_ATUALIZADO.md   # Documentação completa
```

## Módulos Técnicos

### 1. `app.py` - Aplicativo Flask Principal

#### Configurações do Sistema
```python
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'csv'}
```

#### Rotas Implementadas

**Rota Principal** - `GET/POST /`
- **Funcionalidade**: Upload de CSV e processamento GRASPE
- **Parâmetros**: 
  - `arquivo` (file): Arquivo CSV
  - `num_execucoes` (int): Número de execuções (padrão: 5)
- **Processamento**:
  1. Validação de arquivo CSV
  2. Conversão para matriz usando `csv_to_matrix()`
  3. Execução de `grasp_multiplas_execucoes()`
  4. Renderização de resultados
- **Retorno**: Template com resultados GRASPE

**Rota de Visualização** - `GET /visualizar/<filename>`
- **Funcionalidade**: Visualização e reprocessamento de matriz
- **Parâmetros**: `filename` (str): Nome do arquivo de matriz
- **Processamento**:
  1. Leitura da matriz CSV
  2. Limitação para visualização (30x30)
  3. Execução GRASPE com parâmetros do arquivo de configuração
- **Retorno**: Template com visualização da matriz

**Rota de Download** - `GET /download_cruzamentos_csv`
- **Funcionalidade**: Download dos resultados em CSV
- **Arquivo**: `resultado.csv` da pasta uploads
- **Formato**: CSV com melhores cruzamentos

#### Tratamento de Erros
- Validação de extensão de arquivo
- Tratamento de exceções durante processamento
- Mensagens flash para feedback ao usuário
- Logs detalhados para debug

### 2. `csv_to_matrix.py` - Conversor de CSV

#### Função Principal: `csv_to_matrix(arquivo_csv)`
```python
def csv_to_matrix(arquivo_csv):
    """
    Converte arquivo CSV em matriz de parentesco
    
    Args:
        arquivo_csv (str): Caminho para o arquivo CSV
        
    Returns:
        DataFrame: Matriz m×p com relacionamentos
        
    Raises:
        ValueError: Se colunas obrigatórias estão ausentes
        FileNotFoundError: Se arquivo não existe
    """
```

**Processamento**:
1. Leitura do CSV com pandas
2. Validação de colunas obrigatórias (Animal_1, Animal_2, Coef)
3. Criação de matriz com animais únicos
4. Preenchimento com coeficientes ou valores padrão
5. Adição de metadados (contagens, total de animais)

**Complexidade**: O(n + m × p)
- n = linhas do CSV
- m = animais únicos em Animal_1
- p = animais únicos em Animal_2

#### Função Auxiliar: `get_matrix_statistics(matriz)`
```python
def get_matrix_statistics(matriz):
    """
    Calcula estatísticas da matriz
    
    Returns:
        dict: Estatísticas incluindo dimensões, contagens e coeficientes
    """
```

**Estatísticas Calculadas**:
- Dimensões da matriz (linhas, colunas)
- Contagem de animais únicos
- Valores não-zero (excluindo diagonal)
- Coeficientes: média, mínimo, máximo

**Complexidade**: O(m × p)

#### Função Auxiliar: `contagem_animais(arquivo_csv)`
```python
def contagem_animais(arquivo_csv):
    """
    Conta animais distintos em cada coluna
    
    Returns:
        dict: Contagens de Animal_1 e Animal_2
    """
```

**Complexidade**: O(n)

### 3. `graspe.py` - Algoritmo GRASPE

#### Função Objetivo: `f_objetivo(solucao)`
```python
def f_objetivo(solucao):
    """
    Calcula valor objetivo (soma dos coeficientes)
    
    Args:
        solucao (list): Lista de pares {Animal_1, Animal_2, Coeficiente}
        
    Returns:
        float: Soma dos coeficientes
    """
```

**Complexidade**: O(s) onde s = número de pares

#### Construção de Solução: `construir_solucao_rcl_adaptativa(matriz, tamanho_rcl, descartar_valor)`
```python
def construir_solucao_rcl_adaptativa(matriz, tamanho_rcl=0.3, descartar_valor=-1):
    """
    Constrói solução usando RCL adaptativa
    
    Args:
        matriz (DataFrame): Matriz de relacionamentos
        tamanho_rcl (float/int): Tamanho da RCL (proporcional ou fixo)
        descartar_valor (float): Valor a ser descartado
        
    Returns:
        list: Lista de cruzamentos selecionados
    """
```

**Algoritmo**:
1. Para cada Animal_2 disponível:
   - Criar lista de candidatos válidos
   - Ordenar por coeficiente (crescente)
   - Selecionar RCL (top candidatos)
   - Escolher aleatoriamente da RCL
   - Atualizar contadores e disponibilidade

**Complexidade**: O(p × m × log(m))
- p = colunas, m = linhas, log(m) = ordenação

#### Busca Local: `busca_local(solucao, matriz)`
```python
def busca_local(solucao, matriz):
    """
    Otimização local através de trocas entre pares
    
    Args:
        solucao (list): Solução atual
        matriz (DataFrame): Matriz de relacionamentos
        
    Returns:
        list: Solução melhorada
    """
```

**Algoritmo**:
1. Para cada par de posições (i, j):
   - Trocar elementos nas posições i e j
   - Calcular novo valor objetivo
   - Manter troca se melhora a solução

**Complexidade**: O(s²) onde s = número de pares

#### GRASP Individual: `grasp_cruzamentos(matriz, iteracoes, rcl_tamanho, indice_execucao)`
```python
def grasp_cruzamentos(matriz, iteracoes, rcl_tamanho, indice_execucao=None):
    """
    Execução individual do GRASP
    
    Args:
        matriz (DataFrame): Matriz de relacionamentos
        iteracoes (int): Número de iterações
        rcl_tamanho (float): Tamanho da RCL
        indice_execucao (int): Índice da execução
        
    Returns:
        dict: Resultado com melhor solução e estatísticas
    """
```

**Algoritmo**:
1. Para cada iteração:
   - Construir solução com RCL adaptativa
   - Aplicar busca local
   - Calcular valor objetivo
   - Atualizar melhor solução se necessário
   - Salvar resultado em arquivo CSV

**Complexidade**: O(i × (p × m × log(m) + s²))

#### Múltiplas Execuções: `grasp_multiplas_execucoes(matriz, num_execucoes, pasta_saida)`
```python
def grasp_multiplas_execucoes(matriz, num_execucoes, pasta_saida='resultados_grasp'):
    """
    Executa múltiplas instâncias do GRASP
    
    Args:
        matriz (DataFrame): Matriz de relacionamentos
        num_execucoes (int): Número de execuções
        pasta_saida (str): Pasta para salvar resultados
        
    Returns:
        dict: Resultados consolidados de todas as execuções
    """
```

**Algoritmo**:
1. Para cada execução:
   - Gerar parâmetros aleatórios:
     - Iterações: baseado no número de colunas
     - RCL: valor aleatório entre 0.75-0.95
   - Executar GRASP individual
   - Cronometrar tempo de execução
   - Armazenar resultados
2. Calcular estatísticas consolidadas
3. Salvar melhor solução em CSV

**Parâmetros Aleatórios**:
- **Iterações**: `len(matriz.columns)`
- **RCL**: `random.uniform(0.75, 0.95)`

**Complexidade**: O(e × i × (p × m × log(m) + s²))

## Fluxo de Dados

### 1. Upload e Processamento
```
CSV Upload → Validação → csv_to_matrix() → Matriz → GRASPE → Resultados
```

### 2. Execução GRASPE
```
Matriz → Múltiplas Execuções → Parâmetros Aleatórios → GRASP Individual → Melhor Solução
```

### 3. Saída de Resultados
```
Resultados → Estatísticas → Visualização Web → Download CSV
```

## Configurações do Sistema

### Parâmetros Configuráveis
```python
# Limite de upload
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# Extensões permitidas
ALLOWED_EXTENSIONS = {'csv'}

# Pasta de uploads
UPLOAD_FOLDER = 'uploads'

# Pasta de resultados
RESULTADOS_FOLDER = 'resultados_grasp'

# Servidor Flask
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True
```

### Parâmetros do Algoritmo
```python
# Número padrão de execuções
NUM_EXECUCOES_PADRAO = 5

# Faixa de RCL aleatória
RCL_MIN = 0.75
RCL_MAX = 0.95

# Iterações baseadas na matriz
ITERACOES = len(matriz.columns)

# Valor para descartar
DESCARTAR_VALOR = -1
```

## Estrutura de Dados

### Formato CSV de Entrada
```csv
Animal_1,Animal_2,Coef
A001,B001,0.125
A001,B002,0.250
A002,B001,0.000
```

### Estrutura da Matriz
```python
# DataFrame m×p
#        B001    B002    B003
# A001   0.125   0.250   0.000
# A002   0.000   0.125   0.250
# A003   0.250   0.000   0.125
```

### Formato de Solução
```python
solucao = [
    {'Animal_1': 'A001', 'Animal_2': 'B001', 'Coeficiente': 0.125},
    {'Animal_1': 'A002', 'Animal_2': 'B002', 'Coeficiente': 0.125},
    # ...
]
```

### Estrutura de Resultados
```python
resultado = {
    'cruzamentos': solucao,
    'valor_objetivo': float,
    'media_coeficientes': float,
    'total_cruzamentos': int,
    'execucao': int,
    'parametros': {
        'iteracoes': int,
        'rcl_tamanho_proporcional': float
    },
    'tempo_execucao': float
}
```

## Arquivos de Saída

### 1. Arquivos de Execução Individual
```
resultados_grasp/solucoes_execucao_1.csv
resultados_grasp/solucoes_execucao_2.csv
...
```

**Formato**:
```csv
iteracao,valor_objetivo,media_coeficientes,total_cruzamentos
1,2.5000,0.5000,5
2,2.2500,0.4500,5
...
```

### 2. Arquivo de Resultado Final
```
uploads/resultado.csv
```

**Formato**:
```csv
Animal_1,Animal_2,Coeficiente
A001,B001,0.125
A002,B002,0.125
...
```

### 3. Arquivo de Configuração
```
uploads/config_arquivo.json
```

**Formato**:
```json
{
    "num_execucoes": 5
}
```

## Tratamento de Erros

### Validações de Entrada
- Verificação de extensão de arquivo
- Validação de colunas obrigatórias
- Verificação de valores numéricos
- Limite de tamanho de arquivo

### Tratamento de Exceções
```python
try:
    # Processamento
except FileNotFoundError:
    # Arquivo não encontrado
except ValueError:
    # Dados inválidos
except Exception as e:
    # Erro genérico
```

### Logs de Debug
- Informações de processamento
- Tempos de execução
- Parâmetros utilizados
- Resultados de cada iteração

## Otimizações Implementadas

### 1. RCL Adaptativa
- Tamanho proporcional baseado no número de candidatos
- Melhora diversidade sem perder qualidade
- Parâmetros aleatórios para exploração

### 2. Busca Local Eficiente
- Apenas trocas entre pares adjacentes
- Parada antecipada quando não há melhoria
- Complexidade controlada O(s²)

### 3. Múltiplas Execuções
- Execuções independentes com parâmetros diferentes
- Seleção da melhor solução global
- Estatísticas consolidadas

### 4. Gestão de Memória
- Processamento incremental
- Limpeza de variáveis temporárias
- Salvamento em arquivos para grandes volumes

## Métricas de Performance

### Complexidade Temporal
- **CSV para Matriz**: O(n + m × p)
- **GRASP Individual**: O(i × (p × m × log(m) + s²))
- **Múltiplas Execuções**: O(e × i × (p × m × log(m) + s²))

### Complexidade Espacial
- **Matriz**: O(m × p)
- **Soluções**: O(e × s)
- **Resultados**: O(e × i)

### Benchmarks Típicos
- Matriz 100×100: ~5-10 segundos por execução
- Matriz 500×500: ~2-5 minutos por execução
- Matriz 1000×1000: ~10-20 minutos por execução

## Extensibilidade

### Novos Algoritmos
- Interface padrão para novos métodos
- Integração com múltiplas execuções
- Compatibilidade com estruturas existentes

### Novas Métricas
- Funções objetivo personalizadas
- Estatísticas adicionais
- Visualizações customizadas

### Otimizações Futuras
- Paralelização de execuções
- Algoritmos aproximados
- Cache de soluções

## Considerações de Segurança

### Upload de Arquivos
- Validação de extensão
- Limite de tamanho
- Sanitização de nomes
- Quarentena de arquivos

### Processamento
- Timeout para evitar loops infinitos
- Validação de dados de entrada
- Tratamento de memória
- Logs de auditoria

### Dados Sensíveis
- Não armazenamento de dados pessoais
- Limpeza automática de arquivos temporários
- Configurações seguras do Flask