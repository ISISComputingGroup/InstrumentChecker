# EPICS-configchecker

To run tests for all instruments use:

```
run_tests.bat
```

To find which instruments use a specific IOC, use:

```
get_ioc_usage.bat --ioc TPG300
```

To check the scripts of all instruments set the `USER` and `PASS` environment variables to have credentials that are able to connect remotely to instruments then use:

```
scripts_checker.py
```
