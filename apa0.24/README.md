# Sistema de Otimização de Acasalamento Animal

![Sistema GRASP](https://img.shields.io/badge/Algoritmo-GRASP-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)

## Sobre o Sistema

Sistema web desenvolvido para otimizar acasalamentos de animais usando algoritmo GRASP (Greedy Randomized Adaptive Search Procedure), com o objetivo de minimizar coeficientes de coancestralidade entre a prole.

## Execução Única (Instala e Executa Automaticamente)

### Windows
```bash
# Clique duas vezes no arquivo:
executar_sistema.bat
```

### Linux/macOS
```bash
# No terminal, execute:
./executar_sistema.sh
```

O sistema irá:
1. Verificar se Python está instalado
2. Criar ambiente virtual (se necessário)
3. Instalar dependências (se necessário)
4. Iniciar a aplicação
5. Abrir o navegador automaticamente

**Nenhuma configuração manual necessária!**

## Estrutura do Projeto

```
├── app.py                    # Aplicação principal Streamlit
├── data_processor.py         # Processamento de dados
├── grasp_algorithm.py        # Algoritmo GRASP
├── executar_sistema.bat      # Executável único Windows
├── executar_sistema.sh       # Executável único Linux/macOS
├── dependencies.txt          # Lista de dependências
├── DOCUMENTACAO_TECNICA.md   # Documentação técnica completa
├── MANUAL_USUARIO.md         # Manual do usuário
├── README.md                 # Este arquivo
└── replit.md                 # Configurações do projeto
```

## Funcionalidades

- ✅ Upload de dados CSV com validação
- ✅ Algoritmo GRASP com parâmetros configuráveis
- ✅ Múltiplas execuções com comparação de resultados
- ✅ Visualizações interativas com Plotly
- ✅ Download de resultados em CSV
- ✅ Matriz de cruzamentos com destaques
- ✅ Interface em português brasileiro
- ✅ Redirecionamento automático para resultados

## Formato dos Dados

O arquivo CSV deve conter exatamente estas colunas:
- `Animal_1`: ID do primeiro animal
- `Animal_2`: ID do segundo animal
- `Coef`: Coeficiente de coancestralidade (decimal)

## Documentação

- **[Manual do Usuário](MANUAL_USUARIO.md)** - Guia completo para usar o sistema
- **[Documentação Técnica](DOCUMENTACAO_TECNICA.md)** - Detalhes técnicos e arquitetura

## Requisitos

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Plotly

## Desenvolvido para

**Projeto Acadêmico APA 2025/1**
*Universidade - Curso de Análise e Projeto de Algoritmos*

## Suporte

Para problemas técnicos, consulte:
1. [Manual do Usuário](MANUAL_USUARIO.md) - Seção "Solução de Problemas"
2. [Documentação Técnica](DOCUMENTACAO_TECNICA.md) - Seção "Troubleshooting"