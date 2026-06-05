import pandas as pd

from core_utils import filter_verarbeitbare_teilnehmende


ANHANG_SPALTEN = [f'Anhang{i}' for i in range(1, 6)]


def lade_verarbeitbare_teilnehmende(excel_path: str) -> pd.DataFrame:
    df = pd.read_excel(excel_path, sheet_name='Teilnehmende')
    return filter_verarbeitbare_teilnehmende(df)


def lade_mailkonfiguration(excel_path: str) -> pd.DataFrame:
    return pd.read_excel(excel_path, sheet_name='E-Mail-Konfiguration')


def _zellenwert_als_text(value: object) -> str:
    if pd.isna(value):
        return ''
    return str(value).strip()


def finde_mailkonfiguration(mailkonf: pd.DataFrame, template_bez: str) -> tuple[str, str, list[str]] | None:
    mailrow = mailkonf[mailkonf['TemplateBezeichnung'] == template_bez]
    if mailrow.empty:
        return None
    row = mailrow.iloc[0]
    subject = str(row['Subject'])
    body = str(row['BodyText']).replace('\\n', '\n')
    anhaenge: list[str] = []
    for spalte in ANHANG_SPALTEN:
        if spalte in mailkonf.columns:
            wert = _zellenwert_als_text(row.get(spalte, ''))
            if wert:
                anhaenge.append(wert)
    return subject, body, anhaenge[:5]
