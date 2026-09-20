@echo off
setlocal

REM Starter aus src: delegiert an das Build-Skript unter src\scripts
set "SCRIPT=%~dp0scripts\build_tlh.bat"

if not exist "%SCRIPT%" (
    echo [FEHLER] Build-Skript nicht gefunden: "%SCRIPT%"
    exit /b 1
)

call "%SCRIPT%"
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
    echo [FEHLER] Build fehlgeschlagen. Exit-Code: %RC%
    exit /b %RC%
)

echo Build erfolgreich abgeschlossen.
exit /b 0
