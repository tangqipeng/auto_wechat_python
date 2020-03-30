#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import time


class Remark:
    def __init__(self, adb, wechat_list, wechat_names, remarks, startwechat, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 微信好友
        self._wechat_name_list = wechat_names
        # 备注
        self._wechat_remarks = remarks
        # 从哪一个微信开始运行
        self.wechats_index = startwechat

        self.wechat_friends_count = len(self._wechat_name_list)

        self.name_index = 0

        self._main = main

    def find_wechat_friend(self):
        if self.name_index < self.wechat_friends_count:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text(self._wechat_name_list[self.name_index].strip()):
                self._adb.click(0)
                time.sleep(1)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('设置备注和标签'):
                    self._adb.click(0)
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_text(self._wechat_name_list[self.name_index].strip()):
                        self._adb.click(0)
                        self._adb.adb_click(1000, 410)
                        self._adb.adb_click(300, 410)
                        # self._adb.adb_input_chinese(self._wechat_remarks[self.name_index])
                        # self._adb.click_by_text_after_refresh('完成')
                        # print('hahh')

                    else:
                        self._adb.adb_click(300, 410)
                        self._adb.adb_click(1000, 410)
                        self._adb.adb_click(300, 410)
                else:
                    self._adb.click_by_content_after_refresh('更多')
                    self._adb.click_by_text_after_refresh('设置备注和标签')
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_text(self._wechat_name_list[self.name_index].strip()):
                        self._adb.click(0)
                        self._adb.adb_click(1000, 410)
                        self._adb.adb_click(300, 410)
                        # self._adb.adb_input_chinese(self._wechat_remarks[self.name_index])
                        # self._adb.click_by_text_after_refresh('完成')
                        # print('hahh')

                    else:
                        self._adb.adb_click(300, 410)
                        self._adb.adb_click(1000, 410)
                        self._adb.adb_click(300, 410)

                self._adb.adb_input_chinese(self._wechat_remarks[self.name_index].strip())
                self._adb.click_by_text_after_refresh('完成')
                self.name_index += 1
                self.find_wechat_friend()
        else:
            print('改完' + self._wechat_list[self.wechats_index].strip())
            self.wechats_index += 1
            self.find_wechat()

    def clean_wechat(self):
        time.sleep(1)
        # 点击进程按钮，显示所有后台进程
        self._adb.adb_keyboard(82)
        time.sleep(1)
        # 点击清理按钮
        self._adb.click_by_text_do_not_refresh0('清理')
        time.sleep(2)

    # 找到需要打开的微信
    def find_wechat(self):
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self.clean_wechat()
        self._adb.refresh_nodes()
        time.sleep(2)
        if self.wechats_index < len(self._wechat_list):
            if self._adb.find_nodes_by_text(self._wechat_list[self.wechats_index].strip()):
                print('找到' + self._wechat_list[self.wechats_index])
                self._adb.click(0)
                time.sleep(20)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('　取消　'):
                    self._adb.click(0)
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh('通讯录')
                    time.sleep(1)
                    self._adb.adb_swipe(540, 240, 540, 900)
                    self._adb.adb_swipe(540, 240, 540, 900)
                    time.sleep(1)
                    self.find_wechat_friend()
                elif self._adb.find_nodes_by_text('找回密码'):
                    self.wechats_index += 1
                    self.find_wechat()
                else:
                    self._adb.click_by_text_after_refresh('通讯录')
                    time.sleep(1)
                    self._adb.adb_swipe(540, 240, 540, 900)
                    self._adb.adb_swipe(540, 240, 540, 900)
                    time.sleep(1)
                    self.find_wechat_friend()


        else:
            print('所有微信更改完成')

    def main(self):
        try:
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("ADB Keyboard")
            self.find_wechat()
        except KeyboardInterrupt as e:
            print('e', e)
