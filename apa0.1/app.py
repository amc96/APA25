"""
Aplicação web para converter arquivo CSV em matriz.
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import pandas as pd
from werkzeug.utils import secure_filename
from csv_to_matrix import csv_to_matrix, get_matrix_statistics
from imports_especiais import processar_arquivo_csv, detectar_formato_csv

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para mensagens flash

# Configuração de upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar a pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    upload_status = None
    estatisticas = None
    arquivo_matriz = None
    formato_info = None
    
    if request.method == 'POST':
        # Verifica se foi enviado um arquivo
        if 'arquivo' not in request.files:
            flash('Nenhum arquivo enviado')
            return redirect(request.url)
        
        arquivo = request.files['arquivo']
        
        # Verifica se o usuário selecionou um arquivo
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        
        # Verifica se é um arquivo permitido
        if arquivo and arquivo.filename and allowed_file(arquivo.filename):
            # Salva o arquivo com nome seguro
            nome_arquivo = arquivo.filename  # Certifica que filename não é None
            filename = secure_filename(nome_arquivo)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(filepath)
            
            try:
                # Detecta o formato do arquivo e processa
                info_formato = detectar_formato_csv(filepath)
                formato_info = info_formato  # Para exibir na página
                
                if info_formato['formato'] == 'padrao':
                    # Se for o formato padrão, usa a função csv_to_matrix diretamente
                    matriz = csv_to_matrix(filepath)
                else:
                    # Caso contrário, processa o arquivo para o formato padrão primeiro
                    df_processado, _ = processar_arquivo_csv(filepath)
                    
                    # Salva o DataFrame processado em um arquivo temporário
                    temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
                    df_processado.to_csv(temp_filepath, index=False)
                    
                    # Converte o arquivo processado para matriz
                    matriz = csv_to_matrix(temp_filepath)
                    
                    # Remove o arquivo temporário
                    os.remove(temp_filepath)
                
                # Obtém estatísticas
                estatisticas = get_matrix_statistics(matriz)
                
                # Salva a matriz em CSV
                matriz_filename = f"matriz_{filename}"
                matriz_filepath = os.path.join(app.config['UPLOAD_FOLDER'], matriz_filename)
                matriz.to_csv(matriz_filepath)
                
                upload_status = 'sucesso'
                arquivo_matriz = matriz_filename
                
                flash(f'Arquivo convertido com sucesso! Formato detectado: {info_formato["formato"]}')
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
                           formato_info=formato_info)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/visualizar/<filename>')
def visualizar_matriz(filename):
    # Ler o arquivo CSV
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath, index_col=0)
    
    # Limitar o tamanho para visualização (apenas as primeiras linhas e colunas)
    max_rows = 20
    max_cols = 20
    df_amostra = df.iloc[:min(max_rows, df.shape[0]), :min(max_cols, df.shape[1])]
    
    return render_template('visualizar.html', 
                           filename=filename,
                           matriz=df_amostra.to_html(classes='table table-striped'),
                           linhas=df.shape[0],
                           colunas=df.shape[1])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)