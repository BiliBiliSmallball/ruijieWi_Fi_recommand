@echo off
:start
python .\main.py
timeout /t 10
goto start
