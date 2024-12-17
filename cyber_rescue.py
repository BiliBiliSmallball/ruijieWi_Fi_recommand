from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import subprocess
import clash_monitor as clash

# 断开或连接以太网
def manage_ethernet(action):
    try:
        if action in ["disconnect", "disable", "dis"]:
            result = os.system('netsh interface set interface "以太网" admin=disable')
            if result != 0:
                print("Failed to disable Ethernet.")
        elif action in ["connect", "enable", "en"]:
            result = os.system('netsh interface set interface "以太网" admin=enable')
            if result != 0:
                print("Failed to enable Ethernet.")
        else:
            print("Invalid operation, choose 'disconnect' or 'connect'.")
    except Exception as e:
        print(f"Error managing Ethernet interface: {e}")

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
