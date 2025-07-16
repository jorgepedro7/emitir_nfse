import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# ===== CONFIG GOOGLE =====
SERVICE_ACCOUNT_FILE = './credenciais_google.json'
SPREADSHEET_ID = '1A4RIW0ClgGWzegtJnJ3td_GKFZ3TRAR8jlZ8Emd_fPM'
NOME_ABA_CLIENTES = "Dados Clientes JL - 2"

# ===== LOGIN NO PORTAL NFSe =====
def login_nfse():
    login_url = "https://www.nfse.gov.br/EmissorNacional/Login"
    session = requests.Session()
    response = session.get(login_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        token_element = soup.find('input', {'name': '__RequestVerificationToken'})
        token = token_element['value'] if token_element else None   

        if token:
            print(f"Token encontrado: {token}")
            login_data = {
                "__RequestVerificationToken": token,
                "Inscricao": "46.964.533/0001-94",
                "Senha": "Ludimila05"
            }   

            headers = {
                "Host": "www.nfse.gov.br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                "Origin": "https://www.nfse.gov.br",
                "Referer": "https://www.nfse.gov.br/EmissorNacional/Login",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
                "Content-Type": "application/x-www-form-urlencoded",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                "Upgrade-Insecure-Requests": "1"
            }

            login_response = session.post(login_url, headers=headers, data=login_data)
            if login_response.status_code == 200:
                print("Login bem-sucedido!")
                return session
            else:
                print(f"Falha no login: {login_response.status_code}")  
        else:
            print("Token de verificação não encontrado.")
    else:
        print(f"Falha ao acessar a página de login: {response.status_code}")    
    return None

# ===== LER CNPJs DA PLANILHA =====
def ler_clientes_planilha():
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(NOME_ABA_CLIENTES)
    return sheet.get_all_records()

# ===== BUSCAR DADOS DO TOMADOR =====
def buscar_dados_tomador(session, cnpj, data_competencia):
    url = f"https://www.nfse.gov.br/emissornacional/api/EmissaoDPS/RecuperarInfoPessoaJuridicaTomador/{cnpj}?data={data_competencia}"
    headers = {
        "Host": "www.nfse.gov.br",  
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.nfse.gov.br/EmissorNacional/DPS/Pessoas",
        "Connection": "keep-alive", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Falha ao buscar dados do tomador: {response.status_code}")
        print(f"Response Text: {response.text}")
        return None

# ===== ESCREVER DADOS NA PLANILHA =====
def escrever_dados_tomadores_na_planilha(dados_tomadores):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(NOME_ABA_CLIENTES)

    # Cabeçalhos esperados
    headers = [
        "CNPJ", "Razão Social", "País", "CEP", "Código Município",
        "Município", "Bairro", "Logradouro", "Número", "Complemento"
    ]
    sheet.clear()
    sheet.append_row(headers)

    for dados in dados_tomadores:
        linha = [
            dados.get('inscricao', ''),
            dados.get('nomerazaosocial', ''),
            dados.get('codigopais', ''),
            dados.get('cep', ''),
            dados.get('codigoibgemunicipio', ''),
            dados.get('nomemunicipio', ''),
            dados.get('bairro', ''),
            dados.get('logradouro', ''),
            dados.get('numero', ''),
            dados.get('complemento', '')
        ]
        sheet.append_row(linha, value_input_option='USER_ENTERED')

# ===== EXECUÇÃO PRINCIPAL =====
if __name__ == "__main__":
    session = login_nfse()
    if session:
        clientes = ler_clientes_planilha()
        dados_coletados = []
        for cliente in clientes:
            cnpj_tomador = cliente.get('CNPJ')
            if cnpj_tomador:
                cnpj_tomador = cnpj_tomador.replace('.', '').replace('/', '').replace('-', '')
                data_competencia = "2025-04-01"
                tomador_data = buscar_dados_tomador(session, cnpj_tomador, data_competencia)
                if tomador_data:
                    print(f"Dados do tomador {cnpj_tomador}: {tomador_data}")
                    dados_coletados.append(tomador_data)
                else:
                    print(f"Não foi possível obter dados para o tomador {cnpj_tomador}.")

        if dados_coletados:
            escrever_dados_tomadores_na_planilha(dados_coletados)
            print("✅ Planilha atualizada com sucesso!")
        else:
            print("⚠️ Nenhum dado foi coletado.")
    else:
        print("❌ Não foi possível iniciar a sessão de login.")
