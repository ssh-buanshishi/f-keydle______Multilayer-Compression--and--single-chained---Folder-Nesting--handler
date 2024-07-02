@echo off
rem --include-plugin-directory=xxx,yyy,zzz,xxx\111,yyy\222 ^ 自己要编进去的库

call python -m nuitka --mingw64 --standalone --show-progress --remove-output ^
--windows-icon-from-ico="./icon-console.ico" ^
--output-dir="." ^
"extracter.py"

pause
