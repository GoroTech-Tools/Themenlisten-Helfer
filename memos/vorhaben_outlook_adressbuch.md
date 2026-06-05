# Vorhaben: Empfängeradressen aus Outlook-Adressbuch auflösen

## Status

- Stand: 05.06.2026
- Entscheidung: Vorhaben vorerst zurückgestellt
- Aktuelle Produktionslogik bleibt unverändert: Empfängeradresse wird weiterhin aus Vorname/Nachname generiert.

## Hintergrund

Es wurde geprüft, ob E-Mail-Adressen direkt aus Outlook-Adressbüchern (Kontakte/GAL) ermittelt werden können.
Das ist technisch grundsätzlich möglich, setzt in der Praxis jedoch Zugriff auf die Unternehmensumgebung (Domäne/Exchange-Kontext) voraus.

## Zielbild (später)

Optionale Erweiterung der Adressauflösung:

1. Versuch: Auflösung über Outlook-Adressbuch (Kontakte/GAL)
2. Fallback: bestehende Regel `vorname.nachname@ab.bfw.local`
3. Protokollierung: Treffer/Mehrdeutigkeit/Nicht gefunden in den Statusmeldungen

## Offene Punkte

- Verfügbarkeit und Berechtigung in der Unternehmensdomäne
- Eindeutige Zuordnung bei Namensdubletten
- Robuste Ermittlung der SMTP-Adresse je nach Exchange/Outlook-Typ
- Performance bei vielen Datensätzen

## Notiz

Die aktuelle Erzeugungsvariante ist bewusst beibehalten und bleibt der Standard, bis die Domänenbedingungen für einen belastbaren Test vorliegen.
