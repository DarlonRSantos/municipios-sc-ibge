class Config:
    SECRET_KEY = 'sua-chave-secreta'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:T1#labella@localhost/ibge_app'  # Alterar conforme seu banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False