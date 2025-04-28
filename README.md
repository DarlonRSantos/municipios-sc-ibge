# Consulta Municípios IBGE - Santa Catarina 🏙️

Este projeto permite consultar dados de municípios do estado de Santa Catarina usando a API do IBGE. Ele oferece uma interface web simples para realizar buscas pelo nome do município, retornando o código IBGE correspondente. Também grava os resutados da consultas na API no banco de dados.
---

## 📌 Funcionalidades

- Consulta de municípios pela API do IBGE
- Grava lista de municipios do estado selecionado no banco de dados
- Interface web para busca
- Retorno com código do município
- Preparado para ser executado localmente ou via Kubernetes

---

## 🖥️ Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- HTML5 (Jinja2 templates)
- [API IBGE](https://servicodados.ibge.gov.br/)
- [Kubernetes](https://kubernetes.io/) (YAMLs de deploy inclusos)

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3 instalado
- `pip` (gerenciador de pacotes)

### Instalação

1. Clone o repositório:

   git clone https://github.com/DarlonRSantos/consulta-municipios-ibge.git
   cd consulta-municipios-ibge