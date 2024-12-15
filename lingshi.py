import requests
import time
import random

header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '955',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': '10.8.2.2',
    'Origin': 'http://10.8.2.2',
    'Referer': 'http://10.30.12.10:30004/byod/view/byod/template/templatePc.html?customId=16&usermac=00-13-EF-8F-69-E9&userip=10.60.82.213&userurl=http://www.msftconnecttest.com/redirect&original=http://www.msftconnecttest.com/redirect&ssid=gtxy_wifi&nasRedirectUrl=http://10.30.12.10:30004/byod/index.html?usermac=00-13-EF-8F-69-E9&userip=10.60.82.213&userurl=http://www.msftconnecttest.com/redirect&original=http://www.msftconnecttest.com/redirect&ssid=gtxy_wifi',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'  #一般无需修改
}

dataLogin = {
        "userName": "20224301003048",
        "userPassword": "MTIxMzM0",
        "serviceSuffixId": "-1",
        "dynamicPwdAuth": False,
        "code": "",
        "codeTime": "",
        "validateCode": "",
        "licenseCode": "",
        "userGroupId": 0,
        "validationType": 0,
        "guestManagerId": 19806,
        "shopIdE": 'null',
        "wlannasid": 'null'
}

# = {
#     'userId': '',     #填写post请求中的账号
#     'password': '',   #填写post请求中加密过的密码
#     'service': '',    #选择网络接入方式，在post请求中有
#     'queryString': '',#从post请求中复制过来即可
#     'operatorPwd': '',          #不用填
#     'operatorUserId': '',       #不用填
#     'validcode': '',            #不用填
#     'passwordEncrypt': 'true',  #不用修改      
#     'userIndex': ''   #填写post请求中的对应字段
# }

dataCheck = {
        "userName": "20224301003048",
        "userPassword": "MTIxMzM0",
        "serviceSuffixId": "-1",
        "dynamicPwdAuth": False,
        "code": "",
        "codeTime": "",
        "validateCode": "",
        "licenseCode": "",
        "userGroupId": 0,
        "validationType": 0,
        "guestManagerId": 19806,
        "shopIdE": 'null',
        "wlannasid": 'null'
}

#{"code": 0,"msg": "下线成功"}

login = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"#登录地址
checkStatus = "http://10.30.12.10:30004/byod/byodrs/login/queryResult"#验证地址


def work():
    res1 = requests.post(url=checkStatus, headers=header, data=dataCheck)
    res1.encoding = 'utf-8'
    content = str(res1.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode())
    i = content.find('"result":"')
    
    if content[i + 10:i + 14] == 'wait' or content[i + 10:i + 17] == 'success':
        print(time.asctime(time.localtime(time.time())), "当前处于在线状态。")
    else:
        print(time.asctime(time.localtime(time.time())), "当前已经下线，正在尝试登录！")
        res2 = requests.post(url=login, headers=header, data=dataLogin)
        res2.encoding = 'utf-8'
        content2 = str(res2.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode())
        j = content2.find('"result":"')
        #        print(content2)
        if content2[j + 10:j + 17] == 'success':
            print(time.asctime(time.localtime(time.time())), "登录成功！")

while(True):
    try:
        work()
    except:
        print(time.asctime(time.localtime(time.time())), "监测出错，请检查网络是否连通。")
        time.sleep(1)
        continue
    time.sleep(random.randint(20, 40))#这里间隔20~40秒查询一次状态，切莫太频繁
