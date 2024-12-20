@echo off
:start
python .\main.py >> wifi_reconnect_log.txt 2>&1
timeout /t 10
goto start
