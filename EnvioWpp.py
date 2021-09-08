import sys
#es necesario bajar el chrome driver para abrir el chrome
sys.path.insert(0,"/Users/claudio.cordoba/Downloads/chromedriver")
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
def envioWpp(dia,link):
    #texto para enviar por wpp
    text = "Hola a todos, les envio el link para el:"+ dia+" "+ link
    #abro el driver del chrome
    options = webdriver.ChromeOptions()
    #le pongo una ruta donde quiero que me guardar la data como por ej las cookies (para no tener que loguearme varias veces en el wpp)
    options.add_argument(r'--user-data-dir=/Users/claudio.cordoba/Sele/Data')
    driver = webdriver.Chrome('/Users/claudio.cordoba/Downloads/chromedriver',options=options)
    #abro el wpp
    driver.get("https://web.whatsapp.com")

    print("Logged In")
    #espero a que abra la pagina
    time.sleep(10)
    #busco el elempo por xpath donde dice buscar persona
    selected_contact = driver.find_element_by_xpath("//*[@id='side']/div[1]/div/label/div/div[2]")
    #hago click
    selected_contact.click()
    #pongo transmision para que me aparesca el grupo de la transmisino por pantalla
    selected_contact.send_keys("Transmision")
    #espero a que aparesca
    time.sleep(5)
    #selecciono el grupo
    selected_contact = driver.find_element_by_xpath("//span[@title='🔴 Transmisiones en vivo 📡']")
    #click
    selected_contact.click()
    #espero
    time.sleep(4)
    #busco el recuadro para escribir
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    time.sleep(2)
    #envio el texto y le doy enter
    input_box.send_keys(text + Keys.ENTER)
    time.sleep(2)
    driver.quit()