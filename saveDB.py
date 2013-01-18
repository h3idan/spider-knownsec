#!/usr/bin/env python
# coding: utf-8

#**********************************
# author:   h3idan
# datetime: 2012-12-25 17:26
#**********************************


import sqlite3

class SaveDatabase():
    '''
    将抓取到的URL，htmlsource，currentdepth，keys数据保存到dbfile
    '''
    def __init__(self, dbfile):
        self.dbfile = dbfile
        try:
            self.conn = sqlite3.connect(self.dbfile, isolation_level=None, check_same_thread = False)  # 可以让sqlite3多线程使用，自动commit
            self.conn.execute("""
                    create table if not exists html(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    url text, 
                    currentdepth integer,
                    htmlsource text,
                    keys test)
                    """)
        except:
            self.conn = None

    def insert_db(self, url, currentdepth, htmlsource, keys=''):
        if self.conn:
            self.conn.text_factory = str        # 转换编码    
            sql = """insert into html(url, currentdepth, htmlsource, keys) values(?, ?, ?, ?)"""
            self.conn.execute(sql, (url, currentdepth, htmlsource, keys))
        else:
            raise sqlite3.OperationalError, 'sqlite3 is not connected'

    def close(self):            # 关闭数据库链接
        if self.conn:
            self.conn.close()
        else:
            raise sqlite3.OperationalError, 'sqlite3 is not connected'


