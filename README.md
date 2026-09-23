# Emacs NXS 1.0.0

Portable NXS configuration derived from Emacs Solo, with themes, a bookmark
start page, Org, Org-roam, LaTeX, Dired and development tools.

Requires **Emacs 32.0.50 or newer**, Python 3 and internet access for installing
external Emacs packages. Emacs itself is not included. Tested on macOS only.

```sh
python3 install.py
emacs --init-directory "$HOME/.config/nxs-emacs"
```

On the first start, run `M-x emacs-nxs/install-missing-packages`, wait for it to
finish, then restart using the same command. Package versions are downloaded
from GNU ELPA, NonGNU ELPA and MELPA and are not pinned.

The installer refuses to overwrite an existing directory or symlink. Use
`--target PATH` to select a different directory, and pass that same directory
to Emacs with `--init-directory` on every start.

Personal settings belong in the installed `var/private.el`. No private data,
history, installed packages, credentials or caches are distributed. Notes use
`~/org/roam`; create `~/org/agenda` before capturing agenda entries.

Optional external programs are needed for their respective features, including
TeX/latexmk/tabularray, Graphviz, spell checkers, language servers and formatters.
PDF Tools may require build tools and Poppler. The preferred font is
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
