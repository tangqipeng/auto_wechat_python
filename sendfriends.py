#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import time
import glob


class Sendfriends:
    def __init__(self, adb, wechat_list, image_num, strlist, startwechat, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 选择图片的数量
        self._imagenum = image_num
        # 从哪一个微信开始运行
        self.wechats_index = startwechat

        # self.imagelist = sorted(glob.glob(self._image))

        self._strlist = strlist

        print(len(self._strlist))
        print(len(strlist))

        for _str in self._strlist:
            print(_str)

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

    def send_msg(self):
        print('发送')
        self._adb.click_by_text_after_refresh('发表')
        time.sleep(5)
        self._adb.refresh_nodes()
        time.sleep(2)
        if self._adb.find_nodes_by_content('拍照分享'):
            self._main.push('success_circle', self._wechat_list[self.wechats_index].strip() + '  已经发送')
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self.clean_wechat()
            self.wechats_index += 1
            self.find_wechat()
        elif self._adb.find_nodes_by_text('发表'):
            self.send_msg()

        else:
            self._main.push('failed_circle', self._wechat_list[self.wechats_index].strip() + '  发送失败')

    def choice_images(self):
        self._adb.refresh_nodes()
        time.sleep(1)
        print(self._imagenum)
        for num in range(self._imagenum):
            print(num)
            if num < 4:
                self._adb.adb_click(250 * (num + 1), 300)
            elif num >= 4 and num < 8:
                print('4-8')
                self._adb.adb_click(250 * (num - 3), 300 + 250)
            else:
                self._adb.adb_click(250 * (num - 7), 300 + 500)
            time.sleep(1)
        time.sleep(1)
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('完成(' + str(self._imagenum) + '/9)'):
            self._adb.click(0)
        else:
            if self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 1) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 2) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 3) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 4) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 5) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 6) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 7) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('完成(' + str(self._imagenum - 8) + '/9)'):
                self._adb.click(0)

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
            if self._adb.find_nodes_by_text(self._wechat_list[self.wechats_index].strip()):
                print('找到' + self._wechat_list[self.wechats_index].strip())
                self._adb.click(0)
                time.sleep(15)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('　取消　'):
                    self._adb.click(0)
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh('发现')
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh('朋友圈')
                    time.sleep(1)
                    self._adb.refresh_nodes()
                    time.sleep(1)
                    if self._adb.find_nodes_by_content('拍照分享'):
                        print('分享')
                        self._adb.click(0)
                        time.sleep(1)
                        self._adb.refresh_nodes()
                        time.sleep(1)
                        if self._adb.find_nodes_by_text('从相册选择'):
                            self._adb.click(0)
                            time.sleep(3)
                            self.choice_images()
                            time.sleep(3)
                            if len(self._strlist) > 0:
                                self._adb.click_by_text_after_refresh('这一刻的想法...')
                                time.sleep(1)
                                for _str in self._strlist:
                                    string = _str + '\n'
                                    self._adb.adb_input_chinese(string)
                                    time.sleep(1)
                                self.send_msg()
                            else:
                                print(len(self._strlist))

                        else:
                            print('没找到')
                    else:
                        print('未找到分享')
                elif self._adb.find_nodes_by_text('找回密码'):
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self.clean_wechat()
                    self.wechats_index += 1
                    self.find_wechat()
                else:
                    self._adb.click_by_text_after_refresh('发现')
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh('朋友圈')
                    time.sleep(1)
                    self._adb.refresh_nodes()
                    time.sleep(1)
                    if self._adb.find_nodes_by_content('拍照分享'):
                        print('分享')
                        self._adb.click(0)
                        time.sleep(1)
                        self._adb.refresh_nodes()
                        time.sleep(1)
                        if self._adb.find_nodes_by_text('从相册选择'):
                            self._adb.click(0)
                            time.sleep(3)
                            self.choice_images()
                            time.sleep(3)
                            if len(self._strlist) > 0:
                                self._adb.click_by_text_after_refresh('这一刻的想法...')
                                time.sleep(1)
                                for _str in self._strlist:
                                    string = _str + '\n'
                                    self._adb.adb_input_chinese(string)
                                    time.sleep(1)
                                self.send_msg()


                        else:
                            print('没找到')
                    else:
                        print('未找到分享')

            else:
                print('未找到' + self._wechat_list[self.wechats_index].strip())
        else:
            print('已添加完')

    def test(self):
        self.choice_images()

    def main(self):
        try:
            # self.test()
            if self._imagenum >= 1:
                self._adb.adb_keyboard(63)
                self._adb.click_by_text_after_refresh("ADB Keyboard")
                self.find_wechat()
            else:
                print('choicenum设置错误')

        except KeyboardInterrupt as e:
            print('e', e)
