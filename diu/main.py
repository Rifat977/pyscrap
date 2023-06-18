import os
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

protected_url = "https://hall.diu.edu.bd/admission/online/applications/my/view/6245"
login_url = "https://hall.diu.edu.bd/web/login"

username = "dev.abdullah.mamun@gmail.com"
password = "DevRifat97@"

pattern = '<[^<]+?>'


firefox_options = Options()
firefox_options.add_argument('--head')
driver = webdriver.Firefox(executable_path=r'geckodriver', options=firefox_options)


def login(username, password):
    driver.get(login_url)

    driver.find_element("id", "login").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    x = driver.find_elements(By.TAG_NAME, "button")
    x[1].click()

def scrap():
    driver.get(protected_url)
    repos = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div")

    result = repos.get_attribute('innerHTML')
    st_id = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/div")
    st_id = st_id.get_attribute('innerHTML')
    st_id = re.sub(pattern, "", st_id)
    st_id = st_id.replace("Student ID:", "")
    st_id = st_id.replace(" ", "")
    st_id = st_id.replace("\n","")

    html_save_path = "python/pyscrap/diu/data/"+st_id+".html"

    with open(html_save_path, 'w', encoding='utf-8') as html_file:
        for line in result:
            html_file.write(line)



login(username, password)
scrap()