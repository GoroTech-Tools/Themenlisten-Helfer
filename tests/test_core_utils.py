import os
import sys
import tempfile
import unittest

import pandas as pd


SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from core_utils import ersetze_umlaute, finde_vorlagen, filter_verarbeitbare_teilnehmende


class TestCoreUtils(unittest.TestCase):
    def test_ersetze_umlaute(self):
        self.assertEqual(ersetze_umlaute('Jörg Weiß'), 'Joerg Weiss')
        self.assertEqual(ersetze_umlaute('ÄÖÜäöüß'), 'aeoeueaeoeuess')

    def test_finde_vorlagen_ohne_lernbereich(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, 'Themenliste_A.docx'), 'w', encoding='utf-8').close()
            open(os.path.join(tmp, 'Themenliste_B.dotm'), 'w', encoding='utf-8').close()
            open(os.path.join(tmp, 'not-a-template.txt'), 'w', encoding='utf-8').close()

            result = finde_vorlagen(tmp)
            self.assertEqual(len(result), 2)
            self.assertTrue(any(path.endswith('.docx') for path in result))
            self.assertTrue(any(path.endswith('.dotm') for path in result))

    def test_finde_vorlagen_mit_lernbereich(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, 'Themenliste_LB1_A.docx'), 'w', encoding='utf-8').close()
            open(os.path.join(tmp, 'Themenliste_LB2_A.docx'), 'w', encoding='utf-8').close()

            result = finde_vorlagen(tmp, 'LB1')
            self.assertEqual(len(result), 1)
            self.assertIn('Themenliste_LB1_A.docx', os.path.basename(result[0]))

    def test_filter_verarbeitbare_teilnehmende(self):
        df = pd.DataFrame(
            {
                'Name': ['A', 'B', 'C', 'D', 'E'],
                'Verarbeiten': ['ja', ' JA ', 'nein', None, 'Ja'],
            }
        )

        result = filter_verarbeitbare_teilnehmende(df)
        self.assertEqual(result['Name'].tolist(), ['A', 'B', 'E'])

    def test_filter_verarbeitbare_teilnehmende_ohne_spalte(self):
        df = pd.DataFrame({'Name': ['A', 'B']})
        result = filter_verarbeitbare_teilnehmende(df)
        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()
