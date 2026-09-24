#!/usr/bin/env python3
"""Install NXS, its Emacs packages and a verified PDF helper on macOS."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MARKER = '.nxs-install.json'


def install(target):
    target = Path(target).expanduser().absolute()
    if target.exists() or target.is_symlink():
        raise FileExistsError(f'Mappen findes allerede: {target}. Brug --resume for at fortsætte en NXS-installation.')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'config', target)
    (target / MARKER).write_text(json.dumps({'installer': 'emacs-nxs'}))
    return target


def resume_target(target):
    target = Path(target).expanduser().absolute()
    if target.is_symlink() or not target.is_dir():
        raise ValueError('Genoptagelse kræver en eksisterende installationsmappe, ikke et symbolsk link.')
    marker = target / MARKER
    if not marker.is_file() or json.loads(marker.read_text()).get('installer') != 'emacs-nxs':
        raise ValueError('Mappen er ikke oprettet af dette installationsprogram. Vælg en ny mappe med --target.')
    if not (target / 'lisp/emacs-nxs-packages.el').is_file():
        raise ValueError('Installationen mangler pakkemodulet. Installér i en ny mappe med --target.')
    return target


def output(command, env):
    return subprocess.check_output(command, env=env, text=True, stderr=subprocess.STDOUT).strip()


def find_emacs(explicit, env):
    candidates = ([explicit] if explicit else
                  ['/Applications/Emacs.app/Contents/MacOS/Emacs', shutil.which('emacs', path=env['PATH'])])
    for candidate in candidates:
        if candidate and (shutil.which(candidate, path=env['PATH']) or Path(candidate).is_file()):
            executable = shutil.which(candidate, path=env['PATH']) or candidate
            output([executable, '--batch', '-Q', '--eval',
                    '(when (version< emacs-version "32.0.50") (error "NXS requires Emacs 32.0.50 or newer"))'], env)
            return executable
    raise ValueError('Emacs blev ikke fundet. Installér Emacs 32.0.50 eller nyere, eller angiv --emacs /sti/til/Emacs.')


def compiler_environment(base):
    """Select a matching compiler/SDK pair, compiling AND running a probe."""
    candidates = ['/Library/Developer/CommandLineTools']
    try:
        candidates.append(output(['/usr/bin/xcode-select', '-p'], base))
    except subprocess.CalledProcessError:
        pass
    candidates.append('/Applications/Xcode.app/Contents/Developer')
    errors = []
    for directory in dict.fromkeys(candidates):
        if not Path(directory).is_dir():
            continue
        env = base.copy()
        # Do not let inherited SDK/compiler overrides recreate the mixed toolchain.
        for key in ('SDKROOT', 'TOOLCHAINS', 'CC', 'CXX', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS',
                    'CPATH', 'LIBRARY_PATH', 'CPLUS_INCLUDE_PATH', 'C_INCLUDE_PATH',
                    'MACOSX_DEPLOYMENT_TARGET'):
            env.pop(key, None)
        env['DEVELOPER_DIR'] = directory
        try:
            env['SDKROOT'] = output(['/usr/bin/xcrun', '--sdk', 'macosx', '--show-sdk-path'], env)
            env['CC'] = output(['/usr/bin/xcrun', '--find', 'clang'], env)
            env['CXX'] = output(['/usr/bin/xcrun', '--find', 'clang++'], env)
            with tempfile.TemporaryDirectory(prefix='nxs-compiler-') as tmp:
                source, binary = Path(tmp) / 'test.c', Path(tmp) / 'test'
                source.write_text('int main(void) { return 0; }\n')
                output([env['CC'], '-isysroot', env['SDKROOT'], str(source), '-o', str(binary)], env)
                output([str(binary)], env)
            print(f'Compiler og SDK kontrolleret: {directory}', flush=True)
            return env
        except (OSError, subprocess.CalledProcessError) as error:
            errors.append(f'{directory}: {getattr(error, "output", str(error))}')
    raise ValueError('Ingen fungerende Apple-compiler/SDK-kombination. Opdatér Command Line Tools '
                     'via Systemindstillinger → Generelt → Softwareopdatering, '
                     'eller installér dem med xcode-select --install.\n' + '\n'.join(errors))


def ensure_pdf_dependencies(env):
    tools = {'autoreconf': 'autoconf', 'automake': 'automake', 'pkg-config': 'pkgconf'}
    libraries = {'libpng': 'libpng', 'glib-2.0': 'glib', 'poppler': 'poppler',
                 'poppler-glib': 'poppler', 'zlib': 'zlib'}
    def missing():
        required = {formula for tool, formula in tools.items()
                    if not shutil.which(tool, path=env['PATH'])}
        pkg = shutil.which('pkg-config', path=env['PATH'])
        for library, formula in libraries.items():
            if not pkg or subprocess.run([pkg, '--exists', library], env=env).returncode:
                required.add(formula)
        return sorted(required)
    required = missing()
    if required:
        brew = shutil.which('brew', path=env['PATH'])
        if not brew:
            raise ValueError('PDF Tools mangler: ' + ', '.join(required) +
                             '. Installér Homebrew fra https://brew.sh og kør installationen igen.')
        print('Installerer PDF-afhængigheder med Homebrew: ' + ', '.join(required), flush=True)
        subprocess.run([brew, 'install', *required], env=env, check=True)
        if missing():
            raise ValueError('PDF-afhængigheder mangler stadig: ' + ', '.join(missing()))
    if not shutil.which('make', path=env['PATH']):
        raise ValueError('make mangler; opdatér Apples Command Line Tools.')


def setup(target, emacs, env):
    env = dict(env, NXS_INSTALL_TARGET=str(target))
    log = target / 'install.log'
    with log.open('a') as stream:
        with subprocess.Popen([emacs, '--batch', '-Q', '--load', str(ROOT / 'bootstrap.el')],
                              env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, bufsize=1) as process:
            for line in process.stdout:
                print(line, end='', flush=True)
                stream.write(line)
                stream.flush()
            if process.wait():
                raise ValueError(f'Pakkeinstallationen fejlede. Se {log}; PDF-bygningen har sin egen pdf-build.log.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', default='~/.config/nxs-emacs', help='Installationsmappe')
    parser.add_argument('--emacs', help='Sti til Emacs 32.0.50 eller nyere')
    parser.add_argument('--resume', action='store_true', help='Fortsæt uden at kopiere eller overskrive konfigurationen')
    parser.add_argument('--config-only', action='store_true', help='Kopiér kun konfigurationen; installér ikke afhængigheder')
    args = parser.parse_args()
    target = None
    try:
        if args.resume:
            target = resume_target(args.target)
        else:
            candidate = Path(args.target).expanduser().absolute()
            if candidate.exists() or candidate.is_symlink():
                raise FileExistsError(f'Mappen findes allerede: {candidate}. Brug --resume eller vælg en ny --target.')
        if args.config_only:
            target = target or install(args.target)
            print(f'Kun konfigurationen er kopieret: {target}. Afhængighederne er ikke installeret.')
            print(f'Færdiggør med: python3 install.py --resume --target {shlex.quote(str(target))}')
            return 0
        if sys.platform != 'darwin':
            raise ValueError('Automatisk installation understøtter macOS. Brug --config-only til manuel installation på andre systemer.')
        env = os.environ.copy()
        env['PATH'] = '/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:' + env.get('PATH', '/usr/bin:/bin')
        # Include keg-only zlib/libffi metadata without changing the user's shell.
        extra = [f'{prefix}/opt/{name}/lib/pkgconfig' for prefix in ('/opt/homebrew', '/usr/local')
                 for name in ('zlib', 'libffi')]
        env['PKG_CONFIG_PATH'] = os.pathsep.join(extra + [env.get('PKG_CONFIG_PATH', '')])
        emacs = find_emacs(args.emacs, env)
        env = compiler_environment(env)
        ensure_pdf_dependencies(env)
        target = target or install(args.target)
        setup(target, emacs, env)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Installation IKKE færdig: {error}', file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.output:
            print(error.output, file=sys.stderr)
        if target:
            print(f'Fortsæt med: python3 install.py --resume --target {shlex.quote(str(target))}', file=sys.stderr)
        return 1
    print(f'Installation færdig; Emacs-pakker og PDF-hjælper er kontrolleret.\nStart med:\n'
          f'{shlex.quote(emacs)} --init-directory {shlex.quote(str(target))}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
