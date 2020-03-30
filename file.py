#!/usr/local/bin/python
# -*- coding:utf-8 -*-


import os
import json
import time


def delete_line_breaks(line: str):
    return line.rstrip('\n') if line.__contains__('\n') else line


class File:
    def __init__(self):
        self._basePath = os.path.dirname(__file__)

    # 打开文件 替换换行符为 \n
    def open1(self, path: str, mode='r'):
        return open(file=self._basePath + path, mode=mode, newline='\n', encoding='utf_8_sig')

    # 打开文件 替换换行符为 \n
    def open_w(self, path: str, mode='r'):
        return open(file=self._basePath + path, mode=mode, newline='\n', encoding='utf_8_sig')

    def dump1(self, _list, key):
        stamp = time.strftime("%Y%m%d", time.localtime())

        if not os.path.exists(self._basePath + '/result/' + stamp):
            os.makedirs(self._basePath + '/result/' + stamp)

        with self.open1(path='/result/' + stamp + '/' + key + '.txt', mode='a') as f:
            for e in _list:
                f.write(str(e) + '\n')
            f.close()
        # 清空列表
        _list.clear()

    def dump2(self, value, key):
        stamp = time.strftime("%Y%m%d", time.localtime())

        if not os.path.exists(self._basePath + '/result/' + stamp):
            os.makedirs(self._basePath + '/result/' + stamp)

        with self.open1(path='/result/' + stamp + '/' + key + '.txt', mode='a') as f:
            f.write(str(value) + '\n')
            f.close()

    def json(self):
        with self.open1('/config/config.json') as f:
            o = json.load(f)
            f.close()

        return o
