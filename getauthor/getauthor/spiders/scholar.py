# -*- coding: utf-8 -*-
import scrapy
from getauthor.items import GetauthorItem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.http import Request
from scrapy.selector import Selector
from getauthor.Fields import Fields
# from getauthor.scrapy_redis.spiders import RedisSpider
import time
from random import random




Url = 'https://scholar.google.com'
# a=set()


# def geturl(i):
#     a = set()
#     # start = 'https://scholar.google.com/citations?mauthors=label%3Aaerospace&hl=zh-CN&view_op=search_authors'
#     start = 'https://scholar.google.com/citations?view_op=search_authors&hl=zh-CN&mauthors=label:Applied_Math&after_author=1d02ANT8__8J&astart=30'
#     #下边两种方式都不行，真是头疼
#     # driver = webdriver.PhantomJS()
#     # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=True'])
#     driver = webdriver.Chrome()
#     driver.get(start)
#     # 向搜索框内填写数据
#     searchtable = driver.find_element_by_id('gs_hdr_tsi')
#     searchtable.clear()
#     key = 'label:' + i
#     searchtable.send_keys(key)
#     #给个时间载入页面
#     time.sleep(0.3)
#     # 点击搜索
#     search = driver.find_element_by_id('gs_hdr_tsb')
#     search.click()
#     # 应该有一个异常处理的过程，就是搜索界面没有人物使该怎么办，比如big data就没有
#     # 进入当前领域第一页,初始化ur11，url2
#     url1 = '1'
#     url2 = '2'

    # while url1 != url2:
    #     url1 = driver.current_url
    #     a.add(url1)
    #     time.sleep(0.3)
    #     nextpage = driver.find_element_by_xpath('//*[@id="gsc_authors_bottom_pag"]/div/button[2]')
    #     nextpage.click()
    #     url2 = driver.current_url
    #     # try:
    #     #     nextpage=driver.find_element_by_class_name("gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx")
    #     #     # nextpage = driver.find_element_by_class_name('gs_in_ib')
    #     # except NoSuchElementException as msg:
    #     #     url1 = 1
    #     #     url2 = 1
    #     #     #没有的条目可以存在文件里
    #     #     # nextpage = driver.find_element_by_class_name('gs_ico')
    #     #     print 'there are only one page in '+ i
    #     # else:
    #     #     nextpage.click()
    #     #     url2 = driver.current_url
    # driver.close()
    # return list(a)

class ScholarSpider(scrapy.Spider):
# class ScholarSpider(RedisSpider):
    name = 'scholar'
    allowed_domains = ['scholar.google.com']
    # redis_key = "scholar:start_urls"
    start_url = list(set(Fields))
    scrawl_ID = set(start_url)  # 记录待爬
    finish_ID = set()  # 记录已爬


    def start_requests(self):
        #先运行下边这一部分，得到所有7个关键字的学者数据
        #不知道为什么scrawl_ID叠加的起不到相关的作用,是不是并行请求的太多了，我现在把并行的设为16，之前是100，这次应该可以了吧
        while self.scrawl_ID.__len__():
            field = self.scrawl_ID.pop()
            self.finish_ID.add(field)  # 加入已爬队列
            url = 'https://scholar.google.com/citations?view_op=search_authors&hl=zh-CN&mauthors=label:'+field
            yield Request(url=url, callback=self.parse1)
        #上边那一部分运行完后，在运行下面这一部分，爬取相关领域的学者数据
        # with open("./field.txt","r") as f:
        #     fields = f.readlines
        # for field in fields:
        #     url = 'https://scholar.google.com/citations?view_op=search_authors&hl=zh-CN&mauthors=label:' + field
        #     yield Request(url=url, callback=self.parse1)
    def parse1 (self, response):
        #这个解析函数先处理每个领域第一页的人，用selector
        sel = Selector(response)
        authorurl = sel.xpath('//a[contains(@href,"/citations?user")]/@href').extract()
        t1 = response.url
        a = sel.xpath('//*[@id="gsc_authors_bottom_pag"]/div/button[2]/@onclick').extract()
        for url in authorurl:
            aurl= Url + url
            yield Request(url = aurl,callback = self.parse_info)

        if a!=[]:
            b = a[0].split('\\')
            c = b[-3]
            after_author = c[3:len(c)]
            L = t1.split('&')
            next2 = L[0] + '&' + L[1] + '&' + L[2] + '&after_author=' + after_author + '&astart=' + str(10)
            # print '-----------------1---------------------'
            yield Request(url = next2,callback = self.parse2)

    #主要处理某个领域第二页以后的情况
    def parse2(self, response):
        sel = Selector(response)
        authorurl = sel.xpath('//a[contains(@href,"/citations?user")]/@href').extract()

        # print authorurl
        for url in authorurl:
            aurl = Url + url
            yield  Request(url=aurl, callback=self.parse_info)

        t1 = response.url
        a = sel.xpath('//*[@id="gsc_authors_bottom_pag"]/div/button[2]/@onclick').extract()
        if a!=[]:
            b = a[0].split('\\')
            c = b[-3]
            after_author = c[3:len(c)]
            L = t1.split('&')
        # n = int(t1[-2:len(t1)])
        # L[-1]-7为当前页码的位数
            w = len(L[-1])-7
            n=L[-1][-w:]
            N = int(n) + 10
            # print N
            next = L[0] + '&' + L[1] + '&' + L[2] + '&after_author=' + after_author + '&astart=' + str(N)
            # print '-----------------3--------------------'
            yield  Request(url=next, callback=self.parse2)

   #处理作者详情页
    def parse_info(self,response):
        sel = Selector(response)
        i = GetauthorItem()
        url = response.url
        c = url.split('user=')
        i['ID'] = c[1].split('&')[0]
        i['authorurl'] = url
        i['Name'] = sel.xpath('//*[@id="gsc_prf_in"]/text()').extract()[0]
        Fields =sel.xpath('//*[contains(@href,"/citations?view_op=search_author")]/text()').extract()
        for field in Fields:
            if field not in self.finish_ID:
                if field not in self.scrawl_ID:
                    if ' ' in field:
                        field.replace(' ','_')
                        self.scrawl_ID.add(field)
                        # print self.scrawl_ID
                        with open("./field.txt", "a") as f:
                            f.write(field + '\n')


        i['Fields'] = Fields
        Totalref = sel.xpath('//td[@class="gsc_rsb_std"]/text()').extract()
        if Totalref:
            i['Totalref'] = Totalref[0]
        Affi = sel.xpath('//*[@id="gsc_prf_i"]//text()').extract()
        i['Affi'] = Affi[1:len(Affi)-len(Fields)-1]

        coauthorurl = 'https://scholar.google.com/citations?view_op=list_colleagues&hl=zh-CN&user='+response.url[42:54]
        yield Request(url = coauthorurl,meta={'item':i},callback=self.parse_coauthorurl)

    def parse_coauthorurl(self,response):
        i = response.meta['item']
        sel = Selector(response)
        name = sel.xpath('//a[contains(@href,"/citations?user")]//text()').extract()
        # Coauthorurl = sel.xpath('//a[contains(@href,"/citations?user")]/@href').extract()
        i['Coauthor'] = name[1:len(name)]
        yield i

