from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import time

navegador = webdriver.Chrome()

#abrindo o site
navegador.get('https://www.kabum.com.br/promocao/COMPUTADORKABUM?page_number=1&page_size=40&facet_filters=&sort=&variant=null')
navegador.maximize_window()

# ROLAR A TELA DA PÁGINA ATÉ O FINAL PARA CARREGAR TODOS OS PRODUTOS

def scroll_smoothly(driver, duration=5):
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    step = scroll_height // (duration * 10)
    current_position = 0
    
    while current_position < scroll_height:
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(0.1)

# GARANTINDO QUE A PÁGINA FOI ATÉ O FINAL
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# ROLAR A TELA LENTAMENTE PARA NÃO CORRER O RISCO DE DESCER MUITO RÁPIDO E NÃO CARREGAR OS PRODUTOS
scroll_smoothly(navegador, duration=5)

#buscando o primeiro produto
nm_pdt = '//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[1]/article/a/div/button/div/h3/span'
navegador.find_element(By.XPATH, nm_pdt).text
prc_pdt = '//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[1]/article/a/div/div[2]/div[2]/span'
navegador.find_element(By.XPATH, prc_pdt).text

nm_pdt2 = '//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[2]/article/a/div/button/div/h3/span'
navegador.find_element(By.XPATH, nm_pdt2).text
prc_pdt2 = '//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[2]/article/a/div/div[2]/div[2]/span'
navegador.find_element(By.XPATH, prc_pdt2).text

nm_pdt3 = '//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[3]/article/a/div/button/div/h3/span'
navegador.find_element(By.XPATH, nm_pdt3).text
prc_pdt3 = '//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[3]/article/a/div/div[2]/div[2]/span'
navegador.find_element(By.XPATH, prc_pdt3).text

lista_produtos = [] # lista vazia
for produto in range(1,30):
    try:
        print(navegador.find_element(By.XPATH, f'//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[{produto}]/article/a/div/button/div/h3/span').text)
        dado_produto = navegador.find_element(By.XPATH, f'//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[{produto}]/article/a/div/button/div/h3/span').text
        lista_produtos.append(dado_produto)
    except:
        pass


lista_precos = [] # lista vazia
for preco in range(0,30):
    try:
        print(navegador.find_element(By.XPATH, f'//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[{preco}]/article/a/div/div[2]/div[2]/span').text)

        dado_preco = navegador.find_element(By.XPATH, f'//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[{preco}]/article/a/div/div[2]/div[2]/span').text
        lista_precos.append(dado_preco)
    except:
        pass    


lista_qtdp = [] # lista vazia
for parcelas in range(0,30):
    try:
        print(navegador.find_element(By.XPATH, f'//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[{parcelas}]/article/a/div/div[2]/div[3]/span/b').text)

        dado_parcela = navegador.find_element(By.XPATH, f'//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[{parcelas}]/article/a/div/div[2]/div[3]/span/b').text
        lista_qtdp.append(dado_parcela)
    except:
        pass

tabela1 = pd.DataFrame(lista_produtos, columns=['produto'])
tabela1

tabela2 = pd.DataFrame(lista_precos, columns=['precos'])
tabela2

tabela3 = pd.DataFrame(lista_qtdp, columns=['quantidade de parcelas'])
tabela3

df = pd.concat([tabela1, tabela2, tabela3], axis=1)
df

###df.drop(columns=['precos'])
###tratamento das colunas
df['precos']=df.precos.str.replace('\n', ' ').str.replace(' ,', ',').str.replace(', ', ',').str.replace('R$ ', '').str.split(' ').str.get(0).str.replace(',',';').str.replace('.','').str.replace(';', '.')
df['quantidade de parcelas']=df['quantidade de parcelas'].str.replace(', ', ',').str.replace('R$ ', '').str.replace(',',';').str.replace('.','').str.replace(';', '.').str.replace('de', '')
df['precos'] = pd.to_numeric(df['precos'], errors='coerce')
# Garante que as pastas existam
os.makedirs("../bases_originais", exist_ok=True)
os.makedirs("../bases_tratadas", exist_ok=True)


df.to_csv("../bases_originais/dados_kabum.csv", index=False, sep=';', encoding='utf-8')

df.precos.fillna(0, inplace=True)
df.loc[df.precos>50000, 'precos']=50000
df.loc[df.precos<0, 'precos']=100
df.drop_duplicates(inplace=True)

df.to_csv("../bases_tratadas/dados_kabum2.csv", index=False, sep=';', encoding='utf-8')























