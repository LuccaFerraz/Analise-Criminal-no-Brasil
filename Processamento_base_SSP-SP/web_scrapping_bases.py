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
caminho_downloads = os.path.join(os.getcwd(), "temp_data")
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
    arquivos_depois = os.listdir(diretorio)
    novo_arquivo = list(set(arquivos_depois) - set(arquivos_antes))
    if novo_arquivo:
        return os.path.join(diretorio, novo_arquivo[0])
    return None

dropdown_anos = Select(navegador.find_element(By.XPATH, '//select[@formcontrolname="mensalAno"]'))
dropdown_regiao = Select(navegador.find_element(By.XPATH, '//select[@formcontrolname="mensalRegiao"]'))
dropdown_municipio = Select(navegador.find_element(By.XPATH, '//select[@formcontrolname="mensalMunicipio"]'))

for ano in dropdown_anos.options:
    if ano.text == "2024" or ano.text == "2023":
        
        ano.click()
        time.sleep(2)
        for regiao in dropdown_regiao.options:
            #if regiao.text != 'Regiões':
            if regiao.text == "Campinas":
                
                regiao.click()
                time.sleep(2) 
                for municipio in dropdown_municipio.options:
                    if municipio.text != 'Municípios':
                        
                        municipio.click()
                        time.sleep(2)

                        diretorio_base = os.path.join('Dados_ssp_sp',
                                                      ano.text,
                                                      regiao.text,
                                                      municipio.text)
                        
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
                        