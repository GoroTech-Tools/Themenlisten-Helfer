import glob
import os
import re

import pandas as pd


def ersetze_umlaute(s: str) -> str:
    s = re.sub(r'[äÄ]', 'ae', s)
    s = re.sub(r'[öÖ]', 'oe', s)
    s = re.sub(r'[üÜ]', 'ue', s)
    s = re.sub(r'ß', 'ss', s)
    return s


def finde_vorlagen(vorlagen_ordner: str, lernbereich: str | None = None) -> list[str]:
    endungen = ('.docx', '.dotm')
    treffer: list[str] = []
    for endung in endungen:
        if lernbereich is None:
            muster = os.path.join(vorlagen_ordner, f'*{endung}')
        else:
            muster = os.path.join(vorlagen_ordner, f'Themenliste_{lernbereich}*{endung}')
        treffer.extend(glob.glob(muster))
    return sorted(set(treffer))


def filter_verarbeitbare_teilnehmende(df: pd.DataFrame) -> pd.DataFrame:
    verarbeiten = df.get('Verarbeiten')
    if verarbeiten is None:
        return df.iloc[0:0]
    maske = verarbeiten.fillna('').astype(str).str.strip().str.lower() == 'ja'
    return df[maske]
