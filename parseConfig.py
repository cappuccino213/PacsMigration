#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 13:47 
# @Author  : Zhang yp
# @File    : parseConfig.py
# @Software: PyCharm
# @license : Copyright(C), eWord Technology Co., Ltd.
# @Contact : yeahcheung213@163.com
import os
import configparser


class Config:
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("no such file:{}".format(self._path))
        # ConfigParser支持值的插值，即值可以在被 get() 调用返回之前进行预处理,
        # https://docs.python.org/zh-cn/3/library/configparser.html#interpolation-of-values
        self._config = configparser.ConfigParser(allow_no_value=True)
        self._config.read(self._path)

    # 普通解析，返回string
    def get(self, section, name):
        return self._config.get(section, name)

    # 返回int
    def get_int(self, section, name):
        return self._config.getint(section, name)

    # 返回float
    def get_float(self, section, name):
        return self._config.getfloat(section, name)

    # 返回bool
    def get_bool(self, section, name):
        return self._config.getboolean(section, name)


cfg = Config()

if __name__ == '__main__':
    cfg = Config()
    # print(cfg.get('DataBase','srcHost'))
    print(cfg.get('SQLString','query'))