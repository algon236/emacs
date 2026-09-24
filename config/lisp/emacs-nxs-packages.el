;;; emacs-nxs-packages.el --- Install NXS dependencies -*- lexical-binding: t; -*-
;; Copyright (C) 2026 Niels Søndergaard
;; SPDX-License-Identifier: GPL-3.0-or-later

;;; Commentary:
;; Shared package definitions for normal startup and the isolated installer.

;;; Code:
(require 'package)
(require 'seq)
(setq package-user-dir (expand-file-name "elpa" user-emacs-directory)
      package-archives '(("gnu" . "https://elpa.gnu.org/packages/")
                         ("nongnu" . "https://elpa.nongnu.org/nongnu/")
                         ("melpa" . "https://melpa.org/packages/"))
      package-archive-priorities '(("gnu" . 30) ("nongnu" . 20) ("melpa" . 10)))
(package-initialize)

(defconst emacs-nxs-required-packages
  '(auctex card-games casual dired-subtree eat nerd-icons nerd-icons-dired
    org-draw org-modern org-roam org-roam-ui paredit pdf-tools)
  "External packages required by NXS, excluding automatic dependencies.")

(defun emacs-nxs/install-missing-packages ()
  "Install all missing NXS packages, propagating any installation failure."
  (interactive)
  (let ((missing (seq-remove #'package-installed-p emacs-nxs-required-packages)))
    (when missing
      (package-refresh-contents)
      (dolist (package missing)
        (unless (assq package package-archive-contents)
          (error "Pakken %s findes ikke i de hentede pakkelister; prøv igen senere" package)))
      (mapc #'package-install missing))
    (when (seq-remove #'package-installed-p emacs-nxs-required-packages)
      (error "Ikke alle NXS-pakker blev installeret"))
    (message "NXS-pakkerne er installeret. Genstart Emacs efter installationen.")))

(defun emacs-nxs/build-and-check-pdf ()
  "Build epdfinfo synchronously if needed, then test rendering a PDF page."
  (require 'pdf-tools)
  (setq pdf-info-epdfinfo-program
        (expand-file-name "epdfinfo" (file-name-directory (locate-library "pdf-tools"))))
  (unless (ignore-errors (pdf-info-check-epdfinfo) t)
    (let* ((default-directory (pdf-tools-locate-build-directory))
           (target (file-name-directory (locate-library "pdf-tools")))
           (log (expand-file-name "pdf-build.log" user-emacs-directory)))
      (unless default-directory (error "PDF Tools build sources are missing"))
      (with-temp-buffer
        (let ((status (call-process "/bin/sh" nil (list (current-buffer) t) t
                                    "./autobuild" "-D" "-i" target)))
          (write-region (point-min) (point-max) log nil 'silent)
          (unless (eq status 0)
            (error "PDF-bygningen fejlede; se %s og %sconfig.log" log default-directory))))
      (setq pdf-info-epdfinfo-program (expand-file-name "epdfinfo" target))))
  (pdf-info-check-epdfinfo)
  (message "PDF-hjælperen er bygget og har gengivet en PDF-side korrekt."))

(provide 'emacs-nxs-packages)
;;; emacs-nxs-packages.el ends here
