# Yggdra (Basic Setup)

## Metadata
- **Status:** Project Reformation i gang — struktur implementeret, rod-CONTEXT.md og oprydning mangler. M5 step 11-17 venter.
- **Sidst opdateret:** 2026-03-13 (session 13, sen aften)

## Hvad er det
Personligt udvikler-fundament. Startede som Windows-opsætning (Git, VS Code, terminal, projektstruktur, PC-setup), vokset til framework for hvordan Yttre arbejder med AI og kode. Omdøbes til Yggdra ved reformation fase 7.

## Hvor er vi

### Seneste session (13 — 2026-03-13)
Manifest v4 implementeret. Tre iterationer af mappestruktur (pipeline/ → Development/ → projects/) landede på det simpleste: flad projects/-mappe, ét projekt = én mappe. ADR-terminologi og pipeline-stages droppet — erstattet af CONTEXT.md overalt med plain dansk status. Manuals og research ind under projects/. Rod reduceret til 2 mapper (projects/ + .claude/). CONTEXT.md template designet (rekursivt, skalerbart). NOW+PLAN+PROGRESS → CONTEXT.md + PROGRESS.md.

Chatlog v2 krav defineret: én fil (chatlog.md), komplet sessionsdata inkl. tænkeblokke og tool calls, session-baseret inddeling, navigationslinks. Hukommelsesarkitektur skitseret: markdown (nu) → vector DB (snart) → knowledge graph (senere). Claude Memory tilføjet til VS Code workspace.

### Struktur
```
Basic Setup/
├── CONTEXT.md              ← dette dokument (erstatter NOW.md + PLAN.md)
├── PROGRESS.md             ← fuld narrativ, læses efter behov
├── CLAUDE.md, README.md
├── projects/
│   ├── backlog/            ← 13 idé-briefs
│   ├── archive/            ← historiske filer, chatlogs, journals
│   ├── auto-chatlog/       ← chatlog-engine (output → chatlog.md i roden)
│   ├── project-reformation/
│   ├── projekt-omdobning/
│   ├── manuals/            ← git, vscode, terminal håndbøger
│   └── research/           ← archive/ med 8 pre-reformation filer
└── .claude/                ← skills, template, settings
```

### Aktive projekter
- **Project Reformation:** Struktur done, CONTEXT.md og oprydning mangler, omdøbning til sidst. → `projects/project-reformation/CONTEXT.md`
- **Auto-chatlog:** Parser fungerer (1000+ beskeder, 6+ sessions). Mangler automatisering og bedre nøgleord. → `projects/auto-chatlog/CONTEXT.md`

### Afsluttede moduler
- **M1-M3:** Git, VS Code, Terminal (SSH, extensions, WSL, Zsh, Starship)
- **M4:** Projektstruktur (~/dev/ layout, template, /new-project, /checkpoint, dotfiles-repo)

### Venter
- **M5 step 11-17:** Filsystem, X1 Carbon, .wslconfig, fonts, Dev Drive, Poppler, quick reference
- **M6:** Terminal-automatisering (workspace åbner med rigtige terminaler)
- **M7:** Context engineering (selvstændigt projekt, se `projects/backlog/brief.context-engineering.md`)
- **M8:** Skabeloner (nyt projekt på under 5 min)

## Hvad mangler
- [ ] Reformation fase 6: oprydning (checkpoint-skill → CONTEXT-check, forældreløse filer)
- [ ] Reformation fase 7: omdøb repo til Yggdra
- [ ] M5 step 11-17
- [ ] M6, M7/CE, M8

## Beslutninger

**Rækkefølge:** Reformation done → M5 rest → M6 → M7/CE → M8

**Metodik:**
- PDCA-cyklus per modul (Plan-Do-Check-Act, Deming)
- Solnedgangsklausul per implementation (succes/kalibrerings/kill-tegn, evalueringstidspunkt)
- Default: justér → omtænk → kill
- Spørg før du bygger. Diskussion færdig → bekræftelse → kode.

**Scope:** Alt der vokser ud over udvikler-fundament bliver separate projekter i `projects/`.

**State-filer:**
- CONTEXT.md (denne fil) — læses automatisk, altid aktuelt overblik
- PROGRESS.md — fuld narrativ, læses efter behov for kontekst
- Hvert projekt har sin egen CONTEXT.md (samme format, rekursivt design)

## Åbne tråde
- Poppler PATH-verifikation efter restart
- Prettier mangler .prettierrc
- /new-project utestet i praksis
- chatlog-search: for tidligt at evaluere
- Checkpoint-skill: skal opdateres til CONTEXT-check

## Changelog
Komprimeret overblik. Fuld detalje i PROGRESS.md.

- **Session 13** (2026-03-13): projects/ struktur, ADR→CONTEXT.md, chatlog v2 krav, hukommelsesarkitektur, Claude Memory i workspace. → PROGRESS.md#session-13
- **Session 12** (2026-03-12): Manifest v1-v3 implementeret, 13 briefs, 2 ADR'er retroaktivt. → PROGRESS.md#session-12
- **Session 11** (2026-03-12): Fil-audit, references/ opløst, research-arkitektur identificeret. → PROGRESS.md#session-11
- **Session 10** (2026-03-12): Repo→Yggdra besluttet, M7 trukket ud, CONTEXT.md design, context rot rettet. → PROGRESS.md#session-10
- **Session 9** (2026-03-11): Auto-chatlog prototype, Project Reformation startet, "spørg før du bygger." → PROGRESS.md#session-9
- **Session 8** (2026-03-10): M4 afsluttet, skills evalueret. → PROGRESS.md#session-8
- **Session 7** (2026-03-10): Dotfiles-repo, skills-arkitektur revideret. → PROGRESS.md#session-7
- **Session 6** (2026-03-10): Per-projekt skabelon, /checkpoint og /new-project oprettet. → PROGRESS.md#session-6
- **Session 5** (2026-03-10): ~/dev/ layout, PDCA, solnedgangsklausul, parallel-tasks. → PROGRESS.md#session-5
- **Session 4** (2026-03-10): "Basic Setup er ikke basic", cross-session peer review. → PROGRESS.md#session-4
- **Session 3** (2026-03-10): Session-management problem, VPS research, yggdra-gold. → PROGRESS.md#session-3
- **Session 1-2** (2026-03-08/09): M1-M3 done, PLAN v2, ~/dev/ oprettet. → PROGRESS.md#session-1-2
