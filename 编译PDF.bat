@echo off
"%SystemRoot%\System32\chcp.com" 936 >nul
setlocal EnableExtensions
cd /d "%~dp0"
title 人体参数化技术 - 一键编译 PDF

echo ============================================
echo    人体参数化技术  -  一键编译 PDF
echo ============================================
echo.

set "PY="
set "PYARG="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if not defined PY (
    "%SystemRoot%\System32\where.exe" py >nul 2>nul
    if not errorlevel 1 (
        set "PY=py"
        set "PYARG=-3"
    )
)
if not defined PY (
    "%SystemRoot%\System32\where.exe" python >nul 2>nul
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    echo [错误] 没有找到 Python 3。
    echo        请安装 Python 3.12，安装时勾选 "Add python.exe to PATH"。
    pause
    exit /b 1
)
echo 使用 Python: %PY% %PYARG%
echo.

"%PY%" %PYARG% -c "import markdown, playwright, pymupdf, numpy, matplotlib, scipy, PIL" >nul 2>nul
if errorlevel 1 (
    echo [1/4] 缺少依赖，正在安装（首次需要联网）...
    "%PY%" %PYARG% -m pip install -r "book\build\requirements.txt"
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请检查网络后重试。
        pause
        exit /b 1
    )
) else (
    echo [1/4] 依赖检查通过。
)

echo [2/4] 生成附录 C/D 与引用编号 ...
"%PY%" %PYARG% "book\build\gen_appendix.py"
if errorlevel 1 goto fail

if not exist "book\images\cover\cover_front.jpg" (
    echo [3/4] 生成封面与封底 ...
    "%PY%" %PYARG% "book\build\make_covers.py"
    if errorlevel 1 goto fail
) else (
    echo [3/4] 封面已存在，跳过。
)

echo [4/4] 构建 PDF（约 4-6 分钟，请耐心等待）...
echo.
"%PY%" %PYARG% "book\build\build_book.py"
if errorlevel 1 goto fail

echo.
echo ============================================
if exist "output\parametric-human-models-new.pdf" (
    echo 原 PDF 正被阅读器占用，新文件已生成：
    echo    output\parametric-human-models-new.pdf
    echo 关闭阅读器后，用它覆盖旧的 parametric-human-models.pdf 即可。
    start "" "output\parametric-human-models-new.pdf"
) else (
    echo 完成！output\parametric-human-models.pdf
    start "" "output\parametric-human-models.pdf"
)
echo ============================================
echo.
pause
exit /b 0

:fail
echo.
echo [错误] 构建失败，请把上面的报错信息发给维护者。
echo.
pause
exit /b 1
