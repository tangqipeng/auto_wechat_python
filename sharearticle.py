#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import time


class Sharearticle:
    def __init__(self, adb, wechat_list, common_name, sharetxt, article_list, startwechat, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 发送消息的名字
        self._name = common_name
        # 需要分享的话
        self._share_str = sharetxt
        # 分享次数
        self._send_num = 1
        # 从哪一个微信开始运行
        self.wechats_index = startwechat

        self._articlelist = article_list

        self._swipe_index = 0

        self._input_index = 1

        self._main = main

    def clean_wechat(self):
        time.sleep(1)
        # 点击进程按钮，显示所有后台进程
        self._adb.adb_keyboard(82)
        time.sleep(1)
        # 点击清理按钮
        self._adb.click_by_text_do_not_refresh0('清理')
        time.sleep(2)

    def send_msg(self):
        print('发送')
        self._adb.click_by_text_after_refresh('发表')
        time.sleep(5)
        self._adb.refresh_nodes()
        time.sleep(2)
        if self._adb.find_nodes_by_content('发表'):
            self.send_msg()
        else:
            self._main.push('success_share', self._wechat_list[self.wechats_index].strip() + '  已经发送')
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self.clean_wechat()
            self._swipe_index = 0
            self.wechats_index += 1
            self._input_index = 1
            self.find_wechat()

    def repetition_input(self, path):
        print(path)
        self._adb.adb_input(path)
        time.sleep(4)
        self._adb.adb_click(1020, 1900)
        if self._input_index < self._send_num:
            self._input_index += 1
            self.repetition_input(path)

    def affirm_send(self):
        # self._adb.click_by_text_do_not_refresh2('输入信息')
        self._adb.adb_click(500, 1900)
        time.sleep(1)
        if self._articlelist is not None:
            path = self._articlelist[0]
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
            if self._adb.find_nodes_by_content('更多'):
                self._adb.click(0)
                time.sleep(2)
                self._adb.refresh_nodes()
                time.sleep(1)
                self._adb.click_by_text_after_refresh('分享到朋友圈')
                time.sleep(2)
                self._adb.refresh_nodes()
                time.sleep(1)
                self._adb.click_by_text_after_refresh('这一刻的想法...')
                time.sleep(1)
                self._adb.adb_input_chinese(self._share_str)
                time.sleep(1)
                self.send_msg()
            else:
                if len(path) > 25 and len(path) < 50:
                    self._send_num = 8
                elif len(path) > 50:
                    self._send_num = 6
                else:
                    self._send_num = 13
                self.affirm_send()
        else:
            print('没有需要分享的文章')

    def find_name(self):
        time.sleep(1)
        self._adb.refresh_nodes()
        time.sleep(1)
        print('self._name', self._name)
        if self._adb.find_nodes_by_text(self._name):
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
                self._adb.adb_swipe(540, 800, 540, 540)
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
        self._adb.refresh_nodes()
        time.sleep(2)
        if self.wechats_index < len(self._wechat_list):
            if self._adb.find_nodes_by_text(self._wechat_list[self.wechats_index].strip()):
                print('找到' + self._wechat_list[self.wechats_index].strip())
                self._adb.click(0)
                time.sleep(15)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('　取消　'):
                    self._adb.click(0)
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
                    self.wechats_index += 1
                    self._input_index = 1
                    self.find_wechat()
                else:
                    self.clickbook()
                    self.find_name()

        else:
            print('完成')

    def test(self):
        self._adb.refresh_nodes()
        # self._adb.adb_click(700, 1740)
        # self._adb.adb_click(800, 1920)

    def main(self):
        try:
            # self.test()
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("ADB Keyboard")
            self.find_wechat()
        except KeyboardInterrupt as e:
            print('e', e)
