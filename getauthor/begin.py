# -*- coding: utf-8 -*-
from scrapy import cmdline
import time
#name = 'douban_movie -o aerospace.json'
# cmd = 'scrapy crawl


#cmdline.execute(cmd.split())

#cmd = 'scrapy crawl spider -o aerospace.json'
#这样就可以断点续传了。。ctrl+C发出终止命令后，等待一会就会终止，不要着急，访问队列在crawl文件夹里保存，想要再次访问，在此运行就行
# cmdline.execute("scrapy crawl scholar -s LOG_LEVEL=DEBUG -s JOBDIR=crawl_ID".split())
cmdline.execute("scrapy crawl scholar -s LOG_LEVEL=DEBUG -s JOBDIR=crawl".split())
# cmdline.execute("scrapy crawl scholar".split())
# -s LOG_FILE=scrapy.log
# cmdline.execute("scrapy crawl geturl -o refurl_test.csv".split())
# cmdline.execute("scrapy shell 'https://cn.bing.com/academic/search?q=Research+of+Enterprise+Resource+Management+Supporting+Networked+Manufacturing&mkt=zh-cn'".split())
#
# -*- coding: utf-8 -*-
# import scrapy
# from selenium import webdriver
# start_urls = ['https://scholar.google.com/citations?mauthors=label%3Aaerospace&hl=zh-CN&view_op=search_authors']
# # driver = webdriver.PhantomJS()
# driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
# # driver = webdriver.Chrome()
# driver.get(start_urls[0])
# print driver.page_source
# # nextpage = driver.find_element_by_class_name('gs_btnPR')
# nextpage.click()

# searchtable = driver.find_element_by_id('gs_hdr_frm_in_txt')
# searchtable.clear()
# searchtable.send_keys('label:New Materials')
# time.sleep(0.3)
#
# search = driver.find_element_by_id('gs_hdr_tsb')
# search.click()
# try:
#     nextpage = driver.find_element_by_class_name('gs_btnPR')
# except:
#     print '-------------------'
# # nextpage.click()
# cmdline.execute("scrapy shell 'https://scholar.google.com/citations?user=wtMGHCQAAAAJ&hl=zh-CN'".split())

# from selenium import webdriver
#
# driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
# driver.get('http://example.com')
# html_content = driver.page_source
# print(html_content)
# driver.close()
