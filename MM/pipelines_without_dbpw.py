# -*- coding: utf-8 -*-
import json
import codecs
from MM.items import MmItem
import string

import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8' 

import sys 
reload(sys)
sys.setdefaultencoding("utf-8")
 
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import cx_Oracle
import MySQLdb
class MmPipeline(object):
    def __init__(self):
        # self.conn = cx_Oracle.connect('db@host')
        self.conn =  MySQLdb.connect(host='172.16.190.166',user='root',passwd='root',db='weixin')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql1 = []
        sql2 = []
        sql = []
        value = [
            str(item['url']),
            str(item['site']), 
            str(item['source']),
            str(item['pubtime']),
            str(item['fetchtime']),
            # str(item['fetchtime']),
            str(item['title']),
            str(item['content']),
            # str(item['resource']),
            str(item['rawcontent']),
            str(item['keywords']),
            str(item['searchwords']),
            str(item['MD5']),
            str(item['public_opinion']),
            ]
        try:
            # self.cursor.execute("INSERT into WEIXIN_SEARCH_DATA (URL, SITE, SOURCE, PUBTIME, FETCHTIME, TITLE, CONTENT, RAWCONTENT, SEARCHWORDS, MD5) VALUES(item['url'], item['site'], item['source'], item['pubtime'], sysdate, item['title'], item['content'], item['rawcontent'], 'scu', item['MD5'])")
            # ===============================oracle======================================
            # sql1 = 'INSERT INTO '+'WEIXIN_SEARCH_DATA '+'(URL, SITE, SOURCE, PUBTIME, FETCHTIME, TITLE, CONTENT, RAWCONTENT, SEARCHWORDS, MD5) VALUES  '
            # sql2 = ' (:url, :site, :source, :pubtime, :fetchtime, :title, :content, :rawcontent, :searchwords, :MD5) '
            # sql = sql1 + sql2
            # self.cursor.execute(sql, value)
            # ===========================================================================
            sql1 = 'INSERT INTO `data` (`URL`,`SITE`,`SOURCE`,`PUBTIME`,`FETCHTIME`,`TITLE`,`CONTENT`,`RAWCONTENT`,`SEARCHWORDS`,`MD5`) VALUES '
            sql2 = ' (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            sql = "".join([sql1, sql2])
            self.cursor.execute(sql, value)
            self.conn.commit()

        # except cx_Oracle.DatabaseError as e:
        #     error, = e.args
        #     if error.code == 955:
        #         print('Table already exists')
        #     elif error.code == 1031:
        #         print("Insufficient privileges")
        #     print(error.code)
        #     print(error.message)
        #     print(error.context)
        #     raise
        except:
            print "QQQAQQQ!!!!!!!!!!!!"


        # Only commit if it-s necessary.
        # if commit:
        #     self.conn.commit()
        	
        return item

class MmPipelineJosn(object):
    """docstring for MmPipelineJosn"""
    def __init__(self):
        self.file = codecs.open('MM.json','wb', encoding = 'utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode-escape"))
        return item
