import gspread
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright
from datetime import datetime
import time

# --- CONFIGURAÇÕES ---
SERVICE_ACCOUNT_FILE = 'credenciais_google.json'
SPREADSHEET_ID = '1A4RIW0ClgGWzegtJnJ3td_GKFZ3TRAR8jlZ8Emd_fPM'
ABA_CLIENTES = 'Dados Clientes JL - 2'
ABA_REGISTRO = 'Dados Clientes JL' # Nova aba para registrar as notas

def pegar_token(page):
    """Pega o valor do __RequestVerificationToken da página."""
    try:
        token_input = page.locator('input[name="__RequestVerificationToken"]').get_attribute('value')
        if token_input:
            return token_input
        print(f"Token não encontrado na página {page.url}")
        return None
    except Exception as e:
        print(f"Erro ao pegar token: {e}")
        return None

def login_nfse(page):
    """Realiza o login no portal NFSe."""
    print("Iniciando login...")
    page.goto("https://www.nfse.gov.br/EmissorNacional/Login")
    
    page.fill('input[name="Inscricao"]', "46.964.533/0001-94")
    page.fill('input[name="Senha"]', "Ludimila05")
    page.click('button[type="submit"]')
    
    page.wait_for_load_state('networkidle')

    if "Sair" in page.content() or "Logout" in page.content():
        print("Login realizado com sucesso.")
        return True
    else:
        print("Falha no login.")
        return False

def ler_clientes_planilha():
    """Lê os dados dos clientes da planilha Google Sheets."""
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(ABA_CLIENTES)
    return sheet.get_all_records()

from datetime import datetime
import time

from datetime import datetime
import time

def enviar_dados_tomador(page, cliente):
    """Preenche os dados do tomador e avança para a próxima etapa."""
    print(f"🟡 Enviando dados do tomador: {cliente['Nome']}")

    try:
        # Acessa a página
        page.goto("https://www.nfse.gov.br/EmissorNacional/DPS/Pessoas")
        page.wait_for_load_state('networkidle')

        # Preenche data de competência
        page.fill('input#DataCompetencia', datetime.now().strftime('%d/%m/%Y'))
        page.press('input#DataCompetencia', 'Tab')
        time.sleep(1)

        # Seleciona Brasil
        page.click('label:has(input#Tomador_LocalDomicilio[value="1"])')
        page.wait_for_selector('#pnlInscricaoBrasil', state='visible')

        # Preenche CNPJ
        cnpj = str(cliente['CNPJ']).strip()
        page.fill('input#Tomador_Inscricao', cnpj)
        page.press('input#Tomador_Inscricao', 'Tab')

        # Aguarda processamento do CNPJ
        time.sleep(3)  # tempo mínimo de espera
        page.wait_for_timeout(1000)

        # Espera o botão "Avançar" estar visível e habilitado
        botao = page.locator('button:has-text("Avançar")')
        botao.wait_for(state='visible', timeout=10000)
        
        if not botao.is_enabled():
            print("⏳ Aguardando botão 'Avançar' ser habilitado...")
            for _ in range(10):  # aguarda até 10 segundos
                if botao.is_enabled():
                    break
                time.sleep(1)

        # Clica no botão
        botao.click()

        # Aguarda avanço de página
        try:
            page.wait_for_url("**/EmissorNacional/DPS/Servico*", timeout=15000)
            print("✅ Página avançou para etapa de Serviço")
            return True
        except:
            if "Servico" in page.url:
                print("✅ Página avançou (verificação manual)")
                return True

            print("❌ Não avançou para a etapa de Serviço")
            return False

    except Exception as e:
        print(f"❌ Erro ao processar tomador {cliente['Nome']}: {e}")
        return False



def enviar_dados_servico(page, cliente):
    """Preenche os dados do serviço."""
    print("Preenchendo dados do serviço...")
    
    try:
        # Aguarda a página carregar completamente
        page.wait_for_load_state('networkidle')
        
        # Preenche município
        page.locator('span[aria-labelledby="select2-LocalPrestacao_CodigoMunicipioPrestacao-container"]').click()
        page.locator('input.select2-search__field').fill("Luís Eduardo Magalhães/BA")
        page.locator('li.select2-results__option:has-text("Luís Eduardo Magalhães/BA")').click()
        
        # Preenche código de tributação
        page.locator('span[aria-labelledby="select2-ServicoPrestado_CodigoTributacaoNacional-container"]').click()
        page.locator('input.select2-search__field').fill("08.02.01")
        page.locator('li.select2-results__option:has-text("08.02.01 - Instrução, treinamento, orientação pedagógica e educacional, avaliação de conhecimentos de qualquer natureza.")').click()
        

        # Seleciona opção de não exportação
        page.check('input[name="Servico.Prestado.HaExportacaoImunidadeNaoIncidencia"][value="0"]')
        
        # Calcula competência
        mes_atual_num = datetime.now().month
        ano_atual = datetime.now().year
        mes_anterior_num = 12 if mes_atual_num == 1 else mes_atual_num - 1
        ano_competencia = ano_atual if mes_atual_num > 1 else ano_atual - 1

        meses_pt = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        mes_anterior_nome = meses_pt[mes_anterior_num]

        # Preenche descrição
        descricao = f"Consultoria, instrução e treinamento. Competência: {mes_anterior_nome} - {ano_competencia} - R${cliente['Valor']}"
        page.fill('textarea#ServicoPrestrado_Descricao', descricao)
        
        # Aguarda um pouco antes de avançar
        time.sleep(2)
        
        # Clica em avançar
        page.click('button:has-text("Avançar")')

        try:
            page.wait_for_selector('h4:has-text("Valores")', timeout=10000)
            print("Dados do serviço preenchidos com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao tentar avançar para a próxima etapa após preencher os dados do serviço: {e}")
            return False
            
    except Exception as e:
        print(f"Erro ao preencher dados do serviço: {e}")
        return False

def enviar_dados_tributacao(page, cliente):
    """Preenche os dados de tributação."""
    print("Preenchendo dados de tributação...")
    
    try:
        page.wait_for_load_state('networkidle')
        
        # Preenche valor do serviço
        page.fill('#Valores_ValorServico', str(cliente['Valor']))
        
        # Aguarda um pouco antes de submeter
        time.sleep(2)
        
        # Clica em submeter
        page.click('button[type="submit"]')
        
        page.wait_for_load_state('networkidle')
        
        if "Resumo" in page.content():
            print("Tributação preenchida com sucesso.")
            return True
        else:
            print("Falha ao preencher os dados de tributação.")
            return False
            
    except Exception as e:
        print(f"Erro ao preencher dados de tributação: {e}")
        return False

def emitir_nfse(page, cliente):
    """Emite a NFSe e extrai os dados da nota emitida."""
    print(f"Tentando emitir NFSe para {cliente['Nome']}...")
    
    try:
        # Clica no botão de emitir
        page.click('button:has-text("Emitir NFSe")')

        # Aguarda sucesso ou erro
        page.wait_for_selector('div.alert-success, div.alert-danger', timeout=20000)
        
        if page.locator('div.alert-success').count() > 0:
            # Extrai dados da NFSe
            numero_nfse = page.locator('//dt[text()="Número da NFS-e"]/following-sibling::dd').inner_text()
            codigo_verificacao = page.locator('//dt[text()="Código de Verificação"]/following-sibling::dd').inner_text()
            
            print(f"✅ NFSe emitida para {cliente['Nome']}: Nº {numero_nfse}")
            
            return {
                "status": "sucesso",
                "numero_nfse": numero_nfse,
                "codigo_verificacao": codigo_verificacao
            }
        else:
            erro_msg = page.locator('div.alert-danger').inner_text()
            print(f"❌ Erro na emissão da nota para {cliente['Nome']}: {erro_msg}")
            return {"status": "erro", "mensagem": erro_msg}
            
    except Exception as e:
        print(f"❌ Erro na emissão da nota para {cliente['Nome']}: {e}")
        return {"status": "erro", "mensagem": str(e)}

def registrar_emissao_planilha(cliente, dados_nfse):
    """Registra os dados da NFSe emitida em uma nova aba da planilha."""
    try:
        print(f"Registrando nota Nº {dados_nfse['numero_nfse']} na planilha...")
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        try:
            sheet = spreadsheet.worksheet(ABA_REGISTRO)
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title=ABA_REGISTRO, rows="100", cols="10")
            sheet.append_row([
                "Data de Emissão", "Nome do Tomador", "CNPJ do Tomador", 
                "Descrição", "Valor", "Número da NFSe", "Código de Verificação"
            ])

        data_emissao = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        linha_para_adicionar = [
            data_emissao, cliente['Nome'], cliente['CNPJ'],
            cliente.get('Descrição Nota', ''), cliente['Valor'],
            dados_nfse['numero_nfse'], dados_nfse['codigo_verificacao']
        ]
        sheet.append_row(linha_para_adicionar)
        print("✅ Registro salvo com sucesso na planilha.")
        
    except Exception as e:
        print(f"❌ Falha ao registrar a nota na planilha: {e}")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        if not login_nfse(page):
            print("Erro no login, abortando.")
            browser.close()
            exit()

        clientes = ler_clientes_planilha()
        
        for cliente in clientes:
            print(f"\n--- Iniciando processo para: {cliente['Nome']} ---")
            
            if not enviar_dados_tomador(page, cliente):
                print(f"Falha na etapa de 'Dados do Tomador' para {cliente['Nome']}, pulando.")
                continue

            if not enviar_dados_servico(page, cliente):
                print(f"Erro ao enviar dados de serviço para {cliente['Nome']}, pulando.")
                continue

            if not enviar_dados_tributacao(page, cliente):
                print(f"Erro ao enviar dados de tributação para {cliente['Nome']}, pulando.")
                continue

            resultado_emissao = emitir_nfse(page, cliente)

            if resultado_emissao["status"] == "sucesso":
                registrar_emissao_planilha(cliente, resultado_emissao)
            else:
                print(f"Erro na emissão da NFSe para {cliente['Nome']}, não será registrado.")
                
        print("\n--- Processo finalizado ---")
        browser.close()