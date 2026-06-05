from PIL import Image, ImageTk  # Pillow muss installiert sein: pip install pillow
import sys
import os
from typing import Optional, Callable, TypedDict

# === Basisverzeichnis bestimmen (EXE-kompatibel) ===
def get_app_dir() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_resource_dirs() -> list[str]:
    dirs: list[str] = []
    meipass = getattr(sys, '_MEIPASS', None)
    if getattr(sys, 'frozen', False) and isinstance(meipass, str) and meipass:
        dirs.append(meipass)
    dirs.append(get_app_dir())
    return dirs


def resolve_path(*candidates: str, must_exist: bool = False) -> Optional[str]:
    for path in candidates:
        if must_exist:
            if path and os.path.exists(path):
                return path
        else:
            if path:
                return path
    return None


import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
import win32com.client as win32
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import pythoncom
from core_utils import finde_vorlagen
from io_excel import lade_verarbeitbare_teilnehmende, lade_mailkonfiguration, finde_mailkonfiguration
from outlook_mailer import ermittle_empfaengeradresse, ersetze_mail_platzhalter, erstelle_outlook_entwurf
from docx_renderer import erstelle_dateiname, baue_ersetzungen, render_vorlage
from cleanup import loesche_alte_dateien


StatusCallback = Callable[[str], None]


class ThemenlistenResult(TypedDict):
    selected: int
    created: int
    missing_templates: int
    aborted: bool


class EmailResult(TypedDict):
    selected: int
    drafts: int
    missing_templates: int
    missing_attachments: int
    missing_mail_config: int
    aborted: bool


def erstelle_themenlisten(excel_path: str, status_callback: StatusCallback) -> ThemenlistenResult:
    result: ThemenlistenResult = {
        'selected': 0,
        'created': 0,
        'missing_templates': 0,
        'aborted': False
    }
    df = lade_verarbeitbare_teilnehmende(excel_path)
    result['selected'] = len(df)
    app_dir = get_app_dir()
    resource_dirs = get_resource_dirs()
    vorlagen_ordner = resolve_path(
        *[os.path.join(d, 'data', 'Themenlisten-Vorlagen') for d in resource_dirs],
        *[os.path.join(d, 'templates', 'Themenlisten-Vorlagen') for d in resource_dirs],
        *[os.path.join(d, 'Themenlisten-Vorlagen') for d in resource_dirs],
        must_exist=True
    )
    if not vorlagen_ordner:
        status_callback("[FEHLER] Kein Vorlagenordner gefunden (erwartet: data/Themenlisten-Vorlagen, templates/Themenlisten-Vorlagen oder Themenlisten-Vorlagen).")
        result['aborted'] = True
        return result
    vorhandene_vorlagen = finde_vorlagen(vorlagen_ordner)
    if not vorhandene_vorlagen:
        status_callback(f"[FEHLER] Im Vorlagenordner wurden keine .docx- oder .dotm-Dateien gefunden: {vorlagen_ordner}")
        result['aborted'] = True
        return result
    ausgabe_ordner = os.path.join(app_dir, 'Themenlisten')
    os.makedirs(ausgabe_ordner, exist_ok=True)
    for idx, row in df.iterrows():
        lernbereich = str(row['Lernbereich'])
        vorlagen = finde_vorlagen(vorlagen_ordner, lernbereich)
        if not vorlagen:
            status_callback(f"[WARNUNG] Keine Vorlage für Lernbereich '{lernbereich}' gefunden!")
            result['missing_templates'] += 1
            continue
        vorlage = vorlagen[0]
        dateiname = erstelle_dateiname(lernbereich, str(row['Nachname']), str(row['Zeitraum']))
        ersetzungen = baue_ersetzungen(row, lernbereich, dateiname)
        ziel = os.path.join(ausgabe_ordner, dateiname)
        render_vorlage(vorlage, ziel, ersetzungen)
        result['created'] += 1
        status_callback(f"Erstellt: {ziel}")
    status_callback(f"FERTIG: Themenlisten erstellt ({result['created']} von {result['selected']}).")
    return result


def erstelle_emails(excel_path: str, status_callback: StatusCallback) -> EmailResult:
    result: EmailResult = {
        'selected': 0,
        'drafts': 0,
        'missing_templates': 0,
        'missing_attachments': 0,
        'missing_mail_config': 0,
        'aborted': False
    }
    personen = lade_verarbeitbare_teilnehmende(excel_path)
    result['selected'] = len(personen)
    mailkonf = lade_mailkonfiguration(excel_path)
    app_dir = get_app_dir()
    resource_dirs = get_resource_dirs()
    vorlagen_ordner = resolve_path(
        *[os.path.join(d, 'data', 'Themenlisten-Vorlagen') for d in resource_dirs],
        *[os.path.join(d, 'templates', 'Themenlisten-Vorlagen') for d in resource_dirs],
        *[os.path.join(d, 'Themenlisten-Vorlagen') for d in resource_dirs],
        must_exist=True
    )
    if not vorlagen_ordner:
        status_callback("[FEHLER] Kein Vorlagenordner gefunden (erwartet: data/Themenlisten-Vorlagen, templates/Themenlisten-Vorlagen oder Themenlisten-Vorlagen).")
        result['aborted'] = True
        return result
    vorhandene_vorlagen = finde_vorlagen(vorlagen_ordner)
    if not vorhandene_vorlagen:
        status_callback(f"[FEHLER] Im Vorlagenordner wurden keine .docx- oder .dotm-Dateien gefunden: {vorlagen_ordner}")
        result['aborted'] = True
        return result
    ausgabe_ordner = os.path.join(app_dir, 'Themenlisten')
    os.makedirs(ausgabe_ordner, exist_ok=True)
    try:
        outlook = win32.Dispatch('Outlook.Application')
    except Exception as e:
        status_callback(f"[FEHLER] Outlook konnte nicht gestartet werden: {e}")
        result['aborted'] = True
        return result
    for idx, row in personen.iterrows():
        lernbereich = str(row['Lernbereich'])
        vorlagen = finde_vorlagen(vorlagen_ordner, lernbereich)
        if not vorlagen:
            status_callback(f"[WARNUNG] Keine Vorlage für Lernbereich '{lernbereich}' gefunden!")
            result['missing_templates'] += 1
            continue
        vorlage = vorlagen[0]
        dateiname = erstelle_dateiname(lernbereich, str(row['Nachname']), str(row['Zeitraum']))
        anhang = os.path.join(ausgabe_ordner, dateiname)
        if not os.path.exists(anhang):
            status_callback(f"[WARNUNG] Anhang nicht gefunden: {anhang}")
            result['missing_attachments'] += 1
            continue
        empfaenger = ermittle_empfaengeradresse(str(row['Vorname']), str(row['Nachname']))
        template_bez = os.path.splitext(os.path.basename(vorlage))[0]
        config = finde_mailkonfiguration(mailkonf, template_bez)
        if not config:
            status_callback(f"[WARNUNG] Keine E-Mail-Konfiguration für Vorlage {template_bez}")
            result['missing_mail_config'] += 1
            continue
        subject_template, body_template = config
        subject, body = ersetze_mail_platzhalter(subject_template, body_template, row)
        erstelle_outlook_entwurf(outlook, empfaenger, subject, body, anhang)
        result['drafts'] += 1
        status_callback(f"E-Mail-Entwurf für {empfaenger} angezeigt.")
    status_callback(f"FERTIG: E-Mail-Entwürfe erstellt ({result['drafts']} von {result['selected']}).")
    return result


def loesche_alte_themenlisten(_excel_path: str, status_callback: StatusCallback) -> int:
    app_dir = get_app_dir()
    ausgabe_ordner = os.path.join(app_dir, 'Themenlisten')
    return loesche_alte_dateien(ausgabe_ordner, status_callback)


class ThemenlistenApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.status_text = tk.StringVar()
        try:
            resource_dirs = get_resource_dirs()
            version_path = resolve_path(
                *[os.path.join(d, "src", "version.txt") for d in resource_dirs],
                *[os.path.join(d, "config", "version.txt") for d in resource_dirs],
                *[os.path.join(d, "version.txt") for d in resource_dirs],
                must_exist=True
            )
            if version_path:
                with open(version_path, "r", encoding="utf-8") as vf:
                    version = vf.read().strip()
            else:
                version = ""
        except Exception:
            version = ""
        self.root.title(f"Themenlisten-Helfer {version}")
        self.root.geometry("800x400")
        self.excel_path = tk.StringVar()
        self.progress = tk.DoubleVar()
        app_dir = get_app_dir()
        resource_dirs = get_resource_dirs()
        default_excel = resolve_path(
            os.path.join(app_dir, 'data', 'Auswahl Teilnehmende zu Lernbereichen.xlsx'),
            os.path.join(app_dir, 'Auswahl Teilnehmende zu Lernbereichen.xlsx'),
            *[os.path.join(d, 'data', 'Auswahl Teilnehmende zu Lernbereichen.xlsx') for d in resource_dirs],
            *[os.path.join(d, 'Auswahl Teilnehmende zu Lernbereichen.xlsx') for d in resource_dirs],
            must_exist=True
        )
        if not default_excel:
            default_excel = os.path.join(app_dir, 'data', 'Auswahl Teilnehmende zu Lernbereichen.xlsx')
        self.excel_path.set(default_excel)
        frame_outer = tk.Frame(root, padx=20, pady=10)
        frame_outer.pack(fill=tk.BOTH, expand=True)
        status_label = tk.Label(frame_outer, textvariable=self.status_text, fg="red", anchor="w", font=("Calibri", 10))
        status_label.pack(fill=tk.X, pady=(0, 5))

        frame_main = tk.Frame(frame_outer)
        frame_main.pack(fill=tk.BOTH, expand=True)

        frame_left = tk.Frame(frame_main)
        frame_left.grid(row=0, column=0, sticky="nw")
        label_excel = tk.Label(frame_left, text="Excel-Datei: Auswahl Teilnehmende zu Lernbereichen.xlsx", anchor="w", justify="left")
        try:
            label_excel.configure(font=("Calibri", 11))
        except Exception:
            pass
        label_excel.pack(anchor="w", pady=(0, 5))
        btn_excel = tk.Button(frame_left, text="Auswahl Teilnehmende zu Lernbereichen", command=self.excel_bearbeiten, bg="#FFA500", fg="black", activebackground="#FFB733", activeforeground="white")
        btn_start = tk.Button(frame_left, text="Themenlisten-Helfer starten", command=self.batch_starten, bg="#4CAF50", fg="white", activebackground="#6FD36F", activeforeground="white")
        try:
            btn_excel.configure(font=("Calibri", 11))
            btn_start.configure(font=("Calibri", 11))
        except Exception:
            pass
        btn_excel.pack(anchor="w", pady=2, fill=tk.X)
        btn_start.pack(anchor="w", pady=2, fill=tk.X)

        frame_right = tk.Frame(frame_main)
        frame_right.grid(row=0, column=1, sticky="ne", padx=(30, 0))
        anleitung_fett = "Anleitung:"
        anleitung_rest = (
            "\n\n1. Excel-Datei anpassen (z. B. Teilnehmende, Lernbereiche, E-Mail-Konfiguration).\n"
            "2. 'Themenlisten-Helfer starten' ausführen.\n"
            "\nDie generierten Themenlisten und E-Mail-Entwürfe werden automatisch erstellt."
        )
        textbox = tk.Text(frame_right, width=48, height=10, wrap="word", bg=frame_outer.cget("bg"), relief="flat", borderwidth=0)
        try:
            textbox.configure(font=("Calibri", 11))
        except Exception:
            pass
        textbox.tag_configure("fett", font=("Calibri", 11, "bold"))
        textbox.insert("1.0", anleitung_fett, "fett")
        textbox.insert("1.end", anleitung_rest)
        textbox.config(state="disabled")
        textbox.pack(anchor="n", pady=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("grey.Horizontal.TProgressbar", troughcolor="#e0e0e0", background="#888888", bordercolor="#e0e0e0", lightcolor="#bbbbbb", darkcolor="#888888")
        self.progressbar = ttk.Progressbar(frame_outer, variable=self.progress, maximum=100, style="grey.Horizontal.TProgressbar")
        self.progressbar.pack(pady=10, fill=tk.X)
        self.progress_label = tk.Label(frame_outer, text="", font=("Calibri", 11), fg="#4CAF50")
        self.progress_label.pack()

        try:
            resource_dirs = get_resource_dirs()
            img_path = resolve_path(
                *[os.path.join(d, "assets", "images", "Themenlistenhelfer.png") for d in resource_dirs],
                *[os.path.join(d, "Themenlistenhelfer.png") for d in resource_dirs],
                must_exist=True
            )
            if img_path and os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((64, 64), Image.Resampling.LANCZOS)
                self.tk_img = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame_outer, image=self.tk_img)
                img_label.pack(side=tk.RIGHT, anchor="se", padx=10, pady=10)
            else:
                self.status_text.set("Bild 'Themenlistenhelfer.png' nicht gefunden!")
        except Exception as e:
            self.status_text.set(f"Bildfehler: {e}")

    def excel_bearbeiten(self):
        path = self.excel_path.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Fehler", "Die Datei 'Auswahl Teilnehmende zu Lernbereichen.xlsx' wurde nicht gefunden!")
            return
        try:
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte Excel-Datei nicht öffnen: {e}")

    def batch_starten(self):
        path = self.excel_path.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Fehler", "Die Datei 'Auswahl Teilnehmende zu Lernbereichen.xlsx' wurde nicht gefunden!")
            return
        try:
            df = lade_verarbeitbare_teilnehmende(path)
            if df.empty:
                messagebox.showinfo("Hinweis", "In der Excel-Datei sind keine Datensätze aktiviert.")
                return
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Einlesen der Excel-Datei: {e}")
            return
        self.progress.set(0)
        self.progressbar.start(10)
        threading.Thread(target=self.batch_ablauf, args=(path,), daemon=True).start()

    def batch_ablauf(self, path: str) -> None:
        pythoncom.CoInitialize()

        def set_progress(val: float) -> None:
            self.progress.set(val)
            self.root.update_idletasks()
            if val >= 100:
                self.progress_label.config(text="Fertig")
            else:
                self.progress_label.config(text="")

        def gui_callback(msg: str) -> None:
            self.status_text.set(msg)
            self.root.update_idletasks()

        try:
            set_progress(10)
            thema_result = erstelle_themenlisten(path, gui_callback)
            set_progress(50)
            email_result = erstelle_emails(path, gui_callback)
            set_progress(80)
            geloescht = loesche_alte_themenlisten(path, gui_callback)
            set_progress(100)
            if thema_result.get('aborted'):
                self.status_text.set("Abbruch: Es konnten keine gültigen Word-Vorlagen gefunden werden.")
            elif thema_result.get('created', 0) == 0:
                self.status_text.set("Keine Themenlisten erstellt. Bitte Vorlagen/Lernbereiche prüfen.")
            elif email_result.get('aborted'):
                self.status_text.set("Themenlisten erstellt, aber E-Mail-Erstellung wegen fehlender Vorlagen abgebrochen.")
            elif email_result.get('drafts', 0) == 0:
                self.status_text.set("Themenlisten erstellt, aber keine E-Mail-Entwürfe erzeugt (Vorlagen/Konfiguration/Anhänge prüfen).")
            else:
                self.status_text.set(f"Abgeschlossen: {thema_result.get('created', 0)} Themenlisten, {email_result.get('drafts', 0)} E-Mail-Entwürfe, {geloescht} Dateien bereinigt.")
        except Exception as e:
            set_progress(0)
            self.status_text.set(f"Fehler: {e}")
        finally:
            self.progressbar.stop()
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass


def main() -> None:
    root = tk.Tk()
    resource_dirs = get_resource_dirs()
    icon_path = resolve_path(
        *[os.path.join(d, "assets", "icons", "Themenlistenhelfer256.ico") for d in resource_dirs],
        *[os.path.join(d, "Themenlistenhelfer256.ico") for d in resource_dirs],
        must_exist=True
    )
    if icon_path and os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    app = ThemenlistenApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
