import scrapy
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class InstacartBotSpider(scrapy.Spider):
    name = 'instacart_bot'
    allowed_domains = ['instacart.com']
    start_urls = ['http://instacart.com/']

    def start_requests(self):
        DRIVER_PATH = '/home/rifat/Projects/python/scrap/scrapy/instacart/chromedriver'
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get('https://www.beatstars.com/explore-tracks')
        for i in range(1, 4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            elements = driver.find_elements(By.CSS_SELECTOR, ".fit-parent.ng-star-inserted .ng-star-inserted a")
            for element in elements:
                profile_link = element.get_attribute('href')
                yield scrapy.Request(url=profile_link, callback=self.parse_detail)
        driver.quit()
