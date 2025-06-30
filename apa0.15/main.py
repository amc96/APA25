#!/usr/bin/env python3
"""
Aplicativo de Análise de Parentesco - GRASPE
Main entry point for the kinship analysis application.
"""

import os
import sys

# Adicionar o diretório atual ao path do Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """
    Main function to start the Flask application.
    """
    print("======================================")
    print("   Aplicativo de Análise de Parentesco")
    print("======================================")
    print()
    
    # Verificar se o app.py existe
    if not os.path.exists('app.py'):
        print("Erro: arquivo app.py não encontrado!")
        sys.exit(1)
    
    # Criar pasta uploads se não existir
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("Pasta 'uploads' criada com sucesso!")
    
    # Importar e executar a aplicação Flask
    try:
        print("Carregando módulos...")
        from app import app
        print("Aplicação carregada com sucesso!")
        print()
        print("Iniciando servidor...")
        print("Acesse: http://localhost:5000")
        print("Pressione Ctrl+C para parar")
        print()
        
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except ImportError as e:
        print(f"Erro ao importar aplicação: {e}")
        print("Certifique-se de que todas as dependências estão instaladas:")
        print("pip install flask pandas numpy werkzeug")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()