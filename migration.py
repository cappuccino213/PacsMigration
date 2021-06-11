#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/8 14:21 
# @Author  : Zhang yp
# @File    : migration.py
# @Software: PyCharm
# @license : Copyright(C), eWord Technology Co., Ltd.
# @Contact : yeahcheung213@163.com
import time
import threading
from parseConfig import cfg
from MsSQL import MsSql
from generateSQL import generate_sql
from generateSQL import generate_values

# 目的数据库
dst_dict = {'host': cfg.get('DataBase', 'dstHost'),
            'user': cfg.get('DataBase', 'dstUser'),
            'password': cfg.get('DataBase', 'dstPassword'),
            'db': cfg.get('DataBase', 'dstDatabase')}


# 计时函数
def timer(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        cost_time = end - start
        print("耗费时间：{}secs.".format(cost_time))

    return wrapper


# 数据插入
def insert(sql_statement, values):
    dst_db = MsSql(dst_dict)
    dst_db.add_option(sql_statement, values, True)
    dst_db.close_mssql()


def split_list_by_n(list_collection, n):
    """
    将list按照n平均分组
    :param list_collection: 列表集合
    :param n: 分数
    :return:
    """
    list_split = []
    for i in range(0, len(list_collection), n):
        list_split.append(list_collection[i:i + n])
    return list_split


# 数据迁移执行

@timer
def migration_normal():
    """不分组"""
    sql_statements = generate_sql()
    values = generate_values()
    for i in range(len(sql_statements)):
        insert(sql_statements[i], values[i])


# @timer
# def migration():
#     sql_statements = generate_sql()
#     values = generate_values()
#     for j in range(len(values)):  # 根据配置文件的配置DST表依次插入
#         print('开始表{}({})的数据迁移'.format(j, sql_statements[j].split(' ')[2]))
#         task_amount = cfg.get_int('TACTICS', 'taskAmount')  # 单次任务量
#         split_list = split_list_by_n(values[j], task_amount)  # 任务分组
#         for value_set in split_list:
#             print('进行{0}/{1}数据迁移，本组数据量{2}'.format(split_list.index(value_set) + 1, len(split_list), len(value_set)))
#             insert(sql_statements[j], value_set)
#             print('完成第{0}组数据迁移，剩余{1}组数据----'.format(split_list.index(value_set) + 1,
#                                                     len(split_list) - split_list.index(value_set) - 1))

@timer
def migration():
    """分组"""
    sql_statements = generate_sql()
    values = generate_values()
    for j in range(len(values)):  # 根据配置文件的配置DST表依次插入
        print('开始表{}({})的数据迁移'.format(j, sql_statements[j].split(' ')[2]))
        task_amount = cfg.get_int('TACTICS', 'taskAmount')  # 单次任务量
        split_list = split_list_by_n(values[j], task_amount)  # 任务分组

        # 是否启用多线程
        if cfg.get_bool('TACTICS', 'ifMultiThread'):
            threads = [threading.Thread(target=insert, args=(sql_statements[j], value_set,)) for value_set in
                       split_list]
            for thread in threads:
                print('进行{0}/{1}数据迁移'.format(threads.index(thread) + 1, len(threads)))
                thread.start()
                print('完成第{0}组数据迁移，剩余{1}组数据----'.format(threads.index(thread) + 1,
                                                        len(threads) - (threads.index(thread) + 1)))
        else:
            for value_set in split_list:
                print('进行{0}/{1}数据迁移，本组数据量{2}'.format(split_list.index(value_set) + 1, len(split_list), len(value_set)))
                insert(sql_statements[j], value_set)
                print('完成第{0}组数据迁移，剩余{1}组数据----'.format(split_list.index(value_set) + 1,
                                                        len(split_list) - split_list.index(value_set) - 1))


if __name__ == '__main__':
    # migration1()
    migration()
