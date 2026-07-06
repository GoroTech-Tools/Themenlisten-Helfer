# Dokumentation Technik

## Systemüberblick

```mermaid
flowchart LR
    A[GUI src/gui.py] --> B[io_excel.py]
    A --> C[docx_renderer.py]
    A --> D[outlook_mailer.py]
    A --> E[cleanup.py]
    A --> F[core_utils.py]

    B --> G[Excel Teilnehmende + E-Mail-Konfiguration]
    C --> H[Word Vorlagen .docx/.dotm]
    D --> I[Outlook COM]
    E --> J[Ausgabeordner Themenlisten]
```

![Systemüberblick Dokumentation Technik](diagramme/technik_systemuebersicht.svg)

## Architektur (aktuell)

Desktop-Anwendung mit GUI-Orchestrierung in `src/ThemenlistenHelfer_GUI.py` und ausgelagerten Hilfsmodulen.

Kernprozesse (weiterhin GUI-getrieben):

1. `erstelle_themenlisten(...)`
2. `erstelle_emails(...)`
3. `loesche_alte_themenlisten(...)`

Ausgelagerte Module (Stand jetzt):

- `src/core_utils.py` (allgemeine Hilfsfunktionen)
- `src/io_excel.py` (Excel-Lese- und Konfigurationslogik)
- `src/outlook_mailer.py` (Adress- und Mail-Text-Hilfslogik, Entwurferstellung)
- `src/docx_renderer.py` (Word-Rendering inkl. Platzhalterersetzung)
- `src/cleanup.py` (Bereinigung alter Ausgabedateien)
- `src/gui.py` (GUI-Klasse, Ablaufsteuerung und Anwendungseinstieg)

Die GUI startet den Ablauf asynchron über einen Thread.

## Pfadstrategie

Die App nutzt bevorzugt die neue Struktur mit Legacy-Fallback:

- Vorlagen: `data/Themenlisten-Vorlagen/` → `templates/Themenlisten-Vorlagen/` → `Themenlisten-Vorlagen/`
- Ausgabe: `Themenlisten/` (ab 2.5.3 fest; vorher `output/Themenlisten/` mit Legacy-Fallback)
- Daten: `data/Auswahl Teilnehmende zu Lernbereichen.xlsx` → Root-Datei
- Version: `src/version.txt` → `config/version.txt` → `version.txt`
- Assets: `assets/icons|images` → Root-Dateien

Für PyInstaller-Onefile gilt zusätzlich:

- Ressourcen werden zuerst relativ zum Anwendungsverzeichnis gesucht; das Bundle (`sys._MEIPASS`) bleibt als Fallback aktiv.
- Schreiboperationen (z. B. erzeugte Themenlisten) zielen weiterhin auf das EXE-/Projektverzeichnis, nicht auf `_MEIPASS`.

Damit bleiben alte Deployments lauffähig.

## Daten- und Verarbeitungsfluss

```mermaid
flowchart TD
    A[data Auswahldatei] --> B[Excel lesen]
    B --> C[Filter Verarbeiten ja]
    C --> D[Platzhalter ersetzen]
    D --> E[Word Dokument speichern]
    D --> F[E-Mail Entwurf erzeugen]
    E --> G[output Themenlisten]
    F --> H[Outlook Drafts]
```

![Datenfluss Dokumentation Technik](diagramme/technik_datenfluss.svg)

## Build & Packaging

- `scripts/build_tlh.bat` erhöht Patch-Version, nutzt explizit das konfigurierte 64-Bit-Python und erstellt die EXE via PyInstaller.
- `src/ThemenlistenHelfer_GUI.spec` enthält notwendige Datenordner.
- ZIP-Archiv wird mit EXE + relevanten Assets/Daten erzeugt.
- Build prüft Abhängigkeiten aus `src/requirements.txt` (Fallback: `requirements.txt`) vor dem Packaging.

## Relevante Korrekturen in `2.5.2`

- robuste Behandlung fehlender/`None`-Pfade vor `exists`-Prüfungen
- differenziertere Ergebnisobjekte für Themenlisten- und E-Mail-Erstellung
- Vorlagensuche für `.docx` und `.dotm`
- korrigierte Pfadbasis im nicht eingefrorenen Betrieb

## Relevante Korrekturen in `2.5.3`

- Ausgabepfad auf einzelnen Ordner `Themenlisten/` vereinfacht; `output/Themenlisten/` entfällt als Schreibziel
- Pylance-Fehler beseitigt: `_MEIPASS`-Attributzugriff abgesichert, `Optional[str]`-Rückgabetyp in `resolve_path`, explizite `None`-Guards vor `os.makedirs` und `os.path.join`
- MIT-Lizenz eingeführt (Copyright GoroTech-Tools)
- Dokumentation Anwender um Vorlagen- und E-Mail-Konfigurationshinweise erweitert

## Geplante Modularisierung (`src/`)

Empfohlene Aufteilung in nächsten Schritten:

- **Bereits umgesetzt:** `src/core_utils.py` für pure Hilfsfunktionen (`ersetze_umlaute`, `finde_vorlagen`, `filter_verarbeitbare_teilnehmende`).
- **Bereits umgesetzt:** `src/io_excel.py` und `src/outlook_mailer.py`.
- **Bereits umgesetzt:** `src/docx_renderer.py` und `src/cleanup.py`.
- **Bereits umgesetzt:** `src/gui.py` als zentraler UI-Einstieg; `src/ThemenlistenHelfer_GUI.py` fungiert als Kompatibilitäts-Launcher.
- Begleitende Unit-Tests: `tests/test_core_utils.py`, `tests/test_io_excel.py`, `tests/test_outlook_mailer.py`, `tests/test_docx_renderer.py`, `tests/test_cleanup.py`.


## Qualitätsrichtlinien

- kleine, testbare Änderungen
- klare Fehlermeldungen für Anwender
- dokumentationspflichtig bei Pfad-/Prozessänderungen

## Bekannte technische Grenzen

- Outlook/Word-Abhängigkeit erfordert Windows + Office.
- Threading + COM: `pythoncom.CoInitialize()` ist gesetzt, dennoch COM-Fehler je nach Systemzustand möglich.
