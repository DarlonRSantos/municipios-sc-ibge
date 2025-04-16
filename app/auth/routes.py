from flask import render_template, request, redirect, url_for, flash
from app.auth import auth_bp
from app.auth.models import Usuario
from app.extensions import db
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ibge.busca'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        lembrar = bool(request.form.get('lembrar', False))

        usuario = Usuario.query.filter_by(email=email).first()

        # Verificação em etapas para segurança
        if not usuario:
            flash('Credenciais inválidas', 'error')
        elif not usuario.ativo:
            flash('Conta desativada. Entre em contato com o suporte.', 'warning')
        elif not usuario.check_senha(senha):
            flash('Credenciais inválidas', 'error')
        else:
            login_user(usuario, remember=lembrar)
            usuario.atualizar_login()
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('ibge.busca'))

        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('ibge.busca'))

    if request.method == 'POST':
        try:
            nome = request.form.get('nome', '').strip()
            email = request.form.get('email', '').strip().lower()
            senha = request.form.get('senha', '')

            # Validações básicas
            if not all([nome, email, senha]):
                flash('Preencha todos os campos obrigatórios', 'error')
            elif len(senha) < 8:
                flash('A senha deve ter pelo menos 8 caracteres', 'error')
            elif Usuario.query.filter_by(email=email).first():
                flash('E-mail já cadastrado', 'error')
            else:
                novo_usuario = Usuario(
                    nome=nome,
                    email=email,
                    ativo=True
                )
                novo_usuario.set_senha(senha)
                
                db.session.add(novo_usuario)
                db.session.commit()
                
                flash('Cadastro realizado com sucesso! Faça seu login.', 'success')
                return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash('Erro ao processar cadastro. Tente novamente.', 'error')
            # Em produção, logar o erro: logging.error(f"Erro no cadastro: {str(e)}")

        return redirect(url_for('auth.cadastro'))

    return render_template('auth/cadastro.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('auth.login'))