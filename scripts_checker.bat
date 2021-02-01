setlocal

call c:\Instrument\Apps\Python3\genie_python.bat scripts_checker.py
if %errorlevel% neq 0 exit /b %errorlevel%
pause