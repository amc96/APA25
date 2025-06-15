# Análise de Parentesco de Produtos (Método GRASPE)

Sistema otimizado para análise de coeficientes de parentesco entre produtos, processamento de dados CSV e visualização dos melhores cruzamentos.

## Funcionalidades

- Análise direta de arquivos CSV com dados de parentesco entre produtos
- Implementação otimizada do método GRASPE para grandes conjuntos de dados
- Identificação dos melhores cruzamentos priorizando coeficiente 0
- Visualização web dos resultados em formato amigável
- Exportação dos resultados em CSV

## Formato do Arquivo CSV Esperado

O arquivo CSV deve conter três colunas:
- `Animal_1`: Identificador do primeiro produto/animal
- `Animal_2`: Identificador do segundo produto/animal
- `Coef`: Valor do coeficiente de parentesco entre os produtos

Exemplo:
```
Animal_1,Animal_2,Coef
3925318_3926180,3926571_3927975,0.0
3925318_3926180,3926571_3929376,0.0
3925318_3926180,3925318_3927975,0.328125
```

## Método GRASPE

O sistema implementa o método GRASPE para análise de cruzamentos que:
1. Descarta combinações com coeficiente igual a -1 (não válidas)
2. Prioriza cruzamentos com coeficiente 0 primeiro (sem parentesco)
3. Avança para valores gradualmente maiores (menor a maior)
4. Apresenta as melhores combinações de cruzamento

## Como Executar

### Análise de Cruzamentos:
Para analisar um arquivo CSV e gerar a lista dos melhores cruzamentos:
```
python analisar_parentesco.py
```

### Visualização dos Resultados:
Para visualizar os resultados na interface web:
```
python app_resultados.py
```
Depois, acesse no navegador: http://localhost:5000

## Arquivos do Projeto

- `analisar_parentesco.py` - Script otimizado para análise de grandes arquivos CSV
- `graspe.py` - Implementação do método GRASPE para análise de cruzamentos
- `app_resultados.py` - Aplicação web para visualização dos resultados
- `melhores_cruzamentos.csv` - Arquivo com os resultados dos melhores cruzamentos
- `templates/` - Arquivos HTML para interface web
- `uploads/` - Pasta onde os arquivos de entrada são armazenados