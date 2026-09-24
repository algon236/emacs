# Validation — 2026-09-24 — NXS 1.0.1

Platform: macOS on Apple Silicon, GNU Emacs 32.0.50.

- 13 installer tests passed: overwrite and symlink protection, private-state
  exclusion, marked-directory resume with personal edits preserved, default
  automatic setup, explicit configuration-only mode, scoped compiler/SDK
  selection including compilation and execution, compiler failure reporting,
  PDF dependency installation and recheck, missing Homebrew reporting, recorded
  batch failures, and failure followed by successful resume.
- A real installation ran with an empty HOME and an empty destination containing
  a space in its name. All 14 declared Emacs packages and their dependencies were
  fetched from live archives. epdfinfo was built from source in that destination;
  pdf-info-check-epdfinfo successfully rendered its test PDF page.
- The compiler preflight selected CommandLineTools with its own SDK, compiled a
  minimal C program, and executed it. No global developer-directory change was
  made. Existing Homebrew libraries on the test Mac were reused; installing
  absent Homebrew libraries was covered by mocked tests, not a second pristine Mac.
- A fresh Emacs process loaded early-init.el and init.el from the installed
  destination, ran startup hooks, refreshed the bookmark dashboard, confirmed
  all declared packages, and passed the PDF rendering check. No startup errors
  or NXS missing-package warnings appeared.
- Resume completed on the installed test copy. No package downloads or helper
  rebuild were needed. Failure/resume preserving edits is also covered by tests.
- Parenthesis checks passed for configuration Lisp files and installation/test
  entry points. Git whitespace checks passed.
- The release ZIP was integrity-checked, extracted, privacy-screened, and its
  installer tests were run from the extracted copy. Configuration-only copying
  was also exercised from the extracted distribution. A SHA-256 file accompanies
  the ZIP.

This verifies automated installation, startup and PDF helper rendering, not a
visual GUI review or every editor command. Emacs, Python, Apple development tools
and (when libraries are missing) Homebrew remain prerequisites. TeX export,
language servers, Linux and Windows are not validated. External packages are
fetched from live archives and may change after this validation.
