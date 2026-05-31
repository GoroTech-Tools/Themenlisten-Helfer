# Tools

Dieses Verzeichnis ist für projektnahe Hilfsskripte (Wartung, Datenchecks, QA und Release-Unterstützung) vorgesehen.

## Aktueller Stand

Aktuell sind in diesem Ordner noch keine ausführbaren Skripte versioniert.

## Zweck des Ordners

Typische Inhalte, die hier abgelegt werden können:

- Prüfskripte für Daten- und Dateikonsistenz
- Hilfen für Build-/Release-Validierung
- Migrations-/Aufräum-Skripte
- Automatisierte Smoke-Checks

## Konventionen

- Bevorzugte Skriptsprachen: PowerShell (`.ps1`) und Python (`.py`)
- Skripte sollten ohne Seiteneffekte einen `--check`-/Dry-Run-Modus anbieten (wenn sinnvoll)
- Bei Änderungen an produktiven Dateien immer Backup/Recovery-Strategie dokumentieren
- Jede neue Tool-Datei sollte im README kurz dokumentiert werden (Zweck, Parameter, Exit-Codes)

## Pflegehinweis

Sobald das erste Tool-Skript hinzugefügt wird, dieses README um einen Abschnitt **„Enthaltene Skripte“** mit Beispielaufrufen ergänzen.
