#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import time
import file
from adb import By


class Addgroup:
    def __init__(self, adb, wechat_list, group_names, wechat_index, endsign, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 群名
        self._group_list = group_names
        # 从哪一个微信开始运行
        self.wechats_index = wechat_index

        self._end_sign = endsign

        self._main = main

    def add_group(self):
        print('add_group')

    def search_group(self):
        print('search_group')
        self._adb.refresh_nodes()
        time.sleep(1)
        if self._adb.find_nodes_by_text('选择一个群'):
            print('进入')
            self._adb.click(0)
            self._adb.refresh_nodes()
            time.sleep(1)
            if self._adb.find_nodes_by_text(self._group_list[self.wechats_index]):
                self._adb.click(0)
            else:
                self._adb.click_by_text_after_refresh('返回')
        else:
            print('没有')

    # 找到需要打开的微信
    def find_wechat(self):
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.refresh_nodes()
        time.sleep(2)
        if self.wechats_index < len(self._wechat_list):
            if self._adb.find_nodes_by_text(self._wechat_list[self.wechats_index]):
                print('找到' + self._wechat_list[self.wechats_index])
                self._adb.click(0)
                time.sleep(15)
                self._adb.click_by_text_after_refresh('通讯录')
                time.sleep(1)
                self._adb.click_by_text_do_not_refresh('外部联系人')
                time.sleep(1)
                self._adb.click_by_text_do_not_refresh('发起群聊')
                time.sleep(2)
                self.search_group()
                # self._adb.click_by_text_do_not_refresh('公众号')
                # time.sleep(3)

    def test(self):
        self._adb.refresh_nodes()
        self._adb.adb_click(1000, 130)
        time.sleep(0.1)
        self._adb.click_by_content_after_refresh('添加成员')
        time.sleep(0.1)
        self._adb.click_by_text_after_refresh('搜索')
        time.sleep(0.1)
        self._adb.refresh_nodes()

    def main(self):
        # self.test()
        try:
            self.find_wechat()

        except KeyboardInterrupt as e:
            print('e', e)
