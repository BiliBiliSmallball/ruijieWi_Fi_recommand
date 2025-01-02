"""
-*- coding: utf-8 -*-
@Time    : 2025/1/1 21:25
@File    : wifi自动重连.py
@autor   : Ender_Zhu
@Software: vscode
@Desc    : 程序的主函数，wifi自动重连·检测的脚本。
"""
import subprocess
import time
import clash_monitor as clash
import log_config

# 定义常量  
LOG_CLEAR_THRESHOLD = 600
LOG_FILE = "wifi_reconnect_log.txt" 
ERR_LOG_FILE = ".\\err_log.txt"

def is_wifi_connected(): 
    # 检查Wi-Fi是否连接 
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 
    if "已连接" in result.stdout: 
        return True 
    return False 
def connect_to_wifi(ssid): 
    # 连接到指定的Wi-Fi网络 
    subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'])
   
def is_clash_running():
    if clash.test_process("clash-verge.exe"):
        log_config.log_message(0, "clash is running", LOG_FILE, "main.py")
        return True
    else: 
        log_config.log_message(1, "clash is not running", LOG_FILE, "main.py")
        return False
    
def attempt_connection(ssid_list: list) -> bool:
    # 尝试连接到Wi-Fi网络
    for ssid in ssid_list:
        print(f"Attempting to connect to {ssid}...")
        if connect_to_wifi(ssid):
            print(f"Connected to {ssid}.")
            log_config.log_message(0,f"[INFO]Successfully connected to {ssid}.", LOG_FILE, "main.py")
            return True
        else:
            print(f"Failed to connect to {ssid}.")
            log_config.log_message(1,f"Failed to connect to {ssid}.", LOG_FILE, "main.py")
            return False

def main(ssid_list: list): 
    reconnect_count = 0 
    run_count = 0 
    log_clear_count = log_config.log_clear_tic_get(ERR_LOG_FILE)
     
    while True: 
        # 日志时间判断
        t = time.localtime() 
        sleep_time = 10 if 14 <= t.tm_hour or t.tm_hour <= 2 else 600
        
        # 核心
        if not is_wifi_connected(): 
            print("Wi-Fi已断开连接，尝试重新连接...") 
            if attempt_connection(ssid_list):
                print("重新连接成功。") 
                reconnect_count += 1 
                log_config.log_message(1, f"Automatic reconnect successful. Reconnect count: {reconnect_count}", LOG_FILE, "main.py") 
            else:
                print("重新连接失败。") 
                log_config.log_message(1, "Automatic reconnect failed.", LOG_FILE, "main.py")
        else: 
            print("Wi-Fi已连接。") 
            log_config.log_message(0, "Wi-Fi is connected", LOG_FILE, "main.py") 
        
        run_count += 1 
        log_config.log_message(0, f"Run count: {run_count}", LOG_FILE, "main.py")
        
        if run_count % 3 == 0 and not is_clash_running():
            clash.start_process("C:\\Program Files\\Clash Verge\\clash-verge.exe")
        
        # 显示
        print(f"重连次数: {reconnect_count}\n") 
        print(f"运行次数: {run_count}\n") 
        print(f"运行时间: {t.tm_hour}:{t.tm_min}:{t.tm_sec}\n") 
        
        # 日志清理
        if run_count > LOG_CLEAR_THRESHOLD: 
            log_config.log_delete(LOG_FILE, ERR_LOG_FILE, log_clear_count) 
            log_clear_count += 1
            log_config.log_message(1, f"Log cleared automatically. Log clear count: {log_clear_count}", LOG_FILE, "main.py")
            run_count = 0 # 重置运行次数 
            
        time.sleep(sleep_time) 

if __name__ == "__main__": 
    print("启动Wi-Fi重连服务。按Ctrl+C退出。") 
    ssid_list = ['gtxy_wifi',] # 替换为你的Wi-Fi网络名称 
    try: 
        main(ssid_list) 
    except KeyboardInterrupt:
        print("\n停止服务") 
        log_config.log_message(1, "The script is terminated by the user\n---------------------------------------", LOG_FILE,"main.py")
    
    # 请在测试时注释掉下面这一行
    except :
       print("\n未知错误。")
       log_config.log_message(1, "Unknown error\n---------------------------------------", LOG_FILE,"main.py")
