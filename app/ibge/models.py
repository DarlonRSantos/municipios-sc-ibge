from app.extensions import db

class Municipio(db.Model):
    __tablename__ = 'municipios'
    id = db.Column(db.String(36), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    codigo_ibge = db.Column(db.Integer, nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    
    def __repr__(self):
        return f'<Municipio {self.nome}>'