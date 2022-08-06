import scrapy
from ..items import ProjectScrapyItem
from scrapy.http import FormRequest
import pandas as pd
import xlsxwriter

class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com/login"
    ]

    def parse(self, response):
        token = response.css("form input").xpath('@value').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token':token,
            'username':'abcd@gmail.com',
            'password':'BalBal34@'
        }, callback=self.start_scrapping)
        
    
    def start_scrapping(self,response):
        items = ProjectScrapyItem()
        data = response.css('div.quote')
        for quotes in data:
            title = quotes.css("span.text::text").extract()
            author = quotes.css(".author::text").extract()
            tags = quotes.css(".tag::text").extract()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.start_scrapping)