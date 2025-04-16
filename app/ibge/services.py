import requests
import os
from flask import current_app

ARQUIVO_MUNICIPIOS = 'municipios.txt'
UF_PADRAO = 'SC'  # Estado padrão para consulta

def buscar_municipios_ibge():
    """Busca os municípios da API do IBGE e salva no arquivo"""
    try:
        print("Conectando ao IBGE...")
        url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF_PADRAO}/municipios'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        municipios = []
        for municipio in response.json():
            municipios.append(f"{municipio['id']}: {municipio['nome']}")
        
        # Criar o diretório para o arquivo se não existir
        os.makedirs(os.path.dirname(os.path.join(current_app.root_path, 'ibge', ARQUIVO_MUNICIPIOS)), exist_ok=True)
        
        # Salvar dados em um arquivo
        with open(os.path.join(current_app.root_path, 'ibge', ARQUIVO_MUNICIPIOS), 'w', encoding='utf-8') as f:
            f.write('\n'.join(municipios))
        
        msg = f"Lista atualizada! {len(municipios)} municípios de {UF_PADRAO} salvos."
        print(msg)
        return True, msg
    except Exception as e:
        msg = f"Erro ao acessar IBGE: {str(e)}"
        print(msg)
        return False, msg
