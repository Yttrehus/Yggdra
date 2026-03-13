# VS Code — Quick Reference

## Genveje

### Generelt

| Genvej | Hvad den gør |
|--------|--------------|
| `Ctrl+½` | Åbn/luk terminal (custom keybinding) |
| `Ctrl+Shift+P` | Kommandopalet — åbner ALT (søg efter enhver funktion) |
| `Ctrl+P` | Søg og åbn fil hurtigt (skriv filnavn) |
| `Ctrl+B` | Skjul/vis sidepanel |
| `Ctrl+Shift+E` | Filstifinder (Explorer) |
| `Ctrl+Shift+X` | Extensions |

### Redigering

| Genvej | Hvad den gør |
|--------|--------------|
| `Ctrl+/` | Kommenter/uncommenter linje |
| `Alt+↑/↓` | Flyt linje op/ned |
| `Ctrl+D` | Vælg næste forekomst af samme ord (multi-cursor) |
| `Ctrl+Shift+K` | Slet linje |

---

## Extensions

| Extension | Hvad den gør |
|-----------|--------------|
| **GitLens** | Vis hvem der ændrede hvad og hvornår, direkte i editoren |
| **WSL** | Gør at VS Code kan arbejde i WSL (Linux-filer, terminal) |
| **Remote-SSH** | Forbind til VPS og redigér filer direkte |
| **Prettier** | Auto-formatér kode når du gemmer |
| **Python** | Syntax, debugging, IntelliSense for Python |
| **ESLint** | Fanger fejl i JavaScript/TypeScript |

---

## Vigtige settings

Fil: `C:\Users\Krist\AppData\Roaming\Code\User\settings.json`

| Setting | Hvad den gør |
|---------|--------------|
| `formatOnSave` | Prettier formaterer automatisk når du gemmer |
| `autoSave: onFocusChange` | Gemmer filen når du skifter væk fra den |
| `tabSize: 2` | Indrykning er 2 mellemrum (standard i web) |
| `wordWrap: on` | Lange linjer brydes visuelt (ingen vandret scroll) |
| `minimap: false` | Fjerner minimap i højre side |
| `rulers: [80, 120]` | Tynde lodrette linjer ved 80 og 120 tegn (læsbarhedsguide) |
| `terminal: Ubuntu (WSL)` | Terminal i VS Code åbner WSL, ikke PowerShell |
| `font: JetBrains Mono` | Kodefont med ligatures (falder tilbage til Consolas) |

---

## Vigtige filer

| Fil | Hvad |
|-----|------|
| `settings.json` | Bruger-settings (gælder alle projekter) |
| `keybindings.json` | Custom genveje (fx Ctrl+½) |
| `.code-workspace` | Workspace-fil (projekt-specifikke settings) |

---

## Tips

- **Ctrl+Shift+P → "Preferences: Open User Settings (JSON)"** — åbn settings.json direkte
- **Ctrl+Shift+P → "Preferences: Open Keyboard Shortcuts (JSON)"** — åbn keybindings.json
- Workspace-mode (File → Open Workspace from File) giver projekt-specifikke settings
- `Ctrl+Shift+V` for paste i WSL-terminal (ikke Ctrl+V)
