"""
Script para testar a funcionalidade de análise de cruzamentos GRASPE
"""
from csv_to_matrix import csv_to_matrix, analisar_cruzamentos_graspe

def testar_analise_graspe():
    # Carregar o arquivo CSV de exemplo e converter para matriz
    arquivo_exemplo = 'exemplo_animais.csv'
    print(f"Carregando arquivo: {arquivo_exemplo}")
    
    try:
        # Converter CSV em matriz
        matriz = csv_to_matrix(arquivo_exemplo)
        print(f"Matriz criada com sucesso. Dimensões: {matriz.shape[0]}x{matriz.shape[1]}")
        
        # Analisar os melhores cruzamentos
        melhores_cruzamentos = analisar_cruzamentos_graspe(matriz, limite_combinacoes=10)
        
        # Exibir resultados
        print("\n=== Melhores Combinações de Cruzamento (Método GRASPE) ===")
        print("Combinações ordenadas priorizando coeficiente 0, depois valores crescentes")
        for i, comb in enumerate(melhores_cruzamentos, 1):
            print(f"{i}. {comb['Animal_1']} x {comb['Animal_2']} - Coeficiente: {comb['Coeficiente']:.4f}")
            
        return True
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    testar_analise_graspe()