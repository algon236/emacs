# Emacs NXS 1.0.1

En selvstændig installationspakke af NXS-konfigurationen med temaer, startside,
bogmærker, Org, Org-roam, LaTeX, Dired og programmeringsværktøjer.

## Krav

- Emacs **32.0.50 eller nyere**. Konfigurationens eget versionskrav er bevaret;
  den er ikke en pakke til Emacs 29, 30 eller 31.
- Python 3 til installationsprogrammet.
- Internet under installationen.
- Apples Command Line Tools eller Xcode, der kan bygge programmer til den aktuelle macOS-version.
- Homebrew, hvis PDF-bibliotekerne ikke allerede er installeret.
- macOS er testplatformen. Linux og Windows er ikke valideret.

Emacs selv følger ikke med. JetBrainsMono Nerd Font er den foretrukne skrifttype.
Ekstra funktioner kan kræve andre programmer: en TeX-distribution med LuaLaTeX,
latexmk og tabularray til LaTeX, Graphviz til grafer, stavekontrolprogram med
ordbøger, samt de relevante sprogservere og formatteringsprogrammer. PDF Tools kræver en compiler og bl.a. Poppler. Installationsprogrammet kontrollerer
disse og installerer manglende PDF-afhængigheder via en eksisterende Homebrew-installation.
Selve Homebrew og Apples udviklingsværktøjer skal være installeret på forhånd.
Hvis de mangler eller er defekte, stopper programmet med en forklaring.

## Installation på en ny computer

Pak ZIP-filen ud, og åbn en terminal i den udpakkede mappe:

```sh
python3 install.py
```

Denne ene kommando:

1. Finder Emacs og kontrollerer versionskravet.
2. Vælger et sammenhængende Apple-værktøjssæt og SDK og bygger og kører et lille testprogram.
3. Installerer manglende PDF-biblioteker og byggeværktøjer via Homebrew.
4. Kopierer konfigurationen til `~/.config/nxs-emacs` og henter alle 14 Emacs-pakker med deres afhængigheder.
5. Bygger PDF-hjælperen `epdfinfo`, hvis nødvendigt, og kontrollerer, at den kan gengive en PDF-side.

Vent på beskeden **Installation færdig**. Programmet viser derefter den præcise
startkommando. Med Emacs i den normale Mac-mappe er den:

```sh
/Applications/Emacs.app/Contents/MacOS/Emacs --init-directory "$HOME/.config/nxs-emacs"
```

Du skal ikke køre en særskilt pakkeinstallationskommando inde i Emacs.
Brug samme `--init-directory` ved senere starter. Hvis Emacs ligger et andet sted,
kan installationsprogrammet få stien med `--emacs /sti/til/Emacs`.

Apple-værktøjer vælges kun for installationens egne processer. Programmet ændrer
ikke Mac'ens globale Xcode-valg, shell-indstillinger eller automatiske opstart.
Homebrew-afhængigheder installeres i Homebrews almindelige placering.

Hvis en download eller PDF-bygning fejler, er installationen ikke færdig.
Ret den viste fejl, og fortsæt fra den udpakkede mappe med:

```sh
python3 install.py --resume
```

`--resume` bevarer konfigurationen og egne ændringer og prøver de manglende trin
igen. Fejl efter kopiering gemmes i installationsmappens `install.log`; selve
PDF-bygningen har også `pdf-build.log` og pakkens `server/config.log`.
Fejl i forudsætningerne, inden mappen oprettes, vises i Terminal; kør i det tilfælde
`python3 install.py` igen uden `--resume`.

En anden installationsmappe kan vælges med `--target PATH`; brug også denne
indstilling ved genoptagelse og samme mappe ved Emacs' `--init-directory`.
Installationsprogrammet overskriver aldrig en eksisterende mappe eller et
symbolsk link. `--resume` accepterer kun mapper mærket af dette installationsprogram.
En ældre installation opgraderes derfor ved at installere i en ny mappe og
bagefter overføre egne indstillinger efter behov.

Pakkelisten omfatter auctex, card-games, casual, dired-subtree, eat, nerd-icons,
nerd-icons-dired, org-draw, org-modern, org-roam, org-roam-ui, paredit og pdf-tools.
Afhængigheder installeres med dem. Der hentes aktuelle versioner fra GNU ELPA,
NonGNU ELPA og MELPA; ZIP-filen indeholder ikke Emacs, pakkekopier eller
Homebrew-biblioteker. Normal opstart henter eller bygger ikke pakker automatisk.
`M-x emacs-nxs/install-missing-packages` findes stadig til senere vedligeholdelse
af Emacs-pakker; PDF-bygningen håndteres af installationsprogrammet.

Til manuel opsætning kan `python3 install.py --config-only` nøjes med at kopiere
konfigurationen. Det er ikke en færdig installation. Den kan færdiggøres med
`--resume`. Automatisk afhængighedsinstallation er kun understøttet på macOS.

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

## Emacs Lisp

Paredit giver struktureret redigering i Emacs Lisp og IELM. Eldoc, Flymake og
den eksisterende kodefuldførelse bruges fortsat. `C-c e` samler kommandoer:
`d` evaluerer definitionen, `b` bufferen, `r` regionen, `i` åbner IELM,
`e` instrumenterer til Edebug, `t` kører ERT, `p` kontrollerer parenteser,
`c` kontrollerer dokumentation, og `k` bytekompilerer filen.
Evaluering kører koden i den aktuelle Emacs. Bytekompilering spørger før
gemning af en ændret buffer. Standardgenvejene er bevaret.
