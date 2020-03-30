import time
import random


class Chat:
    def __init__(self, adb, wechat_list, chat_mode, wechat_names, wechat_chats, startwechat, endsign):
        self._adb = adb

        # 微信分身数
        self._wechat_list = wechat_list
        # 聊天模式
        self.chatmode = chat_mode
        # 所有微信名
        self._account = wechat_names
        # 聊天的语言
        self._chats = wechat_chats

        # 微信分身个数
        self._wechat = startwechat
        # 通讯录中z的最后一个微信好友名称
        self._end_sign = endsign

        self._swipe_index = 0

        self.facex = 1080 / 7

        self.facey = 0

        self.face1_x = self.facex / 2

        self.face1_y = 0

    def clickbook(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('通讯录'):
            self._adb.click(0)
            time.sleep(1)
            self._adb.click_by_text_after_refresh('通讯录')
            time.sleep(1)
        elif self._adb.find_nodes_by_text('　取消　'):
            self._adb.click(0)
            time.sleep(3)
            self.clickbook()
        else:
            time.sleep(3)
            self.clickbook()

    def choice_face(self):
        facenum = random.randint(0, 19)
        print(facenum)
        if facenum < 7:
            x = self.face1_x + self.facex * facenum
            y = self.face1_y
        elif facenum >= 7 and facenum < 14:
            x = self.face1_x + self.facex * (facenum - 7)
            y = self.face1_y + self.facey
        else:
            x = self.face1_x + self.facex * (facenum - 14)
            y = self.face1_y + self.facey * 2
        self._adb.adb_click(x, y)
        time.sleep(2)

    def find_friend(self, name):
        time.sleep(2)
        self._adb.refresh_nodes()
        time.sleep(2)
        if self._adb.find_nodes_by_text(name):
            self._adb.click_by_text_after_refresh(name)
            time.sleep(2)
            self._adb.click_by_text_after_refresh('发消息')
            time.sleep(3)
            if self._wechat < len(self._wechat_list):
                if self.chatmode == 0:
                    print('发送文字')
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_content('切换到按住说话'):
                        self._adb.adb_click(500, 1900)
                        time.sleep(1)
                        a = random.randint(0, len(self._chats) - 1)
                        text = self._chats[a].strip()
                        self._adb.adb_input_chinese(text)
                        time.sleep(2)
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text(text):
                            time.sleep(2)
                            self._adb.refresh_nodes()
                            if self._adb.find_nodes_by_text('发送'):
                                self._adb.click(0)
                                # self._adb.click_by_text_after_refresh('发送')
                                time.sleep(2)
                                self._adb.adb_put_back()
                                self._adb.refresh_nodes()
                                if self._adb.find_nodes_by_text('通讯录'):
                                    print('next')
                                else:
                                    self._adb.adb_put_back()
                            else:
                                self._adb.refresh_nodes()
                                if self._adb.find_nodes_by_content('聊天信息'):
                                    self._adb.adb_click(1020, 1900)
                                    time.sleep(2)
                                    self._adb.adb_put_back()
                                    self._adb.refresh_nodes()
                                    if self._adb.find_nodes_by_text('通讯录'):
                                        print('next')
                                    else:
                                        self._adb.adb_put_back()
                        else:
                            print('输入失败')
                    elif self._adb.find_nodes_by_content('切换到键盘'):
                        self._adb.click(0)
                        self._adb.adb_click(500, 1900)
                        time.sleep(1)
                        a = random.randint(0, len(self._chats) - 1)
                        text = self._chats[a].strip()
                        self._adb.adb_input_chinese(text)
                        time.sleep(2)
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text(text):
                            time.sleep(2)
                            self._adb.refresh_nodes()
                            if self._adb.find_nodes_by_text('发送'):
                                self._adb.click(0)
                                # self._adb.click_by_text_after_refresh('发送')
                                time.sleep(2)
                                self._adb.adb_put_back()
                                self._adb.refresh_nodes()
                                if self._adb.find_nodes_by_text('通讯录'):
                                    print('next')
                                else:
                                    self._adb.adb_put_back()
                            else:
                                self._adb.refresh_nodes()
                                if self._adb.find_nodes_by_content('聊天信息'):
                                    self._adb.adb_click(1020, 1900)
                                    time.sleep(2)
                                    self._adb.adb_put_back()
                                    self._adb.refresh_nodes()
                                    if self._adb.find_nodes_by_text('通讯录'):
                                        print('next')
                                    else:
                                        self._adb.adb_put_back()
                        else:
                            print('输入失败')
                    # if self._wechat_list[self._wechat] == '微信':
                    #     self._adb.click_by_text_do_not_refresh3('输入信息')
                    #     time.sleep(1)
                    #     a = random.randint(0, len(self._chats)-1)
                    #     text = self._chats[a]
                    #     self._adb.adb_input_chinese(text)
                    #     self._adb.click_by_text_after_refresh('发送')
                    #     time.sleep(2)
                    #     # self._adb.refresh_nodes()
                    #     self._adb.adb_put_back()
                    # else:
                    #     self._adb.click_by_text_do_not_refresh2('输入信息')
                    #     time.sleep(1)
                    #     a = random.randint(0, len(self._chats)-1)
                    #     text = self._chats[a]
                    #     self._adb.adb_input_chinese(text)
                    #     self._adb.click_by_text_do_not_refresh2('发送')
                    #     time.sleep(2)
                    #     # self._adb.refresh_nodes()
                    #     self._adb.adb_put_back()
                elif self.chatmode == 1:
                    print('发送语音')
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_content('切换到按住说话'):
                        self._adb.click(0)
                        self._adb.adb_swipe1(500, 1900, 500, 1901, 5 * 1000)
                        # time.sleep(3)

                    elif self._adb.find_nodes_by_content('切换到键盘'):
                        self._adb.adb_swipe1(500, 1900, 500, 1901, 5 * 1000)

                    time.sleep(1)
                    self._adb.adb_put_back()
                else:
                    print('发送表情')
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_content('表情'):
                        self._adb.click(0)
                        time.sleep(1)
                        self.calculate_face()
                    time.sleep(1)
                    self._adb.adb_put_back()
            else:
                print('微信已加完')
        else:
            if self._adb.find_nodes_by_text(self._end_sign):
                print('not find')
                self._swipe_index = 0
            else:
                self._swipe_index += 1
                self._adb.adb_swipe(540, 980, 540, 540)
                a = name
                self.find_friend(a)

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

    def accountxuhuan(self):
        for line in range(len(self._account)):
            self.clickbook()
            self._swipe_index = 0
            self.find_friend(str(self._account[line].strip()))
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self.clean_wechat()
        self._wechat += 1
        self.enterotherwechat()

    def enterotherwechat(self):
        if len(self._wechat_list) > self._wechat:
            # 切换微信
            self._adb.refresh_nodes()
            time.sleep(2)
            if self._adb.find_nodes_by_text(self._wechat_list[self._wechat].strip()):
                self._adb.click(0)
                time.sleep(20)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('　取消　'):
                    self._adb.click(0)
                    time.sleep(1)
                    self._swipe_index = 0
                    self.accountxuhuan()
                elif self._adb.find_nodes_by_text('找回密码'):
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self.clean_wechat()
                    self._wechat += 1
                    self.enterotherwechat()
                else:
                    self._swipe_index = 0
                    self.accountxuhuan()

            else:
                print('页面错误')
        else:
            print('微信切换完毕')

    def calculate_face(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_content('[微笑]'):
            print('找到1')
            face1_list = self._adb.get_bounds()
            self.face1_y = int(face1_list[3]) - (int(face1_list[3]) - int(face1_list[1])) / 2
            print(self.face1_y)
            if self._adb.find_nodes_by_content('[闭嘴]'):
                print('找到2')
                face2_list = self._adb.get_bounds()
                self.facey = int(face2_list[3]) - int(face1_list[3])
                self.choice_face()
                time.sleep(1)
                self._adb.click_by_text_after_refresh('发送')
                self._adb.adb_put_back()

    def test(self):
        self._adb.refresh_nodes()

    def main(self):
        self._adb.adb_keyboard(63)
        self._adb.click_by_text_after_refresh("ADB Keyboard")
        self.enterotherwechat()

        # self.test()

        # for num in range(30):
        #     print(random.randint(1, 20))
