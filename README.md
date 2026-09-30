# Emacs NXS 1.0.3

Portable NXS configuration derived from Emacs Solo, with themes, a bookmark
start page, Org, Org-roam, LaTeX, Dired and development tools.

Requires **Emacs 32.0.50 or newer**, Python 3 and internet access for installing
external Emacs packages. Emacs itself is not included. Tested on macOS only.

On macOS, install Apple Command Line Tools (or Xcode) and Homebrew first.
The installer checks Emacs, compiles and runs a C test using a matching Apple
compiler and SDK, installs missing PDF dependencies through Homebrew, downloads
all 14 Emacs packages and their dependencies, and builds and tests `epdfinfo`.

```sh
python3 install.py
```

Wait for the success message, then use the exact launch command printed by the
installer, normally:

```sh
/Applications/Emacs.app/Contents/MacOS/Emacs --init-directory "$HOME/.config/nxs-emacs"
```

No separate `M-x` installation step is required. Always use the same
`--init-directory`. The compiler selection is scoped to child processes; global
Xcode settings and shell configuration are unchanged. Homebrew dependencies
are installed into Homebrew's normal prefix. The ZIP does not bundle Emacs,
external packages or Homebrew libraries. Package versions are downloaded from
GNU ELPA, NonGNU ELPA and MELPA and are not pinned.

The installer refuses existing directories and symlinks. Use `--target PATH`
for a different destination or `--emacs PATH` for a different Emacs executable.
After a partial installation, fix the reported problem and run
`python3 install.py --resume` (with the same `--target`, if used). This preserves
all configuration edits and retries missing packages/PDF setup. See `install.log`
and `pdf-build.log` inside the destination for failures. Prerequisite failures
before copying are printed in Terminal; rerun without `--resume` in that case.
Resume accepts only directories marked by this installer. Install older releases
into a new destination instead of overwriting them.

`--config-only` explicitly skips dependency setup; it is not a complete install.
Automatic setup is macOS-only. Normal Emacs startup does not download or build
packages. The manual `M-x emacs-nxs/install-missing-packages` command remains
available for later Emacs-package maintenance.

Personal settings belong in the installed `var/private.el`. No private data,
history, installed packages, credentials or caches are distributed. Notes use
`~/org/roam`; create `~/org/agenda` before capturing agenda entries.

Optional external programs are needed for their respective features, including
TeX/latexmk/tabularray, Graphviz, spell checkers, language servers and formatters.
PDF Tools dependencies are handled by the installer. The preferred font is
JetBrainsMono Nerd Font. Linux and Windows have not been validated.

See `README.da.md` for the detailed Danish installation guide and `VALIDATION.md`
for verification results. Run installer tests with:

```sh
python3 -m unittest discover -s tests -v
```

Developed by Niels Søndergaard from Rahul Martim Juliato's Emacs Solo.
Existing source attribution is retained. GPL-3.0-or-later; see `COPYING`.

## Emacs Lisp

Paredit provides structured editing in Emacs Lisp and IELM, alongside the
existing completion, Eldoc and Flymake setup. `C-c e` groups evaluation (`d`,
`b`, `r`), IELM (`i`), Edebug (`e`), ERT (`t`), parenthesis checking (`p`),
documentation checking (`c`) and byte compilation (`k`). Evaluation runs code
in the current Emacs. Compilation asks before saving modified source.
Standard editing and evaluation bindings remain available.
