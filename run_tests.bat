REM config_env sets CA ADDR LIST and lets us use genie_python's CaChannelWrapper.
call C:\Instrument\Apps\EPICS\config_env.bat

REM Define working directories
set configs_dir=%~dp0\configs
set gui_dir=%~dp0\gui
set reports_dir=%~dp0\test-reports

REM Clone/pull necessary repositories
if exist %configs_dir% (
	cd %configs_dir%
	git reset HEAD --hard
	git clean -fdx
    git pull
	cd %~dp0
) else (
    git clone http://spudulike@control-svcs.isis.cclrc.ac.uk/gitroot/instconfigs/inst.git %configs_dir%
)

REM Clone/pull necessary repositories
if exist %gui_dir% (
	cd %gui_dir%
	git reset HEAD --hard
	git clean -fdx
    git pull
	cd %~dp0
) else (
    git clone https://github.com/ISISComputingGroup/ibex_gui.git %gui_dir%
)

python run_tests.py --configs_repo_path %configs_dir% --gui_repo_path %gui_dir% --reports_path %reports_dir% --instrument DEMO
if %errorlevel% neq 0 exit /b %errorlevel%
