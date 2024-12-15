import pyautogui
import os
import time

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

# 主函数
def main():
    # 断开网口
    manage_ethernet("disconnect")
    
    # 打开浏览器
    pyautogui.hotkey('win', 'r')
    pyautogui.write('chrome')
    pyautogui.press('enter')
    time.sleep(2)  # 等待浏览器打开

    # 在地址栏输入地址
    pyautogui.write('http://example.com')
    pyautogui.press('enter')
    time.sleep(2)  # 等待页面加载

    # 定位用户名和密码输入框，输入预设用户名密码
    username_location = pyautogui.locateOnScreen('username.png')
    password_location = pyautogui.locateOnScreen('password.png')
    login_button_location = pyautogui.locateOnScreen('login_button.png')

    if username_location and password_location and login_button_location:
        pyautogui.click(username_location)
        pyautogui.write('your_username')
        pyautogui.click(password_location)
        pyautogui.write('your_password')
        pyautogui.click(login_button_location)
    else:
        print("Could not locate username or password fields.")

    # 检测到“下线”按钮重新联接网口
    offline_button_location = pyautogui.locateOnScreen('offline_button.png')
    if offline_button_location:
        manage_ethernet("connect")

if __name__ == '__main__':
    main()
