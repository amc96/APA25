# Conversor CSV para Matriz e Análise de Cruzamentos (GRASPE)

Sistema para análise de coeficientes de cruzamento animal, processamento de dados CSV e visualização de matrizes.

## Funcionalidades

- Upload de arquivos CSV com dados de coeficientes entre animais
- Conversão de tabelas para matrizes de coeficientes
- Análise estatística dos dados da matriz
- Método GRASPE para identificação de melhores cruzamentos
- Visualização de matriz e download do resultado

## Formato do Arquivo CSV Esperado

O arquivo CSV deve conter três colunas:
- `Animal_1`: Nome do primeiro animal
- `Animal_2`: Nome do segundo animal
- `Coef`: Valor do coeficiente de cruzamento entre os animais

Exemplo:
```
Animal_1,Animal_2,Coef
Touro1,Vaca1,0.0
Touro1,Vaca2,0.125
Vaca1,Vaca2,0.0
```

## Método GRASPE

O sistema implementa o método GRASPE para análise de cruzamentos que:
1. Descarta combinações com coeficiente igual a -1 (não válidas)
2. Prioriza cruzamentos com coeficiente 0 primeiro (sem parentesco)
3. Avança para valores gradualmente maiores (menor a maior)
4. Apresenta as melhores combinações de cruzamento

## Como Executar

### No Windows:
1. Execute o arquivo `iniciar.bat` com duplo clique
2. Aguarde a instalação das dependências e o inicio do servidor
3. Acesse no navegador: http://localhost:5000

### No Linux/Mac:
1. Abra um terminal na pasta do projeto
2. Execute `chmod +x iniciar.sh` para dar permissão de execução
3. Execute `./iniciar.sh`
4. Acesse no navegador: http://localhost:5000

## Executando sem Interface Web

Para testar o sistema sem a interface web, execute:
```
python simular_app.py
```

Este comando processará o arquivo de exemplo e mostrará os resultados no terminal.

## Arquivos do Projeto

- `app.py` - Aplicação Flask principal
- `csv_to_matrix.py` - Funções para processamento de dados e método GRASPE
- `exemplo_animais.csv` - Arquivo de exemplo para testes
- `iniciar.bat` / `iniciar.sh` - Scripts para fácil execução
- `simular_app.py` - Script para testar funcionalidades sem interface web
- `templates/` - Arquivos HTML para interface web
- `uploads/` - Pasta onde os arquivos enviados e matrizes são armazenados