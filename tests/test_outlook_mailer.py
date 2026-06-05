import os
import sys
import unittest

import pandas as pd


SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from outlook_mailer import ermittle_empfaengeradresse, ersetze_mail_platzhalter


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


if __name__ == '__main__':
    unittest.main()
