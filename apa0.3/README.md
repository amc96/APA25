# Conversor CSV para Matriz

Este projeto converte arquivos CSV de relacionamento entre animais em uma representação de matriz, com Animal_2 nas linhas e Animal_1 nas colunas.

## Funcionalidades

- Conversão de arquivos CSV para matriz
- Interface web para upload de arquivos
- Visualização das estatísticas da matriz
- Download da matriz resultante em formato CSV
- Visualização de amostra da matriz na interface web

## Requisitos

- Python 3.6 ou superior
- Bibliotecas: pandas, numpy, matplotlib, flask

## Como executar

### Windows

1. Dê um duplo clique no arquivo `iniciar.bat`
2. O script instalará as dependências necessárias e iniciará a aplicação web
3. Acesse a aplicação em seu navegador através da URL: http://localhost:5000

### Linux/Mac

1. Abra o terminal na pasta do projeto
2. Execute o comando: `./iniciar.sh`
3. O script instalará as dependências necessárias e iniciará a aplicação web
4. Acesse a aplicação em seu navegador através da URL: http://localhost:5000

## Uso manual (sem scripts)

### Instalação das dependências

```bash
pip install pandas numpy matplotlib flask
```

### Executar a aplicação

```bash
python app.py
```

## Estrutura do projeto

- `app.py` - Aplicação web Flask
- `csv_to_matrix.py` - Módulo principal para conversão de CSV para matriz
- `converter_exemplo.py` - Exemplo de uso do módulo via linha de comando
- `templates/` - Diretório com os templates HTML da interface web
- `uploads/` - Diretório onde os arquivos enviados são armazenados