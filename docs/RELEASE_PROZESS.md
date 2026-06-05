# Release-Prozess (Themenlisten-Helfer)

## Ziel

Verbindlicher, reproduzierbarer Ablauf für Build, Tagging und GitHub-Release — analog zu den Schwesterprojekten.

## Wichtige Vorbedingungen

- `src/version.txt` ist die führende Version.
- GitHub-Tag muss exakt passen: `vMAJOR.MINOR.PATCH`.
- Guard im Workflow: `tag == src/version.txt` (sonst Abbruch).
- Lokales `scripts/build_tlh.bat` erhöht die Patch-Version automatisch.

## Empfohlener Standardablauf (Tag-gesteuerter GitHub-Release)

1. **Version festlegen**
   - `src/version.txt` auf Zielversion setzen (z. B. `X.Y.Z`).

2. **Doku und Notes vorbereiten**
   - `docs/CHANGELOG.md` aktualisieren.
   - `release/RELEASE_NOTES_v<version>.md` prüfen/ergänzen.
   - `docs/RELEASE_QA_CHECKLISTE.md` durchführen.
   - `docs/RELEASE_SMOKETEST_PROTOKOLL.md` ausfüllen.

3. **Lokale Qualitätsprüfung**
   - Unit-Tests ausführen.
   - Optional lokaler Build-/Smoke-Test der EXE.

4. **Commit & Push**
   - Alle Änderungen committen.
   - Commit auf `main` pushen.

5. **Tag erstellen und pushen (exakte Reihenfolge)**
   - Tag lokal erstellen: `v<version>`
   - Tag pushen.

6. **GitHub Release validieren**
   - Workflow `release.yml` erfolgreich.
   - Release-Titel im Produktschema: `Themenlisten-Helfer v...`.
   - Assets vorhanden:
     - `dist/ThemenlistenHelfer_GUI.exe`
     - `release/Themenlisten-Helfer_v<version>.zip`
     - `release/RELEASE_NOTES_v<version>.md`

7. **Abschluss**
   - Freigabevermerk im Smoketest-Protokoll setzen.
   - Optional: Kurzinfo im Teamkanal mit Tag/Release-Link.

## Variante A: Mit lokalem build_tlh.bat

Hinweis: `scripts/build_tlh.bat` erhöht Patch automatisch.

Ablauf:

1. Startwert in `src/version.txt` prüfen.
2. `scripts/build_tlh.bat` ausführen (Version wird erhöht, Artefakte + Release Notes werden erzeugt).
3. Geänderte Dateien prüfen und committen (inkl. neuer Version).
4. Tag exakt auf die neue Version setzen und pushen.
5. GitHub-Release wie oben validieren.

## Variante B: Ohne Auto-Inkrement (präzise Zielversion halten)

Ablauf:

1. `src/version.txt` manuell auf Zielversion setzen.
2. Tests/QA durchführen.
3. Committen und pushen.
4. Tag `v<genau diese version>` erstellen und pushen.
5. GitHub-Release validieren.

## CI-/Release-Checkliste (kurz)

- [ ] `src/version.txt` entspricht Zielversion
- [ ] Changelog aktuell
- [ ] Release Notes vorhanden (`release/RELEASE_NOTES_v<version>.md`)
- [ ] QA-Checkliste durchgeführt
- [ ] Smoketest-Protokoll ausgefüllt
- [ ] Tests grün
- [ ] Tag `v<version>` gepusht
- [ ] GitHub Release + Assets vollständig
