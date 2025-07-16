# 💼 EMITIR_NFSE

Automação em Python para emissão de Notas Fiscais de Serviço Eletrônicas (NFSe) via o portal nacional. Inclui login automatizado, busca e consulta de tomadores, preenchimento de dados e integração com Google Sheets.

## 📁 Estrutura do Projeto

EMITIR_NFSE/
│
├── src/ # Scripts principais da automação
│ ├── api_nfse.py
│ ├── emissao_nfse.py
│ ├── emissao_nfse_gsheets.py
│ ├── login_nfse.py
│ ├── buscar_tomador.py
│ └── consulta_tomador.py
│
├── credentials/ # Credenciais de acesso (não versionar)
│ └── credenciais_google.json
│
├── postman/ # Coleções Postman (opcional)
│
├── tests/ # Arquivos de teste ou desenvolvimento
│ └── teste.html
│
├── nfse-venv/ # Ambiente virtual (ignorado no Git)
├── .gitignore
├── requirements.txt
└── README.md


## 🚀 Funcionalidades

- Login automático no portal da NFSe Nacional
- Consulta e preenchimento de dados de tomadores
- Preenchimento automático dos campos da nota
- Integração com Google Sheets (via API)
- Suporte a geração de relatórios ou coleta de status
- Envio via mensageria (em integração futura)

## 🔧 Pré-requisitos

- Python 3.10+
- Conta Google com acesso a planilha (Sheets API ativada)
- Ambiente virtual configurado (`nfse-venv`)

## 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/emitir_nfse.git
cd emitir_nfse

# Crie e ative o ambiente virtual
python -m venv nfse-venv
source nfse-venv/bin/activate  # Linux/Mac
nfse-venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt


# ⚙️ Uso
- Adicione suas credenciais Google em credentials/credenciais_google.json.

- Configure os dados do login no portal da NFSe em login_nfse.py.

- Execute o script principal:

´python src/emissao_nfse_gsheets.py´


# 📄 Licença

Projeto privado de uso interno. Para uso comercial ou distribuição, consulte o autor.