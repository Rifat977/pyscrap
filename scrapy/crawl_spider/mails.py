import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import xlsxwriter
import pandas as pd

class MailsSpider(CrawlSpider):
    name = 'mails'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    book_details = LinkExtractor(restrict_css='h3 > a')
    next_button = LinkExtractor(restrict_css='.next > a')

    rule_book_details = Rule(book_details, callback='parse_item', follow=True)
    rule_next = Rule(next_button, follow=True)

    rules = (
        rule_book_details,
        rule_next,
    )

    def parse_item(self, response):
        book_name = response.css('h1::text').get()
        price = response.css('.price_color::text').get().replace("£","")
        items = {}
        items['Name'] = book_name
        items['Price'] = price
        yield items        
