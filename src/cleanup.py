import os
import time
from collections.abc import Callable


def loesche_alte_dateien(
    ausgabe_ordner: str,
    status_callback: Callable[[str], None],
    alter_sekunden: int = 24 * 60 * 60,
    geschuetzte_endungen: tuple[str, ...] = ('.txt',),
) -> int:
    os.makedirs(ausgabe_ordner, exist_ok=True)
    jetzt = time.time()
    geloescht = 0

    for fname in os.listdir(ausgabe_ordner):
        pfad = os.path.join(ausgabe_ordner, fname)
        if not os.path.isfile(pfad):
            continue
        if fname.lower().endswith(tuple(ext.lower() for ext in geschuetzte_endungen)):
            continue

        mtime = os.path.getmtime(pfad)
        if jetzt - mtime > alter_sekunden:
            try:
                os.remove(pfad)
                status_callback(f"Gelöscht: {pfad}")
                geloescht += 1
            except Exception as e:
                status_callback(f"[FEHLER] Konnte {pfad} nicht löschen: {e}")

    status_callback(f"Alte Themenlisten gelöscht: {geloescht}")
    return geloescht
