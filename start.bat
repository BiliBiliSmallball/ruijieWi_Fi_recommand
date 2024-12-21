@echo off
if not exist "wifi_reconnect_log.txt" (
    echo. > "wifi_reconnect_log.txt"
)
if not exist "err_log.txt" (
    echo. > "err_log.txt"
)
:start
python .\main.py
timeout /t 10
goto start
