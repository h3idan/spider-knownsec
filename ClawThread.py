#!/usr/bin/env python
# coding: utf-8

#**********************************
# author:   h3idan
# datetime: 2012-12-26 16:13
#**********************************


import threading
from bs4 import BeautifulSoup
from WebPage import GetPage
import re
import urllib2
from SaveDB import SaveDatabase
import logging


log = logging.getLogger('claw.ClawThread')


class ClawThread(threading.Thread):
    '''
    多线程并发爬虫的类
    '''
    def __init__(self, urltuples, urlqueue, keys, dbfile, depth):
        threading.Thread.__init__(self)
        self.urltuples = urltuples      # (0, url) 0:层数，url：链接
        self.urlqueue = urlqueue        # 存放url的队列
        self.keys = keys                # 关键字
        self.savedatabase = SaveDatabase(dbfile)        # 数据库文件
        self.depth = depth              # 深度
        self.urls = []

    def run(self):
        while not self.urlqueue.empty():
            urltuples = self.urlqueue.get()     # 从队列中取出一个url
            currentdepth, url = urltuples
            self.add_urlqueue(urltuples)        # 解析出该url页面中所有的url，加入队列
            print 'clawing url: %s ----- %s' % (url, currentdepth)
            log.info('clawing url: %s ----- %s' % (url, currentdepth))
            self.claw_start(urltuples, url, currentdepth)       # 查找关键字，存入数据库
            print self.urlqueue.qsize()
            print '----------------clawing-----------------------'
        self.savedatabase.close()

    def claw_start(self, urltuples, url, currentdepth):
        ''' 调用find_key_savedb保存数据 '''
        htmlsource = GetPage(urltuples).get_html()
        if htmlsource:
            self.find_key_savedb(url, currentdepth, htmlsource)
        self.urlqueue.task_done()

    def find_key_savedb(self, url, currentdepth, htmlsource):
        ''' 查找关键字，将找到关键字的url及相关数据存到数据库 '''
        if self.keys:
            soup = BeautifulSoup(htmlsource)
            if soup.findAll(text=re.compile(self.keys)):        # 匹配关键字，将找到关键字的URL等数据存入数据库
                self.savedatabase.insert_db(url, currentdepth, htmlsource, self.keys)
                print 'save url: %s ---- %s' %(url, currentdepth)
                log.info('save url: %s ---- %s' %(url, currentdepth)
)
            else:
                print " Don't find keyword:  %s" % url
                log.info(" Don't find keyword:  %s" % url)
        else:
            self.savedatabase.insert_db(url, currentdepth, htmlsource, '')

    def add_urlqueue(self, urltuples):
        ''' 解析URL，向队列中添加解析好的url '''
        id, url = urltuples
        try:
            html = urllib2.urlopen(url).read()
        except Exception, e:
            print "error: %s'\n url: %s'" % (e, url)
            log.debug("error: %s'\n url: %s'" % (e, url))
        else:
            if id <= self.depth-1:        # 判断该url的深度。
                soup = BeautifulSoup(html)
                tag_a = soup.findAll('a', onclick=None, href=re.compile('^http:|^/'))       # 解析出a标签的href属性，去除#
                for i in tag_a:
                    s = i['href'].rstrip('/')
                    href = s.encode('utf-8')
                    if href.startswith('/'):    # 解决相对路径的问题
                        href = url + href
                    if href not in self.urls:       # 判断该url是否在列表中，如果不存在，加入列表，加入队列。避免爬取重复url
                        self.urls.append(href)
                        self.urlqueue.put((id+1, href))

