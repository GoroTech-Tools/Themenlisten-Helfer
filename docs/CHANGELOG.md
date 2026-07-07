# Changelog

Alle relevanten Änderungen an diesem Projekt werden hier dokumentiert.

## [1.0.5] - 2026-07-07

### Fixed (1.0.5)

- Robustere Filterung der zu verarbeitenden Datensätze: `Verarbeiten` wird jetzt fehlertolerant (`NaN`-sicher, trim + lowercase) ausgewertet.
- Outlook-Initialisierung in der E-Mail-Erstellung mit expliziter Fehlerbehandlung abgesichert; bei COM-Startfehlern erfolgt kontrollierter Abbruch mit Statusmeldung.
- COM-Lifecycle im Batch-Ablauf verbessert: `pythoncom.CoUninitialize()` wird im `finally`-Block ausgeführt.
- GitHub-Release-Notes-Generierung im Workflow korrigiert (keine fehlerhaften `` `r ``-Artefakte mehr im Markdown-Body).

### Changed (1.0.5)

- Kleine Codebereinigung in `src/ThemenlistenHelfer_GUI.py` (entfernte ungenutzte Imports, doppelte Dateinamenzuweisung entfernt).
- Erste Modularisierung umgesetzt: pure Hilfsfunktionen in neues Modul `src/core_utils.py` ausgelagert.
- Weitere Modularisierung umgesetzt: Excel-spezifische Logik nach `src/io_excel.py` und Mail-Hilfslogik nach `src/outlook_mailer.py` verschoben.
- `src/ThemenlistenHelfer_GUI.py` orchestriert nun stärker und enthält weniger Fachlogik.
- Word-Rendering wurde nach `src/docx_renderer.py` verschoben; Dateiname, Platzhalterdaten und Render-Pipeline sind dort gekapselt.
- Bereinigungslogik wurde nach `src/cleanup.py` verschoben; GUI nutzt zentrale Löschfunktion.
- Finale GUI-Struktur umgesetzt: Haupt-GUI und Ablaufsteuerung liegen jetzt in `src/gui.py`.
- `src/ThemenlistenHelfer_GUI.py` bleibt als schlanker Kompatibilitäts-Entrypoint erhalten und delegiert an `gui.main()`.
- Typisierung in `src/gui.py` nachgeschärft (typed callbacks, result-`TypedDict`s, präzisere Signaturen).
- Technik-Systemdiagramm auf modulare Architektur (`gui.py`, `io_excel.py`, `docx_renderer.py`, `outlook_mailer.py`, `cleanup.py`, `core_utils.py`) aktualisiert.
- Release-Dokumentation an Schwesterprojekt-Standard angeglichen (QA-Checkliste und Smoketest-Protokoll als Pflichtreferenzen im Release-Prozess).
- E-Mail-Body ergänzt bei vorhandenen Zusatzanhängen automatisch einen PS-Hinweis auf weitere Anlagen.

### Added (1.0.5)

- Unit-Tests für Kernlogik unter `tests/test_core_utils.py` ergänzt (Umlautersetzung, Vorlagenfindung, Filterung `Verarbeiten`).
- Zusätzliche Unit-Tests unter `tests/test_io_excel.py` und `tests/test_outlook_mailer.py` ergänzt.
- Weitere Unit-Tests unter `tests/test_docx_renderer.py` und `tests/test_cleanup.py` ergänzt.
- Neue Release-QA-Dokumente: `docs/RELEASE_QA_CHECKLISTE.md` und `docs/RELEASE_SMOKETEST_PROTOKOLL.md`.
- Release-Notes-Entwurf für die Zielversion `1.0.1`: `release/RELEASE_NOTES_v1.0.1.md`.
- Neuer, verbindlicher Ablauf in fester Reihenfolge: `docs/RELEASE_PROZESS.md`.
- E-Mail-Zusatzanhänge aus Excel-Konfiguration: optionale Spalten `Anhang1` bis `Anhang5` im Blatt `E-Mail-Konfiguration`.
- Zusatzanhang-Suche im Lernbereichspfad `data/Zusatzmaterialien/<<lernbereich>>` inkl. Unterordner.

## [1.0.0] - 2026-05-25

### Changed (1.0.0)

- Python-Abhängigkeiten auf `src/requirements.txt` standardisiert (Root-Datei entfällt).
- Neue `src`-Entrypoints eingeführt: `src/build.ps1`, `src/setup.ps1`.
- Root-Skripte `build.ps1` und `setup.ps1` als Kompatibilitäts-Entrypoints ergänzt.

## Historische interne Projektstände

Die folgenden Einträge dokumentieren frühere interne Entwicklungsstände vor dem ersten offiziellen GitHub-Release `1.0.0`.

## [2.6.0] - 2026-05-18

### Added (2.6.0)

- Noch keine neuen Features.

### Changed (2.6.0)

- Start neue Minor-Versionierung (2.6.x).

### Fixed (2.6.0)

- Keine Bugfixes in diesem Release.

## [2.5.4] - 2026-05-18

### Added (2.5.4)

- Build-Skript aktualisiert Versionsnummern in `README.md`, `docs/DOKUMENTATION_ANWENDER.md` und `docs/DOKUMENTATION_RELEASES.md` nun automatisch mit jedem Build.

### Updated (2.5.4)

- Dokumentation auf Stand 2.5.3 bereinigt (Ausgabepfad, EXE-Referenzen, RELEASE_PROZESS).

## [2.5.3] - 2026-05-18

### Fixed (2.5.3)

- Ausgabepfad vereinfacht: alle erzeugten Dateien landen jetzt ausschließlich im Ordner `Themenlisten/`; der bisherige Fallback auf `output/Themenlisten/` entfällt.
- Pylance-Fehler behoben: `sys._MEIPASS`-Attributzugriff abgesichert (`getattr` + `isinstance`-Guard), `resolve_path` gibt `Optional[str]` zurück, explizite `None`-Checks vor `os.makedirs` und `os.path.join`.

### Updated (2.5.3)

- MIT-Lizenz eingeführt; Copyright-Inhaber: GoroTech-Tools.
- Dokumentation Anwender erweitert: Hinweise zur Vorlagenpflege (Kopf-/Fußzeilen, Platzhalter), E-Mail-Konfiguration im Tabellenblatt `E-Mail-Konfiguration`, sowie Hinweise zu den Tabellenblättern `Vorbereitung` und `Hilfstabellen`.

## [2.5.2] - 2026-05-18

### Fixed (2.5.2)

- PyInstaller-Build verwendet nun konsistent das vorgesehene 64-Bit-Python und installiert Abhängigkeiten aus `src/requirements.txt` (mit Root-Fallback) vor dem Build.
- Fehlende Laufzeit-Abhängigkeiten wie `Pillow` (`PIL`) und `python-docx` (`docx`) werden im Build- und in der Dokumentation Releases korrekt berücksichtigt.
- Pfadauflösung für Onefile-Builds wurde robuster gemacht; Ressourcen werden nun zuverlässig aus `sys._MEIPASS` und dem EXE-Verzeichnis geladen.
- Abstürze durch `None`-Pfade bei Dateiprüfungen wurden abgefangen.
- Statusmeldungen der GUI melden Abbrüche und Teilerfolge jetzt präziser statt fälschlich pauschal Erfolg zu signalisieren.

### Updated (2.5.2)

- Vorlagensuche akzeptiert jetzt sowohl `.docx`- als auch `.dotm`-Vorlagen.
- Nicht eingefrorene Starts arbeiten wieder vom Projektstamm statt versehentlich relativ zu `src/`.
- Build-Artefakte für Version `2.5.2` wurden als EXE und ZIP unter `release/` neu erzeugt.

## [2.4.4] - 2026-05-17

### Added (2.4.4)

- Neue, GitHub-fähige Projektstruktur (`assets`, `config`, `data`, `docs`, `output`, `templates`, `.github`).
- Vollständige Dokumentation Anwender, Dokumentation Technik und Dokumentation Releases.
- GitHub-Standards (`.gitignore`, `.gitattributes`, Issue- und PR-Templates, CI-Workflow).
- `src/requirements.txt` für reproduzierbare Python-Umgebung.

### Changed (2.4.4)

- `src/ThemenlistenHelfer_GUI.py` unterstützt jetzt bevorzugt die neue Struktur mit Legacy-Fallback.
- `scripts/build_tlh.bat` verwendet neue Pfade inkl. Fallback-Logik.
- `ThemenlistenHelfer_GUI.spec` berücksichtigt neue Datenpfade.
- Altartefakte wurden physisch migriert: Root-Dateien liegen jetzt unter `assets/`, `data/` und `release/`.
- Einstiegspunkt und Build-Skript wurden aus dem Projektstamm nach `src/` bzw. `scripts/` verschoben.

## [2.4.3] - 2026-05-17

- Aktueller Ausgangsstand vor Struktur- und GitHub-Härtung.
