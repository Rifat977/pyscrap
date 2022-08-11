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
from amazoncaptcha import AmazonCaptcha



DRIVER_PATH = '/home/rifat/Projects/python/scrap/bs4_pandas/amazon_query/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--head')
webdriver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

search_query = 'winter+jacket'

if (len(sys.argv) >= 2):
    search_query = sys.argv[1]

base_url = "https://www.amazon.com/s?k="+search_query
records = []

def extract_data(item):
    name = item.h2.a.text.strip()
    link = base_url + item.h2.a.get('href')
    try:
        price_parent = item.find('span', 'a-price')
        price = item.find('span', 'a-offscreen').text.strip()
    except:
        price = 'None'
    try:
        review = item.i.text.strip()
        review_count = item.find('span', {'class':'a-size-base'}).text.strip()
    except:
        review = ''
        review_count = ''
    result = (name, link, price, review, review_count)
    return result

def scrap_page():
    # search = driver.find_element(By.NAME, "field-keywords")
    # search.send_keys(search_query + Keys.RETURN)
    # wait.until(presence_of_element_located)        
    html = BeautifulSoup(driver.page_source, "html.parser")
    total_page = html.find('span', class_="s-pagination-item s-pagination-disabled").text.strip()
    total_page =int(total_page)
    for i in range(1, total_page-1):
        driver.get("https://www.amazon.com/s?k="+search_query+"&page="+str(i))
        html = BeautifulSoup(driver.page_source, "html.parser")
        result = html.find_all('div', {'data-component-type':'s-search-result'})
        for item in result:
            record = extract_data(item)
            if record:
                records.append(record)



with webdriver as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(base_url)
    try:
        html = driver.find_element(By.XPATH, '//form[@action="/errors/validateCaptcha"]')
        img = driver.find_element(By.XPATH, '//img[1]')
        img_link = img.get_attribute('src')
        solution = AmazonCaptcha.fromlink(img_link).solve()
        captcha_box = driver.find_element(By.ID, "captchacharacters")
        captcha_box.send_keys(solution + Keys.RETURN)
        scrap_page()
    except:
        scrap_page()
    print(len(records))
        
    driver.close()