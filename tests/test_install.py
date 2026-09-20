import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallationTests(unittest.TestCase):
    def test_install_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'config'
            installer.install(target)
            self.assertEqual((target / 'init.el').read_bytes(), (ROOT / 'config/init.el').read_bytes())
            marker = target / 'my-notes'
            marker.write_text('preserve me')
            with self.assertRaises(FileExistsError):
                installer.install(target)
            self.assertEqual(marker.read_text(), 'preserve me')

    def test_refuse_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'config'
            target.symlink_to(Path(tmp) / 'missing')
            with self.assertRaises(FileExistsError):
                installer.install(target)
            self.assertTrue(target.is_symlink())

    def test_distribution_has_no_private_runtime_state(self):
        for path in (ROOT / 'config').rglob('*'):
            self.assertNotIn('perinf', str(path).lower())
            self.assertNotIn(path.name, ['private.el', 'custom.el', '.DS_Store', '.git', 'elpa', 'cache'])
            if path.is_file() and path.suffix in ['.el', '.org', '.tex']:
                content = path.read_text()
                self.assertNotIn('perinf', content.lower())
                self.assertNotIn('/Users/', content)

if __name__ == '__main__':
    unittest.main()
