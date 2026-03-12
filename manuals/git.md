# Git — Quick Reference

## Hvad er git?
Et versionskontrolsystem. Det holder styr på alle ændringer i din kode, så du kan gå tilbage i tid, arbejde på flere ting parallelt og samarbejde med andre.

---

## Konfiguration (gøres én gang)

```bash
git config --global user.name "Yttre"          # Hvem er du — vises på dine commits
git config --global user.email "..."            # Din email
git config --global init.defaultBranch main     # Nye repos starter på 'main', ikke 'master'
git config --global core.editor "code --wait"   # VS Code åbner når git skal bruge en editor
git config --global core.excludesfile ~/.gitignore_global  # Ignorer visse filer i ALLE repos
```

---

## Et nyt projekt

```bash
git init                        # Gør mappen til et git-repo (opretter skjult .git/ mappe)
git remote add origin <url>     # Fortæl git hvor GitHub-repo'et er
git push -u origin main         # Push til GitHub første gang (-u husker origin/main fremover)
```

---

## Den daglige arbejdsgang

```bash
git st                    # (alias: git status) — se hvad der er ændret/klar til commit
git add README.md         # Tilføj én fil til "staging" (klar til commit)
git add .                 # Tilføj ALLE ændrede filer til staging
git commit -m "besked"    # Gem et snapshot med en beskrivelse
git push                  # Send commits til GitHub
git pull                  # Hent nye commits fra GitHub
```

---

## Branches (arbejd parallelt)

```bash
git br                        # (alias: git branch) — vis alle branches
git co -b feature-navn        # (alias: git checkout -b) — opret og skift til ny branch
git co main                   # Skift tilbage til main
git merge feature-navn        # Flet feature-branch ind i nuværende branch
git branch -d feature-navn    # Slet branch efter merge
```

---

## Overblik og historik

```bash
git lg                    # (alias) — vis historik som graf: hvem committede hvad hvornår
git diff                  # Vis hvad der er ændret men IKKE staged endnu
git diff --staged         # Vis hvad der er staged og klar til commit
git log --oneline         # Kompakt historik uden graf
```

---

## Fortryd

```bash
git restore fil.txt           # Kassér ændringer i en fil (før staging)
git restore --staged fil.txt  # Fjern fil fra staging (behold ændringerne)
git revert HEAD               # Lav en ny commit der fortryder den seneste (sikker metode)
```

---

## SSH til GitHub

```bash
ssh -T git@github.com         # Test at din SSH-nøgle virker mod GitHub
cat ~/.ssh/id_ed25519.pub     # Vis din offentlige nøgle (den du putter ind på GitHub)
```

---

## Ord du skal kende

| Ord | Betyder |
|-----|---------|
| **repository (repo)** | En mappe med git-historik |
| **commit** | Et gemt snapshot af koden |
| **branch** | En parallel version af koden |
| **staging** | Filer markeret klar til næste commit |
| **origin** | Standardnavnet på dit GitHub-remote |
| **push** | Send commits til GitHub |
| **pull** | Hent commits fra GitHub |
| **merge** | Flet to branches sammen |
| **HEAD** | Peger på din nuværende placering i historikken |
