import os
import sys
import tempfile
import unittest

import pandas as pd


SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from outlook_mailer import ermittle_empfaengeradresse, ersetze_mail_platzhalter, resolve_zusatzanhaenge, erstelle_outlook_entwurf


class TestOutlookMailer(unittest.TestCase):
    def test_ermittle_empfaengeradresse_kurz(self):
        adr = ermittle_empfaengeradresse('Max', 'Müller')
        self.assertEqual(adr, 'max.mueller@ab.bfw.local')

    def test_ermittle_empfaengeradresse_lang(self):
        adr = ermittle_empfaengeradresse('Maximilian Franz', 'Müllerschneider')
        self.assertEqual(adr, 'm.muellerschneider@ab.bfw.local')

    def test_ersetze_mail_platzhalter(self):
        row = pd.Series(
            {
                'Vorname': 'Anna',
                'Nachname': 'Beispiel',
                'Anrede': 'Frau',
                'Zeitraum': 'Juni 2026',
                'Kurs': 'AP1',
                'Lernbereich': 'LB1',
            }
        )
        subject, body = ersetze_mail_platzhalter(
            'Hallo <<vorname>> <<nachname>>',
            'Kurs: <<kurs>> / Bereich: <<lernbereich>> / Zeitraum: <<zeitraum>>',
            row,
        )

        self.assertEqual(subject, 'Hallo Anna Beispiel')
        self.assertIn('Kurs: AP1', body)
        self.assertIn('Bereich: LB1', body)
        self.assertIn('Zeitraum: Juni 2026', body)

    def test_resolve_zusatzanhaenge(self):
        row = pd.Series(
            {
                'Vorname': 'Anna',
                'Nachname': 'Beispiel',
                'Anrede': 'Frau',
                'Zeitraum': 'Juni 2026',
                'Kurs': 'AP1',
                'Lernbereich': 'LB1',
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            basis = os.path.join(tmp, 'data', 'Zusatzmaterialien', 'LB1', 'Unterordner')
            os.makedirs(basis, exist_ok=True)
            datei = os.path.join(basis, 'Merkblatt_Anna.pdf')
            with open(datei, 'w', encoding='utf-8'):
                pass

            found, missing = resolve_zusatzanhaenge(['Merkblatt_<<vorname>>.pdf', 'Fehlt.pdf'], tmp, 'LB1', row)
            self.assertEqual(len(found), 1)
            self.assertTrue(found[0].endswith('Merkblatt_Anna.pdf'))
            self.assertEqual(missing, ['Fehlt.pdf'])

    def test_erstelle_outlook_entwurf_mehrere_anhaenge(self):
        class FakeAttachments:
            def __init__(self):
                self.paths = []

            def Add(self, path):
                self.paths.append(path)

        class FakeMail:
            def __init__(self):
                self.To = ''
                self.Subject = ''
                self.Body = ''
                self.Attachments = FakeAttachments()
                self.displayed = False

            def Display(self):
                self.displayed = True

        class FakeOutlook:
            def __init__(self):
                self.mail = FakeMail()

            def CreateItem(self, _):
                return self.mail

        outlook = FakeOutlook()
        erstelle_outlook_entwurf(outlook, 'a@b.c', 'S', 'B', ['a.txt', 'b.txt'])
        self.assertEqual(outlook.mail.Attachments.paths, ['a.txt', 'b.txt'])
        self.assertTrue(outlook.mail.displayed)


if __name__ == '__main__':
    unittest.main()
