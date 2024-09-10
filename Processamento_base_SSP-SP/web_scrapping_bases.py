import pandas as pd
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time

chrome_options  = Options()
# Para realizar os downloads das bases, deve-se criar um diretório chamado "temp_data"
# No mesmo caminho relativo do web_scrapping_bases.py.

caminho_downloads = os.path.join(os.getcwd(), "Processamento_base_SSP-SP", "temp_data")

prefs = {"download.default_directory": caminho_downloads,
         "download.prompt_for_download": False,
         "download.directory_upgrade": True,
         "safebrowsing.enabled": True}

chrome_options.add_experimental_option("prefs", prefs)


servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=chrome_options)

url = "https://www.ssp.sp.gov.br/estatistica/dados-mensais"
navegador.get(url)

def criar_pasta(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

def detectar_novo_arquivo(diretorio, arquivos_antes):
    """
    Verifica se há um novo arquivo no diretório de download web do google
    para que seja possível mover para o devido diretório
    """

    arquivos_depois = os.listdir(diretorio)
    novo_arquivo = list(set(arquivos_depois) - set(arquivos_antes))
    if novo_arquivo:
        return os.path.join(diretorio, novo_arquivo[0])
    return None


def baixar_dados_por_ano_regiao(anos_selecionados, regioes_selecionadas):
    """Função principal para baixar os dados da SSP-SP

    Args:
        anos_selecionados (_type_): lista de anos que se deseja baixar os dados: 2024 - 2001
        
        regioes_selecionadas (_type_): lista de regiões que se deseja baixar os dados
        
        ['Araçatuba', 'Bauru', 'Campinas', 'Capital', 'Grande São Paulo (exclui a Capital),
        'Piracicaba', 'Presidente Prudente', 'Ribeirão Preto', 'Santos', 'São José do Rio Preto',
        'São José dos Campos', 'Sorocaba']
        
    """
    dropdown_anos = Select(navegador.find_element(By.XPATH, '//select[@formcontrolname="mensalAno"]'))
    dropdown_regiao = Select(navegador.find_element(By.XPATH, '//select[@formcontrolname="mensalRegiao"]'))
    dropdown_municipio = Select(navegador.find_element(By.XPATH, '//select[@formcontrolname="mensalMunicipio"]'))

    for ano in dropdown_anos.options:
        if ano.text in anos_selecionados:
            
            ano.click()
            time.sleep(2)
            for regiao in dropdown_regiao.options:
                if regiao.text in regioes_selecionadas:
                    
                    regiao.click()
                    time.sleep(2) 
                    for municipio in dropdown_municipio.options:
                        if municipio.text != 'Municípios':
                            
                            municipio.click()
                            time.sleep(2)

                            diretorio_base = os.path.join("Processamento_base_SSP-SP", 'Dados_ssp_sp',
                                                        ano.text,
                                                        regiao.text,
                                                        municipio.text)
                            
                            if os.path.exists(diretorio_base) and len(os.listdir(diretorio_base)) > 0:
                                print(f"Dados de {municipio.text} para {ano.text}, {regiao.text} já baixados. Pulando...")
                                continue
                            
                            criar_pasta(diretorio_base)                       
                            dir_antes = os.listdir(caminho_downloads)
                            
                            xpath = "/html/body/app-root/body/div[1]/div/app-dados-mensais/div[2]/div[2]/form/div[3]/div[6]/button"
                            botao_download = navegador.find_element(By.XPATH, xpath)
                            botao_download.click()
                            time.sleep(8)
                            
                            novo_arquivo = detectar_novo_arquivo(caminho_downloads, dir_antes)
                            if novo_arquivo:
                                novo_nome = f"{municipio.text}_{ano.text}.xls"
                                destino_arquivo = os.path.join(diretorio_base, novo_nome)
                                shutil.move(novo_arquivo, destino_arquivo)
                            else:
                                print(f"Nenhum novo arquivo foi detectado para {municipio.text}.")
                        
                            time.sleep(2)

def main():
    """Exemplo para baixar os Dados de 2022 referente a todos os municípios
    """
    anos = ['2022']
    regioes = ['Araçatuba', 'Bauru', 'Campinas', 'Capital', 'Grande São Paulo (exclui a Capital)',
        'Piracicaba', 'Presidente Prudente', 'Ribeirão Preto', 'Santos', 'São José do Rio Preto',
        'São José dos Campos', 'Sorocaba']
    
    baixar_dados_por_ano_regiao(anos, regioes)

if __name__ == "__main__":
    main()

