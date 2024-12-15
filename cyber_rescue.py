import pyautogui
import os
import time
import clash_monitor as clash
import subprocess 

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
    if clash.test_process("clash") == True:
        subprocess.run(['taskkill', '/F', '/IM',"clash-verge.exe"], check=True)

# 主函数
def main(username,password):
    #检查clash进程
    check_clash()

    # 断开网口
    #manage_ethernet("disconnect")
    print("正在断开网口（测试）")
    
    # 打开浏览器
    pyautogui.hotkey('win', 'r')
    pyautogui.write('msedge.exe')
    pyautogui.press('enter')
    time.sleep(2)  # 等待浏览器打开

    # 在地址栏输入地址
    pyautogui.write('http://10.30.12.10:30004/byod/view/byod/byodLogin.html')
    pyautogui.click(pyautogui.locateCenterOnScreen('src\\web_click.png'))
    pyautogui.press('enter')
    time.sleep(4)  # 等待页面加载

    # 定位用户名和密码输入框，输入预设用户名密码
    username_location = pyautogui.locateOnScreen('src\\user.png')
    password_location = pyautogui.locateOnScreen('src\\password.png')
    login_button_location = pyautogui.locateOnScreen('src\\login.png')

    if username_location and password_location and login_button_location:
        pyautogui.click(username_location)
        pyautogui.write(username)
        pyautogui.click(password_location)
        pyautogui.write(password)
        pyautogui.click(login_button_location)
    else:
        print("Could not locate username or password fields.")

    # 检测到“下线”按钮重新联接网口
    offline_button_location = pyautogui.locateOnScreen('src\sucessful.png')
    if offline_button_location:
        #manage_ethernet("connect")
        print("正在重连网络（测试）")

if __name__ == '__main__':
    main("20224301003048","121334")
