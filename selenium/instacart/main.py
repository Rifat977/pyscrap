from numpy import product
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = '/home/rifat/Projects/python/scrap/selenium/instacart/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
webdriver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

base_url = "https://www.instacart.com"

search_query = 'milk'

if (len(sys.argv) >= 2):
    search_query = sys.argv[1]
filename = sys.argv[2]

records = []

def product_extract(store_url):
    driver.get(store_url)
    html = BeautifulSoup(driver.page_source, "html.parser")
    products = html.find_all('a', class_="css-er4k5d")
    print(len(products), 'item in store')
    for item in products:
        driver.get(base_url+item['href'])
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1u4ofbf')))
        html = BeautifulSoup(driver.page_source, "html.parser")
        shopName = html.find('h2', class_="css-auh5rw-Header").text
        try:
            productName = html.find('span', class_="css-16ptqna").text
            parent_price = html.find('div', class_="css-1u4ofbf")
            price = parent_price.span.text
            image_parent = html.find('div', class_="ic-image-zoomer")
            image = image_parent.img['src']
        except:
            print("Data mising in this product")

        try:
            photos = []
            ul_element = html.find('ul', class_="css-og0jw3-ImageThumbnails")
            imgs = ul_element.find_all('img')
            for img in imgs:
                photos.append(img['src'])
        except:
            print("No small images")
            photos = 'N/A'
        try:
            weight = html.find('span', class_="css-1eev6ad").text
        except:
            weight = 'N/A'
        try:
            oldPrice = html.find('span', class_="css-1j6mvwz").text
        except:
            oldPrice = 'N/A'
        try:
            discount = html.find('span', class_="css-17ukb5w").text
        except:
            discount = 'N/A'
        try:
            zipcode = html.find('span', class_="css-1r0o67d-AddressButton").text
        except:
            zipcode = 'N/A'
        product_details = []
        try:
            all_details = html.find('div', class_="css-1o229iz-DetailSections")
            pr_details = all_details.find_all('div', class_="css-8atqhb")
            product_details = pr_details
        except:
            print('This product has no details')

        ingredients = ''
        details = ''
        # directions = 'N/A'
        for detail in product_details:
            if(detail.h2.text.strip()=='Ingredients'):
                ingredients = detail.div.text
            if(detail.h2.text.strip()=='Details'):
                details = detail.div.text
        #     if(detail.h2.text.strip()=='Directions'):
        #         directions = detail.dev.text

        try:
            nutration = html.find('div', class_="css-1jjp3po-NutritionalFacts").get_text(' | ')
        except:
            nutration = 'N/A'

        productLink = base_url+item['href']
        result = {
            'shopName' : shopName,
            'productName':productName,
            'price':price,
            'oldPrice':oldPrice,
            'discount':discount,
            'weight':weight,
            'zip':zipcode,
            'details':details,
            'ingredients':ingredients,
            # 'directions' : directions,
            'productLink':productLink, 
            'image':image,
            'nutration' : nutration,
            'photos':photos
            }
        records.append(result)
        data = pd.DataFrame(records)
        split = filename.split('.')
        directory = 'export/'
        if(split[1]=='csv'):
            data.to_csv(directory+filename, index=False)
        elif(split[1]=='json'):
            data.to_json(directory+filename)
        print('Data saving..')

def store_extract(base_url):
    driver.get(base_url+"/store/s?k="+search_query)
    html = BeautifulSoup(driver.page_source, "html.parser")
    stores = html.find_all('a', class_="css-8i7al4")
    print(len(stores), 'stores')
    for item in stores:
        try:
            store_url = base_url+item['href']
            product_extract(store_url)
        except:
            pass

with webdriver as driver:
    wait = WebDriverWait(driver, 20)
    store_extract(base_url)
    driver.close()    


