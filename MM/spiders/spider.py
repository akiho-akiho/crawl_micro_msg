# -*- coding: utf-8 -*-
# ////////////////////////////////////////////////////////////////////
# //                          _ooOoo_                               //
# //                         o8888888o                              //
# //                         88" . "88                              //
# //                         (| ^_^ |)                              //
# //                         O\  =  /O                              //
# //                      ____/`---'\____                           //
# //                    .'  \\|     |//  `.                         //
# //                   /  \\|||  :  |||//  \                        //
# //                  /  _||||| -:- |||||-  \                       //
# //                  |   | \\\  -  /// |   |                       //
# //                  | \_|  ''\---/''  |   |                       //
# //                  \  .-\__  `-`  ___/-. /                       //
# //                ___`. .'  /--.--\  `. . ___                     //
# //              ."" '<  `.___\_<|>_/___.'  >'"".                  //
# //            | | :  `- \`.;`\ _ /`;.`/ - ` : | |                 //
# //            \  \ `-.   \_ __\ /__ _/   .-` /  /                 //
# //      ========`-.____`-.___\_____/___.-`____.-'========         //
# //                           `=---='                              //
# //      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        //
# //              佛祖保佑       永无BUG     永不修改                  //
# ////////////////////////////////////////////////////////////////////

import scrapy
from scrapy.selector import Selector
from MM.items import MmItem
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import hashlib
import time
import string
import os,sys
# import cx_Oracle
import MySQLdb
from snownlp import SnowNLP

class MmSpider(scrapy.Spider):
    name = "Mm"
    start_urls = (
        'http://weixin.sogou.com/',
    )

    def get_keywords(self):
        # conn = MySQLdb.connect(host='172.16.190.140',user='root',passwd='root',db='weixin')
        conn = MySQLdb.connect(host='172.16.190.166',user='root',passwd='root',db='weixin')
        cursor = conn.cursor() 
        sql1 = 'SELECT SEARCHWORDS FROM `keywords`;'
        key = cursor.execute(sql1)
        keywords = cursor.fetchall()

        searchtime = time.strftime('%Y-%m-%d %H:%M')
        sql2 = "update keywords set `searchtime`='"+searchtime + "'"
        n = cursor.execute(sql2)  
        # sql2 = "UPDATE keywords SET LASTSEARCHTIME='" + searchtime +"', KEYWORDS_STAT='1'"
        # sql2 = 'UPDATE `weixin`.`keywords` SET `SEARCHTIME`=' + searchtime + ', `STATUS`=1;'
        # cursor.execute(sql2)
        conn.commit()
        cursor.close()
        conn.close()
        return keywords

    def parse(self, response):
        # keywords = self.get_keywords()
        keywords = [('东软',),('成都东软',)]
        # keywords = [('川大',),('四川大学',),('周永康',)]
        for keyword in keywords:
            for i in range(1,3):
                # url = 'http://weixin.sogou.com/weixin?query=' + keyword +'&fr=sgsearch&type=2&cid=null&page=' + str(i) + '&ie=utf8'
                # sogou_url = 'http://weixin.sogou.com/weixin?type=2&query='+keyword[0]+'&fr=sgsearch&ie=utf8&_ast=1426126848&_asf=null&w=01019900&p=40040100&dp=1&cid=null&sut=2196&sst0=1426126961126&lkt=0%2C0%2C0'
                sogou_url = 'http://weixin.sogou.com/weixin?query='+keyword[0]+'&fr=sgsearch&type=2&page='+str(i)+'&ie=utf8&sourceid=inttime_week'
                yield Request(sogou_url, self.parse_site)


    def parse_site(self, response):
        sel = Selector(response)
        sites = sel.xpath("//div[@class='txt-box']")
        items = []
        for site in sites:
            item = MmItem()
            urls = site.xpath('h4/a/@href').extract()
            for url in urls:
                #item['url'] = url
                searchwords = sel.xpath('//*[@id="upquery"]/@value').extract()
                searchwords = ''.join(searchwords)
                #item['searchwords'] = searchwords
                yield scrapy.Request(url, self.parse_details, meta={'item':item})



    def parse_details(self, response):
        sel = Selector(response)
        item = response.meta['item']
        print item
        title = sel.xpath('//*[@id="activity-name"][1]/text()').extract()        
        pubtime = sel.xpath('//*[@id="post-date"]/text()').extract()
        fetchtime = time.strftime('%Y-%m-%d %H:%M')
        source = sel.xpath('//*[@id="post-user"]/text()').extract()
        content = sel.xpath('//*[@id="js_content"]//text()').extract()
        rawcontent = sel.xpath('//*[@id="js_content"]').extract()
        site = u'微信公众平台'


        # item['site'] = site.encode('utf-8')

        source = ''.join(source)
        # item['source'] = source

        pubtime = ''.join(pubtime)
        item['pubtime'] = pubtime
        
        # item['fetchtime'] = fetchtime

        title1 = ''.join(title)
        item['title'] = title1

        content = ''.join(content)
        # item['content'] = content
        (color, keywords) = self.content_color(content)
        if color >= 0.8:
            item['public_opinion'] = u'正'
        elif color < 0.4:
            item['public_opinion'] = u'负'
        else:
            item['public_opinion'] = u'中'
        # keywords = ','.keywords
        print '++++++++++++++++++++++++++++++++++++++++++++++++++'
        print keywords


        item['keywords'] = keywords

        # rawcontent = ''.join(rawcontent)
        # item['rawcontent'] = rawcontent

        # item['searchwords'] = '川大'
        # title = str(title)
        wait_to_md5 = item['url']+item['searchwords']
        md5 = self.md5(wait_to_md5)
        # item['MD5'] = title_md5
        item['MD5'] = md5

        # populate more `item` fields
        return item
        
    def md5(self, str):
        import hashlib
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()
        
    def content_color(self, content):
        s = SnowNLP(content)
        color = s.sentiments
        keywords = s.keywords(3)
        print keywords
        return color, keywords
