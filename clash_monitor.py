import subprocess 

def is_process_running(process_name):
    """
    检查指定进程是否正在运行。
    该函数通过执行 'tasklist' 命令并检查其输出来确定指定进程是否正在运行。
    参数:
    process_name (str): 要检查的进程名称，例如 'notepad.exe'。
    返回:
    bool: 如果进程正在运行则返回 True，否则返回 False。
    """
    # 执行 'tasklist' 命令并捕获其输出
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True)
    
    # 确定指定的进程名称是否存在于 'tasklist' 的输出中
    return process_name in result.stdout

def test_process(process_name): 
    if is_process_running(process_name): 
        print(f"{process_name} 正在运行。")
        return True 
    else: 
        print(f"{process_name} 未运行。")
        return False 

def start_process(process_path,action="start"): 
    try: 
        if action == "start": 
            subprocess.Popen([process_path]) 
            print(f"启动 {process_path} 成功。") 
        elif action == "kill": 
            subprocess.run(['taskkill', '/F', '/IM', process_path], check=True) 
            print(f"Process {process_path} terminated successfully.") 
        else: 
            print("Invalid action. Use 'start' to start a process or 'kill' to terminate a process.") 
    except subprocess.CalledProcessError as e: 
        print(f"Failed to terminate process {process_path}: {e}")
    except Exception as e: 
        print(f"Error managing process {process_path}: {e}")
                                                       
if __name__ == "__main__": 
    process_name = "clash-verge.exe"
    if not test_process(process_name): 
        start_process("C:\\Program Files\\Clash Verge\\clash-verge.exe")
    test_process('clash-verge-service.exe') 
    
    input("按下Enter键退出")
