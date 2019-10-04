setlocal

REM Define working directories
set configs_dir=%~dp0\configs
set gui_dir=%~dp0\gui
set reports_dir=%~dp0\test-reports

REM Clone necessary repositories
REM Do this here rather than in python because it will make git authentication dialogs visible rather than being in a python thread.
if not exist "%configs_dir%" (
    git clone http://spudulike@control-svcs.isis.cclrc.ac.uk/gitroot/instconfigs/inst.git "%configs_dir%"
)

if not exist "%gui_dir%" (
    git clone https://github.com/ISISComputingGroup/ibex_gui.git "%gui_dir%"
)

call c:\Instrument\Apps\Python\genie_python.bat run_tests.py --configs_repo_path "%configs_dir%" --gui_repo_path "%gui_dir%" --reports_path "%reports_dir%" --instruments DEMO
if %errorlevel% neq 0 exit /b %errorlevel%
