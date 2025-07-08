setlocal

REM Define working directories
set "configs_dir=%~dp0configs"
set "gui_dir=%~dp0gui"
set "reports_dir=%~dp0test-reports"

REM Clone necessary repositories
REM Do this here rather than in python because it will make git authentication dialogs visible rather than being in a python thread.
if not exist "%configs_dir%" (
    git clone http://spudulike@control-svcs.isis.cclrc.ac.uk/gitroot/instconfigs/inst.git "%configs_dir%"
)

if not exist "%gui_dir%" (
    git clone https://github.com/ISISComputingGroup/ibex_gui.git "%gui_dir%"
)

if exist "%reports_dir%" (
    rd /s /q "%reports_dir%"
)

powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/ISISComputingGroup/ibex_utils/refs/heads/try_uv/installation_and_upgrade/set_epics_ca_addr_list.bat " > "%TEMP%/set_epics_ca_addr_list.bat"
call "%TEMP%/set_epics_ca_addr_list.bat"

powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/ISISComputingGroup/ibex_utils/refs/heads/try_uv/installation_and_upgrade/install_or_update_uv.bat | cmd "

uv sync --python 3.12
call .venv\scripts\activate

REM this is a hack to enable a CA context per thread
set "EPICS_CAS_INTF_ADDR_LIST=127.0.0.1"
python run_tests.py --configs_repo_path "%configs_dir%" --gui_repo_path "%gui_dir%" --reports_path "%reports_dir%"
if %errorlevel% neq 0 (
    @echo ERROR: python exited with code %errorlevel%
    exit /b %errorlevel%
)
