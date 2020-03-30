# -*- coding: utf-8 -*-

import json
import os
import config
# from urlparse import parse_qs
from urllib.parse import urlparse
from wsgiref.simple_server import make_server
import requests
# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
def application(environ, start_response):
    # 定义文件请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body，这里只涉及到get
    # 获取当前get请求的所有数据，返回是string类型
    params = urlparse(environ['QUERY_STRING'])
    # 获取get中key为name的值
    url = params.get('adb', [''])[0]
    result = None
    if url == 'info':
        #devices = getDevicesAll()
        devices = config.devices
        result = getInfoAll(devices)
    elif url == 'shot':
        device = params.get('device', [''])[0]
        result = getScreencap(device)
    elif url == 'ctrl':
        ml = params.get('ml', [''])[0]
        if ml == "open":
            ip = params.get('ip', [''])[0]
            result = connectAdb("%s:5555"%(ip),ip)
        elif ml == "close":
            ip = params.get('ip', [''])[0]
            result = disconnectAdb(ip)
    dic = {'result': result,'code':'10000'}
    # 组成一个数组，数组中只有一个字典
    return [json.dumps(dic,ensure_ascii=False)]
def uploadQiniu(bys):
    url = 'http://push.ecfun.cc/petpet/Server/src/app/qiniu/upload.php'
    img_file= {'img': bys}#此处img是服务器端post文件字段
    data_result = requests.post(url, {}, files=img_file)
    return data_result
def convert_img(path):
    result = ""
    with open(path, "r") as f:
        bys = f.read()
        bys_ = bys.replace(b"\r\n",b"\n")  # 二进制流中的"\r\n" 替换为"\n"
        json_data = uploadQiniu(bys_).json()
        result = str(json_data['url'])
    with open(path, "w") as f:
        f.write(bys_)
    return result
def connectAdb(dname,ip):
    state = ""
    try:
        result = os.popen("adb -s "+ dname +" connect "+ ip ).read()
        if 'unable' in result:
            state = 'unable'
        elif 'connected' in result:
            state = 'connected'            
    except:
        state = 'failed'
    return state
def disconnectAdb(ip):
    try:
        os.popen("adb disconnect "+ip)
    except:
        pass
    return 'disconnect'

def getScreencap(dName):
    path_result = "%s/screenshot/%s"%(os.path.split(os.path.realpath(__file__))[0],dName)
    if not os.path.exists(path_result):
        os.makedirs(path_result)
    shell = "adb -s "+dName+" shell screencap -p > "+path_result+"/screen.png"
    try:
        os.popen(shell)
    except:
        pass
    return convert_img("%s/screen.png"%(path_result))
def getDevicesAll():
    devices = []
    try:
        for dName_ in os.popen("adb devices"):
            if "\t" in dName_:
                devices.append(dName_.split("\t")[0])
        devices.sort(cmp=None, key=None, reverse=False)
    except:
        pass
    return devices
def get_wifi_state(dName):
    state = "not connect"
    wifi = "4G"
    try:
        for wifi_ in os.popen("adb -s " + dName + " shell dumpsys wifi"):
            if "enabled" in wifi_:
                state = "connect"
            if "disabled" in wifi_:
                state = "not connect"
            if "ssid" == wifi_[0:4] and state == "connect":
                wifi = wifi_.split("=")[1].replace('\r\n','')
    except:
        pass
    return wifi
def getInfoAll(devices):
    info = []
    for i in range(0,len(devices)):
        model = ""
        barrey = ""
        try:
            for model_ in os.popen("adb -s "+ devices[i][0] +" shell getprop ro.product.model"):
                  model = model_.replace('\r\n', '')
            for battery_ in os.popen("adb -s " + devices[i][0] + " shell dumpsys battery"):
                if "level" in battery_:
                    barrey = battery_.split(":")[1].strip() .replace('\r\n', '')
            if barrey == "":
                info.append({"id":str(i+1),"device":devices[i][0],"model":devices[i][2],"barrey":"0%","wifi":"-","state":"offline"})
            else:
                info.append({"id":str(i+1),"device":devices[i][0],"model":model,"barrey":barrey+"%","wifi":get_wifi_state(devices[i][0]),"state":"online"})
        except:
            pass
    return info
if __name__ == "__main__":
    port = 80
    httpd = make_server("0.0.0.0", port, application)
    print("serving http on port {0}...".format(str(port)))
    httpd.serve_forever()