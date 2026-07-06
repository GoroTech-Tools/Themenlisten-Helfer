import os
import unittest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GUI_PATH = os.path.join(REPO_ROOT, 'src', 'gui.py')


class TestGuiResourceDirs(unittest.TestCase):
    def test_get_resource_dirs_priorisiert_app_dir_vor_meipass(self):
        with open(GUI_PATH, 'r', encoding='utf-8') as f:
            source = f.read()

        self.assertIn("dirs: list[str] = [get_app_dir()]", source)
        self.assertIn("dirs.append(meipass)", source)
        self.assertIn("if meipass not in dirs:", source)


if __name__ == '__main__':
    unittest.main()
