import subprocess
import os
import psutil

def is_process_running(process_name): 
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False
def test_process(process_name):
    if is_process_running(process_name):
        print(f"{process_name} 正在运行。")
        return True
    else:
        print(f"{process_name} 未运行。")
        return False
    
def start_process(process_path):
    if os.path.isfile(process_path) and os.access(process_path, os.X_OK):
        try:
            subprocess.Popen([process_path])
            print(f"启动 {process_path} 成功。")
        except FileNotFoundError as e:
            print(f"启动 {process_path} 失败: 文件未找到 - {e}")
        except OSError as e:
            print(f"启动 {process_path} 失败: 操作系统错误 - {e}")
        except Exception as e:
            print(f"启动 {process_path} 失败: {e}")
    
    def main():
        process_names = ["clash-verge.exe", "clash-verge-service.exe"]
        for name in process_names:
            start_process("C:\\Program Files\\Clash Verge")
            start_process("C:\\Program Files\\Clash Verge\\clash-verge.exe")
        test_process('clash-verge-service.exe') 
        if not test_process('clash-verge-service.exe'):
            start_process("C:\\Program Files\\Clash Verge\\clash-verge-service.exe")
        input("按下Enter键退出")
    
    if __name__ == "__main__":
        main()
