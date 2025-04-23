from flask import render_template, request, flash, redirect, url_for, current_app
from app.ibge import ibge_bp
from app.ibge.services import buscar_municipios_ibge
from app.ibge.models import Municipio
from flask_login import login_required

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
        uf = request.form.get('uf', '').strip().upper()

        if not termo:
            mensagem = "Informe o nome de um município para buscar."
        else:
            query = Municipio.query.filter(Municipio.nome.ilike(f'%{termo}%'))
            if uf:
                query = query.filter_by(uf=uf)

            municipio = query.first()
            if municipio:
                resultado = {
                    'codigo': municipio.codigo_ibge,
                    'nome': municipio.nome,
                    'uf': municipio.uf
                }
            else:
                mensagem = f"Nenhum município encontrado com o nome '{termo}' na UF '{uf}'." if uf else f"Nenhum município encontrado com o nome '{termo}'."

    return render_template('ibge/busca.html', resultado=resultado, mensagem=mensagem)

@ibge_bp.route('/atualizar', methods=['POST'])
@login_required
def atualizar():
    uf = request.form.get('uf', '').strip().upper()
    if not uf:
        mensagem = "UF não selecionada. Por favor, selecione uma UF."
        return render_template('ibge/busca.html', resultado=None, mensagem=mensagem)

    sucesso, mensagem = buscar_municipios_ibge(uf)
    return render_template('ibge/busca.html', resultado=None, mensagem=mensagem)


#from flask import render_template, request, flash
#from app.ibge import ibge_bp
#from app.ibge.services import UF_PADRAO
#from app.ibge.services import buscar_municipios_ibge, ARQUIVO_MUNICIPIOS
#import os
#from flask_login import login_required
#from flask import current_app
#
#@ibge_bp.route('/')
#@login_required
#def index():
#    return redirect(url_for('ibge.busca'))
#
#@ibge_bp.route('/busca', methods=['GET', 'POST']) 
#
#@login_required
#def busca():
#    resultado = None
#    mensagem = None
#
#    if request.method == 'POST':
#        termo = request.form['municipio'].strip().lower()
#        
#        arquivo_path = os.path.join(current_app.root_path, 'ibge', ARQUIVO_MUNICIPIOS)
#        if os.path.exists(arquivo_path):
#            with open(arquivo_path, 'r', encoding='utf-8') as f:
#                for linha in f:
#                    if termo in linha.lower():
#                        partes = linha.strip().split(':')
#                        resultado = {
#                            'codigo': partes[0].strip(),
#                            'nome': partes[1].strip(),
#                            'uf': UF_PADRAO
#                        }
#                        break
#            if not resultado:
#                mensagem = f"Nenhum município encontrado com '{termo.capitalize()}'"
#        else:
#            mensagem = "Arquivo não encontrado. Atualize a lista primeiro."
#    
#    return render_template('ibge/busca.html', resultado=resultado, mensagem=mensagem)
#
#@ibge_bp.route('/atualizar', methods=['POST'])
#@login_required
##def atualizar():
##   sucesso, mensagem = buscar_municipios_ibge()
##  return render_template('ibge/busca.html', resultado=None, mensagem=mensagem)
#def atualizar():
#    uf = request.form.get('uf', '').strip().upper()
#    if not uf:
#        mensagem = "UF não selecionada. Por favor, selecione uma UF."
#        return render_template('ibge/busca.html', resultado=None, mensagem=mensagem)
#
#    sucesso, mensagem = buscar_municipios_ibge(uf)
#    return render_template('ibge/busca.html', resultado=None, mensagem=mensagem)
#
#from flask import redirect, url_for