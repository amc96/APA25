"""
Script para simular o fluxo completo da aplicação usando o arquivo de exemplo
"""
import os
import shutil
from csv_to_matrix import csv_to_matrix, get_matrix_statistics, contagem_animais
from graspe import analisar_cruzamentos_graspe

def simular_processamento_csv():
    # Configuração básica
    arquivo_exemplo = 'exemplo_animais.csv'
    pasta_uploads = 'uploads'
    
    # Criar pasta de uploads se não existir
    os.makedirs(pasta_uploads, exist_ok=True)
    
    # Copiar o arquivo de exemplo para a pasta de uploads
    arquivo_destino = os.path.join(pasta_uploads, arquivo_exemplo)
    shutil.copy(arquivo_exemplo, arquivo_destino)
    print(f"✓ Arquivo copiado para {arquivo_destino}")
    
    # Simular o processamento feito pelo aplicativo Flask
    try:
        # Passo 1: Converter CSV para matriz
        print("\n1. Convertendo CSV para matriz...")
        matriz = csv_to_matrix(arquivo_destino)
        print(f"   ✓ Matriz criada com dimensões: {matriz.shape[0]}x{matriz.shape[1]}")
        
        # Passo 2: Obter estatísticas
        print("\n2. Calculando estatísticas...")
        estatisticas = get_matrix_statistics(matriz)
        print("   ✓ Estatísticas calculadas:")
        for chave, valor in estatisticas.items():
            if isinstance(valor, float):
                print(f"      - {chave}: {valor:.4f}")
            else:
                print(f"      - {chave}: {valor}")
        
        # Passo 3: Obter contagem de animais
        print("\n3. Contando animais...")
        contagem = contagem_animais(arquivo_destino)
        print(f"   ✓ Total de animais em Animal_1: {contagem['Animal_1']['Total de animais distintos']}")
        print(f"   ✓ Total de animais em Animal_2: {contagem['Animal_2']['Total de animais distintos']}")
        print(f"   ✓ Lista de animais em Animal_1: {', '.join(contagem['Animal_1']['Lista de animais'])}")
        print(f"   ✓ Lista de animais em Animal_2: {', '.join(contagem['Animal_2']['Lista de animais'])}")
        
        # Passo 4: Executar o método GRASPE
        print("\n4. Analisando cruzamentos usando método GRASPE...")
        melhores_cruzamentos = analisar_cruzamentos_graspe(matriz, limite_combinacoes=10)
        print("   ✓ Melhores combinações encontradas:")
        for i, comb in enumerate(melhores_cruzamentos, 1):
            print(f"      {i}. {comb['Animal_1']} × {comb['Animal_2']} - Coeficiente: {comb['Coeficiente']:.4f}")
        
        # Passo 5: Salvar a matriz em CSV (simulando o download)
        matriz_filename = f"matriz_{arquivo_exemplo}"
        matriz_filepath = os.path.join(pasta_uploads, matriz_filename)
        matriz.to_csv(matriz_filepath)
        print(f"\n5. Matriz salva em: {matriz_filepath}")
        
        return True
    except Exception as e:
        print(f"\n❌ Erro durante a simulação: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("   SIMULAÇÃO DO PROCESSO COMPLETO DA APLICAÇÃO")
    print("=" * 60)
    
    resultado = simular_processamento_csv()
    
    if resultado:
        print("\n✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\nTodas as funcionalidades da aplicação estão operando corretamente:")
        print("1. Conversão de CSV para matriz")
        print("2. Cálculo de estatísticas")
        print("3. Contagem de animais")
        print("4. Análise de cruzamentos (método GRASPE)")
        print("5. Geração de arquivo CSV da matriz")
    else:
        print("\n❌ SIMULAÇÃO FALHOU!")
        print("Verifique os erros acima.")