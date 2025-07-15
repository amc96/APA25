# Aplicativo de Análise de Parentesco - GRASPE

Sistema web para análise de relacionamento genético entre animais utilizando o algoritmo GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement). O sistema converte arquivos CSV com dados de parentesco em matrizes e executa análises genéticas para encontrar os melhores pares reprodutivos.

## 🚀 Funcionalidades Principais

- **Upload de CSV**: Interface web para upload de arquivos CSV com dados de parentesco
- **Conversão para Matriz**: Transformação automática dos dados CSV em matriz de relacionamento
- **Algoritmo GRASPE**: Análise genética avançada usando metaheurística GRASP
- **Múltiplas Execuções**: Sistema de execução múltipla com parâmetros aleatórios
- **Visualização de Resultados**: Interface web para visualização de matrizes e resultados
- **Exportação de Dados**: Download dos resultados em formato CSV
- **Análise Estatística**: Cálculo de médias, melhores/piores soluções e métricas de qualidade

## 📊 Estrutura dos Dados

### Formato do CSV de Entrada
O arquivo CSV deve conter as seguintes colunas:
- **Animal_1**: Identificador do primeiro animal
- **Animal_2**: Identificador do segundo animal  
- **Coef**: Coeficiente de parentesco (valor numérico)

### Exemplo de Dados
```csv
Animal_1,Animal_2,Coef
A001,B001,0.125
A001,B002,0.250
A002,B001,0.000
...
```

## 🧬 Algoritmo GRASPE

O algoritmo GRASPE implementa uma metaheurística GRASP (Greedy Randomized Adaptive Search Procedure) especificamente adaptada para análise de parentesco:

### Características
- **RCL Adaptativa**: Lista de candidatos restrita que se adapta dinamicamente
- **Busca Local**: Otimização através de trocas entre pares
- **Múltiplas Execuções**: Execução paralela com parâmetros aleatórios
- **Minimização de Coeficientes**: Busca por combinações com menores coeficientes de parentesco

### Parâmetros Configuráveis
- Número de execuções (padrão: 5)
- Tamanho da RCL (variável aleatória entre 0.75-0.95)
- Número de iterações por execução (baseado no número de colunas)

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Dependências
```bash
pip install flask pandas numpy werkzeug
```

### Execução
```bash
# Método 1: Script principal
python main.py

# Método 2: Script alternativo
python app.py
```

### Acesso
Abra o navegador em: **http://localhost:5000**

## 📁 Estrutura do Projeto

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
├── DOCUMENTACAO.md        # Documentação técnica
├── MANUAL_USUARIO.md      # Manual do usuário
└── COMPLEXIDADE.md        # Análise de complexidade
```

## 🔧 Módulos Principais

### 1. `csv_to_matrix.py`
- **Função**: `csv_to_matrix(arquivo_csv)` - Converte CSV em matriz
- **Função**: `get_matrix_statistics(matriz)` - Calcula estatísticas da matriz
- **Função**: `contagem_animais(arquivo_csv)` - Conta animais distintos

### 2. `graspe.py`
- **Função**: `construir_solucao_rcl_adaptativa()` - Constrói solução usando RCL
- **Função**: `busca_local()` - Otimização local da solução
- **Função**: `grasp_cruzamentos()` - Execução individual do GRASP
- **Função**: `grasp_multiplas_execucoes()` - Múltiplas execuções do algoritmo

### 3. `app.py`
- **Rota**: `/` - Página principal com upload
- **Rota**: `/visualizar/<filename>` - Visualização de matriz
- **Rota**: `/download_cruzamentos_csv` - Download de resultados

## 📈 Análise de Complexidade

### Complexidade Temporal
- **Algoritmo GRASP Individual**: O(i × (p × m × log(m) + s²))
- **Múltiplas Execuções**: O(e × i × (p × m × log(m) + s²))

Onde:
- e = número de execuções
- i = número de iterações
- p = número de colunas (Animal_2)
- m = número de linhas (Animal_1)
- s = número de pares na solução

### Complexidade Espacial
- **Matriz Principal**: O(m × p)
- **Armazenamento de Soluções**: O(e × s)

## 🎯 Como Usar

### Passo a Passo:
1. **Upload**: Envie arquivo CSV com dados de parentesco
2. **Configuração**: Escolha o número de execuções (recomendado: 5-20)
3. **Processamento**: Sistema executa múltiplas análises GRASPE
4. **Resultados**: Visualize estatísticas e a melhor solução encontrada
5. **Download**: Baixe resultados completos em formato CSV

### Parâmetros Avançados:
- **Execuções**: Configurável via formulário web
- **Iterações**: Baseado no número de colunas da matriz
- **RCL**: Aleatorização automática (0.75-0.95)

## 📊 Resultados e Métricas

### Estatísticas Calculadas
- **Média das médias**: Média dos coeficientes de todas as execuções
- **Melhor média**: Menor média encontrada
- **Pior média**: Maior média encontrada
- **Valor objetivo**: Soma dos coeficientes da melhor solução
- **Tempo de execução**: Tempo total de processamento

### Formato de Saída
- **CSV de Resultados**: Melhores cruzamentos encontrados
- **Arquivos de Execução**: Detalhes de cada execução individual
- **Estatísticas Consolidadas**: Resumo de todas as execuções

## 🔍 Arquivos de Configuração

### Configuração de Execução
```json
{
  "num_execucoes": 5
}
```

### Logs de Execução
```csv
iteracao,valor_objetivo,media_coeficientes,total_cruzamentos
1,2.5000,0.5000,5
2,2.2500,0.4500,5
...
```

## 🚀 Otimizações Implementadas

### RCL Adaptativa
- Lista de candidatos que se adapta dinamicamente
- Melhora qualidade das soluções sem aumentar complexidade

### Busca Local Eficiente
- Otimização através de trocas entre pares
- Complexidade O(s²) controlada

### Múltiplas Execuções
- Parâmetros aleatórios para diversidade
- Armazenamento de melhores soluções

## 📋 Limitações

### Limitações de Memória
- Matriz O(m × p) pode ser limitante para matrizes muito grandes
- Armazenamento de múltiplas execuções consome memória

### Limitações de Tempo
- Crescimento quadrático na busca local
- Tempo de processamento aumenta com número de execuções

## 🔧 Configuração Avançada

### Parâmetros do Sistema
- **Tamanho máximo de arquivo**: 10MB
- **Formato obrigatório**: CSV
- **Porta padrão**: 5000
- **Diretório de upload**: `uploads/`
- **Diretório de resultados**: `resultados_grasp/`

### Variáveis de Ambiente
- `FLASK_DEBUG`: Modo debug (padrão: True)
- `FLASK_PORT`: Porta do servidor (padrão: 5000)
- `UPLOAD_FOLDER`: Pasta de uploads (padrão: uploads/)

## 📚 Documentação Adicional

- **[DOCUMENTACAO.md](DOCUMENTACAO.md)**: Documentação técnica completa
- **[MANUAL_USUARIO.md](MANUAL_USUARIO.md)**: Manual do usuário
- **[COMPLEXIDADE.md](COMPLEXIDADE.md)**: Análise detalhada de complexidade

## 🐛 Tratamento de Erros

### Erros Comuns
- Arquivo CSV com formato incorreto
- Colunas obrigatórias ausentes
- Valores não numéricos na coluna Coef
- Arquivo muito grande (>10MB)

### Logs de Debug
- Informações de processamento no console
- Detalhes de cada execução GRASPE
- Estatísticas de tempo de execução

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça fork do repositório
2. Crie uma branch para sua feature
3. Implemente suas alterações
4. Teste thoroughly
5. Faça pull request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.