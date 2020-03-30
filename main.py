#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import time
from adb import Adb
import file
from chat import Chat
from addfriends import Addfriends
from addfriend import Addfriend
from addofficial import Addofficial
from sendfriends import Sendfriends
from addgroup import Addgroup
from sharearticle import Sharearticle
from commentcircle import Commentcircle
from readofficial import Readofficial
from remark import Remark
from groupchat import Groupchat
from readbook import Readbook
from sreachw import SreachFriend


class Main:
    def __init__(self, port=None, device=None):
        self._adb = Adb(port, device)

        self._success = []
        self._failed = []

        self._dict = {'success': self._success, 'failed': self._failed, 'success_add_official': self._success,
                      'failed_add_official': self._failed, 'success_circle': self._success,
                      'failed_circle': self._failed, 'success_share': self._success, 'failed_share': self._failed,
                      'male': self._failed, 'female': self._success}

        self.file = file.File()
        self._json = self.file.json()

        # mode 模式
        self._mode = 0
        # 微信名称
        self._wechat_list = self._json['wechataccounts']

        # 要添加好友的手机号码或者微信号文件路径 手机号码一行一个
        self._file_add_friends = self._json['file_add_friends']
        # 提示语
        self._reminder = self._json['reminder']
        # 需要输入的提示语
        self._input_hint = self._json['inputhint']
        # 加标签
        self._tag = self._json['tag']
        # 一个微信连续加几个好友
        self._continue_add = self._json['continue_add']
        # 每个账号加好友的总个数
        self._addfriendcount = self._json['friends']
        # 每加完一轮的休息时间
        self._add_f_sleep = self._json['add_f_sleep']

        # 添加公众号的文件路径
        self._file_add_official = self._json['file_add_official']

        # 聊天
        # 聊天模式
        self._chat_mode = self._json['chatmode']
        # 聊天的微信好友
        self._account = self._json['account']
        # 聊天的语言
        self._chats = self._json['chats']
        # 通讯录中的z的结尾微信名
        self._end_sign = self._json['endsign']

        # 获取需要发送朋友圈的文字
        self._file_send_cicle = self._json['file_send_circle']
        # 选择图片的数量
        self._imagenum = self._json['choicenum']
        # 分享文字的对象
        self._strlist = []

        # 分享文章的文章地址
        self._file_share_article = self._json['file_share_article']
        # 发送消息的名字
        self.common_name = self._json['commonname']
        # 需要分享的话
        self._share_str = self._json['sharetxt']

        # 评论朋友圈
        # 评论模式
        self._comment_mode = self._json['commentmode']
        # 需要针对评论的朋友
        self._comment_wechat_friend = self._json['comment_wechat_friend']
        # 评论文字
        self._comment_list = self._json['commentstrs']

        # 阅读公众号
        # 公众号文章
        self._officialnames = self._json['officialnames']

        # 打备注
        self._wechat_remark_friends_list = self._json['wechat_remark_friends']
        # 备注文字
        self._wechat_remarks = self._json['remark']

        # 群聊
        self.groups_list = self._json['group_names']
        self.file_groups_txt = self._json['file_group_txt']
        self.file_groups_image = self._json['group_image_count']
        self._groups_txt_list = []

        # 所有脚本的运行顺序
        self._run_order = self._json['run_order']

        # 睡觉
        self._fun_sleep = self._json['fun_sleep']

        # 微信分身个数 如果要从微信本身开始运行则设为-1，从微信分身开始运行设为0，从微信分身1开始设为1，以此类推， 需要去config文件中修改startwechat的值，根据你设置的值打开相应的微信分身
        self.wechats_index = self._json['startwechat']

        self.phonelist = []

        self.official_list = []

        self._articlelist = []

        # self._run_index = 0

    # 输出添加结果到内存 或 文件
    def push(self, key, value):
        _list = self._dict[key]
        _list.append(value)

        # list到一定长度 输出到文件
        if 1 == len(_list):
            self.file.dump1(_list, key)

    def next_run(self):
        if self._adb.adb_unlock_screen() == False:
            self._adb.adb_keyboard(26)
            time.sleep(1)
            self._adb.adb_swipe(500, 1700, 500, 300)
            time.sleep(1)
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self.clean_wechat()
        self._adb.adb_back_to_desktop()
        if len(self._run_order) > 0 and len(self._fun_sleep) > 0 and len(self._fun_sleep) + 1 >= len(self._run_order):
            for num in range(len(self._run_order)):
                self._mode = self._run_order[num]
                if num > 0:
                    self.wechats_index = 0
                self.run()
                time1 = self._fun_sleep[num] * 60
                time.sleep(time1)
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self.clean_wechat()
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("搜狗输入法小米版")
            self._adb.adb_back_to_desktop()
            self._adb.adb_keyboard(26)

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

    def run(self):

        try:
            if self._mode == 0:
                print('添加好友')

                for f in self.file.open1(self._file_add_friends):
                    print(f)
                    line = f
                    line = file.delete_line_breaks(line)
                    line = line.strip()
                    self.phonelist.append(line)

                friend = Addfriend(self._adb, self._wechat_list, self._reminder, self._input_hint, self._continue_add,
                                   self._addfriendcount,
                                   self.wechats_index, self.phonelist, self._tag, self._add_f_sleep, self)
                friend.main()

                # 输出最后的添加结果
                self.file.dump1(self._success, 'success')
                self.file.dump1(self._failed, 'failed')
            elif self._mode == 1:
                print('添加公众号')
                for f in self.file.open_w(self._file_add_official):
                    print(f)
                    line = f
                    line = file.delete_line_breaks(line)
                    line = line.strip()
                    self.official_list.append(line)

                off = Addofficial(self._adb, self._wechat_list, self.wechats_index, self.official_list, self)
                off.main()

                # 输出最后的添加结果
                self.file.dump1(self._success, 'success_add_official')
                self.file.dump1(self._failed, 'failed_official')
            elif self._mode == 2:
                print('聊天')

                chat_chat = Chat(self._adb, self._wechat_list, self._chat_mode, self._account, self._chats,
                                 self.wechats_index, self._end_sign)
                chat_chat.main()
            elif self._mode == 3:
                print('发送朋友圈')

                for f in self.file.open_w(self._file_send_cicle):
                    print(f)
                    line = f
                    line = file.delete_line_breaks(line)
                    self._strlist.append(line)

                time.sleep(2)

                send = Sendfriends(self._adb, self._wechat_list, self._imagenum, self._strlist, self.wechats_index,
                                   self)
                send.main()

                # 输出最后的添加结果
                self.file.dump1(self._success, 'success_circle')
                self.file.dump1(self._failed, 'failed_circle')

            elif self._mode == 4:
                print('分享文章')

                for f in self.file.open_w(self._file_share_article):
                    line = f
                    line = file.delete_line_breaks(line)
                    line = line.strip()
                    print(line)
                    self._articlelist.append(line)

                share = Sharearticle(self._adb, self._wechat_list, self.common_name, self._share_str, self._articlelist,
                                     self.wechats_index, self)
                share.main()

                # 输出最后的添加结果
                self.file.dump1(self._success, 'success_share')
                self.file.dump1(self._failed, 'failed_share')

            elif self._mode == 5:
                print('评论朋友圈')
                comment = Commentcircle(self._adb, self._wechat_list, self._comment_mode, self._comment_wechat_friend,
                                        self._comment_list, self.wechats_index, self._end_sign, self)
                comment.main()
            elif self._mode == 6:
                print('阅读公众号文章')
                read = Readofficial(self._adb, self._wechat_list, self._officialnames, self.wechats_index, self)
                read.main()
            elif self._mode == 7:
                print('给好友打备注')
                mark = Remark(self._adb, self._wechat_list, self._wechat_remark_friends_list, self._wechat_remarks,
                              self.wechats_index, self)
                mark.main()
            elif self._mode == 8:
                print('加群')
                group = Addgroup(self._adb, self._wechat_list, self.groups_list, self.wechats_index, self._end_sign,
                                 self)
                group.main()

                # 输出最后的添加结果
                self.file.dump1(self._success, 'success_group')
                self.file.dump1(self._failed, 'failed_group')
            elif self._mode == 9:
                self._adb.adb_keyboard(63)
                self._adb.click_by_text_after_refresh("ADB Keyboard")

                for f in self.file.open_w(self.file_groups_txt):
                    line = f
                    line = file.delete_line_breaks(line)
                    line = line.strip()
                    print(line)
                    self._groups_txt_list.append(line)

                gchat = Groupchat(self._adb, self._wechat_list, self.groups_list, self.wechats_index,
                                  self._groups_txt_list, self.file_groups_image, self)
                gchat.main()
            elif self._mode == 10:
                for f in self.file.open1(self._file_add_friends):
                    print(f)
                    line = f
                    line = file.delete_line_breaks(line)
                    line = line.strip()
                    self.phonelist.append(line)
                sreachw = SreachFriend(self._adb, self._wechat_list, self.phonelist, self.wechats_index, self)
                sreachw.main()

        except KeyboardInterrupt as e:
            print('e', e)

    def test(self):
        self._adb.refresh_nodes()
        # self._adb.click_by_content_after_refresh('微信')
        # a = self._adb.find_nodes_by_text4444()
        # for a1 in a:
        #     print(a1)
        # self._adb.adb_click(500, 650)
        # for f in self.file.open1(self._file_add_friends):
        #     print(f)
        #     line = f
        #     line = file.delete_line_breaks(line)
        #     line = line.strip()
        #     self.phonelist.append(line)
        # sreachw = SreachFriend(self._adb, self._wechat_list, self.phonelist, self)
        # sreachw.main()
        # self._adb.adb_keyboard(63)
        # self._adb.click_by_text_after_refresh("搜狗输入法小米版")
        # self._adb.adb_put_back()
        # self._adb.adb_put_back()
        # self._adb.adb_put_back()
        # self._adb.adb_put_back()
        # self._adb.adb_put_back()
        # read = Readbook(self._adb, self._wechat_list, self.wechats_index, self)
        # read.main()

    def main(self):
        # for i in range(10):
        #     print(random.randint(0,3))
        # self.test()
        self.next_run()
