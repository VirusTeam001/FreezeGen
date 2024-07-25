@echo off
echo Installing required Python packages...
echo.

REM
set PACKAGES=Pillow qrcode faker ipaddress

REM
for %%i in (%PACKAGES%) do (
    pip show %%i > nul 2>&1
    if errorlevel 1 (
        echo Installing %%i...
        pip install %%i
    ) else (
        echo %%i is already installed.
    )
)

echo.
echo Installation complete.
pause
