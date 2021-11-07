# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymysql import cursors
from twisted.enterprise import adbapi


# 知识点待整理; ConnectionPool
class JianShuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': "127.0.0.1",
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'runoob',
            'charset': 'utf8',
            "cursorclass": cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id, title, content, author,avatar, pub_time, article_id, origin_url)
            values (null, %s,  %s,  %s,  %s,  %s,  %s,  %s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['content'], item['author'], item['avatar'],
                            item['pub_time'], item['article_id'], item['origin_url']))

    def handle_error(self, error, item, spider):
        print("=" * 10 + "error begin" + "=" * 10)
        print(error)
        print("=" * 10 + "error end" + "=" * 10)
