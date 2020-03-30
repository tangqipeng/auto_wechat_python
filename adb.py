#!/usr/local/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor
 @file: adb.py
 @time: 2018/11/2 11:02
"""

import time
import os
import re
from plat import adb_path
from enum import Enum
import xml.etree.cElementTree as xmlParser


class By(Enum):
    text = 'text'
    content = 'content-desc'
    naf = 'NAF'
    sel = 'selected'


class Adb:
    def __init__(self, port=None, device=None):
        self._port = port
        self._device = device

        self._p = '' if (port is None) else '-P ' + str(port) + ' '
        self._s = '' if (device is None) else '-s ' + str(device) + ' '

        # 指定端口 指定设备 组装adb命令
        self._baseShell = adb_path() + 'adb ' + self._p + self._s
        # 获取该文件(adb.py) 所在对文件夹路径
        self._basePath = os.path.dirname(__file__)

        # 缓存xml 不需要多此进行文件读取操作
        self._xml = None
        # 缓存当前查找到的nodes => type 列表 | value 字典
        self._nodes = None

        self._x = None
        self._y = None

    def printf(self):
        print(self._port)
        print(self._device)
        print(self._p)
        print(self._s)
        print(self._baseShell)

    def adb_keyboard(self, event):
        os.system(self._baseShell + 'shell input keyevent ' + str(event))

    def adb_unlock_screen(self):
        list = os.popen(self._baseShell + ' shell dumpsys window policy').readlines()
        screenAwakevalue = '    mAwake=true\n'
        if screenAwakevalue in list:
            return True
        else:
            return False

    def adb_put_back(self):
        self.adb_keyboard(4)

    def adb_back_to_desktop(self):
        self.adb_keyboard(3)

    def adb_click(self, x, y):
        os.system(self._baseShell + 'shell input tap ' + str(x) + ' ' + str(y))

    def adb_input(self, text):
        os.system(self._baseShell + 'shell input text ' + str(text))

    def adb_swipe(self, x1, y1, x2, y2):
        self.adb_swipe1(x1, y1, x2, y2, 100)

    def adb_swipe1(self, x1, y1, x2, y2, time):
        os.system(self._baseShell + 'shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(
            y2) + ' ' + str(time))

    def adb_push_image(self, image):
        os.system(self._baseShell + 'push ' + image + ' /sdcard/')
        os.system(
            self._baseShell + 'shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/sdcard0/picture/frame_1.jpg')

    def adb_del_image(self):
        os.system(self._baseShell + 'shell rm -f /storage/sdcard0/picture/frame_1.jpg')

    def adb_refresh(self):
        os.system(self._baseShell + 'shell uiautomator dump /sdcard/dump1.xml')
        os.system(self._baseShell + 'pull /sdcard/dump1.xml ' + self._basePath + '/data/dump1.xml')

    def parse_xml(self):
        self._xml = xmlParser.ElementTree(file=self._basePath + '/data/dump.xml')

    def parse_xml0(self):
        self._xml = xmlParser.ElementTree(file=self._basePath + '/data/dump0.xml')

    def parse_xml1(self):
        self._xml = xmlParser.ElementTree(file=self._basePath + '/data/dump1.xml')

    def parse_xml4(self):
        self._xml = xmlParser.ElementTree(file=self._basePath + '/data/dump4.xml')

    def do_not_refresh_nodes(self):
        # self.adb_refresh()
        self.parse_xml()

    def do_not_refresh_nodes0(self):
        # self.adb_refresh()
        self.parse_xml0()

    def do_not_refresh_nodes4(self):
        # self.adb_refresh()
        self.parse_xml4()

    def refresh_nodes(self):
        self.adb_refresh()
        self.parse_xml1()

    def find_nodes_by_xpath(self, xpath) -> []:
        # 迭代器只能循环一次 故使用self._nodes作为列表保存节点
        nodes = self._xml.iterfind(path=xpath)
        self._nodes = []
        for _node in nodes:
            # elem.attrib 为字典
            self._nodes.append(_node.attrib)
        return self._nodes

    def find_nodes(self, txt, by: By, index=None):
        _index = '' if (index is None) else '[' + str(index) + ']'
        print('_index', _index)
        return self.find_nodes_by_xpath(xpath='.//node[@' + by.value + '="' + txt + '"]' + _index)

    def find_nodes_by_text(self, text, index=None):
        print("text1=" + text)
        return self.find_nodes(text, By.text, index)

    def find_nodes_by_content(self, content, index=None):
        return self.find_nodes(content, By.content, index)

    def search_count(self):
        return len(self._nodes)

    def get_bounds(self, index):
        _bounds = self._nodes[index]['bounds']
        pattern = re.compile(r'\d+')
        return pattern.findall(_bounds)

    def cal_coordinate(self, index=None):
        _index = 0 if (index is None) else index
        _bounds = self._nodes[_index]['bounds']

        pattern = re.compile(r'\d+')
        _result = pattern.findall(_bounds)
        x1 = float(_result[0])
        y1 = float(_result[1])
        x2 = float(_result[2])
        y2 = float(_result[3])

        self._x = (x1 + x2) / 2
        self._y = (y1 + y2) / 2

        return self._x, self._y

    def click(self, cal_index=None):
        self.cal_coordinate(cal_index)
        self.adb_click(self._x, self._y)

    def click_by_text(self, text, index=None):
        self.find_nodes_by_text(text, index)
        self.click(0)

    def click_by_content(self, content, index=None):
        self.find_nodes_by_content(content, index)
        self.click(0)

    def click_by_text_do_not_refresh(self, text, index=None):
        self.do_not_refresh_nodes()
        print("text=" + text)
        self.click_by_text(text, index)

    def click_by_text_do_not_refresh0(self, text, index=None):
        self.do_not_refresh_nodes0()
        print("text=" + text)
        self.click_by_text(text, index)

    def click_by_text_after_refresh(self, text, index=None):
        self.refresh_nodes()
        print("text=" + text)
        time.sleep(2)
        self.click_by_text(text, index)

    def click_by_content_after_refresh(self, content, index=None):
        self.refresh_nodes()
        self.click_by_content(content, index)

    def click_by_text_do_not_refresh4(self, text, index=None):
        self.do_not_refresh_nodes4()
        print("text=" + text)
        self.click_by_text(text, index)

    # ----------------------------------------------------------聊天-----------------------

    def adb_input_chinese(self, text):
        os.system(self._baseShell + 'shell am broadcast -a ADB_INPUT_TEXT --es msg "' + str(text) + '"')

    def click_by_text_after_refresh1(self, text, index=None):
        self.refresh_nodes()
        print("text=" + text)
        time.sleep(2)
        self.click_by_text1(text, index)

    def parse_xml2(self):
        self._xml = xmlParser.ElementTree(file=self._basePath + '/data/dump2.xml')

    def do_not_refresh_nodes2(self):
        # self.adb_refresh()
        self.parse_xml2()

    def click_by_text_do_not_refresh2(self, text, index=None):
        self.do_not_refresh_nodes2()
        print("text=" + text)
        self.click_by_text1(text, index)

    def parse_xml3(self):
        self._xml = xmlParser.ElementTree(file=self._basePath + '/data/dump3.xml')

    def do_not_refresh_nodes3(self):
        # self.adb_refresh()
        self.parse_xml3()

    def click_by_text_do_not_refresh3(self, text, index=None):
        self.do_not_refresh_nodes3()
        print("text=" + text)
        self.click_by_text1(text, index)

    def click_by_text1(self, text, index=None):
        self._text = text
        self.find_nodes_by_text(text, index)
        self.click1(0)

    def click1(self, index=None):
        if self._nodes:
            _index = 0 if (index is None) else index
            _bounds = self._nodes[_index]['bounds']
            print("_bounds=" + _bounds)

            pattern = re.compile(r'\d+')
            _result = pattern.findall(_bounds)
            x1 = float(_result[0])
            y1 = float(_result[1])
            x2 = float(_result[2])
            y2 = float(_result[3])

            self._x = (x1 + x2) / 2
            self._y = (y1 + y2) / 2

            self.adb_click(self._x, self._y)
        else:
            self.adb_swipe(540, 800, 540, 540)
            self.click_by_text_after_refresh1(self._text)
            # if self.find_nodes_by_text(self._text):
            #     self.adb_swipe(540, 1300, 540)
            #     self.click_by_text_after_refresh(self._text)
            # else:
            #     print('没有找到')
