import scrapy
from ..items import AmazonScrapItem

class AmazonBotSpider(scrapy.Spider):
    name = 'amazon_bot'
    allowed_domains = ['amazon.com']
    page_number = 2
    start_urls = [
        'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&qid=1659086064&rnid=1250225011&ref=lp_1000_nr_p_n_publication_date_0'
        ]

    def parse(self, response):
        items = AmazonScrapItem()

        product_name = response.css(".a-size-medium::text").extract()
        product_price = response.css(".s-price-instructions-style .a-price-whole").css("::text").extract()
        product_author = response.css(".a-size-base .a-link-normal .s-underline-text .s-underline-link-text .s-link-style").css("::text").extract()
        product_image = response.css(".s-image::attr(src)").extract()

        items['product_name'] = product_name
        items['product_price'] = product_price
        items['product_author'] = product_author
        items['product_image'] = product_image

        yield items

        next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page=' + str(AmazonBotSpider.page_number) + '&qid=1659088952&rnid=1250225011&ref=sr_pg_' + str(AmazonBotSpider.page_number)
        if AmazonBotSpider.page_number <= 3:
            AmazonBotSpider.page_number += 1
            yield response.follow(next_page, callback= self.parse)

