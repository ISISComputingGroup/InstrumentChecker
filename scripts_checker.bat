setlocal

REM Create local python environment from genie python on share
git clone https://github.com/ISISComputingGroup/ibex_utils.git
CALL ibex_utils\installation_and_upgrade\define_latest_genie_python.bat

%LATEST_PYTHON% scripts_checker.py
if %errorlevel% neq 0 exit /b %errorlevel%
