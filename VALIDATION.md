# Validation — 2026-09-20

Platform: macOS, GNU Emacs 32.0.50 (build dated 2026-08-19).

- Installer tests: fresh installation, refusal to overwrite an existing
  installation, refusal to follow a dangling destination symlink, and exclusion
  of private runtime state passed (3 tests).
- Configuration loaded with early-init.el and init.el in a separate HOME and
  installation directory. Startup hooks and bookmark dashboard were exercised.
- All 13 declared external packages were downloaded and installed, with their
  dependencies, into the temporary installation. A fresh Emacs process then
  loaded the configuration and dashboard successfully with all declared
  packages present and no startup error in the log.
- A separate empty-HOME test also exercises first startup before package
  installation. Missing-package warnings are expected in that case.
- Configuration contains no excluded personal-information module, its bindings
  or dashboard integration, and no /Users/ paths. Author credit is retained.
- Original copied source files were checked against their pre-copy SHA-256
  hashes and were unchanged.
- Distribution ZIP is checked for archive integrity, extracted, and its
  installer and overwrite tests are run again. SHA-256 is supplied alongside it.

These are automated startup and installation checks, not a visual GUI review
or an exhaustive exercise of every editor command. TeX export, language servers,
external tools, Linux and Windows have not been validated. Dependencies are
fetched from live package archives and can change after this validation.
