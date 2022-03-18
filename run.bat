@echo off
set current_path=%~dp0
echo %current_path%
pip install -r requirements.txt
python main.py
pause