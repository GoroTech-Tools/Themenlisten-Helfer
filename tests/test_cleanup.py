import os
import sys
import tempfile
import time
import unittest


SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from cleanup import loesche_alte_dateien


class TestCleanup(unittest.TestCase):
    def test_loesche_alte_dateien(self):
        logs = []

        def cb(msg: str):
            logs.append(msg)

        with tempfile.TemporaryDirectory() as tmp:
            old_docx = os.path.join(tmp, 'alt.docx')
            new_docx = os.path.join(tmp, 'neu.docx')
            old_txt = os.path.join(tmp, 'alt.txt')

            for path in (old_docx, new_docx, old_txt):
                with open(path, 'w', encoding='utf-8'):
                    pass

            now = time.time()
            two_days = 2 * 24 * 60 * 60
            os.utime(old_docx, (now - two_days, now - two_days))
            os.utime(old_txt, (now - two_days, now - two_days))

            geloescht = loesche_alte_dateien(tmp, cb)

            self.assertEqual(geloescht, 1)
            self.assertFalse(os.path.exists(old_docx))
            self.assertTrue(os.path.exists(new_docx))
            self.assertTrue(os.path.exists(old_txt))
            self.assertTrue(any('Alte Themenlisten gelöscht: 1' in m for m in logs))


if __name__ == '__main__':
    unittest.main()
