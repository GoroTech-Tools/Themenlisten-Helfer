@echo off
REM Versionsnummer aus version.txt lesen und hochzählen
setlocal enabledelayedexpansion

REM Immer vom Projektstamm aus arbeiten
cd /d "%~dp0\.."

REM Standardordner
set VERSION_FILE=src\version.txt
if not exist "!VERSION_FILE!" set VERSION_FILE=version.txt

set ICON_FILE=assets\icons\Themenlistenhelfer256.ico
if not exist "!ICON_FILE!" set ICON_FILE=Themenlistenhelfer256.ico

set EXCEL_FILE=data\Auswahl Teilnehmende zu Lernbereichen.xlsx
if not exist "!EXCEL_FILE!" set EXCEL_FILE=Auswahl Teilnehmende zu Lernbereichen.xlsx

set TEMPLATE_DIR=data\Themenlisten-Vorlagen
if not exist "!TEMPLATE_DIR!" set TEMPLATE_DIR=Themenlisten-Vorlagen

set RELEASE_DIR=release
if not exist "!RELEASE_DIR!" mkdir "!RELEASE_DIR!"

set /p VERSION=<"!VERSION_FILE!"

REM Versionsnummer splitten (z.B. 1.0.5)
for /f "tokens=1-3 delims=." %%a in ("!VERSION!") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)
REM Alte Versionsnummer merken (vor dem Inkrementieren)
set OLD_VERSION=!MAJOR!.!MINOR!.!PATCH!

REM Patch-Version um 1 erhöhen, dann ggf. MINOR und MAJOR hochzählen
set /a PATCH=PATCH+1
if !PATCH! gtr 9 (
    set PATCH=0
    set /a MINOR=MINOR+1
    if !MINOR! gtr 9 (
        set MINOR=0
        set /a MAJOR=MAJOR+1
    )
)
set NEWVERSION=!MAJOR!.!MINOR!.!PATCH!

REM Neue Versionsnummer in version.txt schreiben
(echo !NEWVERSION!) > "!VERSION_FILE!"

REM --- Versionsnummern in Dokumentation automatisch aktualisieren ---
echo Aktualisiere Dokumentation (!OLD_VERSION! -^> !NEWVERSION!)...
powershell -NoProfile -Command "$old='!OLD_VERSION!'; $new='!NEWVERSION!'; $enc=[Text.UTF8Encoding]::new($false); $files=@('README.md','docs\DOKUMENTATION_ANWENDER.md','docs\DOKUMENTATION_RELEASES.md'); foreach($f in $files){ if(Test-Path $f){ $fp=(Resolve-Path $f).Path; $c=[IO.File]::ReadAllText($fp,$enc); $u=$c.Replace($old,$new); if($c -ne $u){ [IO.File]::WriteAllText($fp,$u,$enc); Write-Host ('Aktualisiert: '+$f) } } }"
if errorlevel 1 (
    echo [WARNUNG] Dokumentations-Update fehlgeschlagen - Build wird fortgesetzt.
)

REM EXE-Namen mit Versionsnummer setzen
set EXENAME=Themenlisten-Helfer_!NEWVERSION!.exe

REM Vorherige EXE löschen
if exist dist\!EXENAME! del dist\!EXENAME!

REM Build mit PyInstaller (Interpreter robust aufloesen)
set PYTHON64=.venv\Scripts\python.exe
if exist "!PYTHON64!" (
    "!PYTHON64!" -c "import struct, sys; sys.exit(0 if struct.calcsize('P') * 8 == 64 else 1)" >nul 2>&1
    if errorlevel 1 set PYTHON64=
)
if not defined PYTHON64 set PYTHON64=C:\Users\tomgo\AppData\Local\Programs\Python\Python313\python.exe
if not exist "!PYTHON64!" set PYTHON64=C:\Users\thomas.gorontzy\AppData\Local\Programs\Python\Python313\python.exe
if not exist "!PYTHON64!" set PYTHON64=py

"!PYTHON64!" -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] Python nicht verfuegbar ueber .venv, festen Pfad oder py-Launcher.
    exit /b 1
)

"!PYTHON64!" -c "import struct, sys; sys.exit(0 if struct.calcsize('P') * 8 == 64 else 1)" >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] Es wird ein 64-Bit-Python fuer den Build benoetigt.
    exit /b 1
)

set REQUIREMENTS_FILE=src\requirements.txt
if not exist "!REQUIREMENTS_FILE!" set REQUIREMENTS_FILE=requirements.txt

REM Abhaengigkeiten fuer genau dieses Python installieren
if exist "!REQUIREMENTS_FILE!" (
    "!PYTHON64!" -m pip install -r "!REQUIREMENTS_FILE!"
    if errorlevel 1 (
        echo [FEHLER] Installation aus !REQUIREMENTS_FILE! fehlgeschlagen.
        exit /b 1
    )
) else (
    echo [WARNUNG] Keine requirements-Datei gefunden - fahre ohne automatische Abhaengigkeitsinstallation fort.
)

"!PYTHON64!" -m PyInstaller src\ThemenlistenHelfer_GUI.spec
if errorlevel 1 (
    echo [FEHLER] PyInstaller-Build fehlgeschlagen.
    exit /b 1
)

REM EXE umbenennen
set PYINSTALLER_EXE=dist\ThemenlistenHelfer.exe
if not exist "!PYINSTALLER_EXE!" (
    echo [FEHLER] PyInstaller-EXE nicht gefunden: !PYINSTALLER_EXE!
    exit /b 1
)
move /Y "!PYINSTALLER_EXE!" "dist\!EXENAME!"
if errorlevel 1 (
    echo [FEHLER] Versionierte EXE konnte nicht erstellt werden.
    exit /b 1
)

REM --- ältere Release-Artefakte archivieren ---
REM Erst nach erfolgreichem EXE-Build archivieren, damit ein Buildfehler
REM keine bereits vorhandenen Releases verschiebt.
set ARCHIVE_DIR=!RELEASE_DIR!\_Archiv
if not exist "!ARCHIVE_DIR!" mkdir "!ARCHIVE_DIR!"

for %%f in ("!RELEASE_DIR!\Themenlisten-Helfer_v*.zip") do if exist "%%~f" move /Y "%%~f" "!ARCHIVE_DIR!\" >nul
for /d %%d in ("!RELEASE_DIR!\Themenlisten-Helfer_v*") do if exist "%%~d" move /Y "%%~d" "!ARCHIVE_DIR!\" >nul
for %%f in ("!RELEASE_DIR!\RELEASE_NOTES_v*.md") do if exist "%%~f" move /Y "%%~f" "!ARCHIVE_DIR!\" >nul

REM --- Archivierung als ZIP mit Versionsnummer ---
set ZIPNAME=Themenlisten-Helfer_v!NEWVERSION!.zip
if exist "!RELEASE_DIR!\!ZIPNAME!" del "!RELEASE_DIR!\!ZIPNAME!"
powershell -Command "Compress-Archive -Path dist\!EXENAME!, 'data', 'README.md', 'docs' -DestinationPath '!RELEASE_DIR!\!ZIPNAME!'"
if errorlevel 1 (
    echo [FEHLER] ZIP-Archiv konnte nicht erstellt werden.
    exit /b 1
)

echo Archiv erstellt: !RELEASE_DIR!\!ZIPNAME!

REM --- Release Notes fuer dieses Release erzeugen ---
set NOTESNAME=RELEASE_NOTES_v!NEWVERSION!.md
set NOTESFILE=!RELEASE_DIR!\!NOTESNAME!
> "!NOTESFILE!" echo # Release Notes v!NEWVERSION!
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo ## Download
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo - [Release-Seite v!NEWVERSION!](https://github.com/GoroTech-Tools/Themenlisten-Helfer/releases/tag/v!NEWVERSION!)
>> "!NOTESFILE!" echo - [ZIP direkt herunterladen](https://github.com/GoroTech-Tools/Themenlisten-Helfer/releases/download/v!NEWVERSION!/!ZIPNAME!)
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo ## Enthalten
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo - Themenlisten-Helfer im Versionsstand `!NEWVERSION!`.
>> "!NOTESFILE!" echo - Release-Artefakte im Schema `dist\ThemenlistenHelfer.exe`, `Themenlisten-Helfer_vX.Y.Z.zip` und `RELEASE_NOTES_vX.Y.Z.md`.
>> "!NOTESFILE!" echo - Dokumentation unter `docs/` sowie ergaenzende GitHub Release Notes im Release-Eintrag.
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo ## Artefakte
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo - `dist\ThemenlistenHelfer.exe`
>> "!NOTESFILE!" echo - `release/!ZIPNAME!`
>> "!NOTESFILE!" echo - `release/!NOTESNAME!`
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo ## Hinweise
>> "!NOTESFILE!" echo.
>> "!NOTESFILE!" echo - Empfohlenes Testartefakt: `dist\ThemenlistenHelfer.exe`
>> "!NOTESFILE!" echo - Vollstaendiger Commit-Verlauf: `https://github.com/GoroTech-Tools/Themenlisten-Helfer/commits/v!NEWVERSION!`

echo Release Notes erstellt: !NOTESFILE!


REM Nur die letzten 3 Builds im dist-Verzeichnis behalten
pushd dist
for /f "skip=3" %%f in ('dir /b /o-d Themenlisten-Helfer_*.exe') do del "%%f"
popd

REM Bereits vorhandene EXEs im Release-Verzeichnis löschen
for %%f in ("!RELEASE_DIR!\Themenlisten-Helfer_*.exe") do del "%%~f"

echo Build abgeschlossen: dist\!EXENAME! und !RELEASE_DIR!\!ZIPNAME! (+ Release Notes)
if /I "!NO_PAUSE!"=="1" goto :eof
if defined CI goto :eof
pause
