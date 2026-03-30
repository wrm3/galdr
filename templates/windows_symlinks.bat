@echo off

REM === Shared template root ===
REM Set this to the path where you cloned galdr
set SHARED=%~dp0

REM === Current project folder (folder this script is in) ===
set PROJECT=%~dp0

echo.
echo Project folder detected as:
echo %PROJECT%
echo.

echo Updating junction links...

call :relink ".agent"
call :relink ".claude"
call :relink ".codex"
call :relink ".cursor"
call :relink ".opencode"
call :relink ".platforms"
call :relink ".galdr_template"

echo.
echo Done.
pause
exit /b

:relink
set LINK=%PROJECT%%~1
set TARGET=%SHARED%\%~1

echo.
echo Processing %~1

if exist "%LINK%" (
    echo Removing existing link...
    rmdir "%LINK%"
)

echo Creating junction...
mklink /J "%LINK%" "%TARGET%"

exit /b