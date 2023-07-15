# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql
import logging



class WangyinewPipeline:
    """
    同步插入数据库
    """
    def __init__(self):

        self.connect=pymysql.connect(host='localhost',user='root',passwd='123456',db='mydb',charset='utf8',port=3306)
        self.cursor=self.connect.cursor()


    def process_item(self, item, spider):
        table_fields = item.get('table_fields')
        table_name = item.get('table_name')
        if table_fields is None or table_name is None:
            raise Exception('必须要传表名table_name和字段名table_fields，表名或者字段名不能为空')
        values_params = '%s, ' * (len(table_fields) - 1) + '%s'
        keys = ', '.join(table_fields)
        values = ['%s' % str(item.get(i, '')) for i in table_fields]
        insert_sql = 'insert into %s (%s) values (%s)' % (table_name, keys, values_params)
        try:
            self.cursor.execute(insert_sql, tuple(values))
            logging.info("数据插入成功 => " + '1')
        except Exception as e:
            logging.error("执行sql异常 => " + str(e))
            pass
        finally:
            # 要提交，不提交无法保存到数据库
            self.connect.commit()
        return item

        # sql = 'INSERT INTO wangyijob(name,productName,postTypeFullName,description,\
        #     recruitNum,reqEducationName,reqWorkYearsName,requirement,firstPostTypeName,workPlaceNameList) \
        # VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        # self.cursor.execute(sql,(str(item['name']),str(item['productName']),str(item['postTypeFullName']),
        #     str(item['description']),str(item['recruitNum']),str(item['reqEducationName']),
        #     str(item['reqWorkYearsName']),str(item['requirement']),str(item['firstPostTypeName']),str(item['workPlaceNameList'])))
        # self.connect.commit()
        # return item

    def close_spider(self, spider):
        self.connect.close()
        self.cursor.close()




#创建表

# CREATE TABLE `wangyijob` (
#   `name` varchar(255) NOT NULL ,
#   `productName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `postTypeFullName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `recruitNum` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `reqEducationName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `reqWorkYearsName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `requirement` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `firstPostTypeName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
#   `workPlaceNameList` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
# )


