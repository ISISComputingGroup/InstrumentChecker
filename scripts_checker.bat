setlocal

powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/ISISComputingGroup/ibex_utils/refs/heads/try_uv/installation_and_upgrade/set_epics_ca_addr_list.bat " > "%TEMP%/set_epics_ca_addr_list.bat"
call "%TEMP%/set_epics_ca_addr_list.bat"

powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/ISISComputingGroup/ibex_utils/refs/heads/try_uv/installation_and_upgrade/install_or_update_uv.bat | cmd "

uv sync --python 3.12
call .venv\scripts\activate

python -u scripts_checker.py
