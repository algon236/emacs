# Emacs NXS 1.0.0

En selvstændig installationspakke af NXS-konfigurationen med temaer, startside,
bogmærker, Org, Org-roam, LaTeX, Dired og programmeringsværktøjer.

## Krav

- Emacs **32.0.50 eller nyere**. Konfigurationens eget versionskrav er bevaret;
  den er ikke en pakke til Emacs 29, 30 eller 31.
- Python 3 til installationsprogrammet.
- Internet ved installation af eksterne Emacs-pakker.
- macOS er testplatformen. Linux og Windows er ikke valideret.

Emacs selv følger ikke med. JetBrainsMono Nerd Font er den foretrukne skrifttype.
Ekstra funktioner kan kræve andre programmer: en TeX-distribution med LuaLaTeX,
latexmk og tabularray til LaTeX, Graphviz til grafer, stavekontrolprogram med
ordbøger, samt de relevante sprogservere og formatteringsprogrammer. PDF Tools
kan kræve byggeværktøjer og Poppler til sin epdfinfo-hjælper. Disse følger ikke med.

## Installation på en ny computer

Pak ZIP-filen ud, og åbn en terminal i den udpakkede mappe:

```sh
python3 install.py
emacs --init-directory "$HOME/.config/nxs-emacs"
```

Installationsprogrammet opretter `~/.config/nxs-emacs`. Det afviser både en
allerede eksisterende mappe og et eksisterende symbolsk link. Det ændrer ikke
andre Emacs-installationer eller computerens automatiske opstart.

Ved første start køres:

```text
M-x emacs-nxs/install-missing-packages
```

Vent på at installationen er færdig, luk denne Emacs, og start igen med samme
kommando. Brug altid `--init-directory`, også ved senere starter. På macOS kan
hele stien `/Applications/Emacs.app/Contents/MacOS/Emacs` bruges, hvis `emacs`
ikke er tilgængelig i terminalens søgesti.

Pakkelisten omfatter auctex, card-games, casual, dired-subtree, eat, nerd-icons,
nerd-icons-dired, org-draw, org-modern, org-roam, org-roam-ui og pdf-tools.
Afhængigheder installeres med dem. Der hentes aktuelle versioner fra GNU ELPA,
NonGNU ELPA og MELPA; distributionen indeholder ikke fastlåste pakkekopier.
Normal opstart henter ikke automatisk manglende pakker.

En anden installationsmappe kan vælges:

```sh
python3 install.py --target "$HOME/.config/min-emacs"
emacs --init-directory "$HOME/.config/min-emacs"
```

## Egne indstillinger og dokumenter

Egne indstillinger kan lægges i installationens `var/private.el`, som indlæses
efter opstart. Filen følger ikke med. Eksempel:

```elisp
(setq user-full-name "Dit navn"
      user-mail-address "din-mail@example.com")
```

Standardmapperne er `~/org/agenda` til dagsorden og `~/org/roam` til noter.
Opret dagsordensmappen før første capture. Org-roam opretter sin notemappe.
Skabeloner ligger i `var/templates`; tilpas dem efter behov. De medfølgende
skabeloner kræver ikke den oprindelige computers personlige include-filer.
Sundhedsrapporternes standardmappe er `~/org/health`; selve dataene følger ikke med.

## Indhold og oprindelse

Pakken er afledt af NXS-konfigurationen den 20. september 2026. Den bevarer
kildekodens forfatterangivelser og GPL-3.0-or-later-licens. NXS er videreudviklet
af Niels Søndergaard fra Rahul Martim Juliatos Emacs Solo. Se `COPYING` og
licensoplysningerne i kildefilerne.

Startsiden viser bogmærker og systeminformation. Personlige data, historik,
bogmærkefiler, adgangsoplysninger, installerede pakker, kompilerede filer og
maskinens cache følger ikke med.

## Kontrol og afinstallation

```sh
python3 -m unittest discover -s tests -v
```

`tests/smoke.el` kontrollerer opstart og startside i en separat testinstallation;
sæt `HOME` til en tom testmappe og `NXS_TEST_CONFIG` til den installerede kopi.
Se `VALIDATION.md` for den udførte kontrol og dens begrænsninger.

For at afinstallere: luk den Emacs, som bruger pakken, og fjern den valgte
installationsmappe efter at have gemt eventuelle egne indstillinger.
Dokumenterne i `~/org` ligger uden for installationsmappen.
