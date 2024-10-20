@echo off
:: Request administrator privileges
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    powershell start-process -FilePath '%0' -Verb runAs
    exit /b
)

:START
echo Running monitor.py...
:: Run the Python monitor script
python "C:\imageGrabber\monitor.py"
if %errorlevel% neq 0 (
    echo monitor.py exited with error code %errorlevel%.
    echo Restarting monitor.py in 5 seconds...
    timeout /t 5
    goto START
)

:: Optional exit message
echo monitor.py closed successfully.
