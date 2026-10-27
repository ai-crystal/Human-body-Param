@echo off
chcp 65001 >nul
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================
echo   人体参数化技术  -  一键重建 PDF
echo ============================================
echo.

set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY="

if not defined PY (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PY=py"
        set "PYARG=-3"
    )
)
if not defined PY (
    where python >nul 2>nul
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    echo [错误] 未找到 Python 3，请安装 Python 3.12 并勾选 "Add python.exe to PATH"。
    pause
    exit /b 1
)

echo [1/3] 检查依赖 ...
"%PY%" %PYARG% -c "import markdown, playwright, pymupdf, numpy, matplotlib, scipy, PIL" >nul 2>nul
if errorlevel 1 (
    echo       缺少依赖，正在安装 ...
    "%PY%" %PYARG% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败。
        pause
        exit /b 1
    )
)

echo [2/3] 生成附录 C / D 的表格与引用编号 ...
"%PY%" %PYARG% gen_appendix.py
if errorlevel 1 goto fail

if not exist "..\images\cover\cover_front.jpg" (
    echo       封面缺失，重新生成 ...
    "%PY%" %PYARG% make_covers.py
)

echo [3/3] 构建 PDF（图片压缩 + 两遍排版 + 书签 + 字体子集化）...
"%PY%" %PYARG% build_book.py
if errorlevel 1 goto fail

echo.
echo 完成：..\..\output\parametric-human-models.pdf
start "" "..\..\output\parametric-human-models.pdf"
pause
exit /b 0

:fail
echo.
echo [错误] 构建失败，请查看上面的输出。
pause
exit /b 1
