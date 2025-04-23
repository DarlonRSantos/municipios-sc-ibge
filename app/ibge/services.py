import requests
import uuid
from flask import current_app
from app.ibge.models import Municipio, db

def buscar_municipios_ibge(uf):
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios'

    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()

        for municipio in dados:
            codigo_ibge = municipio['id']
            nome = municipio['nome']
            uf_sigla = municipio['microrregiao']['mesorregiao']['UF']['sigla']

            existente = db.session.query(Municipio).filter_by(codigo_ibge=codigo_ibge).first()
            if not existente:
                novo = Municipio(
                    id=str(uuid.uuid4()),
                    nome=nome,
                    codigo_ibge=codigo_ibge,
                    uf=uf_sigla
                )
                db.session.add(novo)

        db.session.commit()
        return True, f"{len(dados)} municípios da UF {uf} foram salvos com sucesso."
    
    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao buscar municípios: {e}"