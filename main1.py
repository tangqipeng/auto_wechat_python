#!/usr/local/bin/python
# -*- coding:utf-8 -*-


import time
from adb import By
from adb import Adb
import file
import random


class Main:
    def __init__(self, port=None, device=None):
        self._adb = Adb(port, device)

        # 用于查找失败三次时 程序暂停半小时
        self._flag = 0

        # 该账号加了多少个
        self._addfriendnum = 0

        self._success = []
        self._failed = []

        self._dict = {'success': self._success, 'failed': self._failed}

        self.file = file.File()
        self._json = self.file.json()

        # config.json 配置信息
        # 查找联系人模式 file | loop
        self._mode = self._json['mode']
        # 循环首尾 包含首 不包含尾
        self._loop = self._json['loop']
        # 文件路径 手机号码一行一个
        self._file = self._json['file']
        # 自动切换账号 微信登录 微信预留账号
        self._account = self._json['account']
        # 累计查找结果达到指定个数 会从内存写入到文件
        self._dump = self._json['dump']
        # 切换账号达到一定次数 会休眠 单位分钟
        self._sleep = self._json['sleep']
        # 切换账号指定次数
        self._sleep_flag = self._json['sleep-flag']
        # 微信分身数
        self._wechat_count = self._json['wechatcount']
        # 该账号加好友的总个数
        # self._addfriendcount = random.randint(10,15)
        self._addfriendcount = self._json['friends']

        # 微信分身个数 如果要从微信本身开始运行则设为-1，从微信分身开始运行设为0，从微信分身1开始设为1，以此类推， 需要去config文件中修改startwechat的值，根据你设置的值打开相应的微信分身
        self._wechat = self._json['startwechat']
        self._old_wechat = self._json['startwechat']
        self.clearnum = self._json['cleanmemory']

        self._end = False

    # 输出添加结果到内存 或 文件
    def push(self, key: str, value):
        _list = self._dict[key]
        _list.append(value)

        # list到一定长度 输出到文件
        if int(self._dump) == len(_list):
            self.file.dump1(_list, key)

    def init(self):
        self._addfriendnum = 0
        if int(self._wechat_count) > self._wechat:
            self._adb.refresh_nodes()
            time.sleep(2)
            if self._adb.find_nodes_by_text('微信多开'):
                if self._wechat == -1:
                    self._adb.click_by_text_after_refresh('微信')
                elif self._wechat == 0:
                    self._adb.click_by_text_after_refresh('微信分身')
                    d = random.randint(30, 60)
                    time.sleep(d)
                else:
                    self._adb.click_by_text_after_refresh('微信分身' + str(self._wechat))
                    e = random.randint(30, 60)
                    time.sleep(e)

                self._adb.click_by_text_after_refresh('通讯录')
                time.sleep(1)
                self._adb.click_by_text_do_not_refresh('外部联系人')
                time.sleep(1)
                self._adb.click_by_text_do_not_refresh('添加朋友')
                time.sleep(1)
                self._adb.click_by_text_do_not_refresh('微信号/手机号')
            else:
                print('页面错误')
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self.init()
        else:
            self._end = True
            print('微信切换完毕')
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()

    def add_friends(self, phone: str):
        print('self._addfriendnum=' + str(self._addfriendnum))
        if int(self._addfriendcount) > self._addfriendnum:
            print('===== 开始查找 ===== ' + phone + ' =====')
            # self._adb.click_by_text_after_refresh('微信号/手机号')

            time.sleep(1)

            # 输入号码
            self._adb.adb_input(phone)

            time.sleep(5)
            self._adb.refresh_nodes()
            time.sleep(2)
            if self._adb.find_nodes_by_text('搜索:' + phone):
                # 点击搜索
                self._adb.click(0)
                print('  ==> 点击搜索 ==>  ' + phone)

                self._adb.refresh_nodes()

                time.sleep(1)
                self._addfriendnum += 1
                if self._adb.find_nodes_by_text('操作过于频繁，请稍后再试'):
                    print('  <== 查找失败 <==  ')
                    self.push('failed', phone + '操作过于频繁，请稍后再试')
                    self._adb.adb_put_back()
                    # 微信退回到主页面
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()

                    # 回到桌面
                    # self._adb.adb_back_to_desktop()

                    self._wechat += 1

                    if (self._wechat - self._old_wechat) / self.clearnum >= 1:
                        time.sleep(5)
                        self._adb.adb_put_back()
                        time.sleep(1)
                        self._adb.adb_keyboard(82)
                        time.sleep(1)
                        self._adb.click_by_text_do_not_refresh0('清理')
                        time.sleep(2)
                    self.init()

                # 查找成功
                elif self._adb.find_nodes_by_text('添加到通讯录'):
                    self._adb.click(0)

                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_text('发送'):
                        self._adb.click(0)
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text('发送'):
                            print('  <== 发送失败 <==  ')
                            self.push('failed', phone + '发送失败，不要删除，还可再用')
                            time.sleep(2)
                            self._adb.adb_put_back()
                            self._adb.adb_put_back()
                        else:
                            print(' !! <== 发送成功 <==  ')
                            self.push('success', phone)
                            self._adb.adb_put_back()

                elif self._adb.find_nodes_by_text('发消息'):
                    print('  <== 已经是好友 无需再次添加 <==  ')
                    self.push('success', phone)
                    self._adb.adb_put_back()

                elif self._adb.find_nodes_by_text('该用户不存在') or self._adb.find_nodes_by_text('被搜帐号状态异常，无法显示'):
                    print('  <== 该用户不存在 或 帐号异常 <==  ')
                    self.push('failed', phone + '该用户不存在 或 帐号异常')

                a = random.randint(15, 20)
                time.sleep(a)
                # 清空已输入的字符
                self._adb.refresh_nodes()
                if self._adb.find_nodes('true', By.naf):
                    self._adb.click(0)
            else:
                print('页面错误')
                # 微信退回到主页面
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()

                # 回到桌面
                # self._adb.adb_back_to_desktop()

                self._wechat += 1
                if (self._wechat - self._old_wechat) / self.clearnum >= 1:
                    time.sleep(5)
                    self._adb.adb_put_back()
                    time.sleep(1)
                    self._adb.adb_keyboard(82)
                    time.sleep(1)
                    self._adb.click_by_text_do_not_refresh0('清理')
                    time.sleep(2)
                self.init()

        elif int(self._addfriendcount) == self._addfriendnum:
            print(' ---- 开始切换账号 ----')

            # 微信退回到主页面
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()
            self._adb.adb_put_back()

            # 回到桌面
            # self._adb.adb_back_to_desktop()

            self._wechat += 1
            if (self._wechat - self._old_wechat) / self.clearnum >= 1:
                time.sleep(5)
                self._adb.adb_put_back()
                time.sleep(1)
                self._adb.adb_keyboard(82)
                time.sleep(1)
                self._adb.click_by_text_do_not_refresh0('清理')
                time.sleep(2)
            self.init()

    def test(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('微信'):
            print('a')
        self._adb.adb_keyboard(82)
        self._adb.click_by_text_do_not_refresh0('清理')
        # if self._adb.find_nodes('true', By.sel, 0):
        #     print('b')

    def main(self):
        # self.test()

        self.init()
        if 'file' == self._mode:
            print("self._file=" + str(self._file))
            for f in self.file.open1(self._file):
                if self._end is False:
                    print(f)
                    line = f
                    line = file.delete_line_breaks(line)
                    self.add_friends(str(line))
        elif 'loop' == self._mode:
            if self._end is False:
                for line in range(len(self._loop)):
                    self.add_friends(str(self._loop[line]))

        # 输出最后的添加结果
        self.file.dump1(self._success, 'success')
        self.file.dump1(self._failed, 'failed')
