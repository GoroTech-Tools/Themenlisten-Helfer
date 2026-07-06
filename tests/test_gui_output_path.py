import os
import unittest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GUI_PATH = os.path.join(REPO_ROOT, 'src', 'gui.py')


class TestGuiOutputPath(unittest.TestCase):
    def test_gui_nutzt_root_themenlisten_als_ausgabeordner(self):
        with open(GUI_PATH, 'r', encoding='utf-8') as f:
            source = f.read()

        self.assertEqual(source.count("os.path.join(app_dir, 'Themenlisten')"), 3)
        self.assertNotIn("os.path.join(app_dir, 'output', 'Themenlisten')", source)


if __name__ == '__main__':
    unittest.main()
