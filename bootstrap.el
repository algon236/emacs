;;; bootstrap.el --- Batch installation entry point -*- lexical-binding: t; -*-
;; Copyright (C) 2026 Niels Søndergaard
;; SPDX-License-Identifier: GPL-3.0-or-later
;;; Code:
(unless (getenv "NXS_INSTALL_TARGET") (error "NXS_INSTALL_TARGET is required"))
(setq user-emacs-directory (file-name-as-directory (getenv "NXS_INSTALL_TARGET"))
      native-comp-jit-compilation nil
      package-native-compile nil)
(when (version< emacs-version "32.0.50") (error "NXS kræver Emacs 32.0.50 eller nyere"))
(load (expand-file-name "lisp/emacs-nxs-packages.el" user-emacs-directory) nil t)
(emacs-nxs/install-missing-packages)
(emacs-nxs/build-and-check-pdf)
(princ "NXS-INSTALL-OK\n")
;;; bootstrap.el ends here
