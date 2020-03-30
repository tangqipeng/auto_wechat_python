import time
import file
from adb import By


class Groupchat:
    def __init__(self, adb, wechat_list, group_names, wechat_index, groups_txt_list, image_num, main):
        self._adb = adb

        # 微信名称
        self._wechat_list = wechat_list
        # 群名
        self._group_list = group_names
        # 从哪一个微信开始运行
        self.wechats_index = wechat_index

        self._groups_txt_list = groups_txt_list

        self._image_count = image_num

        self._group_index = 0

        self._main = main

    def choice_images(self):
        self._adb.refresh_nodes()
        time.sleep(1)
        print(self._image_count)
        for num in range(self._image_count):
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
        if self._adb.find_nodes_by_text('发送(' + str(self._image_count) + '/9)'):
            self._adb.click(0)
        else:
            if self._adb.find_nodes_by_text('发送(' + str(self._image_count - 1) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('发送(' + str(self._image_count - 2) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('发送(' + str(self._image_count - 3) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('发送(' + str(self._image_count - 4) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('发送(' + str(self._image_count - 5) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('发送(' + str(self._image_count - 6) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('发送(' + str(self._image_count - 7) + '/9)'):
                self._adb.click(0)
            elif self._adb.find_nodes_by_text('发送(' + str(self._image_count - 8) + '/9)'):
                self._adb.click(0)

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

    def send_image(self):
        print('发送图片')
        if self._image_count > 0:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_content('更多功能按钮，已展开'):
                self._adb.click(0)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('相册'):
                    self._adb.click(0)
                    self.choice_images()
        else:
            self._group_index += 1
            self.search_group()

    def input_txt(self):
        print('输入文字')
        time.sleep(1)
        for _str in self._groups_txt_list:
            print(_str)
            self._adb.adb_input_chinese(_str)
            self._adb.adb_keyboard(66)
            time.sleep(1)

    def search_group(self):
        print('找群')
        if self.wechats_index < len(self._group_list) or self._group_index < len(self._group_list[self.wechats_index]):
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text(self._group_list[self.wechats_index][self._group_index]):
                print('找到' + self._group_list[self.wechats_index][self._group_index])
                self._adb.click(0)
                time.sleep(1)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_content('切换到按住说话'):
                    self._adb.adb_click(500, 1900)
                elif self._adb.find_nodes_by_content('切换到键盘'):
                    self._adb.click(0)
                self.input_txt()
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('发送'):
                    self._adb.click(0)
                    self.send_image()
        else:
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self.clean_wechat()
            self.wechats_index += 1
            self.find_wechat()

    def search_book(self):
        self._adb.click_by_text_after_refresh('通讯录')
        self._adb.click_by_text_after_refresh('群聊')
        time.sleep(2)
        self.search_group()

    # 找到需要打开的微信
    def find_wechat(self):
        self._group_index = 0
        self._adb.refresh_nodes()
        time.sleep(2)
        if self.wechats_index < len(self._wechat_list):
            if self._adb.find_nodes_by_text(self._wechat_list[self.wechats_index]):
                print('找到' + self._wechat_list[self.wechats_index])
                self._adb.click(0)
                time.sleep(15)
                self.search_book()

    def test(self):
        self._adb.refresh_nodes()

    def main(self):
        # self.test()
        try:
            self.find_wechat()
        except KeyboardInterrupt as e:
            print('e', e)
