from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import subprocess
import requests
import time
from log_config import log_message
from clash_monitor import is_process_running, start_process

# 定义请求头部信息
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'connection':'keep-alive',
    'Cache-Control': 'no-cache',
    "cookie":"testcookie=yes; userip=10.20.172.199",
    'host': '10.30.12.10:30004',
    'pragma':'no-cache',
    'Referer': 'http://10.30.12.10:30004/byod/index.html?usermac=00-13-EF-5F-40-4A&userip=10.20.172.199&userurl=http://www.msftconnecttest.com/redirect&original=http://www.msftconnecttest.com/redirect&ssid=gtxy_wifi',
    "upgrade-insecure-requests": '1',
    'x-requested-with':'XMLHttpRequest'
}

# 登录和检查状态的数据
dataCheck = {
    "code": 0,
    "msg": "success",
    "data": {
        "showLoginDown": True
    }
}

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

auth_url = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"
checkStatus = "http://10.30.12.10:30004/byod/byodrs/login/queryResult"
username = "20224301003001"
password = "MTQwMzY5"

# 网口操作
def manage_ethernet(action):
    try:
        log_message(0, f"正在执行以太网操作: {action}", "wifi_reconnect_log.txt", "cyber_rescue.py")
        if action in ["disconnect", "disable", "dis"]:
            result = os.system('netsh interface set interface "以太网" admin=disable')
            if result != 0:
                log_message(1, "Failed to disable Ethernet.", "wifi_reconnect_log.txt", "cyber_rescue.py")
        elif action in ["connect", "enable", "en"]:
            result = os.system('netsh interface set interface "以太网" admin=enable')
            if result != 0:
                log_message(1, "Failed to enable Ethernet.", "wifi_reconnect_log.txt", "cyber_rescue.py")
        else:
            log_message(1, "Invalid operation, choose 'disconnect' or 'connect'.", "wifi_reconnect_log.txt", "cyber_rescue.py")
    except Exception as e:
        log_message(1, f"Error managing Ethernet interface: {e}", "wifi_reconnect_log.txt", "cyber_rescue.py")

def check_clash():
    try:
        if clash.test_process("clash") == True:
            subprocess.run(['taskkill', '/F', '/IM',"clash-verge.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error killing clash: {e}")

def main(username, password):
    # 检查Clash进程
    #check_clash()

    # 断开以太网（测试时注释掉）
    # manage_ethernet("disconnect")
    print("正在断开网口（测试）")

    """设置浏览器选项
    浏览器选项:
    edge_options.add_argument('--profile-directory=Default')：指定用户配置文件目录。
    edge_options.add_argument('start-maximized')：启动时最大化窗口。
    edge_options.add_argument('--disable-popup-blocking')：禁用弹窗拦截。
    """
    edge_options = EdgeOptions()
    edge_options.add_argument('--profile-directory=Default')
    edge_options.add_argument('start-maximized')
    edge_options.add_argument('--disable-popup-blocking')

    # 使用Selenium打开浏览器并导航到登录页面
    driver = webdriver.Edge(options=edge_options)
    driver.get("http://10.30.12.10:30004/byod/view/byod/byodLogin.html")
    driver.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_userNamet")))

    try:
        # 定位用户名和密码输入框并输入预设用户名和密码
        username_field = driver.find_element(By.ID, "id_userName")
        time.sleep(10)  # 增加等待时间
        password_field = driver.find_element(By.ID, "id_userPwd")
        time.sleep(10)  # 增加等待时间
        login_button = driver.find_element(By.ID, "id_lable_loginbutton_auth")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
    except Exception as e:
        print(f"Error during login: {e}")

    # 检测到“下线”按钮重新连接以太网
    try:
        time.sleep(10)  # 增加等待时间
        offline_button = driver.find_element(By.ID,"id_logout")
        if offline_button:
            # manage_ethernet("connect")
            print("正在重连网络（测试）")
    except Exception as e:
        print(f"Error finding offline button: {e}")

    driver.quit()

if __name__ == '__main__':
    main("20224301003048", "121334")
