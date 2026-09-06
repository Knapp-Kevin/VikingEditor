@echo off
setlocal EnableExtensions

cd /d "%~dp0"
if errorlevel 1 goto :working_directory_failed

if not exist "requirements.txt" goto :incomplete_source
if not exist "main.py" goto :incomplete_source

set "VENV_DIR=.wulfpack-forge-venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "REQUIREMENTS_STAMP=%VENV_DIR%\wulfpack-forge-requirements.txt"

if exist "%VENV_PYTHON%" goto :install_if_needed

call :find_python
if errorlevel 1 goto :python_missing

echo Creating Wulfpack Forge's private Python environment...
%PYTHON_COMMAND% -m venv "%VENV_DIR%"
if errorlevel 1 goto :setup_failed

:install_if_needed
if exist "%REQUIREMENTS_STAMP%" (
    fc /b "requirements.txt" "%REQUIREMENTS_STAMP%" >nul 2>&1
    if not errorlevel 1 goto :launch
)

echo Installing Wulfpack Forge dependencies...
echo The first run may take several minutes and requires an internet connection.
"%VENV_PYTHON%" -m pip install --disable-pip-version-check -r "requirements.txt"
if errorlevel 1 goto :setup_failed

copy /y "requirements.txt" "%REQUIREMENTS_STAMP%" >nul
if errorlevel 1 goto :setup_failed

:launch
echo Starting Wulfpack Forge...
"%VENV_PYTHON%" "main.py" %*
set "APP_EXIT_CODE=%ERRORLEVEL%"
if not "%APP_EXIT_CODE%"=="0" goto :application_failed
exit /b 0

:find_python
for %%V in (3.12 3.13 3.14 3.11 3.10) do (
    py -%%V -c "import sys" >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_COMMAND=py -%%V"
        exit /b 0
    )
)

where python >nul 2>&1
if errorlevel 1 exit /b 1

python -c "import sys; raise SystemExit(sys.version_info[:2] not in [(3,10),(3,11),(3,12),(3,13),(3,14)])" >nul 2>&1
if errorlevel 1 exit /b 1

set "PYTHON_COMMAND=python"
exit /b 0

:python_missing
echo.
echo Python 3.10 through 3.14 was not found.
echo Install 64-bit Python 3.12 from https://www.python.org/downloads/windows/
echo Keep the Python launcher selected during installation, then run this file again.
goto :failed

:incomplete_source
echo.
echo Wulfpack Forge's source files are missing.
echo Extract the complete source ZIP before running this file.
goto :failed

:working_directory_failed
echo.
echo Wulfpack Forge could not open its source folder.
goto :failed

:setup_failed
echo.
echo Wulfpack Forge setup failed. Check the message above and your internet connection.
goto :failed

:application_failed
echo.
echo Wulfpack Forge exited with code %APP_EXIT_CODE%.
goto :failed

:failed
echo.
pause
exit /b 1
