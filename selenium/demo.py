from numpy import product
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



DRIVER_PATH = '/home/rifat/Projects/python/scrap/selenium/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
webdriver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

base_url = "https://www.instacart.com"

records = []

def page_scrap(base_url):
    driver.get(base_url+"/store/cvs/storefront?guest=true")
    html = BeautifulSoup(driver.page_source, "html.parser")
    products = html.find_all('a', class_="css-er4k5d")
    for item in products:
        driver.get(base_url+item['href'])
        html = BeautifulSoup(driver.page_source, "html.parser")
        try:
            name = html.find('span', class_="css-16ptqna").text
        except:
            name = ''
        try:
            parent_price = html.find('div', class_="css-1u4ofbf")
            price = parent_price.span.text
        except:
            price = ''
        result = {'product_name':name, 'price':price}
        records.append(result)
        print(name)
    for item in records:
        print(item)
    

with webdriver as driver:
    wait = WebDriverWait(driver, 30)
    page_scrap(base_url)
    driver.close()    


