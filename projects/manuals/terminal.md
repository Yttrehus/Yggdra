# Terminal — Quick Reference

## Shell-aliases (genveje i terminalen)

Defineret i `~/.zshrc`. Virker kun i WSL.

### Git-genveje

| Alias | Kommando | Hvad den gør |
|-------|----------|--------------|
| `gs` | `git status` | Vis ændrede/nye/staged filer |
| `ga` | `git add` | Tilføj filer til staging (fx `ga .` eller `ga fil.txt`) |
| `gc` | `git commit` | Lav en commit (fx `gc -m "besked"`) |
| `gp` | `git push` | Push til GitHub |
| `gd` | `git diff` | Vis ændringer i filer |
| `gl` | `git log --oneline -10` | De seneste 10 commits, én linje hver |

### Navigation

| Alias | Hvad den gør |
|-------|--------------|
| `ll` | Vis alle filer inkl. skjulte, med detaljer (størrelse, dato, rettigheder) |
| `..` | Gå én mappe op |
| `...` | Gå to mapper op |

### Git-aliases (fra ~/.gitconfig)

| Alias | Kommando | Hvad den gør |
|-------|----------|--------------|
| `git st` | `git status` | Vis status |
| `git co` | `git checkout` | Skift branch (fx `git co main`) |
| `git br` | `git branch` | Vis alle branches |
| `git lg` | `git log --graph` | Pæn log med graf og farver |

---

## Installeret software

| Hvad | Hvad det gør |
|------|--------------|
| **Zsh** | Shell (erstatning for bash) — hurtigere, smartere tab-completion |
| **Oh My Zsh** | Framework ovenpå zsh — plugins, temaer, nemmere config |
| **Starship** | Prompt der viser mappe, git-branch, sprog, fejlkoder |
| **zsh-autosuggestions** | Foreslår kommandoer mens du skriver (baseret på historik) — tryk → for at acceptere |
| **zsh-syntax-highlighting** | Farver kommandoer grøn (findes) eller rød (findes ikke) mens du skriver |

---

## Vigtige filer

| Fil | Hvad |
|-----|------|
| `~/.zshrc` | Shell-config — aliases, plugins, Starship, Oh My Zsh |
| `~/.gitconfig` | Git-config — navn, email, aliases, editor |
| `~/.gitignore_global` | Filer git altid ignorerer (OS-filer, secrets, node_modules) |
| `~/.oh-my-zsh/` | Oh My Zsh framework (plugins, temaer) |

---

## Nyttige kommandoer

```bash
source ~/.zshrc       # Reload shell-config uden at lukke terminalen
which <program>       # Vis stien til et program (fx which zsh → /usr/bin/zsh)
chsh -s $(which zsh)  # Skift default shell (kræver password)
nano ~/.zshrc         # Redigér shell-config (Ctrl+O gem, Ctrl+X luk)
```
