import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class MailsSpider(CrawlSpider):
    name = 'mails'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    book_details = LinkExtractor(restrict_css='h3 > a')
    next_button = LinkExtractor(restrict_css='.next > a')
    # cats = LinkExtractor(restrict_css='.side_categories > ul > li > ul > li')

    rule_book_details = Rule(book_details, callback='parse_item', follow=True)
    rule_next = Rule(next_button, follow=True)
    # rule_cats = Rule(cats, follow=False)

    rules = (
        rule_book_details,
        rule_next,
        # rule_cats,
    )

    def parse_item(self, response):
        book_name = response.css('h1::text').get()
        price = response.css('.price_color::text').get().replace("£","")
        yield{
            'book_name':book_name,
            'price':price
        }
