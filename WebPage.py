#!/usr/bin/env python
# coding: utf-8

#**********************************
# author:   h3idan
# datetime: 2012-12-26 15:58
#**********************************


import urllib2
from bs4 import BeautifulSoup
import chardet
import re
import logging
import traceback


log = logging.getLogger('claw.GetPage')

class GetPage():
    '''
    读取到url的htmlsource，解析出该htmlsource中所有href
    '''
    def __init__(self, urltuples):
        self.urltuples = urltuples
        self.urls = []


    def get_html(self):
        url = self.urltuples[1]
        try:
            html = urllib2.urlopen(url, timeout=15).read()
        except Exception, e:
            print "error: %s'\n url: %s'" % (e, url)
            log.debug("URL: %s" % url + traceback.format_exc())
 
        else:
            return html
    
    
    #def get_url(self):
    #    id, url = self.urltuples
    #    try:
    #        html = urllib2.urlopen(url, timeout=15).read()
    #    except Exception, e:
    #        print "error: %s'\n url: %s'" % (e, url)
    #    else:
    #        soup = BeautifulSoup(html)
    #        tag_a = soup.findAll('a', onclick=None, href=re.compile('^http:|^/'))   # 查找a标签，
    #        for i in tag_a:
    #            s = i['href'].rstrip('/')
    #            href = s.encode('utf-8')
    #            if href.startswith('/'):  # 解决锚点的问题
    #                href = url + href
    #            self.urls.append((id+1, href))
    #        urllist = list(set(self.urls))
    #        return urllist
