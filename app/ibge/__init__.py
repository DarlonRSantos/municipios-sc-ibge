from flask import Blueprint

ibge_bp = Blueprint('ibge', __name__, url_prefix='')

from app.ibge import routes