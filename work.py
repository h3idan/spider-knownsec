#!/usr/bin/env python
# coding: utf-8

#**********************************
# author:   h3idan
# datetime: 2012-12-25 16:13
#**********************************


import Queue
from clawThread import ClawThread
from optparse import OptionParser
import logging
import time


def logger_config(logfile, loglevel):
    
    level = {
            1:logging.CRITICAL,
            2:logging.ERROR,
            3:logging.WARNING,
            4:logging.INFO,
            5:logging.DEBUG,
            }

    log_format = logging.Formatter("%(levelname)s -10s %(asctime)s %(message)s")
    
    clawlog_handler = logging.FileHandler(logfile)
    clawlog_handler.setFormatter(log_format)
    
    claw_log = logging.getLogger('claw')
    claw_log.setLevel(level.get(loglevel))
    claw_log.addHandler(clawlog_handler)


def work(url, depth, threadNum, keys, dbfile, logfile, loglevel):

    logger_config(logfile, loglevel)

    urlqueue = Queue.Queue(0)
    urltuples = (0, url)
    urlqueue.put(urltuples)
    
    for i in range(threadNum):
        c = ClawThread(urltuples, urlqueue, keys, dbfile, depth)
        c.setDaemon(True)
        c.start()

    urlqueue.join()
    print u'###claw is over###'


if __name__ == '__main__':

    usage = u''

    parser = OptionParser(usage)
    parser.add_option("-u", dest="url", type="string",
                      help=u"指定爬虫开始地址")
    parser.add_option("-d", dest="depth", type="int",
                      help=u"指定爬虫深度")
    parser.add_option("--thread", dest="thread", default="10", type="int",
                      help=u"指定线程池大小，多线程爬取页面，可选参数，默认10")
    parser.add_option("--key", metavar="key", default="", type="string",
                      help=u"页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面")
    parser.add_option("--dbfile", dest="dbfile", type="string", default='sqlite3.db',
                      help=u"存放结果数据到指定的数据库(sqlite)文件中")
    parser.add_option("-f", dest="logfile", default="spider.log", type="string",
                      help=u"日志记录文件，默认spider.log")
    parser.add_option("-l", dest="loglevel", default="4", type="int",
                      help=u"日志记录文件记录详细程度，数字越大记录越详细，可选参数")
    (options, args) = parser.parse_args()

    work(options.url, options.depth, options.thread, options.key, options.dbfile, options.logfile, options.loglevel)
