#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import time
import random


class Readbook:
    def __init__(self, adb, wechat_list, startwechat, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 从哪一个微信开始运行
        self.wechats_index = startwechat

        self._main = main

        self._swipe_index = 0

        self._input_index = 1

        self._swipe_index_read = 0

    def clean_wechat(self):
        time.sleep(1)
        # 点击进程按钮，显示所有后台进程
        self._adb.adb_keyboard(82)
        time.sleep(1)
        # 点击清理按钮
        self._adb.click_by_text_do_not_refresh0('清理')
        time.sleep(2)

    def send_msg(self):
        print('阅读')
        # self._adb.refresh_nodes()
        time.sleep(2)
        if self._swipe_index_read < 300:
            self._swipe_index_read += 1
            self._adb.adb_swipe(540, 900, 540, 540)
            time.sleep(random.randint(3, 6))
            self.send_msg()
        else:
            self._main.push('success_share', self._wechat_list[self.wechats_index].strip() + '  已经发送')
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self.clean_wechat()
            self._swipe_index = 0
            self._swipe_index_read = 0
            self.wechats_index += 1
            self._input_index = 1
            self.find_wechat()

    def repetition_input(self, path):
        print(path)
        self._adb.adb_input(path)
        time.sleep(4)
        self._adb.adb_click(1020, 1900)
        if self._input_index < 10:
            self._input_index += 1
            self.repetition_input(path)

    def affirm_send(self):
        # self._adb.click_by_text_do_not_refresh2('输入信息')
        self._adb.adb_click(500, 1900)
        time.sleep(1)
        path = 'https://book.qidian.com/info/1013541014'
        print(len(path))
        self.repetition_input(path)
        time.sleep(3)
        if len(path) > 25 and len(path) < 50:
            self._adb.adb_click(700, 1680)
        elif len(path) > 50:
            self._adb.adb_click(700, 1600)
        else:
            self._adb.adb_click(700, 1740)
        time.sleep(5)
        self._adb.refresh_nodes()
        time.sleep(2)
        if self._adb.find_nodes_by_text('免费试读'):
            self._adb.click_by_text_after_refresh('加入书架')
            time.sleep(3)
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('微信'):
                self._adb.click(0)
                time.sleep(8)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('允许'):
                    self._adb.click(0)
                time.sleep(3)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('免费试读'):
                    self._adb.click(0)
                elif self._adb.find_nodes_by_text('继续阅读'):
                    self._adb.click(0)
                time.sleep(3)
                self.send_msg()
            else:
                print('没有进入')
                time.sleep(3)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('微信'):
                    self._adb.click(0)
                    time.sleep(8)
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_text('允许'):
                        self._adb.click(0)
                    time.sleep(3)
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_text('免费试读'):
                        self._adb.click(0)
                    elif self._adb.find_nodes_by_text('继续阅读'):
                        self._adb.click(0)
                    time.sleep(3)
                    self.send_msg()
        elif self._adb.find_nodes_by_text('继续阅读'):
            self._adb.click(0)
            time.sleep(3)
            self.send_msg()
        else:
            self._adb.adb_click(700, 800)
            time.sleep(2)
            self._adb.adb_click(400, 1500)
            time.sleep(2)
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('允许'):
                self._adb.click(0)
            time.sleep(2)
            self._adb.adb_click(700, 800)
            time.sleep(2)
            self._adb.adb_click(200, 800)
            time.sleep(3)
            self.send_msg()

    def find_name(self):
        time.sleep(1)
        self._adb.refresh_nodes()
        time.sleep(1)
        if self._adb.find_nodes_by_text('zzzz'):
            self._adb.click(0)
            time.sleep(2)
            self._adb.refresh_nodes()
            time.sleep(2)
            self._adb.click_by_text_after_refresh('发消息')
            time.sleep(2)
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_content('切换到按住说话'):
                self.affirm_send()
            elif self._adb.find_nodes_by_content('切换到键盘'):
                self._adb.click(0)
                self.affirm_send()
        else:
            if self._swipe_index < 100:
                print('swipe next')
                self._swipe_index += 1
                self._adb.adb_swipe1(540, 1500, 540, 240, 200)
                self.find_name()
            else:
                print('not find')
                self._swipe_index = 0

    def clickbook(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('通讯录'):
            self._adb.click(0)
            time.sleep(1)
            self._adb.click_by_text_after_refresh('通讯录')
            time.sleep(1)
        else:
            time.sleep(3)
            self.clickbook()

    def find_wechat(self):
        time.sleep(2)
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.refresh_nodes()
        time.sleep(2)
        if self.wechats_index < len(self._wechat_list):
            if self._adb.find_nodes_by_text(self._wechat_list[self.wechats_index].strip()):
                print('找到' + self._wechat_list[self.wechats_index].strip())
                self._adb.click(0)
                time.sleep(20)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('　取消　'):
                    self._adb.click(0)
                    time.sleep(1)
                    self.clickbook()
                    self.find_name()
                elif self._adb.find_nodes_by_text('找回密码'):
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self.clean_wechat()
                    self._swipe_index = 0
                    self._swipe_index_read = 0
                    self.wechats_index += 1
                    self._input_index = 1
                    self.find_wechat()
                else:
                    self.clickbook()
                    self.find_name()

        else:
            print('完成')

    def main(self):
        try:
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("ADB Keyboard")
            self.find_wechat()
        except KeyboardInterrupt as e:
            print('e', e)
