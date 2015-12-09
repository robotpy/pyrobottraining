@echo off

setlocal

if "%1" == "" echo Usage: run_single.bat TEST_NUMBER
if "%1" == "" goto end

cd %~dp0
set TESTNAME=test_challenges.py::test_%1

for /f "tokens=1,* delims= " %%a in ("%*") do set ALL_BUT_FIRST=%%b

py -3 robot.py test -- -l %ALL_BUT_FIRST% %TESTNAME%

:end

endlocal
