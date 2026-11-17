@echo off
rem Build all volumes of the Parametric Human series (or one volume).
rem Usage:
rem   build.bat              build every volume
rem   build.bat math         build one volume (intro / math / body / recon / face-hand / frontier)
rem   build.bat figures      redraw all figures
rem   build.bat list         list volumes
setlocal enabledelayedexpansion
chcp 936 >nul
cd /d "%~dp0"

set PY=
for %%P in (python.exe) do if not defined PY if exist "%%~$PATH:P" set PY=%%~$PATH:P
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
if not defined PY (
  echo [!] Python not found. Install Python 3.10+ and run again.
  pause
  exit /b 1
)

"%PY%" -c "import markdown, pymupdf, playwright, PIL" 2>nul
if errorlevel 1 (
  echo [*] Installing dependencies...
  "%PY%" -m pip install -r books\build\requirements.txt
  "%PY%" -m playwright install chromium
)

set TARGET=%1
if "%TARGET%"=="" goto all
if /i "%TARGET%"=="all" goto all
if /i "%TARGET%"=="list" goto list
if /i "%TARGET%"=="figures" goto figures
goto one

:list
"%PY%" books\build\build.py --list
goto end

:figures
for %%F in (intro math body recon face-hand frontier) do (
  for /d %%D in (books\%%F\code\ch*) do (
    if exist "%%D\*.py" (
      echo [*] figures: %%D
      "%PY%" "%%D\fig_*.py" 2>nul
    )
  )
)
goto end

:all
"%PY%" books\build\gen_appendix.py || goto err
"%PY%" books\build\build.py --all || goto err
goto end

:one
"%PY%" books\build\gen_appendix.py --book %TARGET% || goto err
"%PY%" books\build\build.py --book %TARGET% || goto err
goto end

:err
echo.
echo [!] Build failed. See the messages above.
pause
exit /b 1

:end
echo.
echo [OK] PDF files are in output\
pause
