#!/usr/bin/env python3
"""Install NXS configuration without replacing an existing installation."""
import argparse
from pathlib import Path
import shutil
import sys


def install(target):
    target = Path(target).expanduser().absolute()
    if target.exists() or target.is_symlink():
        raise FileExistsError(f'Installation already exists: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(Path(__file__).resolve().parent / 'config', target)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', default='~/.config/nxs-emacs', help='New configuration directory')
    args = parser.parse_args()
    try:
        target = install(args.target)
    except (OSError, shutil.Error) as error:
        print(error, file=sys.stderr)
        return 1
    print(f'Installed: {target}\nStart with: emacs --init-directory "{target}"\nThen run M-x emacs-nxs/install-missing-packages and restart Emacs.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
