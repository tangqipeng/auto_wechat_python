#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import time


class Commentcircle:
    def __init__(self, adb, wechat_list, comment_mode, comment_wechat_friend, comment_strs, startwechat, end_sign,
                 main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 评论模式
        self._comment_mode = comment_mode
        # 需要评论的微信好友
        self._comment_wechat_friend = comment_wechat_friend
        # 评论的语言
        self._comment_list = comment_strs
        # 从哪一个微信开始运行
        self.wechats_index = startwechat
        # 通讯录页结束标记
        self._end_sign = end_sign

        # 要评论的个数
        self.comment_count = len(self._comment_list)

        self.comment_index = 0

        self.node_count = 0

        self.click_index = 0

        self._main = main

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

    def jugde_comment(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('赞'):
            self._adb.click(0)
            time.sleep(2)
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_content('评论'):
                self._adb.click(self.pinglunnum)
                time.sleep(2)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('评论'):
                    self._adb.click(0)
                    self._adb.adb_input_chinese(self._comment_list[self.comment_index].strip())
                    self._adb.click_by_text_after_refresh('发送')
                    time.sleep(2)
                    self.comment_index += 1
                    self.comment()
        elif self._adb.find_nodes_by_text('取消'):
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_content('评论'):
                self._adb.click(self.pinglunnum)
                # self.comment_index += 1
                if self.comment_count > 1:
                    time.sleep(1)
                    try:
                        self.pinglunnum += 1
                        self._adb.click(self.pinglunnum)
                        time.sleep(2)
                        self.jugde_comment()
                    except IndexError as e:
                        print(e)
                        self.pinglunnum = 0
                        self._adb.adb_swipe(540, 900, 540, 540)
                        self.comment()
                else:
                    print('已评论过')
                    self.comment_index = 0
                    self.wechats_index += 1
                    self.find_wechat()

    def jugde_comment1(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('赞'):
            self._adb.click(0)
            time.sleep(2)
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_content('评论'):
                self._adb.click(self.click_index)
                time.sleep(2)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('评论'):
                    self._adb.click(0)
                    self._adb.adb_input_chinese(self._comment_list[self.comment_index].strip())
                    self._adb.click_by_text_after_refresh('发送')
                    time.sleep(2)
                    self.node_count = 0
                    self.click_index += 1
                    self.comment_index += 1
                    self.comment()
        elif self._adb.find_nodes_by_text('取消') and self.comment_index == 0:
            print('评论完毕' + self._wechat_list[self.wechats_index].strip())
            self.click_index = 0
            self.node_count = 0
            self.comment_index = 0
            self.wechats_index += 1
            self.find_wechat()

    def comment(self):
        print('self.comment_index', self.comment_index)
        print('self.comment_count', self.comment_count)
        if self.comment_index < self.comment_count:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_content('评论'):
                # self.node_count = self.node_count + self._adb.search_count()
                self.node_count = self._adb.search_count()
                print('self.click_index', self.click_index)
                if self.click_index < self.node_count:
                    bounds = self._adb.get_bounds(self.click_index)
                    if int(bounds[1]) > 200:
                        if int(bounds[3]) < 2040:
                            self._adb.click(self.click_index)
                            time.sleep(2)
                            self.jugde_comment1()
                        else:
                            print(self.click_index + '的坐标底部大于2040')
                            self._adb.adb_swipe1(540, 2000, 540, 200, 1000)
                            time.sleep(2)
                            self.click_index = 0
                            self.comment()
                    else:
                        print(self.click_index + '的坐标顶部小于200')
                        self._adb.adb_swipe1(540, 2000, 540, 1800, 500)
                        self.click_index = 0
                        time.sleep(2)
                        self.comment()
                else:
                    print(str(self.click_index) + '大于当前页面的总个数' + str(self.node_count))
                    self.click_index = 0
                    self._adb.adb_swipe1(540, 2000, 540, 200, 1000)
                    self.comment()

            else:
                self.click_index = 0
                self._adb.adb_swipe1(540, 2000, 540, 240, 1000)
                self.comment()
        else:
            print('评论完毕' + self._wechat_list[self.wechats_index].strip())
            self.click_index = 0
            self.node_count = 0
            self.comment_index = 0
            self.wechats_index += 1
            self.find_wechat()

    def find_friend(self):
        # self._adb.click_by_text_after_refresh(self._comment_wechat_friend[self.wechats_index])
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text(self._comment_wechat_friend[self.wechats_index].strip()):
            self._adb.click(0)
            time.sleep(2)
            self._adb.click_by_text_after_refresh('朋友圈')
            # todo 接下来评论

        else:
            if self._adb.find_nodes_by_text(self._end_sign):
                print('not find')
                self.comment_index = 0
                self.wechats_index += 1
                self.find_wechat()
            else:
                self._adb.adb_swipe(540, 900, 540, 540)
                self.find_friend()

    # 找到需要打开的微信
    def find_wechat(self):
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self.clean_wechat()
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
                    time.sleep(1)
                    if self._comment_mode == 0:
                        self._adb.click_by_text_after_refresh('发现')
                        time.sleep(1)
                        self._adb.click_by_text_after_refresh('朋友圈')
                        time.sleep(1)
                        self._adb.adb_swipe(540, 220, 540, 2000)
                        self._adb.adb_swipe(540, 220, 540, 2000)
                        time.sleep(1)
                        self._adb.adb_swipe(540, 850, 540, 540)
                        time.sleep(1)
                        self.comment()
                    else:
                        print('模式1')
                        self._adb.click_by_text_after_refresh('通讯录')
                        time.sleep(2)
                        self.find_friend()
                elif self._adb.find_nodes_by_text('找回密码'):
                    self.click_index = 0
                    self.node_count = 0
                    self.comment_index = 0
                    self.wechats_index += 1
                    self.find_wechat()
                else:
                    if self._comment_mode == 0:
                        self._adb.click_by_text_after_refresh('发现')
                        time.sleep(1)
                        self._adb.click_by_text_after_refresh('朋友圈')
                        time.sleep(1)
                        self._adb.adb_swipe(540, 220, 540, 2000)
                        self._adb.adb_swipe(540, 220, 540, 2000)
                        time.sleep(1)
                        self._adb.adb_swipe(540, 850, 540, 540)
                        time.sleep(1)
                        self.comment()
                    else:
                        print('模式1')
                        self._adb.click_by_text_after_refresh('通讯录')
                        time.sleep(2)
                        self.find_friend()


        else:
            print('所有微信评论完')

    def test(self):
        # self._adb.adb_swipe1(540, 2000, 540, 240, 1000)
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_content('评论'):
            bounds0 = self._adb.get_bounds(0)
            bounds1 = self._adb.get_bounds(1)
            self._adb.click(0)
            print(bounds0)
            print(bounds1)

    def main(self):
        try:
            # self.test()
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("ADB Keyboard")
            self.find_wechat()
        except KeyboardInterrupt as e:
            print('e', e)
