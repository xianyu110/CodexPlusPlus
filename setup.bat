@echo off
setlocal EnableExtensions
chcp 65001 >nul

cd /d "%~dp0" || (
    echo Failed to enter script directory.
    pause
    exit /b 1
)

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"

set "VENV_DIR=%ROOT_DIR%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

:menu
cls
echo ========================================
echo              Codex++ Setup
echo ========================================
echo.
echo Project directory:
echo %ROOT_DIR%
echo.
echo [1] Install Codex++
echo [2] Uninstall Codex++
echo [3] Update Codex++
echo [4] Recreate venv only
echo [5] Exit
echo.
set /p choice=Please select an option [1-5]:

if "%choice%"=="1" goto install
if "%choice%"=="2" goto uninstall
if "%choice%"=="3" goto update
if "%choice%"=="4" goto recreate_venv
if "%choice%"=="5" goto end

echo.
echo Invalid choice.
pause
goto menu


:install
echo.
call :ensure_venv
if errorlevel 1 goto error

echo.
echo Installing Codex++ into venv...
"%VENV_PY%" -m pip install -e .
if errorlevel 1 goto error

echo.
echo Installing Codex++ shortcut and uninstall entry...
"%VENV_PY%" -m codex_session_delete setup
if errorlevel 1 goto error

echo.
echo Codex++ installed successfully.
echo You can launch it from the Codex++ desktop shortcut.
pause
goto end


:uninstall
echo.
if exist "%VENV_PY%" (
    echo Using venv Python:
    echo %VENV_PY%
    echo.
    echo Uninstalling Codex++ shortcut and uninstall entry...
    "%VENV_PY%" -m codex_session_delete remove
    if errorlevel 1 goto error
) else (
    echo Codex++ venv not found, falling back to system Python.
    call :detect_python
    if errorlevel 1 goto error

    echo.
    echo Uninstalling Codex++ shortcut and uninstall entry...
    %PY_CMD% -m codex_session_delete remove
    if errorlevel 1 goto error
)

echo.
echo Codex++ uninstalled successfully.
pause
goto end


:update
echo.
call :ensure_venv
if errorlevel 1 goto error

echo.
echo Updating Codex++ from GitHub Release...
"%VENV_PY%" -m codex_session_delete update
if errorlevel 1 goto error

echo.
echo Codex++ update finished.
pause
goto end


:recreate_venv
echo.
call :recreate_venv_func
if errorlevel 1 goto error

echo.
echo Venv recreated successfully.
pause
goto menu


:ensure_venv
if exist "%VENV_PY%" (
    echo Found existing venv Python:
    echo %VENV_PY%
    exit /b 0
)

call :recreate_venv_func
exit /b %errorlevel%


:recreate_venv_func
echo.
echo Checking Python...

call :detect_python
if errorlevel 1 (
    echo.
    echo Python was not found.
    echo Please install Python 3.11+ from python.org.
    echo During installation, check:
    echo   Add python.exe to PATH
    echo   pip
    echo   venv
    exit /b 1
)

echo.
echo Using Python command:
echo %PY_CMD%

echo.
%PY_CMD% --version
if errorlevel 1 exit /b 1

%PY_CMD% -c "import sys; print(sys.executable)"
if errorlevel 1 exit /b 1

echo.
if exist "%VENV_DIR%" (
    echo Removing broken or old venv:
    echo %VENV_DIR%
    rmdir /s /q "%VENV_DIR%"
    if exist "%VENV_DIR%" (
        echo Failed to remove old venv.
        echo Please close programs that may be using it and try again.
        exit /b 1
    )
)

echo.
echo Creating Python virtual environment at:
echo %VENV_DIR%

%PY_CMD% -m venv --copies "%VENV_DIR%"
if errorlevel 1 (
    echo.
    echo Failed to create venv.
    echo Make sure Python 3.11+ is installed correctly.
    exit /b 1
)

if not exist "%VENV_PY%" (
    echo.
    echo Venv was created, but this file was not found:
    echo %VENV_PY%
    echo.
    echo This usually means Python installation is broken or Windows Store alias is interfering.
    echo.
    echo Please run these commands manually and check the output:
    echo   where python
    echo   python --version
    echo   py -0p
    echo.
    echo If where python shows WindowsApps, disable Python aliases:
    echo Settings ^> Apps ^> Advanced app settings ^> App execution aliases
    echo Then turn off python.exe and python3.exe.
    exit /b 1
)

echo.
echo Venv Python found:
echo %VENV_PY%

echo.
echo Bootstrapping pip...
"%VENV_PY%" -m ensurepip --upgrade
if errorlevel 1 (
    echo.
    echo ensurepip failed.
    exit /b 1
)

echo.
echo Upgrading pip / setuptools / wheel inside venv...
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo.
    echo Failed to upgrade pip / setuptools / wheel.
    exit /b 1
)

exit /b 0


:detect_python
set "PY_CMD="

py -3 --version >nul 2>nul
if not errorlevel 1 (
    set "PY_CMD=py -3"
    exit /b 0
)

python --version >nul 2>nul
if not errorlevel 1 (
    set "PY_CMD=python"
    exit /b 0
)

exit /b 1


:error
echo.
echo Operation failed. Please check the error output above.
pause
exit /b 1


:end
endlocal
exit /b 0
