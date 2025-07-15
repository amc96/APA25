# Manual do Usuário - Aplicativo de Análise de Parentesco

## Introdução

Este aplicativo ajuda você a analisar dados de parentesco entre animais e encontrar os melhores cruzamentos usando tecnologia avançada. É muito fácil de usar - basta fazer upload de um arquivo e ver os resultados!

## Como Começar

### Passo 1: Iniciar o Aplicativo

**No Windows:**
1. Clique duas vezes no arquivo `iniciar.bat`
2. Uma janela preta vai abrir e instalar tudo automaticamente
3. Aguarde até aparecer a mensagem "Iniciando o aplicativo..."

**No Mac/Linux:**
1. Abra o Terminal
2. Navegue até a pasta do aplicativo
3. Digite: `./iniciar.sh`
4. Pressione Enter e aguarde a instalação

### Passo 2: Acessar a Interface

1. Abra seu navegador (Chrome, Firefox, Safari...)
2. Digite na barra de endereço: `http://localhost:5000`
3. A página principal do aplicativo vai carregar

## Como Usar o Aplicativo

### Upload do Arquivo

1. **Clique em "Escolher arquivo"** na página principal
2. **Selecione seu arquivo CSV** com os dados de parentesco
3. **Clique em "Enviar Arquivo"**
4. Aguarde o processamento (pode levar alguns segundos)

### Formato do Arquivo CSV

Seu arquivo deve ter exatamente estas 3 colunas:

```
Animal_1,Animal_2,Coef
A001,A002,0.25
A001,A003,0.5
A002,A003,0.0
```

**Onde:**
- **Animal_1**: Código do primeiro animal
- **Animal_2**: Código do segundo animal  
- **Coef**: Valor do parentesco (número entre 0 e 1)

### Entendendo os Resultados

Após o upload, você verá:

#### Estatísticas Gerais
- **Total de registros**: Quantas linhas seu arquivo tinha
- **Animais únicos**: Quantos animais diferentes foram encontrados
- **Matriz gerada**: Tamanho da matriz criada

#### Visualizar Resultados

1. **Clique em "Visualizar Matriz"**
2. Você verá uma tabela com parte da matriz
3. **Scroll para baixo** para ver os **Melhores Cruzamentos**

### Melhores Cruzamentos

O aplicativo mostra os melhores cruzamentos ordenados por qualidade:

#### Códigos de Cores:
- 🟢 **Verde (0.0)**: Cruzamento ideal - sem parentesco
- 🔵 **Azul (0.0-0.25)**: Cruzamento bom - parentesco baixo
- 🟡 **Amarelo (0.25-0.5)**: Cruzamento aceitável - parentesco médio
- 🔴 **Vermelho (>0.5)**: Evitar - parentesco alto

#### Como Interpretar:
- **Coeficiente 0.0**: Animais sem parentesco - melhor opção
- **Coeficiente 0.25**: Parentesco distante - ainda aceitável
- **Coeficiente 0.5**: Parentesco próximo - cuidado
- **Coeficiente 1.0**: Mesmo animal ou parentesco total - evitar

#### Regras de Distribuição:
- **Animal_1 (linhas)**: Pode aparecer várias vezes nos cruzamentos
- **Animal_2 (colunas)**: Aparece apenas uma vez
- **Todos os Animal_2**: Recebem um cruzamento garantido
- **Limite por Animal_1**: Calculado automaticamente pela fórmula (Animal_2/Animal_1)+1

### Downloads Disponíveis

#### 1. Baixar Matriz Completa
- Arquivo CSV com toda a matriz de parentesco
- Útil para análises avançadas
- Contém todos os cruzamentos possíveis

#### 2. Baixar Resultados dos Cruzamentos
- Lista com os melhores cruzamentos encontrados
- Arquivo pronto para usar
- Ordenado do melhor para o pior

## Dicas Importantes

### Preparação do Arquivo

✅ **Faça assim:**
- Use apenas números e letras nos códigos dos animais
- Mantenha o formato CSV (separado por vírgulas)
- Valores de coeficiente entre 0 e 1
- Uma linha de cabeçalho com os nomes das colunas

❌ **Evite:**
- Caracteres especiais nos códigos (@, #, %, etc.)
- Valores de coeficiente maiores que 1
- Linhas vazias no arquivo
- Formatos diferentes de CSV

### Tamanho dos Arquivos

- **Máximo**: 10MB por arquivo
- **Recomendado**: Até 1MB para melhor performance
- **Muitos dados?** Divida em arquivos menores

### Resolução de Problemas

#### "Erro ao processar arquivo"
- Verifique se o arquivo tem as 3 colunas corretas
- Confirme se os valores de coeficiente são números
- Teste com um arquivo menor primeiro

#### "Arquivo não encontrado"
- Certifique-se de que enviou o arquivo corretamente
- Tente fazer upload novamente
- Verifique se o arquivo não está corrompido

#### "Nenhum cruzamento encontrado"
- Seus dados podem ter apenas valores inválidos (-1 ou 1.0)
- Verifique se há variedade nos coeficientes
- Confirme se os animais são diferentes entre si

## Exemplo Prático

### 1. Arquivo de Entrada (exemplo.csv):
```
Animal_1,Animal_2,Coef
Touro_001,Vaca_001,0.0
Touro_001,Vaca_002,0.25
Touro_002,Vaca_001,0.0
Touro_002,Vaca_002,0.5
```

### 2. Resultado dos Melhores Cruzamentos:
```
1. Touro_001 × Vaca_001 - Coeficiente: 0.0000 ✅
2. Touro_002 × Vaca_001 - Coeficiente: 0.0000 ✅
3. Touro_001 × Vaca_002 - Coeficiente: 0.2500 ⚠️
4. Touro_002 × Vaca_002 - Coeficiente: 0.5000 ❌
```

### 3. Interpretação:
- **Cruzamentos 1 e 2**: Ideais (sem parentesco)
- **Cruzamento 3**: Aceitável (parentesco baixo)
- **Cruzamento 4**: Evitar (parentesco alto)

## Perguntas Frequentes

### O aplicativo funciona offline?
Sim! Uma vez instalado, funciona completamente no seu computador sem internet.

### Posso usar com qualquer tipo de animal?
Sim! O aplicativo funciona com qualquer código que você usar (bovinos, suínos, aves, etc.).

### Os dados ficam seguros?
Sim! Todos os dados ficam apenas no seu computador, nada é enviado para a internet.

### Posso processar vários arquivos?
Sim! Você pode fazer upload de um arquivo por vez. Os resultados anteriores ficam salvos na pasta "uploads".

### Como parar o aplicativo?
Feche a janela do navegador e pressione Ctrl+C na janela preta (terminal) para parar o servidor.

## Suporte

Se tiver dúvidas ou problemas:

1. **Verifique este manual** primeiro
2. **Teste com um arquivo pequeno** para confirmar que funciona
3. **Confira o formato do seu arquivo CSV**
4. **Reinicie o aplicativo** se necessário

## Próximos Passos

Depois de dominar o básico:
- Experimente com diferentes tamanhos de arquivo
- Compare resultados de diferentes análises
- Use os arquivos baixados para suas próprias análises
- Mantenha um backup dos seus melhores resultados

**Aproveite o aplicativo e bons cruzamentos! 🐄🚀**