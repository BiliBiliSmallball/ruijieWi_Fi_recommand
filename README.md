# Wi-Fi Reconnection Service

## 功能概述

这个程序用于自动检测并重连Wi-Fi连接，能够根据时间调整检测频率，并记录每次重连和运行的信息。此外，它还包含一个手动检测Wi-Fi连接的功能，用户可以通过按下Enter键来触发手动检测。

## 项目升级计划：
## 增加功能

### ~~用户界面~~
- ~~为项目添加图形用户界面（GUI），使用户交互更加友好。~~

### 多SSID支持
- 允许用户配置多个Wi-Fi网络，并在连接失败时尝试连接下一个网络。

### 管理网页
- 通过Web访问服务器地址的特定端口，显示`err_log`的内容。

## 性能优化

### 检测频率调整
- 根据用户的实际使用情况，优化检测频率，以减少资源消耗。

### 错误处理
- 增强错误处理机制，确保程序在遇到异常情况时能够稳定运行。

## 日志和监控

### 详细日志记录
- 增加日志记录的详细程度，包括更多的调试信息，以便于问题排查。

### 性能监控
- 添加性能监控，记录程序运行的关键性能指标。  

## 功能实现

1. **Wi-Fi连接检测**：
   - 使用 `is_wifi_connected()` 函数，通过运行 `netsh wlan show interfaces` 命令来检查Wi-Fi是否连接。
   - 如果未连接，则尝试通过 `connect_to_wifi(ssid)` 函数重新连接Wi-Fi。

2. **日志记录**：
   - 所有运行日志将记录在 `wifi_reconnect_log.txt` 文件中，包括每次检测和重连的时间戳和结果。检查  
   - 文件`./err_log.txt`将记录错误和警告，定时检查该文件即可

3. **Clash进程检测**：
   - 使用 `is_clash_running()` 函数检测 `clash-verge.exe` 是否正在运行。
   - 如果未运行，则尝试通过 `start_process(process_path)` 函数启动 `clash-verge.exe`。

4. **手动检测功能**：
   - ~~用户可以通过按下Enter键来手动检测Wi-Fi连接。~~  
   - ~~调用 `manual_check()` 函数，手动触发Wi-Fi连接检测并记录结果。~~  
   - 什么时候写出来在说吧

## 使用方法

1. **配置Wi-Fi网络名称**：
   - 修改代码中的 `ssid` 变量，替换为你自己的Wi-Fi网络名称：
     ```python
     ssid = 'gtxy_wifi'  # 替换为你的Wi-Fi网络名称
     ```

2. **运行程序**：
   - 打开命令提示符或终端，导航到脚本所在目录，运行以下命令启动程序：
     ```sh
     python wifi_reconnect_service.py
     ```
   - 程序启动后，会自动检测并重连Wi-Fi。

3. **日志查看**：
   - 所有运行日志将记录在 `wifi_reconnect_log.txt` 文件中，包括每次检测和重连的时间戳和结果。
   - 可以通过查看日志文件来查看程序运行情况
   - 错误提示将被记录在 `error_log.txt` 文件中。  

## 注意事项

- 程序运行时，需要保持命令提示符或终端窗口打开。
- 程序会根据设定的检测频率自动进行Wi-Fi连接状态检测。

## 示例输出

程序运行时的示例输出如下：
```powershell
Starting Wi-Fi reconnection service. press Ctrl+C to exit.   
Wi-Fi is connected.  
Reconnection attempts: 0  
Run count: 1  
运行时间：16:00:00
```

## 特别鸣谢 && 支持 && 来源
- ![使用zerotier实现免费上网](./使用zerotier实现免费上网%20-%20Yet%20Another%20何榜文's%20Blog.pdf)
- > 虽然我的环境好像不需要zerotier。

## 欢迎fork和pr!
## Forks and PRs are welcome!