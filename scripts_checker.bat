setlocal

REM Create local python environment from genie python on share
git clone https://github.com/ISISComputingGroup/ibex_utils.git
CALL ibex_utils\installation_and_upgrade\define_latest_genie_python.bat

%LATEST_PYTHON% -u scripts_checker.py

if %errorlevel% neq 0 (
    set errcode = %ERRORLEVEL%
    call ibex_utils\installation_and_upgrade\remove_genie_python.bat %LATEST_PYTHON_DIR%
    EXIT /b !errcode!
)

call ibex_utils\installation_and_upgrade\remove_genie_python.bat %LATEST_PYTHON_DIR%
