# Wi-Fi Reconnection Service

## 功能概述

这个程序用于自动检测并重连Wi-Fi连接，能够根据时间调整检测频率，并记录每次重连和运行的信息。此外，它还包含一个手动检测Wi-Fi连接的功能，用户可以通过按下Enter键来触发手动检测。

## 功能实现

1. **Wi-Fi连接检测**：
   - 使用 `is_wifi_connected()` 函数，通过运行 `netsh wlan show interfaces` 命令来检查Wi-Fi是否连接。
   - 如果未连接，则尝试通过 `connect_to_wifi(ssid)` 函数重新连接Wi-Fi。

2. **日志记录**：
   - 使用 `log_message(message)` 函数，将运行日志记录到 `wifi_reconnect_log.txt` 文件中，包括时间戳和消息内容。

3. **自动检测和重连**：
   - 主函数 `main()` 通过 `while` 循环持续运行，定期检查Wi-Fi连接状态。
   - 根据时间调整检测频率：夜间（16:00至次日02:00）每10秒检测一次，白天每20分钟检测一次。
   - 如果Wi-Fi连接断开，程序会尝试重新连接并记录重连次数。

4. **手动检测功能**：
   - 用户可以通过按下Enter键来手动检测Wi-Fi连接。
   - 调用 `manual_check()` 函数，手动触发Wi-Fi连接检测并记录结果。

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
   - 程序启动后，会自动检测并重连Wi-Fi。用户可以通过按下Enter键手动触发检测。

3. **日志查看**：
   - 所有运行日志将记录在 `wifi_reconnect_log.txt` 文件中，包括每次检测和重连的时间戳和结果。

## 注意事项

- 程序运行时，需要保持命令提示符或终端窗口打开。
- 程序会根据设定的检测频率自动进行Wi-Fi连接状态检测。
- 用户可以随时按下Enter键手动触发Wi-Fi检测。

## 示例输出

程序运行时的示例输出如下：
```powershell
Starting Wi-Fi reconnection service. press Ctrl+C to exit.   
Wi-Fi is connected.  
Reconnection attempts: 0  
Run count: 1  
运行时间：16:00:00
```