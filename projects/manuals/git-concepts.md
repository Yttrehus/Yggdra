# Git og GitHub — Hvad er det egentlig?

## Den korte version

**Git** er et program der kører på din computer.
**GitHub** er en hjemmeside der gemmer en kopi af din kode på internettet.

De er separate ting. Git kan bruges uden GitHub. Men de arbejder godt sammen.

---

## Analogien der giver mening

Tænk på det som at skrive en bog:

- **Din mappe med filer** = manuskriptet du arbejder på
- **Git** = den der tager et fotografi af manuskriptet hvert gang du siger "gem dette"
- **Et commit** = ét fotografi (snapshot) med en beskrivelse: *"tilføjede kapitel 3"*
- **Historikken** = albummet med alle fotografier — du kan altid bladre tilbage
- **GitHub** = en sikkerhedskopi af albummet i skyen, som andre også kan se

---

## Hvad løser git?

**Problem 1: Du ødelægger noget**
Uden git: du sidder med ødelagt kode og ingen vej tilbage.
Med git: `git restore fil.txt` — filen er som den var ved sidste commit.

**Problem 2: Du vil prøve noget nyt uden at risikere det eksisterende**
Uden git: du laver en kopi af hele mappen (projekt-backup-final-v2-ny).
Med git: `git checkout -b eksperiment` — en branch. Virker det ikke, sletter du den.

**Problem 3: To personer arbejder på samme fil**
Uden git: den ene overskriver den andens arbejde.
Med git: git merger de to versioner og markerer konflikter.

---

## Begreber forklaret

### Repository (repo)
En mappe som git holder øje med. Når du kører `git init` i en mappe, begynder git at
spore ændringer i den. Der oprettes en skjult `.git/` mappe — rør ikke ved den.

### Commit
Et gemt øjebliksbillede af dine filer. Hvert commit har:
- En unik ID (f.eks. `2cd066b`)
- En besked du selv skriver ("first commit")
- Et tidsstempel
- En reference til det forrige commit

Commits slettet aldrig. Historikken er permanent.

### Staging (index)
Området *mellem* dine filer og et commit. Du bestemmer præcist hvilke ændringer
der skal med i næste commit. Ikke alt behøver at gå med.

```
Dine filer  →  git add  →  Staging  →  git commit  →  Historik
```

### Branch
En parallel tidslinje. `main` er din primære branch. Når du laver en ny branch,
tager git et "copy" af main fra det punkt — du kan ændre frit uden at påvirke main.

```
main:     A - B - C
                   \
feature:            D - E
```

Når du er tilfreds merger du feature tilbage i main.

### Remote
En kopi af dit repo et andet sted — typisk GitHub. `origin` er standard-navnet for
dit GitHub-remote. Kommandoerne:

```
git push   →  send dine commits TIL GitHub
git pull   →  hent nye commits FRA GitHub
```

### HEAD
En pil der peger på "hvor du er nu" i historikken. Normalt peger HEAD på din
nuværende branch, som peger på det seneste commit.

---

## Det typiske flow — dag til dag

```
1. Arbejd på din kode
2. git st          → se hvad der er ændret
3. git add .       → klargør alle ændringer
4. git commit -m "beskriv hvad du lavede"
5. git push        → synk til GitHub
```

Princip: **commit ofte, med meningsfulde beskeder.** Et commit per logisk ændring,
ikke én kæmpe commit med "did stuff".

---

## Hvad GitHub tilføjer

GitHub er ikke bare opbevaring. Det er også:

- **Issues** — fejlrapporter og opgavelister
- **Pull Requests** — forslag til ændringer (selv til dine egne repos)
- **Actions** — automatiske tests/deployments når du pusher
- **README.md** — vises automatisk på repo-siden

Når du pusher dit repo til GitHub og åbner det i browseren, ser du README.md
renderet som en pæn forside. Det er standard for alle open source projekter.

---

## SSH vs HTTPS

To måder at forbinde til GitHub:

**HTTPS:** `https://github.com/Yttrehus/repo.git`
— bruger brugernavn + password (eller token). Nemt at starte, besværligt i dagligdagen.

**SSH:** `git@github.com:Yttrehus/repo.git`
— bruger din SSH-nøgle. Kræver opsætning én gang, men derefter ingen passwords.

Vi bruger SSH. Det er det professionelle valg.

---

## Hvilken terminal bruger du hvornår?

Du har tre muligheder på Windows. Her er reglen:

| Terminal | Bruges til |
|----------|-----------|
| **WSL** | Alt der har med kode at gøre — git, Python, SSH, npm |
| **PowerShell** | Windows-ting — installere programmer, styre Windows |
| **Git Bash** | Undgå — det er et kompromis, ikke det rigtige valg |

**Tommelfingerregel: Åbn WSL. Bliv i WSL.**

---

### Sådan åbner du WSL

**Fra PowerShell eller Windows Terminal:**
```bash
wsl
```

**Fra VS Code** (anbefalet):
- `Ctrl+`` ` ` (backtick) — åbner terminal i bunden
- Klik på `+` pilen → vælg `Ubuntu` eller `WSL`

**Direkte fra Start-menu:**
Søg efter "Ubuntu" — åbner WSL direkte.

---

### Sådan forbinder du til din VPS via SSH

Du er i WSL. Skriv:
```bash
ssh root@72.62.61.51
```

Første gang spørger den om du stoler på serveren — skriv `yes`.
Derefter logger du ind uden password fordi din SSH-nøgle er registreret.

For at komme tilbage til din egen maskine:
```bash
exit
```

---

### Sådan kloner du et GitHub-repo

"Clone" betyder: hent en kopi af et repo fra GitHub ned til din maskine.

```bash
cd ~/dev                                          # gå til din dev-mappe
git clone git@github.com:Yttrehus/repo-navn.git  # hent repo'et
cd repo-navn                                      # gå ind i mappen
```

Nu har du en lokal kopi, forbundet til GitHub via SSH.

---

### SSH-nøglen — hvad er den egentlig?

Din SSH-nøgle er et par filer:

```
~/.ssh/id_ed25519      ← den private nøgle (ALDRIG del denne med nogen)
~/.ssh/id_ed25519.pub  ← den offentlige nøgle (den du putter på GitHub/VPS)
```

Det fungerer som lås og nøgle: GitHub og VPS har låsen (public key), du har nøglen (private key). Ingen passwords nødvendige.

---

## Professionelle arbejdsgange

### Solo-udvikler (dit niveau nu)

Den simpleste workflow der stadig er professionel:

```
main  →  altid stabil, kan deployes
         ↑
feature-branches  →  al ny kode sker her
```

**Konkret:**
```bash
git co -b fix-login-bug      # start ny branch til hver opgave
# ... arbejd, commit løbende ...
git co main
git merge fix-login-bug      # merge når det virker
git branch -d fix-login-bug  # ryd op
git push
```

Reglen: **main er altid ren.** Du arbejder aldrig direkte på main.

---

### Commit-beskeder der er værd noget

Dårligt:
```
"fix"
"changes"
"wip"
"asdfgh"
```

Godt — brug imperativ (som ordrer):
```
"Add login form validation"
"Fix crash when user has no email"
"Remove unused API key from config"
"Update README with setup instructions"
```

Format mange teams bruger (Conventional Commits):
```
feat: add dark mode toggle
fix: correct date formatting in invoice
docs: update deployment guide
chore: upgrade dependencies
```

Første ord fortæller *hvad slags* ændring det er. Resten fortæller *hvad* der sker.

---

### .gitignore — hvad pusher du ALDRIG

Aldrig til GitHub:
- `.env` — passwords, API-nøgler, hemmeligheder
- `node_modules/` — kan altid regenereres med `npm install`
- `__pycache__/` — Python's kompilerede filer
- `.DS_Store` — macOS-skrald
- Binære filer der er store (videoer, databaser)

Reglen: **kode og konfiguration pushes. Hemmeligheder og genererede filer pushes ikke.**

---

### Pull Requests (PR) — selv solo

Selv når du arbejder alene er PR en god vane:

1. Lav en feature-branch
2. Push den til GitHub: `git push -u origin feature-navn`
3. Åbn en Pull Request på GitHub
4. Se diff'en — gennemgå dine egne ændringer
5. Merge

Fordelen: du tvinges til at **læse dine egne ændringer** før de ryger i main.
Det finder fejl. Altid.

---

### Tags — marker vigtige øjeblikke

```bash
git tag v1.0.0          # marker den nuværende commit som version 1.0.0
git push --tags         # push tags til GitHub
```

GitHub viser tags som "Releases". Nyttigt når du deployer eller sender noget til andre.

---

### Stash — gem arbejde midlertidigt

Du er midt i noget, men skal hurtigt skifte til noget andet:

```bash
git stash           # gem nuværende ændringer væk (uden commit)
git co anden-branch # skift og lav det du skulle
git co tilbage
git stash pop       # hent dine ændringer frem igen
```

Tænk på det som at skubbe arbejdet i en skuffe midlertidigt.

---

### Daglig rutine — professionel version

```
Morgen:
  git pull                    → hent seneste fra GitHub

Undervejs:
  git st                      → løbende tjek
  git add -p                  → gennemgå ændringer del for del (avanceret)
  git commit -m "feat: ..."   → commit per logisk enhed

Slut på dagen:
  git push                    → altid push inden du lukker ned
```

**Guldreglen:** Slut aldrig dagen med uncommitted arbejde der ikke er pushet.
Disk kan gå ned. Computere kan forsvinde. GitHub kan ikke.
