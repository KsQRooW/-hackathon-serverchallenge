@echo off
echo Check and install requirements.txt
call pip install -r requirements.txt
echo Start main.py
call python main.py 2>nul
pause