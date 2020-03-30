#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import time
import file
from adb import By


class Addofficial:
    def __init__(self, adb, wechat_list, startwechat, official_list, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 从哪一个微信开始运行
        self.wechats_index = startwechat

        self.official_list = official_list

        self.official_index = 0

        self._main = main

    def change_setting(self):
        self._adb.adb_keyboard(3)
        time.sleep(2)
        self._adb.refresh_nodes()
        time.sleep(2)
        if self._adb.find_nodes_by_text("设置"):
            self._adb.click(0)
            time.sleep(1)
            self._adb.adb_swipe(540, 1300, 540, 540)
            time.sleep(1)
            self._adb.refresh_nodes()
            time.sleep(1)
            if self._adb.find_nodes_by_text("更多设置"):
                self._adb.click(0)
                time.sleep(1)
                self._adb.refresh_nodes()
                time.sleep(1)
                if self._adb.find_nodes_by_text("语言和输入法"):
                    self._adb.click(0)
                    time.sleep(1)
                    self._adb.refresh_nodes()
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh("当前输入法")
                    time.sleep(2)
                    self._adb.refresh_nodes()
                    time.sleep(1)
                    if self._adb.find_nodes_by_text("搜狗输入法小米版"):
                        self._adb.click(-1)

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

    def clean_search(self):
        self._adb.refresh_nodes()
        time.sleep(1)
        if self._adb.find_nodes_by_content("当前所在页面,搜一搜"):
            if self._adb.find_nodes('true', By.naf):
                self._adb.click(-1)
                time.sleep(2)
                self.official_index += 1
                self.find_official(self.official_index)

        else:
            time.sleep(1)
            self._adb.adb_put_back()
            time.sleep(2)
            self._adb.refresh_nodes()
            time.sleep(2)
            if self._adb.find_nodes_by_text("进入公众号"):
                time.sleep(1)
                self._adb.adb_put_back()
                time.sleep(1)
                self.clean_search()

    # 找到需要添加的公众号
    def find_official(self, index):
        if index < len(self.official_list):
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("ADB Keyboard")
            time.sleep(2)
            self._adb.refresh_nodes()
            time.sleep(1)
            if self._adb.find_nodes_by_text("搜索公众号"):
                # self._adb.click_by_text_after_refresh("搜索公众号")
                self._adb.click(0)
                time.sleep(2)
                official = self.official_list[index].strip()
                self._adb.adb_input_chinese(official)
                time.sleep(5)
                self._adb.refresh_nodes()
                time.sleep(1)
                if self._adb.find_nodes_by_text("关注的公众号"):
                    if self._adb.find_nodes_by_text(official):
                        print('找结果')
                        self._adb.click(0)
                        time.sleep(2)
                        self._adb.refresh_nodes()
                        time.sleep(2)
                        if self._adb.find_nodes_by_content('聊天信息'):
                            print('聊天页1')
                            time.sleep(2)
                            self._adb.adb_put_back()
                            self._main.push('success_add_official',
                                            official + ' ' + self._wechat_list[self.wechats_index].strip() + '  已经关注')
                            time.sleep(2)
                            self.clean_search()
                        else:
                            print('另一种情况1')
                    else:
                        print('没有找到')
                else:
                    print('另一种情况')
                    self._adb.adb_keyboard(63)
                    self._adb.click_by_text_after_refresh("搜狗输入法小米版")
                    time.sleep(2)
                    self._adb.refresh_nodes()
                    time.sleep(1)
                    if self._adb.find_nodes_by_text(official):
                        print(official)
                        self._adb.click(0)
                        time.sleep(2)
                        self._adb.adb_click(980, 1900)
                        time.sleep(5)
                        self._adb.refresh_nodes()
                        time.sleep(1)
                        if self._adb.find_nodes_by_text("公众号"):
                            if self._adb.find_nodes_by_text(official):
                                self._adb.click(0)
                                time.sleep(1)
                                self._adb.refresh_nodes()
                                time.sleep(1)
                                if self._adb.find_nodes_by_text("关注公众号"):
                                    self._adb.click(0)
                                    print('搜到了1')
                                    time.sleep(3)
                                    self._adb.refresh_nodes()
                                    time.sleep(2)
                                    if self._adb.find_nodes_by_content('聊天信息'):
                                        print('聊天页2')
                                        time.sleep(2)
                                        self._adb.adb_put_back()
                                        self._main.push('success_add_official', official + ' ' + self._wechat_list[
                                            self.wechats_index].strip() + '  已经关注')
                                        time.sleep(2)
                                        self._adb.refresh_nodes()
                                        time.sleep(2)
                                        if self._adb.find_nodes_by_text("进入公众号"):
                                            time.sleep(1)
                                            self._adb.adb_put_back()
                                            time.sleep(1)
                                            self.clean_search()
                                        else:
                                            time.sleep(1)
                                            self._adb.adb_put_back()
                                            time.sleep(2)
                                            self._adb.refresh_nodes()
                                            time.sleep(2)
                                            if self._adb.find_nodes_by_text("关注公众号"):
                                                self._adb.click(0)
                                                print('搜到了1')
                                                time.sleep(3)
                                                self._adb.refresh_nodes()
                                                time.sleep(2)
                                                if self._adb.find_nodes_by_content('聊天信息'):
                                                    print('聊天页2')
                                                    time.sleep(2)
                                                    self._adb.adb_put_back()
                                                    self._main.push('success_add_official',
                                                                    official + ' ' + self._wechat_list[
                                                                        self.wechats_index].strip() + '  已经关注')
                                                    time.sleep(2)
                                                    self._adb.refresh_nodes()
                                                    time.sleep(2)
                                                    if self._adb.find_nodes_by_text("进入公众号"):
                                                        time.sleep(1)
                                                        self._adb.adb_put_back()
                                                        time.sleep(1)
                                                        self.clean_search()
                                                    else:
                                                        time.sleep(1)
                                                        self._adb.adb_put_back()
                                                        time.sleep(2)
                                                        self._adb.refresh_nodes()
                                                        time.sleep(2)
                                                        if self._adb.find_nodes_by_text("关注公众号"):
                                                            self._adb.click(0)
                                                        elif self._adb.find_nodes_by_text("进入公众号"):
                                                            time.sleep(1)
                                                            self._adb.adb_put_back()
                                                            time.sleep(1)
                                                            self.clean_search()
                                                        else:
                                                            self.clean_search()
                                            elif self._adb.find_nodes_by_text("进入公众号"):
                                                time.sleep(1)
                                                self._adb.adb_put_back()
                                                time.sleep(1)
                                                self.clean_search()
                                            else:
                                                self.clean_search()

                                elif self._adb.find_nodes_by_text("进入公众号"):
                                    print('搜到了2')
                                    self._main.push('success_add_official', official + ' ' + self._wechat_list[
                                        self.wechats_index].strip() + '  已经关注')
                                    time.sleep(1)
                                    self._adb.adb_put_back()
                                    time.sleep(2)
                                    self.clean_search()

                                else:
                                    print('没有搜到1')
                                    self._main.push('failed_official', official + ' ' + self._wechat_list[
                                        self.wechats_index].strip() + '   没有搜索到')
                                    time.sleep(2)
                                    self.clean_search()

                        else:
                            self._adb.adb_click(400, 500)
                            time.sleep(2)
                            self._adb.refresh_nodes()
                            if self._adb.find_nodes_by_text("关注公众号"):
                                self._adb.click(0)
                                print('搜到了3')
                                time.sleep(3)
                                self._adb.refresh_nodes()
                                time.sleep(2)
                                if self._adb.find_nodes_by_content('聊天信息'):
                                    print('聊天页2')
                                    self._main.push('success_add_official', official + ' ' + self._wechat_list[
                                        self.wechats_index].strip() + '  已经关注')
                                    time.sleep(2)
                                    self._adb.adb_put_back()
                                    time.sleep(2)
                                    self._adb.refresh_nodes()
                                    time.sleep(2)
                                    if self._adb.find_nodes_by_text("进入公众号"):
                                        time.sleep(1)
                                        self._adb.adb_put_back()
                                        time.sleep(1)
                                        self.clean_search()
                                    else:
                                        time.sleep(1)
                                        self._adb.adb_put_back()
                                        time.sleep(2)
                                        self._adb.refresh_nodes()
                                        time.sleep(2)
                                        if self._adb.find_nodes_by_text("进入公众号"):
                                            time.sleep(1)
                                            self._adb.adb_put_back()
                                            time.sleep(1)
                                            self.clean_search()
                                        else:
                                            self.clean_search()

                            elif self._adb.find_nodes_by_text("进入公众号"):
                                print('搜到了4')
                                self._main.push('success_add_official', official + ' ' + self._wechat_list[
                                    self.wechats_index].strip() + '  已经关注')
                                time.sleep(1)
                                self._adb.adb_put_back()
                                time.sleep(2)
                                self.clean_search()

                            else:
                                print('没有搜到2')
                                self._main.push('failed_official',
                                                official + ' ' + self._wechat_list[
                                                    self.wechats_index].strip() + '   没有搜索到')
                                time.sleep(2)
                                self.clean_search()
                    else:
                        print('没有搜索到')
                        self._main.push('failed_official',
                                        official + ' ' + self._wechat_list[self.wechats_index].strip() + '   没有搜索到')
                        time.sleep(2)
                        self.clean_search()
            else:
                print('页面错误')
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self.clean_wechat()
                print('下一个微信')
                time.sleep(2)
                self.find_wechat()

        else:
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self.clean_wechat()
            print('下一个微信')
            self.official_index = 0
            time.sleep(2)
            self.wechats_index += 1
            self.find_wechat()

    def test(self):
        # self._adb.adb_put_back()
        self._adb.refresh_nodes()
        # self._adb.click_by_text_after_refresh("贝因美")
        self._adb.adb_click(400, 500)
        time.sleep(2)
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text("进入公众号"):
            time.sleep(1)
            self._adb.adb_put_back()
            time.sleep(1)
            self.clean_search()
        else:
            time.sleep(1)
            self._adb.adb_put_back()
            time.sleep(2)
            self._adb.refresh_nodes()
            time.sleep(2)
            if self._adb.find_nodes_by_text("进入公众号"):
                time.sleep(1)
                self._adb.adb_put_back()
                time.sleep(1)
                self.clean_search()
            else:
                self.clean_search()
        # self._adb.adb_swipe(540, 1300, 540, 540)
        # self._adb.click_by_text_after_refresh("搜索公众号")
        # time.sleep(2)
        # self._adb.adb_input_chinese('去哪')
        # time.sleep(2)
        # self._adb.refresh_nodes()
        # if self._adb.find_nodes_by_text("肯德基"):
        #     self._adb.click(0)
        # self._adb.adb_put_back()
        # time.sleep(2)
        # self._adb.refresh_nodes()
        # if self._adb.find_nodes('true', By.naf):
        #     self._adb.click(3)

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
            if self._adb.find_nodes_by_content(self._wechat_list[self.wechats_index].strip()):
                print('找到' + self._wechat_list[self.wechats_index].strip())
                self._adb.click_by_content_after_refresh(self._wechat_list[self.wechats_index].strip())
                time.sleep(20)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('　取消　'):
                    self._adb.click(0)
                    self._adb.click_by_text_do_not_refresh('外部联系人')
                    time.sleep(1)
                    self._adb.click_by_text_do_not_refresh('添加朋友')
                    time.sleep(1)
                    self._adb.click_by_text_do_not_refresh('公众号')
                    time.sleep(3)
                    if self.official_index < len(self.official_list):
                        self.find_official(self.official_index)
                elif self._adb.find_nodes_by_text('找回密码'):
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self.clean_wechat()
                    self.wechats_index += 1
                    self.find_wechat()
                else:
                    self._adb.click_by_text_do_not_refresh('外部联系人')
                    time.sleep(1)
                    self._adb.click_by_text_do_not_refresh('添加朋友')
                    time.sleep(1)
                    self._adb.click_by_text_do_not_refresh('公众号')
                    time.sleep(3)
                    if self.official_index < len(self.official_list):
                        self.find_official(self.official_index)

    def main(self):
        # self.test()
        try:

            self.find_wechat()

        except KeyboardInterrupt as e:
            print('e', e)
