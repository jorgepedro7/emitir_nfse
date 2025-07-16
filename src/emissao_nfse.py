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
def buscar_dados_tomador(session, cnpj):
    url = f"https://www.nfse.gov.br/emissornacional/api/EmissaoDPS/RecuperarInfoPessoaJuridicaTomador/{cnpj}?data=2024-06-01"
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
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Falha ao buscar dados do tomador: {response.status_code}")
        return None

# Função para emitir nota fiscal
def emitir_nfse(session, tomador_data, servico_descricao, valor):
    emitir_nfse_url = "https://www.nfse.gov.br/EmissorNacional/DPS/EmitirNFSe?idr=RzJqbkNlKzlYS2J2SXkvcGh2ZVM0UT090"

    nfse_data = {
        "NotaDoMei": "False",
        "Prestador.LocalDomicilio": "0",
        "DataCompetencia": "01/06/2024",
        "SerieDPS": "",
        "NumeroDPS": "",
        "TipoEmitente": "1",
        "Prestador.EnderecoNacional.NomeMunicipio": "Luís Eduardo Magalhães/BA",
        "Prestador.EnderecoNacional.CodigoMunicipio": "2919553",
        "Prestador.InscricaoMunicipal": "",
        "Prestador.Inscricao": "46.964.533/0001-94",
        "Prestador.Nome": "JORGE PEDRO SOUZA SILVA 01628987626",
        "SimplesNacional.Opcao": "2",
        "SimplesNacional.RegimeApuracaoTributosSN": "",
        "Prestador.Telefone": "(77)99136-8196",
        "Prestador.Email": "jldesing35@gmail.com",
        "Prestador.EnderecoNacional.CEP": "47862-108",
        "Prestador.EnderecoNacional.Logradouro": "ANTONIO CARLOS MAGALHAES",
        "Prestador.EnderecoNacional.Numero": "1245",
        "Prestador.EnderecoNacional.Complemento": "",
        "Prestador.EnderecoNacional.Bairro": "JARDIM DAS ACACIAS",
        "Tomador.LocalDomicilio": "1",
        "Tomador.Inscricao": tomador_data['inscricao'],
        "Tomador.InscricaoMunicipal": tomador_data['inscricaoMunicipal'],
        "Tomador.NIF": "",
        "Tomador.MotivoNaoInformacaoNIF": "",
        "Tomador.Nome": tomador_data['nome'],
        "Tomador.Telefone": tomador_data['telefone'],
        "Tomador.Email": tomador_data['email'],
        "Tomador.InformarEndereco": "true",
        "Tomador.EnderecoNacional.CEP": tomador_data['endereco']['cep'],
        "Tomador.EnderecoNacional.CodigoMunicipio": tomador_data['endereco']['codigoMunicipio'],
        "Tomador.EnderecoNacional.NomeMunicipio": tomador_data['endereco']['nomeMunicipio'],
        "Tomador.EnderecoNacional.Bairro": tomador_data['endereco']['bairro'],
        "Tomador.EnderecoNacional.Logradouro": tomador_data['endereco']['logradouro'],
        "Tomador.EnderecoNacional.Numero": tomador_data['endereco']['numero'],
        "Tomador.EnderecoNacional.Complemento": tomador_data['endereco']['complemento'],
        "Intermediario.LocalDomicilio": "0",
        "Intermediario.Inscricao": "",
        "Intermediario.InscricaoMunicipal": "",
        "Intermediario.NIF": "",
        "Intermediario.MotivoNaoInformacaoNIF": "",
        "Intermediario.Nome": "",
        "Intermediario.Telefone": "",
        "Intermediario.Email": "",
        "Intermediario.EnderecoNacional.CEP": "",
        "Intermediario.EnderecoNacional.CodigoMunicipio": "",
        "Intermediario.EnderecoNacional.NomeMunicipio": "",
        "Intermediario.EnderecoNacional.Bairro": "",
        "Intermediario.EnderecoNacional.Logradouro": "",
        "Intermediario.EnderecoNacional.Numero": "",
        "Intermediario.EnderecoNacional.Complemento": "",
        "Intermediario.EnderecoExterior.Logradouro": "",
        "Intermediario.EnderecoExterior.Numero": "",
        "Intermediario.EnderecoExterior.Complemento": "",
        "Intermediario.EnderecoExterior.Bairro": "",
        "Intermediario.EnderecoExterior.Cidade": "",
        "Intermediario.EnderecoExterior.CodigoEnderecamentoPostal": "",
        "Intermediario.EnderecoExterior.EstadoProvinciaRegiao": "",
        "Intermediario.EnderecoExterior.NomePais": "",
        "Intermediario.EnderecoExterior.CodigoPais": "",
        "Servico.Descricao": servico_descricao,
        "Servico.ValorServicos": valor
    }

    headers = {
        "Host": "www.nfse.gov.br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Referer": "https://www.nfse.gov.br/EmissorNacional/DPS/Tributacao?idr=RzJqbkNlKzlYS2J2SXkvcGh2ZVM0UT090",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = session.post(emitir_nfse_url, headers=headers, data=nfse_data)
    if response.status_code == 200:
        print("Nota fiscal emitida com sucesso!")
        print(f"Response Text: {response.text}")
    else:
        print(f"Falha na emissão da nota fiscal: {response.status_code}")

# Lista de tomadores com CNPJ, descrição do serviço e valor
tomadores = [
    {
        "cnpj": "46.675.304/0001-50",
        "descricao_servico": "Serviço de Consultoria",
        "valor": "1500.00"
    },
    # Adicione mais tomadores aqui
]

# Realizar o login
session = login_nfse()
if session:
    # Emitir notas fiscais para cada tomador
    for tomador in tomadores:
        tomador_data = buscar_dados_tomador(session, tomador['cnpj'])
        if tomador_data:
            emitir_nfse(session, tomador_data, tomador['descricao_servico'], tomador['valor'])
