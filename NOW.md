# NOW — Hvor vi er

**Sidst opdateret:** 2026-03-13 (session 13)
**Status:** Project Reformation — strukturændring v3 (manifest v4 implementeret). Næste: fase 5 (CONTEXT.md).

## Næste step (start her)

**Denne session:** Manifest v4 implementeret. Klar til commit.
1. Commit + push strukturændring
2. Opdatér referencer i projekt-CONTEXT.md-filer (gamle pipeline/-stier)
3. Derefter: fase 5 — rod-CONTEXT.md (egen session)

## Hvad session 13 producerede

### Strukturændring v3 → v4
- `pipeline/` → `Development/` → `projects/` (flad, ét projekt = én mappe)
- Pipeline-stages (0_backlog, 1_PoC, 2_DLR, 3_SIP, 9_ARC) → `backlog/` + `archive/` + projektmapper
- ADR-filer → CONTEXT.md (samme format som rod-CONTEXT.md, rekursivt design)
- `manuals/` og `research/` ind under `projects/` (de er projekter)
- `research/_ARC/` → `research/archive/`
- Governance READMEs → arkiveret (stage er metadata i CONTEXT.md)
- BMS → BSL (ISO/IEC 12207 terminologi i dokumentation)

### Beslutninger
- Ét format: CONTEXT.md overalt — rod og projekter
- Briefs i `projects/backlog/` er embryoniske CONTEXT.md'er
- Stage er metadata i CONTEXT.md, ikke mappestruktur
- Ingen ADR-terminologi, ingen pipeline-stages i mappenavne
- `projects/` i roden, ikke `development/` (konsistent med VPS)

## Ny struktur

```
Basic Setup/
├── CLAUDE.md, NOW.md, PLAN.md, PROGRESS.md, README.md
├── .editorconfig, .gitattributes, .gitignore, .code-workspace
│
├── projects/
│   ├── backlog/            ← 13 briefs
│   ├── archive/            ← chatlogs, journals, historisk
│   ├── auto-chatlog/       ← CONTEXT.md + engine + output
│   ├── project-reformation/← CONTEXT.md + governance + templates
│   ├── projekt-omdobning/  ← CONTEXT.md
│   ├── manuals/            ← git.md, vscode.md, terminal.md
│   └── research/           ← archive/ med 8 pre-reformation filer
│
└── .claude/                ← skills, template, settings
```

## Åbne tråde

- M5 step 11-17 (filsystem, X1, fonts, Dev Drive, wslconfig, quick reference)
- Checkpoint-skill: ADR-check mangler → CONTEXT-check
- Poppler PATH-verifikation efter restart
- Prettier mangler .prettierrc
- Gamle pipeline/-referencer i CONTEXT.md-filer skal opdateres
