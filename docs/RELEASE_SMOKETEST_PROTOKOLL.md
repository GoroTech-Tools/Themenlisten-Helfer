# Release-Smoketest-Protokoll

## Metadaten

- Version: `1.0.1`
- Datum: `2026-06-05`
- Tester/in: GitHub Copilot (Assistenz, CI-/Release-Verifikation)
- Testumgebung (Windows/Office-Version): GitHub Actions `windows-latest` (lokale Office-Validierung ausstehend)
- Testartefakt (Pfad): `dist/ThemenlistenHelfer_GUI.exe`

## 1) Automatisierte Kernprüfung

- Tests ausgeführt: Ja
- Ergebnis: `14/14` Tests grün (`python -m unittest discover -s tests -p "test_*.py"`)
- Auffälligkeiten: keine

## 2) Smoke-Test Ergebnisse

- GUI-Start: N/A (lokaler manueller EXE-Starttest nachzureichen)
- Excel-Laden: N/A (lokaler manueller Test nachzureichen)
- Themenlisten-Erstellung: N/A (lokaler manueller Test nachzureichen)
- Outlook-Entwurf: N/A (lokaler manueller Test nachzureichen)
- Platzhalterersetzung: N/A (lokaler manueller Test nachzureichen)
- Bereinigung alter Dateien: N/A (lokaler manueller Test nachzureichen)

Details / Abweichungen:

- CI-Release-Workflow erfolgreich: `https://github.com/TomGorontzy/Themenlisten-Helfer/actions/runs/27027207899`
- GitHub-Release veröffentlicht: `https://github.com/TomGorontzy/Themenlisten-Helfer/releases/tag/v1.0.1`

## 3) Post-Release-Verifikation

- ZIP vorhanden: Ja (`Themenlisten-Helfer_v1.0.1.zip`, 49.009.219 Bytes)
- ZIP entpackbar: N/A (lokale Verifikation ausstehend)
- Pflichtinhalte vollständig: N/A (lokale Verifikation ausstehend)
- EXE-Starttest erfolgreich: N/A (lokale Verifikation ausstehend)
- SHA256 dokumentiert: Nein (ausstehend)

## 4) Offene Punkte / Risiken

- Lokaler Smoke-Test der EXE inkl. Office-Interaktion (Word/Outlook) steht noch aus.
- SHA256 für Release-ZIP und EXE ist noch nicht dokumentiert.

## 5) Freigabe

- Freigabe erteilt: Ja (technische CI-/Release-Freigabe)
- Begründung: Workflow `Release` erfolgreich, Release `v1.0.1` veröffentlicht, Pflichtassets vorhanden (`RELEASE_NOTES_v1.0.1.md`, `Themenlisten-Helfer_v1.0.1.zip`, `ThemenlistenHelfer_GUI.exe`). Fachlicher lokaler Smoke-Test wird nachgezogen.
