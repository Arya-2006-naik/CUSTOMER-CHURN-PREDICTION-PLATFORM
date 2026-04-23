@echo off
setlocal
cd /d "%~dp0"
echo Starting Customer Churn Prediction Platform...
echo.

echo Checking port 8000 availability...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /R /C:":8000 .*LISTENING"') do set "PID_8000=%%a"
if defined PID_8000 (
    echo ERROR: Port 8000 is already in use by process %%PID_8000%%.
    echo Close that process or stop the existing backend before running this script.
    pause
    exit /b 1
)

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d "%~dp0backend" && python main.py"

echo Waiting for backend to listen on port 8000...
set /a counter=0
:wait_backend
powershell -NoProfile -Command "$tcp = New-Object System.Net.Sockets.TcpClient; try { $async = $tcp.BeginConnect('127.0.0.1',8000,$null,$null); Start-Sleep -Milliseconds 200; if ($async.AsyncWaitHandle.WaitOne(0)) { $tcp.Close(); exit 0 } else { exit 1 } } catch { exit 1 }"
if %ERRORLEVEL%==0 (
    echo Backend is ready.
) else (
    if %counter% geq 15 (
        echo Backend did not start within 15 seconds.
        echo Please check the Backend Server window for errors.
        goto start_frontend
    )
    timeout /t 1 /nobreak >nul
    set /a counter+=1
    goto wait_backend
)

:start_frontend
echo Starting Frontend...
start "Frontend" cmd /k "cd /d "%~dp0frontend" && python -m http.server 3000"

echo Waiting for frontend to listen on port 3000...
set /a counter=0
:wait_frontend
powershell -NoProfile -Command "$tcp = New-Object System.Net.Sockets.TcpClient; try { $async = $tcp.BeginConnect('127.0.0.1',3000,$null,$null); Start-Sleep -Milliseconds 200; if ($async.AsyncWaitHandle.WaitOne(0)) { $tcp.Close(); exit 0 } else { exit 1 } } catch { exit 1 }"
if %ERRORLEVEL%==0 (
    echo Frontend is ready.
    goto open_browser
) else (
    if %counter% geq 15 (
        echo Frontend did not start within 15 seconds.
        echo Please check the Frontend window for errors.
        goto open_browser
    )
    timeout /t 1 /nobreak >nul
    set /a counter+=1
    goto wait_frontend
)

:open_browser
echo.
echo Backend is expected at: http://127.0.0.1:8000
echo Frontend is expected at: http://127.0.0.1:3000
echo.
echo Opening the application in your default browser...
start http://127.0.0.1:3000

echo Both servers have been launched. Close this window to stop this script.
pause
