# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class JianshuPipeline:

    def __init__(self):
        dbparams = {
            'host': "127.0.0.1",
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'runoob',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.curser = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.curser.execute(self.sql, (item['title'], item['content'], item['author'], item['avatar'],
                            item['pub_time'], item['article_id'], item['origin_url']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id, title, content, author,avatar, pub_time, article_id, origin_url)
            values (null, %s,  %s,  %s,  %s,  %s,  %s,  %s)
            """
            return self._sql
        return self._sql
