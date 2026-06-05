# Release-QA-Checkliste

## Ziel

Kurzer, reproduzierbarer Pflichtdurchlauf vor jedem Release (analog Schwesterprojekte).

## 1) Automatisierte Kernprüfung

- Unit-Tests ausführen (`python -m unittest discover -s tests -p "test_*.py"`)
- Erwartung: alle Tests grün
- Optional: Build-Skript ohne Fehler durchlaufbar (`scripts/build_tlh.bat`)

## 2) Smoke-Test (fachlicher Ablauf)

1. Anwendung starten (`src/ThemenlistenHelfer_GUI.py` bzw. EXE)
2. Excel-Datei öffnen und mindestens einen Datensatz mit `Verarbeiten=ja` prüfen
3. Themenlisten-Erstellung starten und Dokumentausgabe verifizieren
4. Outlook-Entwurfserstellung prüfen (inkl. Platzhalterersetzung)
5. Statusmeldungen im GUI auf Warnungen/Fehler prüfen
6. Bereinigungslauf verifizieren (alte Dateien >24h, `.txt` bleibt erhalten)

## 2a) Post-Release-Verifikation (skriptbar)

- Release-ZIP vorhanden, Größe + SHA256 protokolliert
- ZIP in isoliertes Temp-Verzeichnis entpackbar
- Pflichtinhalte vorhanden (`*.exe`, `docs/`, `data/` bzw. laufzeitrelevante Verzeichnisse)
- EXE startet bis GUI-Idle und lässt sich kontrolliert beenden
- Ergebnisse im `docs/RELEASE_SMOKETEST_PROTOKOLL.md` dokumentiert

## 2b) Anwenderprüfung (nicht-technisch)

- Kurzprüfung durch Fachanwender durchführen (Bedienbarkeit, Verständlichkeit, Fehlermeldungen)
- Auffälligkeiten und Rückmeldungen im Protokoll erfassen

## 3) Sollkriterien

- Themenlisten werden korrekt aus Vorlagen (`.docx`/`.dotm`) erzeugt
- E-Mail-Entwürfe werden mit passendem Anhang erstellt
- Keine neuen Fehler in Tests und keine Blocker im GUI-Hauptpfad
- Doku/Release Notes entsprechen dem tatsächlichen Versionsstand

## 4) Freigabeentscheidung

Release nur freigeben, wenn:

- automatisierte Prüfung grün
- Smoke-Checkliste vollständig durchlaufen
- Post-Release-Verifikation inkl. Protokoll abgeschlossen
- keine offenen Blocker vorhanden
