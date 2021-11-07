import scrapy
import logging
from feed.items import QuotesItem

# # 这种方法会出现中文乱码，没有指定文件的编码格式
# logging.basicConfig(
#     filename='log.txt',
#     format='%(levelname)s: %(message)s',
#     level=logging.INFO
# )

# 先创建一个文件并指定编码格式，解决中文乱码问题
# file = open("log.txt", encoding="utf-8", mode="a")
# logging.basicConfig(
#     # filename='log.txt',
#     stream=file,
#     format='%(levelname)s: %(message)s',
#     level=logging.INFO
# )

logger = logging.getLogger('mycustomlogger')

class FdSpider(scrapy.Spider):
    name = 'fd'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com//']
    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_URI': 'quotes.jsonlines',
        'FEED_EXPORT_INDENT': 4,
    }

    # custom_settings = {
    #     'FEED_EXPORT_ENCODING': 'utf-8',
    #     'FEED_FORMAT': 'csv',
    #     'FEED_URI': '%(name)s.csv',
    #     'FEED_EXPORT_FIELDS': ['text','author']
    # }

    def __init__(self, category=None, *args, **kwargs):
        super(FdSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://quotes.toscrape.com/tag/life/']

    def parse(self, response):
        self.logger.info('========》 Parse function called on %s', response.url)
        logger.info('========》 Parse function called on %s', response.url)
        quote_block = response.css('div.quote')
        for quote in quote_block:
            text = quote.css('span.text::text').extract_first()
            author = quote.xpath('span/small/text()').extract_first()
            # item = dict(text=text, author=author)
            item = QuotesItem()
            item['text'] = text[1:10]  # 获取1~9个字符
            item['author'] = author
            yield item

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
