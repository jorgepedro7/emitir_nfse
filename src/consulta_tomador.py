import requests
from bs4 import BeautifulSoup

# Função para fazer login e retornar a sessão
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

# Função para buscar os dados do tomador
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
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    print(f"Fazendo requisição para URL: {url}")
    
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Falha ao buscar dados do tomador: {response.status_code}")
        print("Resposta:", response.text)
        return None

# Testar a consulta
session = login_nfse()
if session:
    cnpj_tomador = "20664370000130"
    data_competencia = "2024-07-01"  # Ajuste a data de competência conforme necessário
    tomador_data = buscar_dados_tomador(session, cnpj_tomador, data_competencia)
    if tomador_data:
        print("Dados do tomador encontrados:")
        print(tomador_data)
    else:
        print("Não foi possível obter os dados do tomador.")
