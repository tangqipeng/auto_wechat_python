import time
import random


class SreachFriend:
    def __init__(self, adb, wechat_list, phone_list, wechats_index, main):
        self._adb = adb
        self._wechat_list = wechat_list
        self.phonelist = phone_list
        self._main = main
        self.wechat_index = wechats_index
        self.phone_index = 0

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

    def save_search(self, phone: str):
        if self._adb.find_nodes_by_text('操作过于频繁，请稍后再试'):
            print('  <== 查找失败 <==  ')
            self._main.push('failed', phone + ' ' + '操作过于频繁，请稍后再试')
            return 1
        elif self._adb.find_nodes_by_text('添加到通讯录'):
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_content('女'):
                print('性别女')
                self.phone_index += 1
                self._main.push('female', phone)
            elif self._adb.find_nodes_by_content('男'):
                print('性别男')
                self.phone_index += 1
                self._main.push('male', phone + ' ' + '性别 男')
            else:
                print('性别保密')
                self.phone_index += 1
                self._main.push('female', phone)
            self._adb.adb_put_back()
            return 0
        elif self._adb.find_nodes_by_text('发消息'):
            print('  <== 已经是好友 无需再次添加 <==  ')
            self.phone_index += 1
            self._main.push('male', phone + ' ' + '已是好友')
            self._adb.adb_put_back()
            return 0
        elif self._adb.find_nodes_by_text('该用户不存在') or self._adb.find_nodes_by_text('被搜帐号状态异常，无法显示'):
            print('  <== 该用户不存在 或 帐号异常 <==  ')
            self.phone_index += 1
            self._main.push('male', phone + ' ' + '不存在')
            self._adb.adb_put_back()
            return 0

    def sreach_phone(self):
        print('开始')
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
                    self._adb.refresh_nodes()
                    result = self.save_search(phone)
                    print('result=', result)
                    if result == 0:
                        self.sreach_phone()
        else:
            self._adb.adb_put_back()
            self.sreach_phone()

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
            self.sreach_phone()
        else:
            print('页面不对')

    def find_wechat(self):
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text(self._wechat_list[self.wechat_index]):
            self._adb.click(0)
            time.sleep(13)
            self.exit_search()
        else:
            print('')
            # self.clean_wechat()

    def main(self):
        try:
            # self.test()
            self._adb.adb_keyboard(63)
            self._adb.click_by_text_after_refresh("ADB Keyboard")
            self.find_wechat()
        except KeyboardInterrupt as e:
            print(e)
