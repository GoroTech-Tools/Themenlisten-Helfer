# Dokumentation Anwender

## Zweck

Der Themenlisten-Helfer erstellt automatisch:

- personalisierte Themenlisten (Word)
- Outlook-E-Mail-Entwürfe mit passendem Anhang

Zusätzlich dient die Anwendung als Arbeitserleichterung für die Begleitung der kaufmännischen Qualifizierung von Personen im BFW Weser-Ems.

## Ablauf auf einen Blick

```mermaid
flowchart LR
   A[Anwendung starten] --> B[Excel-Datei prüfen]
   B --> C[Vorlagen bereitstellen]
   C --> D[Themenlisten-Helfer starten]
   D --> E[Themenlisten erzeugen]
   E --> F[Outlook-Entwürfe erstellen]
   F --> G[Ergebnisse in Themenlisten prüfen]
```

![Ablauf Dokumentation Anwender](diagramme/anwender_ablauf.svg)

## Voraussetzungen

- Windows 10/11
- Microsoft Word und Outlook
- Berechtigung zum Öffnen/Ändern der Excel-Datei

## Vorbereitung

1. Excel-Datei bereitstellen:
   - bevorzugt: `data/Auswahl Teilnehmende zu Lernbereichen.xlsx`
2. Word-Vorlagen bereitstellen:
   - bevorzugt: `data/Themenlisten-Vorlagen/`
   - unterstützte Formate: `.docx` und `.dotm`
   - Anpassungen an Vorlagen ausschließlich im Ordner `Themenlisten-Vorlagen` vornehmen
   - Kopf- und Fußzeilen nicht bearbeiten; dort befinden sich Platzhalter, die automatisch aus der Excel-Arbeitsmappe gefüllt werden
3. Optional: bestehende Legacy-Struktur ist weiterhin möglich (`Themenlisten-Vorlagen`, `Themenlisten`).

## Excel-Struktur (Blatt `Teilnehmende`)

Erwartete Spalten:

- `Anrede`
- `Vorname`
- `Nachname`
- `Zeitraum`
- `Kurs`
- `Lernbereich`
- `Verarbeiten` (`ja`/`nein`)

Hinweis: Bei `Verarbeiten` wird Groß-/Kleinschreibung ignoriert; führende oder nachgestellte Leerzeichen werden automatisch bereinigt.

Zusätzlich wird das Blatt `E-Mail-Konfiguration` genutzt (`TemplateBezeichnung`, `Subject`, `BodyText`, optional `Anhang1` bis `Anhang5`).

Das Tabellenblatt `Vorbereitung` dient als internes Hilfsmittel und sollte nicht manipuliert oder gelöscht werden.

Das Tabellenblatt `Hilfstabellen` dient ebenfalls als Hilfsmittel und sollte nicht manipuliert oder gelöscht werden. Es enthält eine nützliche Funktion, mit der Namen im Format `Nachname, Vorname` funktionsgesteuert in separate Teilstrings für Nach- und Vornamen zerlegt werden können.

## Bedienung

1. Anwendung starten.
2. Über **„Auswahl Teilnehmende zu Lernbereichen“** die Excel-Datei prüfen/anpassen.
3. Über **„Themenlisten-Helfer starten“** den Prozess ausführen.
4. Statusmeldungen oben im Fenster beachten.
5. Ergebnisse im Ordner `Themenlisten/` prüfen.

## Verhalten der Anwendung

- Platzhalter wie `<<vorname>>` werden in Dokument, Tabellen, Kopf- und Fußzeilen ersetzt.
- Platzhalter in Kopf- und Fußzeilen werden automatisch auf Basis der Excel-Arbeitsmappe `Auswahl Teilnehmende zu Lernbereichen.xlsx` gefüllt und dürfen nicht manuell verändert werden.
- Für jede Person mit `Verarbeiten=ja` wird ein Dokument erzeugt.
- Für jede erzeugte Themenliste wird ein Outlook-Entwurf geöffnet.
- Alte Dateien im Ausgabeordner (älter als 24h) werden bereinigt; `.txt` bleibt erhalten.
- Die Statusanzeige meldet Abbrüche, fehlende Vorlagen und Teilerfolge gezielt.

## Anpassung von Vorlagen und E-Mails

- E-Mail-Betreff und E-Mail-Nachricht werden ausschließlich in der Datei `Auswahl Teilnehmende zu Lernbereichen.xlsx` im Tabellenblatt `E-Mail-Konfiguration` angepasst.
- Platzhalter in diesem Tabellenblatt dürfen nicht verändert oder gelöscht werden.
- `\n` steht dabei für einen Zeilenumbruch in der E-Mail-Nachricht.
- Für zusätzliche Anhänge können optional die Spalten `Anhang1` bis `Anhang5` verwendet werden.
- Zusatzanhänge werden primär im Ordner `data/Zusatzmaterialien/<<lernbereich>>` gesucht (inkl. Unterordner).
- In den Anhang-Spalten sind Dateinamen, relative Pfade oder absolute Pfade möglich.
- Platzhalter wie `<<vorname>>`, `<<nachname>>`, `<<lernbereich>>` sind auch in den Anhang-Spalten möglich.

## Fehlerbehebung

### Keine Vorlage gefunden

- Prüfen, ob Datei nach Muster `Themenliste_<Lernbereich>*.docx` oder `Themenliste_<Lernbereich>*.dotm` vorliegt.
- Ordner prüfen: `data/Themenlisten-Vorlagen/`.
- Bei Nutzung der EXE bitte möglichst die aktuelle Version `release/Themenlisten-Helfer_1.0.0.exe` verwenden.

### Excel-Datei nicht gefunden

- Datei in `data/` ablegen oder im GUI manuell öffnen.

### Outlook-Fehler

- Outlook installiert und lokal startbar?
- Ggf. Outlook einmal manuell starten.
- Prüfen, ob im Blatt `E-Mail-Konfiguration` für den jeweiligen Lernbereich eine passende `TemplateBezeichnung` hinterlegt ist.

### Umlaute in Mailadresse

- Werden automatisch ersetzt (`ä->ae`, `ö->oe`, `ü->ue`, `ß->ss`).
