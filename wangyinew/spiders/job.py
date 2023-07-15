import scrapy
from wangyinew.items import WangyinewItem
import json

next_page =1 

class JobSpider(scrapy.Spider):
    name = "job"
    allowed_domains = ["163.com"]
    #start_urls = ["https://hr.163.com/job-list.html"]
    start_urls = ["https://hr.163.com/api/hr163/position/queryPage"]
    # allowed_domains = ["tencent.com"]
    # start_urls = ["https://careers.tencent.com/search.html?&start=O#a"]

    def __init__(self):
        self.table_name = 'wangyijob'
        self.table_fields = ['name','productName','postTypeFullName','description','recruitNum',
        'reqEducationName','reqWorkYearsName','requirement','firstPostTypeName','workPlaceNameList']


    def start_requests(self):
        url = self.start_urls[0]
        print(url)
        # 起始url参数
        payload = {
            "currentPage": "1",
            "keyword":"Python",
            "pageSize": "10"
        }
        print(json.dumps(payload))
        # 构建post请求
        yield scrapy.Request(
            url=url,
            body=json.dumps(payload),
            method='POST',
            callback=self.parse,
            headers={'Content-Type': 'application/json'}
        )

    def parse(self, response):
        dic = response.json()
        job_list = dic['data']['list']
        item = WangyinewItem()
        item['table_fields'] = self.table_fields
        item['table_name'] = self.table_name
        for job in job_list:
            item['name'] = job['name']
            item['productName'] = job['productName']
            item['postTypeFullName'] = job['postTypeFullName']
            item['description'] = job['description'].replace('\t','').replace('\n','')
            item['recruitNum'] = job['recruitNum']
            item['reqEducationName'] = job['reqEducationName']
            item['reqWorkYearsName'] = job['reqWorkYearsName']
            item['requirement'] = job['requirement'].replace('\t','').replace('\n','')
            item['firstPostTypeName'] = job['firstPostTypeName']
            item['workPlaceNameList'] = str(job['workPlaceNameList']).replace('[','').replace(']','').replace("'",'')
            # 处理数据
            yield item

        #模拟翻页

        page_stutas = dic['data']['lastPage']  # 返回的数据中来判断是否为最后一页 true为最后一页    
        global next_page 
        next_page = next_page + 1
        print(next_page)
        if page_stutas == False:  # 回调出口
            payload = {
            "currentPage":"{}".format(next_page),
            "keyword":"Python",
            "pageSize": "10"
            }
            print(payload)
            url = self.start_urls[0]           
            yield scrapy.Request(
                url=url,
                body=json.dumps(payload),
                method='POST',
                callback=self.parse,
                headers={'Content-Type':'application/json'}
            )
        



