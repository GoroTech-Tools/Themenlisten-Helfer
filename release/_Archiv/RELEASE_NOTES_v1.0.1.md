# Release Notes v1.0.1

## Enthalten

- Modulare Architektur konsolidiert: `src/gui.py`, `src/core_utils.py`, `src/io_excel.py`, `src/outlook_mailer.py`, `src/docx_renderer.py`, `src/cleanup.py`.
- Stabilitätsverbesserungen in Kernpfaden (robustere Datensatzfilterung, Outlook-Fehlerbehandlung, COM-Cleanup).
- Ausbau der Testabdeckung auf zentrale Module.
- Aktualisierte Technik-/Diagramm-Dokumentation zur neuen Struktur.

## Qualitätssicherung

- Lokale Unit-Tests erfolgreich (`14` Tests, grün).
- Release-QA-Schema an Schwesterprojekte angeglichen:
  - `docs/RELEASE_QA_CHECKLISTE.md`
  - `docs/RELEASE_SMOKETEST_PROTOKOLL.md`

## Artefakte

- `dist/ThemenlistenHelfer_GUI.exe`
- `release/Themenlisten-Helfer_v1.0.1.zip`
- `release/RELEASE_NOTES_v1.0.1.md`

## Hinweise

- Empfohlenes Testartefakt: `dist/ThemenlistenHelfer_GUI.exe`
- GitHub Release sollte mit Tag `v1.0.1` erstellt werden (Tag/`src/version.txt` müssen übereinstimmen).
