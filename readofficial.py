#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import time


class Readofficial:
    def __init__(self, adb, wechat_list, officialnames, startwechat, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 公众号名称
        self._official_list = officialnames
        # 从哪一个微信开始运行
        self.wechats_index = startwechat

        self.official_count = len(self._official_list)

        self.official_index = 0

        self._main = main

        self._swipe_index = 0

        self._official_swipe_index = 0

        # 输出添加结果到内存 或 文件

    def clean_wechat(self):
        time.sleep(5)
        self._adb.adb_put_back()
        time.sleep(1)
        # 点击进程按钮，显示所有后台进程
        self._adb.adb_keyboard(82)
        time.sleep(1)
        # 点击清理按钮
        self._adb.click_by_text_do_not_refresh0('清理')
        time.sleep(2)

    def jugde_read_end(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_content('更多'):
            self._swipe_index += 1
            if self._adb.find_nodes_by_text('阅读') or self._swipe_index >= 13:
                print('下一个')
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('公众号'):
                    self._adb.click(0)
                self._swipe_index = 0
                self.official_index += 1
                self.find_official()
            else:
                self._swipe_index += 1
                self._adb.adb_swipe(540, 1100, 540, 240)
                time.sleep(3)
                self.jugde_read_end()

    def find_official(self):
        if self.official_index < self.official_count:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text(self._official_list[self.official_index].strip()):
                self._adb.click(0)
                time.sleep(2)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_content('聊天信息'):
                    print('找到了')
                    self._adb.adb_click(1020, 100)
                    time.sleep(2)
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_text('进入公众号'):
                        self._adb.adb_click(500, 1900)
                        time.sleep(2)
                        self.jugde_read_end()
                else:
                    print('没有进入')
            else:
                print('继续找')
                if self._adb.find_nodes_by_text('z'):
                    if self._official_swipe_index < 3:
                        self._official_swipe_index += 1
                        self._adb.adb_swipe(540, 900, 540, 540)
                    else:
                        self._adb.adb_put_back()
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text('公众号'):
                            self._adb.click(0)
                        self._swipe_index = 0
                        self._official_swipe_index = 0
                        self.official_index += 1
                        self.find_official()
                else:
                    self._official_swipe_index += 1
                    if self._official_swipe_index < 10:
                        self._adb.adb_swipe(540, 900, 540, 540)
                        self.find_official()
                    else:
                        self._adb.adb_put_back()
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text('公众号'):
                            self._adb.click(0)
                        self._swipe_index = 0
                        self._official_swipe_index = 0
                        self.official_index += 1
                        self.find_official()
        else:
            print('阅读完毕')
            self.wechats_index += 1
            self.find_wechat()

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

    # 找到需要打开的微信
    def find_wechat(self):
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self.clean_wechat()
        self._adb.refresh_nodes()
        time.sleep(2)
        self.official_index = 0
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
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh('公众号')
                    time.sleep(1)
                    self.find_official()
                elif self._adb.find_nodes_by_text('找回密码'):
                    self.wechats_index += 1
                    self.find_wechat()
                else:
                    self.clickbook()
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh('公众号')
                    time.sleep(1)
                    self.find_official()


        else:
            print('所有微信阅读完')

    def test(self):
        self._adb.adb_click(1020, 100)
        # for a in self._imagenum:
        #     print('a', a)

    def main(self):
        try:
            # self.test()
            self.find_wechat()
        except KeyboardInterrupt as e:
            print('e', e)
