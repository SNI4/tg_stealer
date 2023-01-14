echo off

pyinstaller -F -w CCleaner.py -i default.ico


rmdir /s /q __pycache__
rmdir /s /q build

:cmd
pause null