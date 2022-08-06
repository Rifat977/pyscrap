import scrapy
import json
import pandas as pd

class SunglassSpider(scrapy.Spider):
    name = 'sunglass'
    allowed_domains = ['sunglasshut.com']
    start_urls = ['https://www.sunglasshut.com/wcs/resources/plp/10152/byCategoryId/3074457345626651837?isProductNeeded=true&isChanelCategory=false&pageSize=18&responseFormat=json&currency=USD&catalogId=20602&top=Y&beginIndex=0&viewTaskName=CategoryDisplayView&storeId=10152&langId=-1&categoryId=3074457345626651837&pageView=image&orderBy=default&currentPage=1']

    def parse(self, response):
        data = json.loads(response.body)
        yield from data['plpView']['products']['products']['product']
        next_page = data['plpView']['nextPageURL']
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        dt = data['plpView']['products']['products']['product']
        df = pd.DataFrame(dt)
        df.to_excel('demo.xlsx', index=False)
