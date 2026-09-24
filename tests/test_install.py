import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import os
import subprocess

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

class SetupTests(unittest.TestCase):
    def test_resume_preserves_personal_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = installer.install(Path(tmp) / 'nxs')
            (target / 'init.el').write_text('my edits')
            self.assertEqual(installer.resume_target(target), target)
            self.assertEqual((target / 'init.el').read_text(), 'my edits')

    def test_resume_refuses_unmarked_directory_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                installer.resume_target(tmp)
            target = installer.install(Path(tmp) / 'nxs')
            link = Path(tmp) / 'link'
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                installer.resume_target(link)

    def test_compiler_pair_is_scoped_and_actually_tested(self):
        original = {'PATH': '/usr/bin:/bin', 'SDKROOT': '/wrong/sdk', 'CC': 'wrong',
                    'CFLAGS': '-bad', 'TOOLCHAINS': 'wrong'}
        calls = []
        def fake_output(command, env):
            calls.append((command, env.copy()))
            if command[0].endswith('xcode-select'):
                return '/Applications/Xcode.app/Contents/Developer'
            self.assertEqual(env['DEVELOPER_DIR'], '/Library/Developer/CommandLineTools')
            self.assertNotIn('CFLAGS', env)
            self.assertNotIn('TOOLCHAINS', env)
            if '--show-sdk-path' in command:
                return '/matching/sdk'
            if '--find' in command:
                return '/matching/' + command[-1]
            self.assertEqual(env['SDKROOT'], '/matching/sdk')
            return ''
        with patch.object(installer.Path, 'is_dir', return_value=True), patch.object(installer, 'output', side_effect=fake_output):
            env = installer.compiler_environment(original)
        self.assertEqual(original['SDKROOT'], '/wrong/sdk')
        self.assertEqual(env['CC'], '/matching/clang')
        self.assertTrue(any('-isysroot' in cmd for cmd, _ in calls))
        self.assertTrue(any(cmd[0].endswith('/test') for cmd, _ in calls))

    def test_failed_compiler_does_not_report_success(self):
        with patch.object(installer.Path, 'is_dir', return_value=True), patch.object(installer, 'output', side_effect=subprocess.CalledProcessError(1, 'clang', output='unknown architecture')):
            with self.assertRaisesRegex(ValueError, 'unknown architecture'):
                installer.compiler_environment({'PATH': '/usr/bin'})

    def test_batch_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / 'fake emacs'
            executable.write_text('#!/bin/sh\necho "simulated package failure"\nexit 1\n')
            executable.chmod(0o755)
            with self.assertRaisesRegex(ValueError, 'Pakkeinstallationen fejlede'):
                installer.setup(Path(tmp), str(executable), os.environ)
            self.assertIn('simulated package failure', (Path(tmp) / 'install.log').read_text())

    def test_default_install_invokes_setup(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'fresh'
            with patch('sys.argv', ['install.py', '--target', str(target)]), patch.object(installer.sys, 'platform', 'darwin'), patch.object(installer, 'find_emacs', return_value='/fake/emacs'), patch.object(installer, 'compiler_environment', side_effect=lambda env: env), patch.object(installer, 'ensure_pdf_dependencies'), patch.object(installer, 'setup') as setup:
                self.assertEqual(installer.main(), 0)
                self.assertEqual(setup.call_args.args[0], target)

    def test_config_only_does_not_install_packages(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('sys.argv', ['install.py', '--target', str(Path(tmp) / 'fresh'), '--config-only']), patch.object(installer, 'setup') as setup:
                self.assertEqual(installer.main(), 0)
                setup.assert_not_called()

    def test_missing_pdf_library_is_installed_and_rechecked(self):
        installed = False
        def fake_run(command, **kwargs):
            nonlocal installed
            if command[0] == '/fake/brew':
                self.assertEqual(command, ['/fake/brew', 'install', 'poppler'])
                installed = True
                return subprocess.CompletedProcess(command, 0)
            missing = command[-1] in ('poppler', 'poppler-glib') and not installed
            return subprocess.CompletedProcess(command, int(missing))
        with patch.object(installer.shutil, 'which', side_effect=lambda name, **kwargs: '/fake/' + name), patch.object(installer.subprocess, 'run', side_effect=fake_run):
            installer.ensure_pdf_dependencies({'PATH': '/fake'})
        self.assertTrue(installed)

    def test_missing_homebrew_is_actionable_failure(self):
        with patch.object(installer.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(ValueError, 'Installér Homebrew'):
                installer.ensure_pdf_dependencies({'PATH': '/empty'})

    def test_failed_setup_can_be_resumed_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'fresh'
            with patch('sys.argv', ['install.py', '--target', str(target)]), patch.object(installer.sys, 'platform', 'darwin'), patch.object(installer, 'find_emacs', return_value='/fake/emacs'), patch.object(installer, 'compiler_environment', side_effect=lambda env: env), patch.object(installer, 'ensure_pdf_dependencies'), patch.object(installer, 'setup', side_effect=ValueError('download failed')):
                self.assertEqual(installer.main(), 1)
            (target / 'init.el').write_text('preserve edits')
            with patch('sys.argv', ['install.py', '--resume', '--target', str(target)]), patch.object(installer.sys, 'platform', 'darwin'), patch.object(installer, 'find_emacs', return_value='/fake/emacs'), patch.object(installer, 'compiler_environment', side_effect=lambda env: env), patch.object(installer, 'ensure_pdf_dependencies'), patch.object(installer, 'setup'):
                self.assertEqual(installer.main(), 0)
            self.assertEqual((target / 'init.el').read_text(), 'preserve edits')

if __name__ == '__main__':
    unittest.main()
