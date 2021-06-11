#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 14:29 
# @Author  : Zhang yp
# @File    : MsSQL.py
# @Software: PyCharm
# @license : Copyright(C), eWord Technology Co., Ltd.
# @Contact : yeahcheung213@163.com

import pymssql


class MsSql:
    def __init__(self, _connect):
        """
        :param _connect: 数据库连接的dict
        """
        self.conn = pymssql.connect(host=_connect.get('host'),
                                    user=_connect.get('user'),
                                    password=_connect.get('password'),
                                    database=_connect.get('db'),
                                    charset='utf8')
        # 定义游标
        self.cur = self.conn.cursor()

        # 定义返回字典的游标
        self.cur_dict = self.conn.cursor(as_dict=True)

    def query(self, sql_statement, is_dict=False):
        """
        sql语句查询
        :param sql_statement: sql语句
        :param is_dict: 返回带有字段名的字典或是元祖
        :return:
        """
        if is_dict:
            # columns = [column[0] for column in self.cur.description]
            # data = []
            # for row in self.cur.fetchall():
            #     data.append(dict(zip(columns, row)))
            # return data
            self.cur_dict.execute(sql_statement)
            return self.cur_dict.fetchall()
        else:
            self.cur.execute(sql_statement)
            return self.cur.fetchall()

    def add_option(self, sql_statement, value, is_batch=False):
        """
        数据插入操作
        :param sql_statement: 插入语句
        :param value: 插入数据值
        :param is_batch: 是否批量插入
        :return:
        """
        try:
            if is_batch:
                self.cur.executemany(sql_statement, value)
            else:
                self.cur.execute(sql_statement, value)
        except Exception as e:
            print("执行{0}{1}异常，异常{2}，操作回滚".format(sql_statement, value, str(e)))
        else:
            self.conn.commit()
            print("表{}事务提交成功".format(sql_statement.split(' ')[2]))

    def close_mssql(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    from parseConfig import cfg

    con_dict = {'host': cfg.get('DataBase', 'srcHost'),
                'user': cfg.get('DataBase', 'srcUser'),
                'password': cfg.get('DataBase', 'srcPassword'),
                'db': cfg.get('DataBase', 'srcDatabase')}

    my_mssql = MsSql(con_dict)
    statement = cfg.get('SQLString', 'query')
    get_data = my_mssql.query(statement, True)
    print([data for data in get_data])
