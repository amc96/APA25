# Replit.md - Aplicativo de Análise de Parentesco

## Overview

Este é um aplicativo web completo construído com Flask que analisa dados de parentesco entre animais usando o método GRASPE (Genetic Relationship Analysis for Strategic Pairing Enhancement). O sistema converte arquivos CSV em matrizes de relacionamento, identifica combinações ótimas de cruzamento e calcula estatísticas incluindo a média dos melhores cruzamentos.

## System Architecture

### Frontend Architecture
- **Technology**: HTML templates with Bootstrap 5 para UI responsiva
- **Template Engine**: Jinja2 (padrão do Flask)
- **Styling**: Bootstrap CSS framework para interface limpa e mobile-responsive
- **Pages**: 
  - Index page para upload de arquivos
  - Página de visualização para matriz e resultados com estatísticas
  - Página de erro para tratamento de exceções

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Design modular com arquivos separados por responsabilidade
- **Processing Pipeline**: CSV → Conversão de Matriz → Análise GRASPE → Exibição de Resultados
- **File Handling**: Upload seguro de arquivos com validação e armazenamento temporário

## Key Components

### 1. Flask Application (app.py)
- **Purpose**: Servidor web principal e manipulação de rotas
- **Key Routes**:
  - `/` - Upload e processamento de arquivos
  - `/visualizar/<filename>` - Visualização da matriz
  - `/download/<filename>` - Download de arquivos
  - `/download_cruzamentos_csv` - Download de resultados dos cruzamentos
- **Features**: Validação de arquivos, tratamento de erros, mensagens flash

### 2. CSV to Matrix Converter (csv_to_matrix.py)
- **Purpose**: Transforma dados CSV em matrizes de relacionamento
- **Input Format**: CSV com colunas Animal_1, Animal_2, Coef
- **Output**: Pandas DataFrame matriz com animais como linhas/colunas
- **Statistics**: Calcula dimensões da matriz e estatísticas básicas

### 3. GRASPE Algorithm (graspe.py) - ATUALIZADO
- **Purpose**: Implementa o método de otimização GRASPE
- **Algorithm**: GRASP (Greedy Randomized Adaptive Search Procedure)
- **Functionality**: Encontra combinações ótimas de cruzamento baseadas em coeficientes de relacionamento
- **NEW**: Calcula média dos coeficientes dos melhores cruzamentos
- **NEW**: Retorna estrutura completa com estatísticas (valor objetivo, média, total)
- **Optimization**: Usa busca local para melhorar soluções iniciais

### 4. Template System - ATUALIZADO
- **Base Framework**: Bootstrap 5 para estilo consistente
- **Responsive Design**: Interface amigável para dispositivos móveis
- **Data Visualization**: Tabelas HTML com exibição limitada (30x30) para performance
- **NEW**: Exibição de estatísticas dos cruzamentos incluindo média e qualidade

## Data Flow

1. **File Upload**: Usuário envia arquivo CSV pela interface web
2. **Validation**: Sistema valida formato e estrutura do arquivo
3. **Matrix Conversion**: Dados CSV são convertidos em matriz de relacionamento
4. **Statistics Calculation**: Estatísticas básicas são computadas
5. **GRASPE Analysis**: Algoritmo identifica combinações ótimas de cruzamento
6. **NEW**: Cálculo automático da média dos coeficientes
7. **Results Display**: Matriz e recomendações são mostradas ao usuário com estatísticas
8. **File Download**: Usuário pode baixar resultados processados

## External Dependencies

### Python Packages
- **Flask**: Framework web para a aplicação
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Suporte para computação numérica
- **Werkzeug**: Utilitários WSGI para manipulação segura de nomes de arquivo

### Frontend Dependencies
- **Bootstrap 5**: Framework CSS (carregado via CDN)
- **Bootstrap Icons**: Biblioteca de ícones para elementos da UI

### File System
- **Upload Directory**: Pasta `uploads/` para armazenamento temporário de arquivos
- **Template Directory**: `templates/` para templates HTML
- **Static Files**: CSS e JavaScript servidos através do Flask

## Deployment Strategy

### Local Development
- **Initialization Scripts**: 
  - `iniciar.bat` para Windows
  - `iniciar.sh` para Linux/Mac
- **Auto-setup**: Scripts lidam com instalação de dependências e inicialização do servidor
- **Local Server**: Executa em `localhost:5000`

### Configuration
- **File Limits**: 10MB tamanho máximo de upload
- **Allowed Formats**: Apenas arquivos CSV
- **Security**: Manipulação segura de nomes de arquivo e validação de arquivos
- **Session Management**: Chave secreta do Flask para segurança de sessão

### Platform Support
- **Cross-platform**: Funciona em Windows, macOS, e Linux
- **Python Environment**: Usa pyproject.toml para gerenciamento de dependências
- **Web Browser**: Qualquer navegador moderno para acesso à interface

## Recent Changes

### Atualizações de 29 de junho de 2025:
✓ Implementado cálculo da média dos coeficientes dos melhores cruzamentos
✓ Atualizado algoritmo GRASPE para retornar estrutura completa com estatísticas
✓ Modificado app.py para usar nova estrutura do GRASPE
✓ Adicionada classificação de qualidade (Excelente/Boa/Regular/Cuidado)
✓ Removidos arquivos desnecessários (.old, graspe_v2.py, uv.lock)
✓ Atualizado main.py para funcionar como ponto de entrada correto
✓ Configurado workflow "Aplicativo GRASPE" na porta 5000
✓ Implementadas múltiplas execuções GRASPE com parâmetros aleatórios
✓ Criado sistema de gráficos interativos com Chart.js
✓ Modificada tela de resultados para mostrar imediatamente após conversão
✓ Análise GRASPE executada automaticamente durante upload
✓ Removido limite de 50 execuções - agora sem limite máximo
✓ Interface completa com estatísticas avançadas e downloads organizados
✓ README.md atualizado com todas as novas funcionalidades

## User Preferences

```
Preferred communication style: Simple, everyday language in Portuguese.
```