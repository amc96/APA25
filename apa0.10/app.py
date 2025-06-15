"""
Aplicação web para converter arquivo CSV em matriz e analisar cruzamentos.
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, send_from_directory
import os
import pandas as pd
from werkzeug.utils import secure_filename
from csv_to_matrix import csv_to_matrix, get_matrix_statistics, contagem_animais
from graspe import analisar_cruzamentos_graspe, ordenar_cruzamentos_por_coeficiente, filtrar_cruzamentos_inviaveis

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para mensagens flash

# Configuração de upload 
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Aumentar limite de tamanho de upload para 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Criar a pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Diretório de uploads: {UPLOAD_FOLDER}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    upload_status = None
    estatisticas = None
    arquivo_matriz = None
    contagem_animal1 = None
    contagem_animal2 = None
    
    if request.method == 'POST':
        # Verifica se foi enviado um arquivo
        if 'arquivo' not in request.files:
            flash('Nenhum arquivo enviado')
            print("Erro: Nenhum arquivo encontrado no formulário")
            return redirect(request.url)
        
        arquivo = request.files['arquivo']
        
        # Verifica se o usuário selecionou um arquivo
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado')
            print("Erro: Nome de arquivo vazio")
            return redirect(request.url)
        
        # Verifica se é um arquivo permitido
        if arquivo and arquivo.filename and allowed_file(arquivo.filename):
            try:
                # Salva o arquivo com nome seguro
                nome_arquivo = arquivo.filename  # Certifica que filename não é None
                filename = secure_filename(nome_arquivo)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"Tentando salvar arquivo em: {filepath}")
                arquivo.save(filepath)
                print(f"Arquivo salvo com sucesso em: {filepath}")
            except Exception as e:
                flash(f'Erro ao salvar arquivo: {str(e)}')
                print(f"Erro ao salvar arquivo: {str(e)}")
                return redirect(request.url)
            
            try:
                # Obter contagens de animais
                contagem = contagem_animais(filepath)
                if contagem:
                    contagem_animal1 = contagem['Animal_1']
                    contagem_animal2 = contagem['Animal_2']
                
                # Converte o CSV para matriz
                matriz = csv_to_matrix(filepath)
                
                # Obtém estatísticas
                estatisticas = get_matrix_statistics(matriz)
                
                # Adiciona informação sobre o total de animais na matriz
                if hasattr(matriz, 'attrs') and 'total_animais' in matriz.attrs:
                    estatisticas['total_animais'] = matriz.attrs['total_animais']
                
                # Calcular melhores cruzamentos usando método GRASPE
                print("Calculando melhores cruzamentos com método GRASPE...")
                
                # Salva a matriz em CSV
                matriz_filename = f"matriz_{filename}"
                matriz_filepath = os.path.join(app.config['UPLOAD_FOLDER'], matriz_filename)
                matriz.to_csv(matriz_filepath)
                
                upload_status = 'sucesso'
                arquivo_matriz = matriz_filename
                
                flash('Arquivo convertido com sucesso! Visualize a matriz para ver os melhores cruzamentos.')
            except Exception as e:
                upload_status = 'erro'
                flash(f'Erro ao processar o arquivo: {str(e)}')
        else:
            upload_status = 'erro'
            flash('Tipo de arquivo não permitido. Por favor, envie um arquivo CSV.')
    
    return render_template('index.html', 
                           upload_status=upload_status, 
                           estatisticas=estatisticas,
                           arquivo_matriz=arquivo_matriz,
                           contagem_animal1=contagem_animal1,
                           contagem_animal2=contagem_animal2)

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Tentando baixar arquivo: {filepath}")
    if os.path.exists(filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        flash(f"Arquivo não encontrado: {filename}")
        return redirect(url_for('index'))

@app.route('/download_cruzamentos_csv')
def download_cruzamentos_csv():
    """Gera e baixa um CSV com os melhores cruzamentos da análise atual."""
    try:
        # Buscar o arquivo de matriz mais recente
        matriz_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.startswith('matriz_') and f.endswith('.csv')]
        
        if not matriz_files:
            flash('Nenhuma matriz encontrada. Faça upload de um arquivo primeiro.')
            return redirect(url_for('index'))
        
        # Pegar o arquivo mais recente
        matriz_files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
        latest_matriz = matriz_files[0]
        
        # Ler a matriz
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], latest_matriz)
        df = pd.read_csv(filepath, index_col=0)
        
        # Analisar os melhores cruzamentos
        melhores_cruzamentos = analisar_cruzamentos_graspe(df, limite_combinacoes=50)
        
        if not melhores_cruzamentos:
            flash('Nenhum cruzamento válido encontrado.')
            return redirect(url_for('index'))
        
        # Criar DataFrame com os resultados
        df_resultados = pd.DataFrame(melhores_cruzamentos)
        
        # Salvar CSV temporário
        csv_filename = 'melhores_cruzamentos_resultado.csv'
        csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        df_resultados.to_csv(csv_filepath, index=False, encoding='utf-8')
        
        return send_from_directory(app.config['UPLOAD_FOLDER'], csv_filename, 
                                 as_attachment=True, 
                                 download_name='melhores_cruzamentos.csv')
        
    except Exception as e:
        flash(f'Erro ao gerar arquivo CSV: {str(e)}')
        return redirect(url_for('index'))

@app.route('/visualizar/<filename>')
def visualizar_matriz(filename):
    try:
        # Ler o arquivo CSV
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Lendo arquivo da matriz: {filepath}")
        df = pd.read_csv(filepath, index_col=0)
        
        # Limitar o tamanho para visualização (30x30 conforme solicitado)
        max_rows = 30
        max_cols = 30
        df_amostra = df.iloc[:min(max_rows, df.shape[0]), :min(max_cols, df.shape[1])]
        
        # Obter contagens se disponíveis
        contagem_animal1 = None
        contagem_animal2 = None
        
        # Analisar os melhores cruzamentos usando método GRASPE
        print("Iniciando análise GRASPE para encontrar melhores cruzamentos...")
        melhores_cruzamentos = analisar_cruzamentos_graspe(df, limite_combinacoes=30)
        print(f"Foram encontrados {len(melhores_cruzamentos)} cruzamentos potenciais.")
        
        # Imprimir primeiros 3 cruzamentos para depuração
        for i, comb in enumerate(melhores_cruzamentos[:3], 1):
            print(f"Cruzamento {i}: {comb['Animal_1']} × {comb['Animal_2']} - Coef: {comb['Coeficiente']}")
        
        try:
            # Tentar obter contagens do arquivo original
            arquivo_original = filename.replace("matriz_", "")
            arquivo_original_path = os.path.join(app.config['UPLOAD_FOLDER'], arquivo_original)
            
            if os.path.exists(arquivo_original_path):
                contagem = contagem_animais(arquivo_original_path)
                if contagem:
                    contagem_animal1 = contagem['Animal_1']
                    contagem_animal2 = contagem['Animal_2']
        except Exception as e:
            # Se houver qualquer erro, apenas continuar sem as contagens
            print(f"Erro ao obter contagens: {str(e)}")
            pass
    except Exception as e:
        flash(f"Erro ao processar a matriz: {str(e)}")
        print(f"Erro ao processar a matriz: {str(e)}")
        return redirect(url_for('index'))
    
    return render_template('visualizar.html', 
                           filename=filename,
                           matriz=df_amostra.to_html(classes='table table-striped'),
                           linhas=df.shape[0],
                           colunas=df.shape[1],
                           contagem_animal1=contagem_animal1,
                           contagem_animal2=contagem_animal2,
                           melhores_cruzamentos=melhores_cruzamentos)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)