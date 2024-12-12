import subprocess 

def is_process_running(process_name): 
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True) 
    return process_name in result.stdout 
def test_process(process_name): 
    if is_process_running(process_name): 
        print(f"{process_name} 正在运行。")
        return True 
    else: 
        print(f"{process_name} 未运行。")
        return False 

def start_process(process_path): 
    try: 
        subprocess.Popen([process_path]) 
        print(f"启动 {process_path} 成功。") 
    except Exception as e: 
        print(f"启动 {process_path} 失败: {e}")
                                                       
if __name__ == "__main__": 
    process_name = "clash-verge.exe"
    if not test_process(process_name): 
        start_process("C:\\Program Files\\Clash Verge\\clash-verge.exe")
    test_process('clash-verge-service.exe') 
    
    input("按下Enter键退出")
