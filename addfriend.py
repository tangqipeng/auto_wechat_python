import time
import random


class Addfriend:
    def __init__(self, adb, wechat_list, defaulthint_list, new_hint_list, continue_add, friends, startwechat,
                 phone_list, tag, sleep, main):
        self._adb = adb

        self._wechat_list = wechat_list

        self._reminder = defaulthint_list

        self._input_hint = new_hint_list

        self._continue_add = continue_add

        self._addfriendcount = friends

        if friends % continue_add == 0:
            self._addfriend_circle_count = int(friends / continue_add)
            self._last_circle_num = continue_add
        else:
            self._addfriend_circle_count = int(friends / continue_add) + 1
            self._last_circle_num = friends % continue_add

        print('self._addfriend_circle_count=' + str(self._addfriend_circle_count))
        print('self._last_circle_num=' + str(self._last_circle_num))

        self.old_wechat_index = startwechat

        self._old_tag = tag

        self._tag = ""

        self._main = main

        # 微信总个数
        self._wechat_count = len(self._wechat_list)

        # 从哪一个微信开始运行
        self.wechats_index = startwechat

        self._circle_sleep = sleep
        # 按照要加好友的个数，循环调用次数
        self.circle_index = 1

        self.phone_index = 0

        self._single_add_index = 0

        self.phonelist = phone_list

        self._end = False

        # 输出添加结果到内存 或 文件

    def clean_wechat(self):
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        time.sleep(3)
        self._adb.adb_put_back()
        # 点击进程按钮，显示所有后台进程
        self._adb.adb_keyboard(82)
        time.sleep(1)
        # 点击清理按钮
        self._adb.click_by_text_do_not_refresh0('清理')

    def verify_apply_for(self, phone, wechatname):
        if self._adb.find_nodes_by_text('验证申请'):
            if self.wechats_index < len(self._reminder) and self.wechats_index < len(self._input_hint):
                if self._reminder[self.wechats_index].strip() != self._input_hint[self.wechats_index].strip():
                    if self._adb.find_nodes_by_text(self._reminder[self.wechats_index].strip()):
                        self._adb.click(0)
                        time.sleep(1)
                        self._adb.adb_click(980, 400)
                        time.sleep(1)
                        self._adb.adb_input_chinese(self._input_hint[self.wechats_index].strip())
                        time.sleep(1)
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text('发送'):
                            self._adb.click(0)
                            time.sleep(3)
                            self._adb.refresh_nodes()
                            if self._adb.find_nodes_by_text('验证申请'):
                                self.phone_index += 1
                                print('  <== 发送失败 <==  ')
                                self._main.push('failed', phone + ' ' + wechatname + '发送失败')
                            else:
                                self.phone_index += 1
                                print(' !! <== 发送成功 <==  ')
                                self._main.push('success', phone + ' ' + wechatname)
                    else:
                        if self._adb.find_nodes_by_text('发送'):
                            self._adb.click(0)
                            time.sleep(3)
                            self._adb.refresh_nodes()
                            if self._adb.find_nodes_by_text('验证申请'):
                                self.phone_index += 1
                                print('  <== 发送失败 <==  ')
                                self._main.push('failed', phone + ' ' + wechatname + '发送失败')
                            else:
                                self.phone_index += 1
                                print(' !! <== 发送成功 <==  ')
                                self._main.push('success', phone + ' ' + wechatname)
                else:
                    if self._adb.find_nodes_by_text('发送'):
                        self._adb.click(0)
                        time.sleep(3)
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text('验证申请'):
                            self.phone_index += 1
                            print('  <== 发送失败 <==  ')
                            self._main.push('failed', phone + ' ' + wechatname + '发送失败')
                        else:
                            self.phone_index += 1
                            print(' !! <== 发送成功 <==  ')
                            self._main.push('success', phone + ' ' + wechatname)
            else:
                print('提示语个数不对，请检查')
        elif self._adb.find_nodes_by_text('发消息'):
            print('  <== 添加好友成功 <==  ')
            self.phone_index += 1
            self._main.push('success', phone + ' ' + wechatname)
        elif self._adb.find_nodes_by_content('添加到通讯录'):
            print('  <== 添加好友成功1 <==  ')
            self.phone_index += 1
            self._main.push('success', phone + ' ' + wechatname + '账号异常')

    def is_success(self, phone, wechatname):
        if self._adb.find_nodes_by_text('标签'):
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('添加到通讯录'):
                self._adb.click(0)
                time.sleep(3)
                self._adb.refresh_nodes()
                time.sleep(1)
                self.verify_apply_for(phone, wechatname)

        else:
            if self._adb.find_nodes_by_text('设置备注和标签'):
                self._adb.click(0)
                time.sleep(1)
                if self._adb.find_nodes_by_text('添加标签对联系人进行分类'):
                    self._adb.click(0)
                else:
                    self._adb.adb_click(500, 600)
                time.sleep(1)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('添加标签'):
                    if self._adb.find_nodes_by_text(self._tag):
                        self._adb.click(0)
                    else:
                        self._adb.click_by_text_after_refresh('添加标签')
                        self._adb.adb_input_chinese(self._tag)
                    time.sleep(1)
                    self._adb.click_by_text_after_refresh('保存')
                self._adb.refresh_nodes()
                time.sleep(1)
                if self._adb.find_nodes_by_text('设置备注和标签'):
                    self._adb.click(0)
                    if self._adb.find_nodes_by_text(self._tag):
                        self._adb.click_by_text_after_refresh('保存')
                        self._adb.refresh_nodes()
                        if self._adb.find_nodes_by_text('添加到通讯录'):
                            if self._adb.find_nodes_by_text(self._tag):
                                self._adb.click_by_text_after_refresh('添加到通讯录')
                                time.sleep(3)
                                self._adb.refresh_nodes()
                                self._adb.click_by_text_after_refresh('发送')
                                time.sleep(1)
                                self.verify_apply_for(phone, wechatname)

            else:
                print('不是设置标签页')

    def verify_search(self, phone, wechatname):
        if self._adb.find_nodes_by_text('操作过于频繁，请稍后再试'):
            self._single_add_index = self._continue_add
            print('  <== 查找失败 <==  ')
            self._main.push('failed', phone + ' ' + wechatname + '操作过于频繁，请稍后再试')
            return 1
        elif self._adb.find_nodes_by_text('添加到通讯录'):
            self._adb.refresh_nodes()
            self.is_success(phone, wechatname)
            self.phone_index += 1
            self._main.push('success', phone + ' ' + wechatname)

            # if self._adb.find_nodes_by_content('女'):
            #     self._tag = self._old_tag + 'w'
            #     self._single_add_index += 1
            #     print('  self._tag =  ' + self._tag)
            #     self.is_success(phone, wechatname)
            # elif self._adb.find_nodes_by_content('男'):
            #     self._tag = self._old_tag + 'm'
            #     self.phone_index += 1
            #     self._main.push('failed', phone + ' ' + wechatname + '性别 男')
            # else:
            #     self._tag = self._old_tag
            #     self._single_add_index += 1
            #     print('  self._tag =  ' + self._tag)
            #     self.is_success(phone, wechatname)

        elif self._adb.find_nodes_by_text('发消息'):
            print('  <== 已经是好友 无需再次添加 <==  ')
            self.phone_index += 1
            self._single_add_index += 1
            self._main.push('success', phone + ' ' + wechatname)

        elif self._adb.find_nodes_by_text('该用户不存在') or self._adb.find_nodes_by_text('被搜帐号状态异常，无法显示'):
            print('  <== 该用户不存在 或 帐号异常 <==  ')
            self.phone_index += 1
            self._single_add_index += 1
            self._main.push('failed', phone + ' ' + wechatname + '该用户不存在 或 帐号异常')

    def search_friend(self):
        if self.circle_index < int(self._addfriend_circle_count):
            single_wechat_add_count = self._continue_add
        else:
            single_wechat_add_count = self._last_circle_num
        if self._single_add_index < single_wechat_add_count:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('微信号/手机号'):
                self._adb.click(0)
                time.sleep(1)
                self._adb.refresh_nodes()
                if self._adb.find_nodes_by_text('添加朋友'):
                    print('微信号/手机号')
                    self._adb.click_by_text_after_refresh('微信号/手机号')
                if self.phone_index < len(self.phonelist):
                    phone = self.phonelist[self.phone_index].strip()
                    wechatname = self._wechat_list[self.wechats_index].strip()
                    print('===== 开始查找 ===== ' + phone + ' =====')
                    time.sleep(1)
                    # 输入号码
                    self._adb.adb_input(phone)
                    time.sleep(5)
                    self._adb.refresh_nodes()
                    time.sleep(1)
                    if self._adb.find_nodes_by_text("搜索:" + phone):
                        # 点击搜索
                        self._adb.click(0)
                        time.sleep(1)
                        print('  ==> 点击搜索 ==>  ' + phone)
                        self._adb.refresh_nodes()
                        time.sleep(1)
                        self.verify_search(phone, wechatname)

                        time.sleep(1)
                        # self._adb.adb_put_back()
                        # self._adb.adb_put_back()
                        # self._adb.adb_put_back()
                        # self._adb.adb_put_back()

                    else:
                        print('页面错误')

                        self._adb.adb_click(500, 280)
                        time.sleep(1)
                        print('  ==> 点击搜索 ==>  ' + phone)
                        self._adb.refresh_nodes()
                        time.sleep(1)
                        self.verify_search(phone, wechatname)

                        time.sleep(3)

                        # 微信退回到主页面
                        # self._adb.adb_put_back()
                        # self._adb.adb_put_back()
                        # self._adb.adb_put_back()
                        # self._adb.adb_put_back()
                        # self._adb.adb_back_to_desktop()

                    self._adb.adb_put_back()
                    time.sleep(1)
                    self._adb.refresh_nodes()
                    if self._adb.find_nodes_by_text('添加朋友'):
                        self._adb.click(0)
                        time.sleep(1)
                        self.search_friend()
                    else:
                        self._adb.adb_put_back()
                        time.sleep(1)
                        self.search_friend()
                else:
                    print('手机号不足，已经全部加完')
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    self._adb.adb_put_back()
                    time.sleep(3)
                    self._adb.adb_put_back()
                    # 点击进程按钮，显示所有后台进程
                    self._adb.adb_keyboard(82)
                    time.sleep(1)
                    # 点击清理按钮
                    self._adb.click_by_text_do_not_refresh0('清理')
            else:
                self._adb.adb_put_back()
                self.search_friend()
        else:
            print('下一个')
            self.clean_wechat()
            if int(self._wechat_count) > self.wechats_index:
                self.wechats_index += 1
            else:
                time.sleep(self._circle_sleep)
                self.wechats_index = 0
                print('微信切换完最后一个')
                print('wechat_index' + str(self.wechats_index))
                self.circle_index += 1
            self.find_wechat()

    def exit_search(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('通讯录'):
            a = random.randint(0, 2)
            if a == 0:
                self._adb.click_by_text_after_refresh('微信')
            elif a == 1:
                self._adb.click_by_text_after_refresh('通讯录')
            elif a == 2:
                self._adb.click_by_text_after_refresh('发现')

            self._adb.click_by_text_do_not_refresh('外部联系人')
            self._adb.click_by_text_do_not_refresh('添加朋友')
            self.search_friend()
        else:
            print('还未进入')
            self.check_dialog()

    def check_dialog(self):
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('　取消　'):
            self._adb.click(0)
            self.exit_search()
        elif self._adb.find_nodes_by_text('找回密码'):
            self.clean_wechat()
            if int(self._wechat_count) > self.wechats_index:
                self.wechats_index += 1
            else:
                time.sleep(self._circle_sleep)
                self.wechats_index = 0
                print('微信切换完最后一个')
                print('wechat_index' + str(self.wechats_index))
                self.circle_index += 1
            self.find_wechat()
        else:
            self.exit_search()

    def find_wechat(self):
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._single_add_index = 0
        if int(self._addfriend_circle_count) >= self.circle_index:
            self._adb.refresh_nodes()
            if self.wechats_index < len(self._wechat_list):
                if self._adb.find_nodes_by_content(self._wechat_list[self.wechats_index].strip()):
                    self._adb.click(0)
                    time.sleep(13)
                    self.exit_search()
                else:
                    self.clean_wechat()
                    if int(self._wechat_count) > self.wechats_index:
                        self.wechats_index += 1
                    else:
                        time.sleep(self._circle_sleep)
                        self.wechats_index = 0
                        print('微信切换完最后一个')
                        print('wechat_index' + str(self.wechats_index))
                        self.circle_index += 1
                    self.find_wechat()
            else:
                print('微信切换完最后一个')
                time.sleep(2)
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                self._adb.adb_put_back()
                time.sleep(self._circle_sleep)
                self.wechats_index = 0
                print('wechat_index' + str(self.wechats_index))
                self.circle_index += 1
                self.find_wechat()

        else:
            print(str(self._wechat_count) + '个微信都已加完' + str(self._addfriendcount) + '个好友')
            self.clean_wechat()

    def test(self):
        print('ceshi')
        self._adb.refresh_nodes()

    def main(self):
        try:
            # self.test()
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("ADB Keyboard")
            if len(self._reminder) == self._wechat_count and self._wechat_count == len(self._input_hint):
                self.find_wechat()
            else:
                print('提示语个数不对，请检查', "提示语个数 " + str(len(self._reminder)) + " 微信个数 " + self._wechat_count)
        except KeyboardInterrupt as e:
            print(e)
