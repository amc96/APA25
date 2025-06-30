# Documentação - Aplicativo de Análise de Parentesco

## Visão Geral

Este aplicativo web permite analisar dados de parentesco entre animais/produtos utilizando o método GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement). O sistema converte arquivos CSV em matrizes de parentesco e identifica os melhores cruzamentos possíveis através de múltiplas execuções com parâmetros aleatórios.

## Estrutura do Projeto

```
├── app.py                  # Aplicativo Flask principal
├── csv_to_matrix.py        # Conversão de CSV para matriz
├── graspe.py              # Algoritmo GRASPE para análise
├── main.py                # Ponto de entrada da aplicação
├── iniciar.bat            # Script de inicialização (Windows)
├── iniciar.sh             # Script de inicialização (Linux/Mac)
├── templates/             # Templates HTML
│   ├── index.html         # Página principal de upload
│   ├── resultados.html    # Página de resultados GRASPE
│   └── visualizar_novo.html # Visualização de matriz
├── uploads/               # Arquivos enviados pelos usuários
├── pyproject.toml         # Configuração de dependências
└── README.md              # Documentação básica
```

## Componentes Principais

### 1. main.py - Ponto de Entrada

**Funcionalidades:**
- Verificação de arquivos necessários
- Criação de pasta uploads
- Inicialização da aplicação Flask
- Tratamento de erros de importação

**Fluxo de Execução:**
1. Verifica se app.py existe
2. Cria pasta uploads se necessário
3. Importa e executa a aplicação Flask
4. Configura servidor na porta 5000

### 2. app.py - Aplicativo Principal

**Funcionalidades:**
- Upload de arquivos CSV
- Conversão para matriz de parentesco
- Execução do algoritmo GRASPE
- Visualização de resultados
- Download de arquivos processados

**Rotas Implementadas:**
- `GET/POST /` - Página principal com upload
- `GET /visualizar/<filename>` - Visualização de matriz
- `GET /download/<filename>` - Download de arquivos
- `GET /download_cruzamentos_csv` - Download de resultados

**Configurações:**
- Limite de upload: 10MB
- Formatos aceitos: CSV apenas
- Chave secreta para sessões Flask

### 3. csv_to_matrix.py - Conversor de CSV

**Função Principal:** `csv_to_matrix(arquivo_csv)`
- Lê arquivo CSV com pandas
- Valida colunas necessárias (Animal_1, Animal_2, Coef)
- Cria matriz quadrada simétrica
- Preenche diagonal principal com zeros
- Trata valores ausentes

**Funções Auxiliares:**
- `get_matrix_statistics(matriz)` - Estatísticas da matriz
- `contagem_animais(arquivo_csv)` - Contagem de animais únicos

**Validações:**
- Verifica existência das colunas obrigatórias
- Trata erros de leitura de arquivo
- Retorna mensagens de erro detalhadas

### 4. graspe.py - Algoritmo GRASPE

**Implementação GRASP:**
- Função objetivo: minimizar soma dos coeficientes
- Construção gulosa com lista de candidatos restrita (RCL)
- Busca local para melhoria da solução
- Múltiplas execuções com parâmetros aleatórios

**Funções Principais:**
- `f_objetivo(solucao)` - Cálculo da função objetivo
- `calcular_media_cruzamentos(solucao)` - Média dos coeficientes
- `construir_solucao_rcl(matriz, tamanho_rcl)` - Construção gulosa
- `busca_local(solucao, matriz)` - Melhoria local
- `grasp_cruzamentos(matriz, iteracoes, tamanho_rcl)` - GRASP único
- `grasp_multiplas_execucoes(matriz, num_execucoes)` - Múltiplas execuções

**Parâmetros Aleatórios:**
- Número de iterações: 30-100 por execução
- Tamanho RCL: 2-6 candidatos
- Seleção aleatória dentro da RCL

### 5. Templates HTML

**index.html:**
- Formulário de upload de arquivo
- Seleção de número de execuções GRASPE
- Validação JavaScript básica
- Interface Bootstrap 5

**visualizar_novo.html:**
- Exibição de matriz limitada (30x30 para performance)
- Estatísticas da matriz
- Botões de navegação
- Responsivo para mobile

**resultados.html:**
- Gráficos interativos com Chart.js
- Estatísticas completas das execuções
- Classificação de qualidade dos cruzamentos
- Download de resultados em CSV
- Sistema de cores para qualidade

## Fluxo de Dados

### 1. Upload e Processamento
```
CSV Upload → Validação → Conversão para Matriz → Estatísticas
```

### 2. Análise GRASPE
```
Matriz → Múltiplas Execuções GRASPE → Estatísticas → Melhor Solução
```

### 3. Visualização
```
Resultados → Gráficos → Tabelas → Downloads
```

## Dependências

### Python (pyproject.toml)
```toml
[project]
dependencies = [
    "flask>=2.3.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "werkzeug>=2.3.0"
]
```

### Frontend (CDN)
- Bootstrap 5.3.0 - Framework CSS
- Chart.js 3.9.1 - Gráficos interativos
- Bootstrap Icons - Ícones

## Configurações de Segurança

### Upload de Arquivos
- Extensões permitidas: apenas .csv
- Tamanho máximo: 10MB
- Validação de nome de arquivo seguro
- Pasta uploads isolada

### Flask
- Chave secreta configurada
- Debug mode habilitado para desenvolvimento
- Host 0.0.0.0 para acesso externo
- Porta configurável via variável de ambiente

## Performance

### Otimizações Implementadas
- Visualização limitada de matriz (30x30)
- Processamento assíncrono via JavaScript
- Compressão de dados para download
- Cache de resultados na sessão

### Limitações
- Matrizes muito grandes podem causar lentidão
- Múltiplas execuções aumentam tempo de processamento
- Visualização completa limitada por performance do browser

## Tratamento de Erros

### Validações de Arquivo
- Arquivo não enviado
- Formato inválido
- Colunas ausentes
- Dados corrompidos

### Erros de Processamento
- Falha na conversão de matriz
- Erro no algoritmo GRASPE
- Problemas de memória
- Timeouts de processamento

### Interface de Usuário
- Mensagens flash para feedback
- Indicadores de carregamento
- Tratamento de erros JavaScript
- Redirecionamentos apropriados

## Algoritmo GRASPE Detalhado

### Método GRASP
1. **Fase Construtiva:**
   - Cria lista de todos os pares possíveis
   - Ordena por coeficiente (guloso)
   - Seleciona aleatoriamente da RCL
   - Evita animais já selecionados

2. **Fase de Busca Local:**
   - Tenta trocar pares na solução atual
   - Aceita melhorias na função objetivo
   - Continua até não encontrar melhorias

3. **Múltiplas Execuções:**
   - Executa GRASP várias vezes
   - Varia parâmetros aleatoriamente
   - Mantém a melhor solução global
   - Calcula estatísticas de todas as execuções

### Classificação de Qualidade
- **Excelente (Verde):** Média ≤ 0.1
- **Boa (Azul):** 0.1 < Média ≤ 0.3  
- **Regular (Laranja):** 0.3 < Média ≤ 0.5
- **Cuidado (Vermelho):** Média > 0.5

## Scripts de Inicialização

### iniciar.bat (Windows)
```batch
@echo off
echo Instalando dependências...
pip install flask pandas numpy werkzeug
echo Iniciando aplicativo...
python main.py
pause
```

### iniciar.sh (Linux/Mac)
```bash
#!/bin/bash
echo "Instalando dependências..."
pip install flask pandas numpy werkzeug
echo "Iniciando aplicativo..."
python main.py
```

## Manutenção e Extensões

### Possíveis Melhorias
- Cache de resultados em banco de dados
- Processamento em background com Celery
- API REST para integração externa
- Autenticação de usuários
- Histórico de análises

### Monitoramento
- Logs de erro detalhados
- Métricas de performance
- Utilização de recursos
- Estatísticas de uso

---

**Esta documentação reflete o estado atual do código implementado e em funcionamento.**