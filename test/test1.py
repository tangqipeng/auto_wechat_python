# -*- coding: utf-8 -*-
import os
import sys
import config
def control(argv):
    devices = config.devices
    if argv[1] == "1":
        for device in devices:
            try:
                result = os.popen("adb connect "+device[0]).read()
                if 'unable' in result:
                    print(u"%s-%s连接失败"%(device[0],device[1]))
                elif 'connected' in result:
                    print(u"%s-%s连接成功"%(device[0],device[1]))
            except:
                print(u"%s-%s连接失败"%(device[0],device[1]))
    elif argv[1] == "2":
        for device in devices:
            try:
                print(os.popen("adb disconnect "+device[3]).read())
            except:
                print(u"%s-%s连接失败"%(device[0],device[1]))
    elif argv[1] == "3":
        for device in devices:
            try:
                os.popen("adb -s " + device[0] + " shell input keyevent 164")
            except:
                print(u"%s-%s连接失败"%(device[0],device[1]))
    elif argv[1] == "4":
        for device in devices:
            try:
                os.popen("adb -s " + device[0] + " shell input keyevent 24")
            except:
                print(u"%s-%s连接失败"%(device[0],device[1]))
    elif argv[1] == "5":
        for device in devices:
            try:
                os.popen("adb -s " + device[0] + " shell input keyevent 26")
                os.popen("adb -s " + device[0] + " shell am start -n com.xbw.arukas/com.xbw.arukas.ui.ADActivity")
            except:
                print(u"%s-%s连接失败"%(device[0],device[1]))
    elif argv[1] == "6":
        if len(sys.argv)==2:
            print("请输入安装软件路径\n")
        else:
            for device in devices:
                try:
                    os.popen("adb -s " + device[0] + " install -r " + argv[2])
                except:
                    print(u"%s-%s连接失败"%(device[0],device[1]))
    elif argv[1] == "7":
        if len(sys.argv)==2:
            print("请输入卸载软件包名\n")
        else:
            for device in devices:
                try:
                    os.popen("adb -s " + device[0] + " uninstall " + argv[2])
                except:
                    print(u"%s-%s连接失败"%(device[0],device[1]))
    else:
        print(u"参数错误")
if __name__ == '__main__':
    devices = config.devices
    if len(sys.argv)==1:
        print(u"请输入参数\n1.连接adb\n2.断开adb\n3.静音\n4.响铃\n5.启动一次广告\n6.安装软件\n7.卸载软件")
    else:
        control(sys.argv)
