from flask import Flask
from app.extensions import db, migrate, login_manager
from config import Config
import os
from app.ibge.models import Municipio
from app.auth.models import Usuario

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Registrar blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.ibge.routes import ibge_bp
    app.register_blueprint(ibge_bp)
    
    # Configurar erros
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Inicializar arquivo de municípios se não existir
    from app.ibge.services import buscar_municipios_ibge
    with app.app_context():
        if not os.path.exists(os.path.join(app.root_path, 'ibge', 'municipios.txt')):
            buscar_municipios_ibge()
    
    return app

from flask import render_template