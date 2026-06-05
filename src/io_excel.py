import pandas as pd

from core_utils import filter_verarbeitbare_teilnehmende


def lade_verarbeitbare_teilnehmende(excel_path: str) -> pd.DataFrame:
    df = pd.read_excel(excel_path, sheet_name='Teilnehmende')
    return filter_verarbeitbare_teilnehmende(df)


def lade_mailkonfiguration(excel_path: str) -> pd.DataFrame:
    return pd.read_excel(excel_path, sheet_name='E-Mail-Konfiguration')


def finde_mailkonfiguration(mailkonf: pd.DataFrame, template_bez: str) -> tuple[str, str] | None:
    mailrow = mailkonf[mailkonf['TemplateBezeichnung'] == template_bez]
    if mailrow.empty:
        return None
    subject = str(mailrow.iloc[0]['Subject'])
    body = str(mailrow.iloc[0]['BodyText']).replace('\\n', '\n')
    return subject, body
