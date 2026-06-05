# Release Notes v1.0.2

## Enthalten

- Erweiterung der E-Mail-Funktion um optionale Zusatzanhänge aus der Excel-Konfiguration (`Anhang1` bis `Anhang5`).
- Rekursive Suche von Zusatzanhängen im Lernbereichspfad `data/Zusatzmaterialien/<<lernbereich>>`.
- Anlegen der Lernbereichs-Unterordner unter `data/Zusatzmaterialien/`.
- Aktualisierte Anwenderdokumentation zur Pflege zusätzlicher E-Mail-Anhänge.

## Qualitätssicherung

- Unit-Tests erfolgreich ausgeführt (`16` Tests, grün).
- Release-Workflow ist tag-basiert (`v1.0.2`) mit Versions-Guard gegen `src/version.txt`.

## Artefakte

- `dist/ThemenlistenHelfer_GUI.exe`
- `release/Themenlisten-Helfer_v1.0.2.zip`
- `release/RELEASE_NOTES_v1.0.2.md`

## Hinweise

- Empfohlenes Testartefakt: `dist/ThemenlistenHelfer_GUI.exe`
- Zusatzanhänge sind optional; fehlende Dateien werden als Warnung protokolliert, die Entwurfserstellung läuft weiter.
