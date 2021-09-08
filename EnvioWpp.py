import pywhatkit as kt
import sys
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
    text = "Hola a todos, les envio el link para el:"+ dia+" "+ link
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=/Users/claudio.cordoba/Sele/Data')
    driver = webdriver.Chrome('/Users/claudio.cordoba/Downloads/chromedriver',options=options)

    driver.get("https://web.whatsapp.com")

    print("Logged In")

    inp_xpath_search = "//input[@title='Search or start new chat']"
    #input_box_search = WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
    time.sleep(10)
    selected_contact = driver.find_element_by_xpath("//*[@id='side']/div[1]/div/label/div/div[2]")
    selected_contact.click()
    selected_contact.send_keys("Transmision")
    time.sleep(5)
    selected_contact = driver.find_element_by_xpath("//span[@title='🔴 Transmisiones en vivo 📡']")
    selected_contact.click()

    #input_box_search.click()
    print("buscando")
    time.sleep(2)
    #input_box_search.send_keys(contact)
    time.sleep(2)
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    time.sleep(2)
    input_box.send_keys(text + Keys.ENTER)
    time.sleep(2)
    driver.quit()