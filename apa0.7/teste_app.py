"""
Script para testar as funcionalidades da aplicação
"""
import os
from csv_to_matrix import csv_to_matrix, analisar_cruzamentos_graspe

def testar_matriz_e_graspe():
    # Verificar se o arquivo de exemplo existe
    arquivo_exemplo = 'exemplo_animais.csv'
    if not os.path.exists(arquivo_exemplo):
        print(f"Erro: Arquivo {arquivo_exemplo} não encontrado.")
        return False
    
    print(f"Testando com arquivo: {arquivo_exemplo}")
    
    try:
        # Converter CSV em matriz
        matriz = csv_to_matrix(arquivo_exemplo)
        print(f"✓ Matriz criada com sucesso. Dimensões: {matriz.shape[0]}x{matriz.shape[1]}")
        
        # Obter algumas estatísticas básicas
        valores_diag = sum(matriz.loc[animal, animal] for animal in matriz.index)
        print(f"✓ Valores na diagonal principal: {valores_diag}")
        
        # Testar método GRASPE para análise de cruzamentos
        melhores_cruzamentos = analisar_cruzamentos_graspe(matriz, limite_combinacoes=5)
        
        print("\n=== Melhores Combinações de Cruzamento (Método GRASPE) ===")
        print("Combinações ordenadas priorizando coeficiente 0, depois valores crescentes")
        for i, comb in enumerate(melhores_cruzamentos, 1):
            print(f"{i}. {comb['Animal_1']} x {comb['Animal_2']} - Coeficiente: {comb['Coeficiente']:.4f}")
        
        print("\n✓ Análise GRASPE funcionando corretamente!")
        
        return True
    except Exception as e:
        print(f"✗ Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    sucesso = testar_matriz_e_graspe()
    
    if sucesso:
        print("\n=== Teste concluído com sucesso! ===")
        print("O aplicativo está funcionando corretamente.")
        print("\nPara usar a aplicação completa, execute:")
        print("python app.py")
        print("E acesse a interface web em um navegador.")
    else:
        print("\n=== Teste falhou! ===")
        print("Verifique os erros reportados acima.")