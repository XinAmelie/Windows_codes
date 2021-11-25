#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
import sqlite3
from config.settings import Settings as ST


# 封装类
class MysqlHelp(object):
    # 构造
    def __init__(self,host,user,passwd,port,database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = database

    # 创建连接
    def open_coon(self):
        self.coon = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd,port =self.port,db=self.db,charset='utf8')
        self.cursor = self.coon.cursor()

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.coon.cursor()

    # 调用语句
    def insert_delete_update(self, sql, params=[]):
        try:
            self.open_coon()
            self.cursor.execute(sql, params)
            print("OK")
            self.coon.commit()
            self.close()

        except Exception as erorr:
            print(erorr)

    # 查询 接收全部的返回结果行

    def select_fetchall(self, sql, params=[]):
        try:
            self.open_coon()
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            self.coon.commit()
            self.close()
            return results

        except Exception as erorr:
            print(erorr)


class Sqlite3Tools():
    """
    simpleToolSql for sqlite3
    简单数据库工具类
    编写这个类主要是为了封装sqlite，继承此类复用方法
    """

    def __init__(self, path=ST.DBPATH):
        """
        初始化数据库，默认文件名 stsql.db
        filename：文件名
        """
        self.db = sqlite3.connect(path)
        self.c = self.db.cursor()

    def close(self):
        """
        关闭数据库
        """
        self.c.close()
        self.db.close()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.c.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            return False, e
        if count > 0:
            return True
        else:
            return False

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        if param is None:
            self.c.execute(sql)
        else:
            self.c.execute(sql, param)
        return self.c.fetchall()


if __name__ == '__main__':
    handle_sql = MysqlHelp("lportal")
    result = handle_sql.select_fetchall("select * from journalarticle;")
    print(result)


