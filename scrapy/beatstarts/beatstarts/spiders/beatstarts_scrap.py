import scrapy
from ..items import BeatstartsItem
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class BeatstartsScrapSpider(scrapy.Spider):
    name = 'beatstarts_scrap'
    allowed_domains = ['beatstarts.com', 'www.beatstarts.com']
    start_urls = [
        'https://www.beatstars.com/explore-tracks'
    ]
    
    def start_requests(self):
        DRIVER_PATH = '/home/rifat/Projects/python/scrap/scrapy/beatstarts/chromedriver'
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

    def parse_detail(self, response):
        items = BeatstartsItem()
        name = response.css(".heading-s .name").css("::text").extract()
        bio = response.css(".vb-margin-b-xl .ng-star-inserted").css("::text").extract()
        followers = response.css(".social-interaction-line:nth-child(1) .ng-star-inserted").css("::text").extract()
        items['name'] = name
        items['bio'] = bio
        items['followers'] = followers
        yield items

        
        
