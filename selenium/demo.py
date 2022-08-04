# from unittest import result
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.expected_conditions import presence_of_elements_located
# import time
# import sys


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

DRIVER_PATH = '/home/rifat/Projects/python/scrap/selen/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get('https://www.beatstars.com/explore-tracks')

for i in range(1, 5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    elements = driver.find_elements(By.CSS_SELECTOR, ".fit-parent.ng-star-inserted .ng-star-inserted a")
    for element in elements:
        print(element.get_attribute('href'))
    driver.quit()

















