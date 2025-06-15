"""
Script para verificar duplicidade entre os vetores Animal_1 e Animal_2,
removendo animais duplicados do vetor_animal2.
"""

import pandas as pd
import sys

def verificar_e_remover_duplicados():
    """
    Verifica duplicidade entre vetor_animal1.csv e vetor_animal2.csv,
    removendo animais duplicados do vetor_animal2.
    """
    try:
        # Carregar os vetores
        print("Carregando vetores existentes...")
        df_animal1 = pd.read_csv('vetor_animal1.csv')
        df_animal2 = pd.read_csv('vetor_animal2.csv')
        
        # Obter listas de animais
        animal1 = df_animal1['Animal_1'].tolist()
        animal2 = df_animal2['Animal_2'].tolist()
        
        print(f"Vetor Animal_1: {len(animal1)} animais")
        print(f"Vetor Animal_2: {len(animal2)} animais")
        
        # Encontrar animais duplicados (presentes em ambos vetores)
        set_animal1 = set(animal1)
        set_animal2 = set(animal2)
        
        duplicados = set_animal1.intersection(set_animal2)
        unicos_animal1 = set_animal1 - set_animal2
        unicos_animal2 = set_animal2 - set_animal1
        
        print(f"\nAnálise de duplicidade:")
        print(f"- Animais presentes em ambos vetores: {len(duplicados)}")
        print(f"- Animais exclusivos do vetor Animal_1: {len(unicos_animal1)}")
        print(f"- Animais exclusivos do vetor Animal_2: {len(unicos_animal2)}")
        
        # Se houver duplicados, removê-los do vetor_animal2
        if duplicados:
            print(f"\nRemovendo {len(duplicados)} animais duplicados do vetor Animal_2...")
            
            # Criar novo vetor Animal_2 sem os duplicados
            animal2_sem_duplicados = sorted(list(unicos_animal2))
            
            # Salvar o novo vetor Animal_2
            df_animal2_novo = pd.DataFrame(animal2_sem_duplicados, columns=['Animal_2'])
            df_animal2_novo.to_csv('vetor_animal2_sem_duplicados.csv', index=False)
            
            print(f"Novo vetor Animal_2 criado: {len(animal2_sem_duplicados)} animais")
            print("Salvo em: vetor_animal2_sem_duplicados.csv")
            
            # Exibir amostras do novo vetor
            if animal2_sem_duplicados:
                print("\nPrimeiros 5 valores do novo vetor Animal_2:")
                for i, animal in enumerate(animal2_sem_duplicados[:5]):
                    print(f"  {i+1}. {animal}")
            else:
                print("\nAtenção: O novo vetor Animal_2 está vazio!")
        else:
            print("\nNão foram encontrados animais duplicados entre os vetores.")
        
        # Criar um resumo dos resultados
        if duplicados:
            print("\nResumo dos duplicados:")
            duplicados_list = sorted(list(duplicados))
            for i, animal in enumerate(duplicados_list[:5]):
                print(f"  {i+1}. {animal}")
            
            if len(duplicados_list) > 5:
                print(f"  ... e mais {len(duplicados_list) - 5} animais")
        
    except Exception as e:
        print(f"Erro ao processar vetores: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_e_remover_duplicados()