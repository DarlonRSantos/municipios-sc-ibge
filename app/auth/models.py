from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    ultimo_login = db.Column(db.DateTime)
    
    
    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        if 'senha' in kwargs:
            self.set_senha(kwargs['senha'])

    def set_senha(self, senha):
        """Gera um hash seguro para a senha"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
        """Verifica se a senha corresponde ao hash armazenado"""
        return check_password_hash(self.senha_hash, senha)

    def atualizar_login(self):
        """Registra o momento do último login"""
        self.ultimo_login = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Usuario {self.email}>'