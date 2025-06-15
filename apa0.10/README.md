# Aplicativo de Análise de Parentesco

Sistema web para análise de parentesco entre animais utilizando o método GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement).

## Características

✅ **Interface Web Amigável** - Upload e visualização simples  
✅ **Método GRASPE** - Algoritmo avançado para melhores cruzamentos  
✅ **Processamento Automático** - Converte CSV em matriz de parentesco  
✅ **Resultados Visuais** - Tabelas coloridas e estatísticas detalhadas  
✅ **Download de Dados** - Exporta resultados em CSV  
✅ **Multiplataforma** - Funciona no Windows, Mac e Linux  

## Início Rápido

### Windows
```bash
# Duplo clique em:
iniciar.bat
```

### Linux/Mac
```bash
# No terminal:
./iniciar.sh
```

### Acesso
Abra o navegador em: **http://localhost:5000**

## Como Usar

1. **Upload**: Envie arquivo CSV com dados de parentesco
2. **Processamento**: Sistema converte em matriz automaticamente
3. **Visualização**: Veja os melhores cruzamentos identificados
4. **Download**: Baixe resultados em formato CSV

## Formato dos Dados

```csv
Animal_1,Animal_2,Coef
A001,A002,0.25
A001,A003,0.0
A002,A003,0.5
```

## Documentação Completa

- 📖 **[Documentação Técnica](DOCUMENTACAO.md)** - Para desenvolvedores
- 👤 **[Manual do Usuário](MANUAL_USUARIO.md)** - Guia passo a passo

## Requisitos

- Python 3.11+
- Flask, pandas, numpy, werkzeug
- 10MB máximo por arquivo
- Formato CSV obrigatório

## Estrutura do Projeto

```
├── app.py                  # Aplicativo Flask principal
├── csv_to_matrix.py        # Conversão de CSV para matriz
├── graspe.py              # Algoritmo GRASPE
├── iniciar.bat            # Script Windows
├── iniciar.sh             # Script Linux/Mac
├── templates/             # Interface web
└── uploads/               # Arquivos do usuário
```