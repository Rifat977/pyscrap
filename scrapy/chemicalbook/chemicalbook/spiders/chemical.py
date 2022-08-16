import scrapy
from scrapy.utils.response import open_in_browser
from scrapy import FormRequest

class ChemicalSpider(scrapy.Spider):
    name = 'chemical'
    allowed_domains = ['chemicalbook.com']
    keyword = input("Keyword: ")
    start_urls = ['https://www.chemicalbook.com/Search_EN.aspx?keyword='+str(keyword)]

    def parse(self, response):
        open_in_browser(response)