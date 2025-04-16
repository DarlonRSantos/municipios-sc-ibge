from flask import render_template, request, flash
from app.ibge import ibge_bp
from app.ibge.services import UF_PADRAO
from app.ibge.services import buscar_municipios_ibge, ARQUIVO_MUNICIPIOS
import os
from flask_login import login_required
from flask import current_app

@ibge_bp.route('/')
@login_required
def index():
    return redirect(url_for('ibge.busca'))

@ibge_bp.route('/busca', methods=['GET', 'POST']) 

@login_required
def busca():
    resultado = None
    mensagem = None

    if request.method == 'POST':
        termo = request.form['municipio'].strip().lower()
        
        arquivo_path = os.path.join(current_app.root_path, 'ibge', ARQUIVO_MUNICIPIOS)
        if os.path.exists(arquivo_path):
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    if termo in linha.lower():
                        partes = linha.strip().split(':')
                        resultado = {
                            'codigo': partes[0].strip(),
                            'nome': partes[1].strip(),
                            'uf': UF_PADRAO
                        }
                        break
            if not resultado:
                mensagem = f"Nenhum município encontrado com '{termo.capitalize()}'"
        else:
            mensagem = "Arquivo não encontrado. Atualize a lista primeiro."
    
    return render_template('ibge/busca.html', resultado=resultado, mensagem=mensagem)

@ibge_bp.route('/atualizar', methods=['POST'])
@login_required
def atualizar():
    sucesso, mensagem = buscar_municipios_ibge()
    return render_template('ibge/busca.html', resultado=None, mensagem=mensagem)

from flask import redirect, url_for