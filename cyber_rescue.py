import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# 断开或连接以太网
def manage_ethernet(action):
    try:
        if action in ["disconnect", "disable", "dis"]:
            os.system('netsh interface set interface "以太网" admin=disable')
        elif action in ["connect", "enable", "en"]:
            os.system('netsh interface set interface "以太网" admin=enable')
        else:
            print("Invalid operation, choose 'disconnect' or 'connect'.")
    except Exception as e:
        print(f"Error managing Ethernet interface: {e}")

# 锐捷认证登录
def ruijie_login(auth_url, username, password):
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    driver = webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe', options=options)

    driver.get(auth_url)
    time.sleep(2)  # 等待页面加载

    # 找到并填写用户名和密码
    username_input = driver.find_element(By.NAME, "userName")
    password_input = driver.find_element(By.NAME, "userPassword")
    username_input.send_keys(username)
    password_input.send_keys(password)

    # 找到并点击提交按钮
    submit_button = driver.find_element(By.NAME, "submit_button_name")
    submit_button.click()
    time.sleep(5)  # 等待认证完成

    # 判断是否登录成功
    login_success = "登录成功的标志" in driver.page_source

    driver.quit()
    return login_success

# 检查WiFi连接状态
def check_wifi_status():
    wifi_status = os.popen('netsh wlan show interfaces').read()
    return "状态 : 已连接" in wifi_status

# 开始连接过程
def start_connect(auth_url, username, password):
    manage_ethernet("disconnect")
    time.sleep(3)

    login_success = False
    while not check_wifi_status():
        login_success = ruijie_login(auth_url, username, password)
        if login_success:
            print("认证成功，等待WiFi连接...")
            time.sleep(5)  # 确保有足够的时间完成WiFi连接
        else:
            print("认证失败，重试中...")
            time.sleep(5)  # 等待几秒后重试

    if login_success:
        print("WiFi已连接")
    else:
        print("WiFi连接失败")

    manage_ethernet("connect")
    time.sleep(5)

def main():
    auth_url = "http://你的校园网认证网址"
    username = "你的用户名"
    password = "你的密码"

    start_connect(auth_url, username, password)

if __name__ == '__main__':
    main()
