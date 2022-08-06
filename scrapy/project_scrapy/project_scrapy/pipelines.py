
from optparse import Values
from itemadapter import ItemAdapter
from tomlkit import value
import xlsxwriter

class ProjectScrapyPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        file_name = crawler.settings.get('XLSX_FILE')
        return cls(xlsx_name=file_name)

    def __init__(self, xlsx_name):
        self.xlsx_name = xlsx_name
        self.workbook = None
        self.worksheet = None
        self.row_index = 0

    def process_item(self, item, spider):
        spider.logger.info('IN SPIDER PROCESSSING')
        adapter = ItemAdapter(item)
        d = adapter.asdict()

        if self.row_index == 0:
            data = d.values()
        else:
            data = d.values()
        
        for col, value in enumerate(data):
            self.worksheet.write_row(self.row_index, col, value)
        self.row_index += 1
        return item

    def open_spider(self, spider):
        spider.logger.info('IN SPIDER OPENING')
        self.workbook = xlsxwriter.Workbook(self.xlsx_name)
        self.worksheet = self.workbook.add_worksheet()

    def close_spider(self, spider):
        spider.logger.info('IN SPIDER CLOSING')
        self.workbook.close()
