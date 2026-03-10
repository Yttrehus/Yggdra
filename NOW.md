# NOW — Hvor vi er

**Sidst opdateret:** 2026-03-10 (session 7)
**Status:** M4 igangværende — step 4 DONE, step 5 næste

## Næste step (start her)

M4 step 5: workspace-fil skabelon for VS Code
Derefter:
- M4 step 6: evaluering af /checkpoint og /new-project skills
- M4 PDCA-evaluering (Check/Act)

## Hvad sessionen producerede

- **Dotfiles-repo:** ~/dev/projects/dotfiles/ — stow-managed .zshrc, .gitconfig kopi, scripts i bin/, pushed til GitHub (Yttrehus/dotfiles, privat)
- **Software installeret:** GNU Stow (WSL), GitHub CLI (Windows, autentificeret som Yttrehus)
- **Workspace-oprydning:** slettet cruft (5 filer + 2 mapper), oprettet chatlogs/, flyttet filer til references/
- **dump-chatlog.js omskrevet:** grupperer per dato, fletter sessions kronologisk
- **.gitattributes + .editorconfig tilføjet til BS** (fra template/)
- **Skills-arkitektur revideret:** BS-specifikke skills flyttet fra global → projekt-niveau, feedback-log separeret til .claude/implementationlogs/, chatlog-search skill oprettet
- **README.md** opdateret til aktuel struktur, references/README.md oprettet

## .claude/ struktur (BS projekt-niveau)

```
.claude/
  skills/              ← instruktioner (hvad)
    checkpoint.md
    session-state.md
    chatlog-search.md
    infrastructure.md
    notion.md
  implementationlogs/  ← brugsjournal (hvordan det gik)
    checkpoint.md
    chatlog-search.md
```

Skills starter lokalt i projektet. Promoveres til global (~/.claude/skills/) når bevist på tværs af projekter.

## Beslutninger taget (denne session)

- GNU Stow til WSL dotfiles, manuel kopi til Windows .gitconfig
- gh CLI installeret — bruges til GitHub-operationer fremover
- Workspace-root: kun state-filer + konventionsfiler, alt andet i mapper
- Skills er projekt-lokale først, globale når bevist
- implementationlogs/ for brugs-feedback, separeret fra skill-definitioner
- .claude/skills/ er reelt instruktionsfiler (kontekst for Claude), ikke executable skills

## Vigtig kontekst

- Claude Code Bash-tool kører i Windows, ikke WSL
- Windows git konfigureret med SSH — Claude kan commit+push
- gh CLI autentificeret som Yttrehus (HTTPS)
- **INGEN session-save hook på PC** — NOW.md skal opdateres manuelt

## Åbne tråde

- JetBrains Mono font ikke installeret
- Mermaid Preview extension ikke installeret
- Notion-struktur venter
- Poppler PATH-verifikation efter restart
- Session-management hook til PC (M7-scope)
- vscode.md reference nævner ting der ikke er installeret endnu
- Integrationer parkeret: Gmail, Hotmail, Google (Drev/Calendar/Sheets), mobil-adgang
- 7 parallel task briefs i ~/parallel-tasks/ — klar til Cowork
