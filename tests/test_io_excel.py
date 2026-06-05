import os
import sys
import unittest

import pandas as pd


SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from io_excel import finde_mailkonfiguration


class TestIoExcel(unittest.TestCase):
    def test_finde_mailkonfiguration_vorhanden(self):
        df = pd.DataFrame(
            {
                'TemplateBezeichnung': ['Themenliste_LB1'],
                'Subject': ['Hallo <<vorname>>'],
                'BodyText': ['Zeile1\\nZeile2'],
            }
        )

        result = finde_mailkonfiguration(df, 'Themenliste_LB1')
        self.assertIsNotNone(result)
        subject, body = result or ('', '')
        self.assertEqual(subject, 'Hallo <<vorname>>')
        self.assertEqual(body, 'Zeile1\nZeile2')

    def test_finde_mailkonfiguration_nicht_vorhanden(self):
        df = pd.DataFrame(
            {
                'TemplateBezeichnung': ['Themenliste_LB2'],
                'Subject': ['X'],
                'BodyText': ['Y'],
            }
        )

        result = finde_mailkonfiguration(df, 'Themenliste_LB1')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
