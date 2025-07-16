import requests
from bs4 import BeautifulSoup

# URL da página de login
login_url = "https://www.nfse.gov.br/EmissorNacional/Login"

# Inicializar a sessão
session = requests.Session()

# Fazer a requisição GET para a página de login
response = session.get(login_url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parsear o HTML da página de login
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar o token de verificação no HTML
    token_element = soup.find('input', {'name': '__RequestVerificationToken'})
    token = token_element['value'] if token_element else None
    
    # Verificar se o token foi encontrado e exibir
    if token:
        print(f"Token encontrado: {token}")
    else:
        print("Token de verificação não encontrado.")
    
    # Dados do formulário de login
    login_data = {
        "__RequestVerificationToken": token,
        "Inscricao": "46.964.533/0001-94",
        "Senha": "Ludimila05"
    }
    
    # Cabeçalhos HTTP
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

    # Fazer a requisição POST para fazer login
    if token:
        login_response = session.post(login_url, headers=headers, data=login_data)
        
        # Verificar se o login foi bem-sucedido
        if login_response.status_code == 200:
            print("Login bem-sucedido!")
            print(f"Response Text: {login_response.text}")
        else:
            print(f"Falha no login: {login_response.status_code}")
else:
    print(f"Falha ao acessar a página de login: {response.status_code}")
