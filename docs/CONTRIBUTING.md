# Beitragen zum Projekt

Vielen Dank für deinen Beitrag! 🎉

## Projektstatus

Das Projekt ist fachlich abgeschlossen und befindet sich im Wartungsmodus.

Änderungswünsche bitte ausschließlich über GitHub einreichen:

- Fehler über Issue-Typ **Bug Report**
- Erweiterungen/Verbesserungen über Issue-Typ **Feature Request**

Direkte Änderungsaufträge außerhalb von GitHub sind nicht vorgesehen.

## Branching

- `main`: stabiler Stand
- Feature-Branches: `feature/<kurzbeschreibung>`
- Bugfix-Branches: `fix/<kurzbeschreibung>`

## Commit-Konvention (empfohlen)

- `feat:` neue Funktion
- `fix:` Fehlerbehebung
- `docs:` Dokumentation
- `chore:` Wartung/Build

## Pull Requests

1. Branch aktuell halten.
2. Änderungen klein und fokussiert halten.
3. Doku bei Verhaltensänderung mit aktualisieren.
4. PR-Template vollständig ausfüllen.

## Dokumentationsregel für Versionen

- In laufender Dokumentation keine statischen Versionsnummern als "aktuell" eintragen.
- Stattdessen Muster (`X.Y.Z`, `vX.Y.Z`) oder verlässliche Quellen referenzieren (`src/version.txt`, GitHub Releases).
- Konkrete Versionshistorie ausschließlich in `docs/CHANGELOG.md`, `release/RELEASE_NOTES_v<version>.md` und Release-Protokollen führen.

## Qualitätssicherung

- Anwendung lokal starten und Smoke-Test durchführen.
- Build (`scripts/build_tlh.bat`) einmal lokal testen.
- Keine generierten Binärdateien committen (`.exe`, `.zip`, `dist/`, `build/`).
