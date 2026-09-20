# Themenlisten-Helfer

Portable Windows-Anwendung zur automatisierten Erstellung von Themenlisten (Word) und E-Mail-Entwürfen (Outlook) auf Basis einer Excel-Datei.

Das Projekt dient als Arbeitserleichterung für die Begleitung der kaufmännischen Qualifizierung von Personen im BFW Weser-Ems.

## Projektstatus

- Status: **Fertig / abgeschlossen**
- Das Projekt wird im Wartungsmodus geführt.
- Änderungswünsche und Erweiterungen bitte ausschließlich über GitHub formulieren:
   - Fehler: GitHub Issue „Bug Report"
   - Verbesserungen: GitHub Issue „Feature Request"

## Aktueller Stand

- Aktuelle Release-Version: siehe `src/version.txt` und GitHub Releases.
- Empfohlenes Artefakt für Tests und Verteilung: aktuelle Release-Artefakte gemäß Schema `Themenlisten-Helfer_v<version>.zip` bzw. die EXE aus `dist/`.
- Word-Vorlagen werden in den Formaten `.docx` und `.dotm` unterstützt.
- Onefile-Builds laden eingebettete Ressourcen robust aus dem Bundle und verwenden das EXE-Verzeichnis für laufzeitnahe Dateien.

## Ziele des Projekts

- einfache Bedienung über GUI
- reproduzierbarer Build als EXE
- klare Trennung von Quellcode, Daten, Assets und Ausgabe
- wartbar und kollaborativ über GitHub

## Empfohlene Verzeichnisstruktur

```text
Themenlisten-Helfer/
├── .github/                      # Workflows, Issue-/PR-Templates
├── data/                         # Eingabedateien und Vorlagen
│   ├── Auswahl Teilnehmende zu Lernbereichen.xlsx
│   └── Themenlisten-Vorlagen/
├── docs/                         # fachliche Dokumentation und Standards
├── release/                      # veröffentlichte EXE/ZIP-Artefakte
├── src/                          # Anwendungsquellcode
│   ├── assets/                   # Icons und GUI-Bilder
│   ├── scripts/                  # Build-/Release-Skript
│   ├── ThemenlistenHelfer_GUI.py # aktueller Einstiegspunkt
│   ├── ThemenlistenHelfer_GUI.spec # PyInstaller-Spec
│   ├── build.ps1                 # Build-Entrypoint
│   ├── setup.ps1                 # Setup-Entrypoint
│   ├── requirements.txt          # Python-Abhängigkeiten
│   ├── tests/                    # Unit-Tests für die Quellmodule
│   └── version.txt               # semantische Version
├── build.ps1                     # Kompatibilitäts-Entrypoint
├── setup.ps1                     # Kompatibilitäts-Entrypoint
└── README.md
```

## Schnellstart

1. Python-Umgebung einrichten.
2. Abhängigkeiten installieren (`src/requirements.txt`, empfohlen via `src/setup.ps1`).
3. Eingabedatei nach `data/Auswahl Teilnehmende zu Lernbereichen.xlsx` legen.
4. Vorlagen in `data/Themenlisten-Vorlagen/` bereitstellen.
5. App starten über `src/ThemenlistenHelfer_GUI.py` oder EXE verwenden.

### Hinweise zu Vorlagen

- Bevorzugtes Suchmuster: `Themenliste_<Lernbereich>*`
- Unterstützte Dateitypen: `.docx`, `.dotm`
- Bei mehreren passenden Vorlagen wird die erste gültige Datei verwendet.

## Build

Der Build läuft über `src/scripts/build_tlh.bat` und erzeugt:

- EXE in `dist/`
- ZIP-Artefakte in `release/`
- automatische Versionserhöhung in `src/version.txt`

Historische versionsspezifische Änderungen sind im `docs/CHANGELOG.md` dokumentiert.

Optionaler Komfortaufruf aus `src`: `src/build.bat` (delegiert intern an `src/scripts/build_tlh.bat`).

Für einen lokalen Build `src/build.bat` oder direkt `src/scripts/build_tlh.bat` ausführen.

## GitHub Release-Automation

- Workflow: `.github/workflows/release.yml`
- Trigger: Push eines Tags im Format `v*` (z. B. `v2.4.5`)
- Ergebnis: Build auf `windows-latest`, automatische Release-Notes-Datei unter `release/RELEASE_NOTES_v<version>.md` sowie Upload von EXE, ZIP und Release Notes als Release-Assets
- Release-Titel-Schema: `Themenlisten-Helfer v...` (z. B. `Themenlisten-Helfer vX.Y.Z`)
- Guard: Bei Tag-Builds muss `src/version.txt` exakt zur Tag-Version passen (z. B. `vX.Y.Z` ↔ `X.Y.Z`), sonst bricht der Workflow mit Fehler ab
- Guard: Tags müssen semantisch formatiert sein: `vMAJOR.MINOR.PATCH` (z. B. `vX.Y.Z`)
- Guardrail: Falls ein Release versehentlich mit Titelmuster `Release v...` erstellt wurde, normalisiert der Workflow den Titel automatisch auf das Produktschema.

Für das aktuelle Release gilt daher: Git-Stand committen, sicherstellen, dass `src/version.txt` auf die gewünschte Version steht, dann den entsprechenden Tag pushen (z. B. `vX.Y.Z`).

### Release-Workflow testen

1. `src/version.txt` auf eine Testversion setzen (z. B. `X.Y.Z`).
2. Test-Tag erstellen und pushen:
   - `git tag vX.Y.Z`
   - `git push origin vX.Y.Z`
3. In GitHub prüfen:
   - Workflow-Lauf unter **Actions**
   - neues Release mit EXE/ZIP unter **Releases**
4. Optional aufräumen (nur bei Test-Tag):
   - `git tag -d vX.Y.Z`
   - `git push origin :refs/tags/vX.Y.Z`

## Migration (Mai 2026)

Folgende Altdateien wurden in die neue Struktur verschoben:

- Icons → `src/assets/icons/`
- GUI-Bild → `src/assets/images/`
- Eingabe-Excel → `data/`
- veröffentlichte EXE/ZIP → `release/`

## Dokumentation

Diese `README.md` im Projektwurzelverzeichnis ist die zentrale Einstiegsdokumentation.

- Benutzer: `docs/DOKUMENTATION_ANWENDER.md`
- Entwicklung: `docs/DOKUMENTATION_TECHNIK.md`
- Release: `docs/DOKUMENTATION_RELEASES.md`
- Diagramme: `docs/DOKUMENTATION_DIAGRAMME.md`
- Änderungen: `docs/CHANGELOG.md`
- Beitrag: `docs/CONTRIBUTING.md`
- Verhaltenskodex: `docs/CODE_OF_CONDUCT.md`
- Lizenz: `docs/LICENSE`

## Markdown-Regel (verbindlich)

Für Markdown-Dateien gelten projektweit die Regeln aus `.markdownlint.json` (aktuell `MD022` und `MD032`).

## Lizenz

MIT License – Copyright (c) 2026 GoroTech-Tools.
Siehe [LICENSE](docs/LICENSE) für den vollständigen Lizenztext.
