import os
from typing import Any

from core_utils import ersetze_umlaute


def ermittle_empfaengeradresse(vorname: str, nachname: str, domain: str = 'ab.bfw.local', max_laenge: int = 20) -> str:
    vornamen_roh = str(vorname).lower()
    nachname_norm = ersetze_umlaute(str(nachname).lower())
    vornamen_ohne_leer = ersetze_umlaute(vornamen_roh.replace(' ', ''))

    empfaenger_vorname = vornamen_ohne_leer
    if len(empfaenger_vorname + '.' + nachname_norm) > max_laenge and vornamen_roh:
        empfaenger_vorname = ersetze_umlaute(vornamen_roh[0])

    return f"{empfaenger_vorname}.{nachname_norm}@{domain}"


def ersetze_mail_platzhalter(subject_template: str, body_template: str, row: Any) -> tuple[str, str]:
    platzhalter = {
        '<<vorname>>': row['Vorname'],
        '<<nachname>>': row['Nachname'],
        '<<anrede>>': row['Anrede'],
        '<<zeitraum>>': row['Zeitraum'],
        '<<kurs>>': row['Kurs'],
        '<<lernbereich>>': row['Lernbereich'],
    }
    subject = str(subject_template)
    body = str(body_template)
    for key, value in platzhalter.items():
        subject = subject.replace(key, str(value))
        body = body.replace(key, str(value))
    return subject, body


def resolve_zusatzanhaenge(anhang_templates: list[str], app_dir: str, lernbereich: str, row: Any) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    missing: list[str] = []
    bereits: set[str] = set()
    basisordner = os.path.join(app_dir, 'data', 'Zusatzmaterialien', lernbereich)

    for template in anhang_templates[:5]:
        kandidat = str(template).strip()
        if not kandidat:
            continue

        _, kandidat = ersetze_mail_platzhalter(kandidat, kandidat, row)
        kandidat = kandidat.strip()
        pfad: str | None = None

        if os.path.isabs(kandidat) and os.path.isfile(kandidat):
            pfad = kandidat
        else:
            pruefpfade = [
                os.path.join(app_dir, kandidat),
                os.path.join(app_dir, 'data', kandidat),
                os.path.join(basisordner, kandidat),
            ]
            for p in pruefpfade:
                if os.path.isfile(p):
                    pfad = p
                    break

            if pfad is None and os.path.isdir(basisordner):
                suchname = os.path.basename(kandidat).lower()
                treffer: list[str] = []
                for root, _, files in os.walk(basisordner):
                    for datei in files:
                        if datei.lower() == suchname:
                            treffer.append(os.path.join(root, datei))
                if treffer:
                    pfad = sorted(treffer)[0]

        if pfad is None:
            missing.append(kandidat)
            continue

        key = os.path.normcase(os.path.abspath(pfad))
        if key not in bereits:
            bereits.add(key)
            resolved.append(pfad)

    return resolved, missing


def erstelle_outlook_entwurf(outlook: Any, empfaenger: str, subject: str, body: str, anhaenge: str | list[str]) -> None:
    mail = outlook.CreateItem(0)
    mail.To = empfaenger
    mail.Subject = subject
    mail.Body = body
    if isinstance(anhaenge, str):
        mail.Attachments.Add(anhaenge)
    else:
        for anhang in anhaenge:
            mail.Attachments.Add(anhang)
    mail.Display()
