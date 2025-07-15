# Aplicativo de Análise de Parentesco - GRASPE

Sistema web avançado para análise de parentesco entre animais utilizando múltiplas execuções do método GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement) com parâmetros aleatórios.

## Características Principais

✅ **Interface Web Moderna** - Upload e visualização intuitiva com Bootstrap 5  
✅ **Múltiplas Execuções GRASPE** - Executa quantas vezes desejar com parâmetros aleatórios  
✅ **Gráficos Interativos** - Visualização das médias de todas as execuções  
✅ **Melhor Solução Global** - Salva e apresenta automaticamente a melhor solução encontrada  
✅ **Estatísticas Avançadas** - Média das médias, melhor e pior resultado  
✅ **Cálculo Automático de Média** - Média dos coeficientes dos melhores cruzamentos  
✅ **Classificação de Qualidade** - Sistema de cores para avaliar qualidade dos cruzamentos  
✅ **Processamento Inteligente** - Converte CSV em matriz de parentesco automaticamente  
✅ **Download Completo** - Exporta resultados detalhados em CSV  
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

### Passo a Passo:
1. **Upload**: Envie arquivo CSV com dados de parentesco (Animal_1, Animal_2, Coef)
2. **Configuração**: Escolha o número de execuções (recomendado: 5-20)
3. **Processamento**: Sistema executa múltiplas análises GRASPE com parâmetros aleatórios
4. **Resultados**: Visualize gráficos, estatísticas e a melhor solução encontrada
5. **Download**: Baixe resultados completos em formato CSV

### Parâmetros Avançados:
- **Execuções**: Sem limite (mais execuções = resultados mais precisos)
- **Iterações**: Aleatorização automática (30-100 por execução)
- **RCL (Lista de Candidatos)**: Aleatorização automática (2-6)

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