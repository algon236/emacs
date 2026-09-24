#!/usr/bin/env python3
"""Build the portable distribution from an explicit file allowlist."""
from pathlib import Path
import hashlib
import zipfile

root = Path(__file__).resolve().parent
version = (root / 'VERSION').read_text().strip()
name = f'emacs-nxs-{version}'
out = root / 'dist'
out.mkdir(exist_ok=True)
files = [root / p for p in ('README.md', 'README.da.md', 'COPYING', 'VERSION',
                           'VALIDATION.md', 'install.py', 'bootstrap.el', 'build.py', '.gitignore',
                           'tests/test_install.py', 'tests/smoke.el')]
files += [root / 'config/early-init.el', root / 'config/init.el', root / 'config/lisp/LICENSE', root / 'config/images/ringe.png']
files += sorted((root / 'config/lisp').glob('*.el'))
files += sorted((root / 'config/var/templates').glob('*'))
archive = out / f'{name}.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in files:
        z.write(path, f'{name}/{path.relative_to(root).as_posix()}')
checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
(archive.with_suffix('.zip.sha256')).write_text(f'{checksum}  {archive.name}\n')
print(f'{archive}\nSHA256 {checksum}')
