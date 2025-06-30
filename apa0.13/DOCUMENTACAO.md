# Documentação - Aplicativo de Análise de Parentesco

## Visão Geral

Este aplicativo web permite analisar dados de parentesco entre animais/produtos utilizando o método GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement). O sistema converte arquivos CSV em matrizes de parentesco e identifica os melhores cruzamentos possíveis.

## Estrutura do Projeto

```
├── app.py                  # Aplicativo Flask principal
├── csv_to_matrix.py        # Conversão de CSV para matriz
├── graspe.py              # Algoritmo GRASPE para análise
├── iniciar.bat            # Script de inicialização (Windows)
├── iniciar.sh             # Script de inicialização (Linux/Mac)
├── templates/             # Templates HTML
│   ├── index.html         # Página principal
│   ├── visualizar.html    # Visualização de resultados
│   └── error.html         # Página de erro
├── uploads/               # Arquivos enviados pelos usuários
├── pyproject.toml         # Configuração de dependências
└── README.md              # Documentação básica
```

## Componentes Principais

### 1. app.py - Aplicativo Principal

**Funcionalidades:**
- Upload de arquivos CSV
- Conversão para matriz de parentesco
- Análise GRASPE dos melhores cruzamentos
- Visualização de resultados
- Download de arquivos

**Rotas Principais:**

#### `/ (GET/POST)` - Página Principal
- **GET**: Exibe formulário de upload
- **POST**: Processa arquivo CSV enviado
- Valida tipo de arquivo (.csv)
- Converte CSV em matriz
- Calcula estatísticas

#### `/visualizar/<filename> (GET)` - Visualização
- Exibe matriz em formato de tabela (limitado a 30x30)
- Mostra melhores cruzamentos usando GRASPE
- Permite download da matriz completa

#### `/download/<filename> (GET)` - Download de Arquivos
- Permite baixar matrizes geradas
- Controla acesso a arquivos na pasta uploads

#### `/download_cruzamentos_csv (GET)` - Download de Resultados
- Gera CSV com melhores cruzamentos
- Utiliza análise GRASPE mais recente
- Retorna arquivo formatado para download

**Configurações:**
- Porta: 5000
- Host: 0.0.0.0 (acessível externamente)
- Pasta de uploads: ./uploads
- Limite de arquivo: 10MB
- Extensões permitidas: .csv

### 2. csv_to_matrix.py - Conversão de Dados

**Função Principal: `csv_to_matrix(csv_file)`**

Converte arquivo CSV com dados de parentesco em matriz quadrada.

**Entrada esperada:**
```csv
Animal_1,Animal_2,Coef
A001,A002,0.25
A001,A003,0.5
...
```

**Processo:**
1. Lê arquivo CSV usando pandas
2. Identifica todos os animais únicos
3. Cria matriz quadrada com todos os animais
4. Preenche valores de coeficiente
5. Adiciona valores simétricos (A×B = B×A)
6. Preenche diagonal principal com 1.0

**Saída:**
- DataFrame pandas com matriz completa
- Índices e colunas são os IDs dos animais
- Valores são coeficientes de parentesco

**Funções Auxiliares:**

#### `get_matrix_statistics(matrix)`
Calcula estatísticas da matriz:
- Dimensões (linhas × colunas)
- Valores únicos
- Distribuição de coeficientes
- Porcentagem de valores válidos

#### `contagem_animais(csv_file)`
Conta animais únicos por categoria:
- Total de Animal_1 distintos
- Total de Animal_2 distintos
- Estatísticas de distribuição

### 3. graspe.py - Algoritmo GRASPE

**Método GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement)**

Algoritmo proprietário para identificar os melhores cruzamentos baseado em:
- Priorização de coeficiente 0 (sem parentesco)
- Ordenação crescente de coeficientes baixos
- Eliminação de valores inviáveis (-1)
- Animal_1 pode cruzar múltiplas vezes (máximo: (Animal_2/Animal_1)+1)
- Animal_2 pode cruzar uma única vez
- Todos os Animal_2 precisam ter um cruzamento

**Função Principal: `analisar_cruzamentos_graspe(matriz, limite_combinacoes=30)`**

**Parâmetros:**
- `matriz`: DataFrame com matriz de parentesco
- `limite_combinacoes`: Número máximo de cruzamentos a retornar

**Processo:**
1. **Filtragem**: Remove valores -1 (inviáveis) e 1.0 (parentesco total)
2. **Ordenação**: Prioriza coeficiente 0, depois valores crescentes
3. **Cálculo de Limite**: Máximo por Animal_1 = (Animal_2/Animal_1)+1
4. **Distribuição**: Cada Animal_2 recebe exatamente um cruzamento
5. **Controle**: Animal_1 pode cruzar até o limite calculado

**Saída:**
Lista de dicionários com:
```python
{
    'Animal_1': 'ID_do_animal_1',
    'Animal_2': 'ID_do_animal_2', 
    'Coeficiente': 0.0
}
```

**Funções Auxiliares:**

#### `filtrar_cruzamentos_inviaveis(matriz)`
Remove cruzamentos com:
- Coeficiente -1 (valor de descarte)
- Coeficiente 1.0 (parentesco total)
- Cruzamentos entre mesmo animal

#### `ordenar_cruzamentos_por_coeficiente(cruzamentos)`
Ordena cruzamentos seguindo método GRASPE:
1. Coeficiente 0 (prioridade máxima)
2. Valores crescentes (0.1, 0.2, 0.3...)
3. Evita valores extremos

## Templates HTML

### 1. index.html - Página Principal

**Componentes:**
- Formulário de upload com validação
- Exibição de estatísticas após processamento
- Contadores de animais por categoria
- Links para visualização e download

**Recursos:**
- Bootstrap 5 para interface responsiva
- Validação JavaScript para tipos de arquivo
- Mensagens flash para feedback
- Indicadores de progresso

### 2. visualizar.html - Visualização de Resultados

**Seções:**

#### Informações da Matriz
- Nome do arquivo processado
- Dimensões da matriz (linhas × colunas)
- Amostra visual (limitada a 30×30)

#### Estatísticas de Animais
- Contagem de Animal_1 e Animal_2
- Totais e porcentagens de utilização

#### Melhores Cruzamentos (GRASPE)
- Tabela com os melhores cruzamentos
- Códigos de cores por coeficiente:
  - Verde: 0.0 (ideal)
  - Azul: 0.0-0.25 (bom)
  - Amarelo: 0.25-0.5 (aceitável)
  - Vermelho: >0.5 (alto parentesco)

#### Controles de Download
- Download da matriz completa
- Download dos resultados dos cruzamentos

### 3. error.html - Página de Erro

**Funcionalidade:**
- Exibe mensagens de erro personalizadas
- Interface consistente com o resto do aplicativo
- Link para retornar à página principal

## Scripts de Inicialização

### iniciar.bat (Windows)

**Funcionalidades:**
- Verifica instalação do Python
- Instala dependências automaticamente
- Cria pasta de uploads
- Inicia servidor Flask
- Interface com feedback em português

### iniciar.sh (Linux/Mac)

**Funcionalidades:**
- Detecta Python3/pip3 automaticamente
- Instala dependências do sistema
- Configura permissões necessárias
- Executa aplicativo
- Tratamento de erros robusto

## Fluxo de Uso

1. **Inicialização**
   - Executar `iniciar.bat` ou `./iniciar.sh`
   - Acessar http://localhost:5000

2. **Upload de Dados**
   - Selecionar arquivo CSV com dados de parentesco
   - Formato: Animal_1, Animal_2, Coef
   - Aguardar processamento

3. **Visualização**
   - Clicar em "Visualizar Matriz"
   - Analisar estatísticas e cruzamentos
   - Verificar melhores combinações GRASPE

4. **Download**
   - Baixar matriz completa (CSV)
   - Baixar resultados dos cruzamentos (CSV)

## Dependências

### Principais
- **Flask 3.1.1**: Framework web
- **pandas 2.2.3**: Manipulação de dados
- **numpy 2.2.6**: Operações numéricas
- **werkzeug 3.1.3**: Utilitários Flask

### Instalação
```bash
pip install flask pandas werkzeug numpy
```

## Configuração de Ambiente

### Desenvolvimento
- Debug mode ativado
- Recarregamento automático
- Log detalhado de erros

### Produção
Para produção, modificar em `app.py`:
```python
app.run(host='0.0.0.0', port=port, debug=False)
```

## Tratamento de Erros

### Validações Implementadas
- Tipo de arquivo (apenas .csv)
- Tamanho máximo (10MB)
- Estrutura do CSV (colunas obrigatórias)
- Valores numéricos válidos

### Mensagens de Erro
- Upload: Problemas com arquivo
- Processamento: Erros na conversão
- Visualização: Arquivo não encontrado
- Download: Permissões e disponibilidade

## Segurança

### Medidas Implementadas
- Validação de nomes de arquivo (secure_filename)
- Controle de tipos de arquivo
- Limite de tamanho de upload
- Sanitização de caminhos

### Recomendações
- Usar HTTPS em produção
- Implementar autenticação se necessário
- Validar dados de entrada mais rigorosamente
- Implementar rate limiting

## Performance

### Otimizações
- Visualização limitada (30×30) para matrizes grandes
- Processamento em lote para análise GRASPE
- Cache de resultados em arquivos CSV
- Reutilização de cálculos quando possível

### Limitações
- Arquivos muito grandes podem causar lentidão
- Análise GRASPE limitada a 50 combinações por padrão
- Interface pode ser lenta com muitos dados

## Manutenção

### Logs
- Servidor Flask gera logs automáticos
- Prints de debug em operações críticas
- Rastreamento de uploads e processamento

### Backup
- Arquivos na pasta `uploads/` devem ser backupeados
- Matrizes geradas são preservadas automaticamente
- Configurações em `pyproject.toml`

### Atualizações
- Verificar compatibilidade de dependências
- Testar com diferentes tipos de dados
- Monitorar performance com arquivos grandes

## Contribuição

### Estrutura do Código
- Comentários em português
- Funções bem documentadas
- Separação clara de responsabilidades
- Padrões consistentes de nomenclatura

### Extensões Possíveis
- Interface mais avançada
- Algoritmos adicionais de análise
- Exportação para outros formatos
- API REST para integração
- Autenticação e multi-usuário