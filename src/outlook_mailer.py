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
    subject = str(subject_template)
    body = str(body_template)
    for key, value in {
        '<<vorname>>': row['Vorname'],
        '<<nachname>>': row['Nachname'],
        '<<anrede>>': row['Anrede'],
        '<<zeitraum>>': row['Zeitraum'],
        '<<kurs>>': row['Kurs'],
        '<<lernbereich>>': row['Lernbereich'],
    }.items():
        subject = subject.replace(key, str(value))
        body = body.replace(key, str(value))
    return subject, body


def erstelle_outlook_entwurf(outlook: Any, empfaenger: str, subject: str, body: str, anhang: str) -> None:
    mail = outlook.CreateItem(0)
    mail.To = empfaenger
    mail.Subject = subject
    mail.Body = body
    mail.Attachments.Add(anhang)
    mail.Display()
