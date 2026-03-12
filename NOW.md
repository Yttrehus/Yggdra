# NOW — Hvor vi er

**Sidst opdateret:** 2026-03-12 ~17:00 (session 12)
**Status:** Project Reformation — fase 0.5 (fil-audit) v2 DONE + implementeret.

## Næste step (start her)

**Denne session:** Fil-audit v2 er implementeret. Klar til commit.
1. ✅ Pipeline-mapper samlet under `pipeline/` med numeriske præfikser
2. ✅ `template/` → `.claude/template/`
3. ✅ `/new-project` skill opdateret med ny template-sti
4. Commit: "reformation fase 1-2 v2: pipeline/ + template-flytning"
5. Derefter: fase 3 (briefs), fase 4 (ADR'er), fase 5 (CONTEXT.md, egen session)

## Ny struktur (fase 1-2 v2)

```
Basic Setup/
├── CLAUDE.md, NOW.md, PLAN.md, PROGRESS.md, README.md
├── .editorconfig, .gitattributes, .gitignore, .code-workspace
│
├── pipeline/
│   ├── 0_backlog/
│   ├── 1_PoC/
│   ├── 2_DLR/
│   │   └── project-reformation/
│   ├── 3_SIP/
│   │   └── auto-chatlog/
│   └── 4_ARC/
│       ├── chatlogs/
│       ├── implementation-journals/
│       └── diverse arkiv-filer
│
├── manuals/          ← git.md, vscode.md, terminal.md (levende håndbøger)
├── research/         ← tom, afventer research-arkitektur projekt
│   └── _ARC/        ← 8 pre-reformation research-filer
│
└── .claude/
    ├── skills/ (6 stk)
    ├── template/ (8 filer, flyttet fra template/)
    └── settings.local.json
```

## Hvad session 12 producerede

### Beslutninger
- **pipeline/ som overmappe:** _backlog, PoC, DLR, SIP, _ARC samlet — pipeline er processen, BMS (roden) er resultatet
- **Numeriske præfikser:** 0_backlog → 4_ARC — kronologisk sortering, visuelt grupperet
- **template/ → .claude/template/:** Skill-infrastruktur, ikke synlig i roden
- **research/ er research-architecture projektets hjem:** Starter som backlog-brief, research/_ARC/ er input
- **automation.md → backlog-brief:** Forældet index, erstattes af kommende system

### Ændringer fra session 11 manifest
- Pipeline-mapper under `pipeline/` i stedet for i roden
- `template/` absorberet i `.claude/`
- Rod reduceret fra 10 synlige mapper til 3 (pipeline, manuals, research)

## Åbne tråde

- M5 step 11-17 (filsystem, X1, fonts, Dev Drive, wslconfig, quick reference)
- Checkpoint-skill: ADR-check mangler
- ~/parallel-tasks/ 7 outputs → mapping til briefs (fase 3)
- Poppler PATH-verifikation efter restart
- Prettier mangler .prettierrc

## Nye backlog-briefs (fase 3)
- brief.research-architecture.md — forskningspraksis, multi-LLM, VPS audit. Høj prioritet post-reformation.
- brief.automation-index.md — levende automation-overblik, cruft-forebyggelse.
