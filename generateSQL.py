#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 17:01 
# @Author  : Zhang yp
# @File    : generateSQL.py
# @Software: PyCharm
# @license : Copyright(C), eWord Technology Co., Ltd.
# @Contact : yeahcheung213@163.com
from parseConfig import cfg
from uuid import uuid4

# 获取插入表
tables = cfg.get('DST', 'tableList')

# 数据源链接
con_dict = {'host': cfg.get('DataBase', 'srcHost'),
            'user': cfg.get('DataBase', 'srcUser'),
            'password': cfg.get('DataBase', 'srcPassword'),
            'db': cfg.get('DataBase', 'srcDatabase')}


# 1生成insert语句
def generate_sql():
    # 获取插入的表list
    table_names = tables.split(',')
    insert_sql_list = []
    for table in table_names:
        # 获取插入的字段名
        filed_name = cfg.get('DST', table)
        # 去掉读取配置中出现的换行符
        if "\n" in filed_name:
            filed_name = filed_name.replace("\n", "")
        # 拼接插入语句
        insert_part = "INSERT INTO {0} ({1})".format(table, filed_name)
        # 拼接赋值语句
        filed_num = len(filed_name.split(','))
        placeholder = ','.join(['%s' for _ in range(filed_num)])
        value_part = "VALUES ({})".format(placeholder)
        # print('表{}的insert语句已生成'.format(table))
        insert_sql_list.append(insert_part + ' ' + value_part)
    return insert_sql_list


# 2获取数据，根据insert表的字段生成与之对应的数据格式
def generate_values():
    from MsSQL import MsSql
    statement = cfg.get('SQLString', 'query')
    data_dict = MsSql(con_dict).query(statement, True)
    data_group = []  # 按表名分组
    for i in range(len(data_dict)):
        data_set = []
        for table in tables.split(','):  # 获取待插入表的表名
            field_string = cfg.get('DST', table)
            if "\n" in field_string:  # 除去换行
                field_string = field_string.replace("\n", "")
            field_list = field_string.split(',')
            values_list = []
            for field in field_list:
                if field in data_dict[i].keys():
                    if field == 'ReportID' and data_dict[i][field] is None:  # 处理ReportID为空的情况
                        data_dict[i][field] = uuid4()
                    if isinstance(data_dict[i][field], str):  # 处理\xa0 空格
                        if u'\xa0' in data_dict[i][field]:
                            data_dict[i][field] = data_dict[i][field].replace(u'\xa0', u'')
                    values_list.append(data_dict[i][field])
                else:
                    values_list.append('')
            data_set.append(tuple(values_list))
        data_group.append(data_set)
    table_group = list(map(list, zip(*data_group)))
    return table_group


if __name__ == '__main__':
    # print(generate_sql())
    print(generate_values())
