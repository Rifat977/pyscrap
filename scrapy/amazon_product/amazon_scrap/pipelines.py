# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import xlsxwriter


class AmazonScrapPipeline:

    def __init__(self):
        self.workbook = None
        self.worksheet = None
        self.row_index = 0

    def process_item(self, item, spider):
        spider.logger.info('IN SPIDER PROCESSSING')
        adapter = ItemAdapter(item)
        d = adapter.asdict()

        if self.row_index == 0:
            data = d.keys()
        else:
            data = d.values()
        
        for col, value in enumerate(data):
            self.worksheet.write_row(self.row_index, col, value)
        self.row_index += 1
        return item

    def open_spider(self, spider):
        spider.logger.info('IN SPIDER OPENING')
        self.workbook = xlsxwriter.Workbook("demo.xlsx")
        self.worksheet = self.workbook.add_worksheet()

    def close_spider(self, spider):
        spider.logger.info('IN SPIDER CLOSING')
        self.workbook.close()
