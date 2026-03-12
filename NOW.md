# NOW — Hvor vi er

**Sidst opdateret:** 2026-03-12 ~16:00 (session 11)
**Status:** Project Reformation — fase 0.5 (fil-audit) DONE. Klar til implementering (fase 1-2).

## Næste step (start her)

**Denne session:** Implementer fil-manifestet (fase 1 → fase 2).
1. Opret mapper: _backlog/, PoC/, DLR/, SIP/, _ARC/, manuals/, research/ med README'er
2. Flyt filer ifølge manifestet (se nedenfor)
3. Slet tømte mapper (references/, chatlogs/, auto-chatlog/, project-reformation/)
4. Tilføj .firecrawl/ til .gitignore
5. Commit: "reformation fase 1-2: mappestruktur + fil-flytning"
6. Derefter: fase 3 (briefs), fase 4 (ADR'er), fase 5 (CONTEXT.md, egen session)

## Fil-manifest (fase 0.5 resultat)

### Nye mapper
- `_backlog/` — idéer og briefs
- `PoC/` — prototyper
- `DLR/` — design/development
- `SIP/` — staging/integration
- `_ARC/` — arkiv (+ chatlogs/, implementation-journals/)
- `manuals/` — levende håndbøger (git, vscode, terminal)
- `research/` — tom nu, afventer research-arkitektur projekt
  - `research/_ARC/` — al pre-reformation research

### Flytninger
- references/git.md, vscode.md, terminal.md → manuals/
- references/ (9 research-filer) → research/_ARC/
- references/PLAN.v1.md, git-concepts.md, google-ai-samtale-rd-framework.md → _ARC/
- chatlogs/*.md → _ARC/chatlogs/
- chatlogs/dump-chatlog.js → _ARC/
- .claude/implementation journals/* → _ARC/implementation-journals/
- auto-chatlog/* → SIP/auto-chatlog/
- project-reformation/* → DLR/project-reformation/
- references/ → slettes (opløst)
- chatlogs/ → slettes (pensioneret)

### Nye backlog-briefs (fase 3)
- brief.research-architecture.md — høj prioritet post-reformation
- brief.automation-index.md — levende automation-overblik

## Hvad session 11 producerede (indtil nu)

### Beslutninger
- **references/ opløses:** 3 typer (manualer, research, arkiv) var blandet — separeres
- **manuals/ oprettes:** Levende håndbøger (git, vscode, terminal) der kan vokse
- **research/ oprettes med _ARC/:** Al eksisterende research er pre-reformation
- **Research-arkitektur:** Omfattende fremtidigt projekt → backlog, høj prioritet
- **automation.md → backlog:** Forældet, erstattes af kommende automation-index system
- **chatlogs/ pensioneres nu:** Flyttes til _ARC/chatlogs/
- **.firecrawl/ ignoreres:** Ikke git-tracked, tilføjes til .gitignore

## Åbne tråde

- M5 step 11-17 (filsystem, X1, fonts, Dev Drive, wslconfig, quick reference)
- Checkpoint-skill: ADR-check mangler
- ~/parallel-tasks/ 7 outputs → mapping til briefs (fase 3)
- Poppler PATH-verifikation efter restart
- Prettier mangler .prettierrc
