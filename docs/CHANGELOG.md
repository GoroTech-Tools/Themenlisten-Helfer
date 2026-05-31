# Changelog

Alle relevanten Änderungen an diesem Projekt werden hier dokumentiert.

## [Unreleased]

_Keine Änderungen._

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

- Build-Skript aktualisiert Versionsnummern in `README.md`, `docs/ANWENDERDOKUMENTATION.md` und `docs/RELEASE_PROZESS.md` nun automatisch mit jedem Build.

### Updated (2.5.4)

- Dokumentation auf Stand 2.5.3 bereinigt (Ausgabepfad, EXE-Referenzen, RELEASE_PROZESS).

## [2.5.3] - 2026-05-18

### Fixed (2.5.3)

- Ausgabepfad vereinfacht: alle erzeugten Dateien landen jetzt ausschließlich im Ordner `Themenlisten/`; der bisherige Fallback auf `output/Themenlisten/` entfällt.
- Pylance-Fehler behoben: `sys._MEIPASS`-Attributzugriff abgesichert (`getattr` + `isinstance`-Guard), `resolve_path` gibt `Optional[str]` zurück, explizite `None`-Checks vor `os.makedirs` und `os.path.join`.

### Updated (2.5.3)

- MIT-Lizenz eingeführt; Copyright-Inhaber: Dr. Thomas Gorontzy (GoroTech).
- Anwenderdokumentation erweitert: Hinweise zur Vorlagenpflege (Kopf-/Fußzeilen, Platzhalter), E-Mail-Konfiguration im Tabellenblatt `E-Mail-Konfiguration`, sowie Hinweise zu den Tabellenblättern `Vorbereitung` und `Hilfstabellen`.

## [2.5.2] - 2026-05-18

### Fixed (2.5.2)

- PyInstaller-Build verwendet nun konsistent das vorgesehene 64-Bit-Python und installiert Abhängigkeiten aus `src/requirements.txt` (mit Root-Fallback) vor dem Build.
- Fehlende Laufzeit-Abhängigkeiten wie `Pillow` (`PIL`) und `python-docx` (`docx`) werden im Build- und Release-Prozess korrekt berücksichtigt.
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
- Vollständige Dokumentation für Anwender, Entwicklung und Release-Prozess.
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
