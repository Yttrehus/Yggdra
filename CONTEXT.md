# Yggdra (Basic Setup)

## Metadata
- **Status:** Reformation fase 6 næsten done. Fase 7 (omdøb repo) venter. M5 step 11-17 derefter.
- **Sidst opdateret:** 2026-03-13 (session 14, aften)

## Hvad er det
Personligt udvikler-fundament. Startede som Windows-opsætning (Git, VS Code, terminal, projektstruktur, PC-setup), vokset til framework for hvordan Yttre arbejder med AI og kode. Omdøbes til Yggdra ved reformation fase 7.

## Hvor er vi

### Seneste session (14 — 2026-03-13)
Chatlog-engine v3: gap-sektioner, subagent-abstracts, danske datoer, secret-redaction. Sessions fra 5 projektmapper samlet i én (~2500 beskeder, 30 sessions). Checkpoint og chatlog-search integreret i auto-chatlog-projektet. Skills audit: forældede stier rettet, checkpoint/chatlog-search forenklet til pointere. Archive ryddet: journals, manuelle chatlogs, dump-scripts slettet (alt i git). Template opdateret: NOW.md+PLAN.md → CONTEXT.md. architecture.R&D fået CONTEXT.md.

### Session 13 (2026-03-13)
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
│   ├── .archive/            ← architecture.R&D (med CONTEXT.md)
│   ├── auto-chatlog/       ← chatlog-engine (output → chatlog.md i roden)
│   ├── project-reformation/
│   ├── projekt-omdobning/
│   ├── manuals/            ← git, vscode, terminal håndbøger
│   └── research/           ← archive/ med 8 pre-reformation filer
└── .claude/                ← skills, template, settings
```

### Aktive projekter
- **Project Reformation:** Fase 6 (oprydning) næsten done, fase 7 (omdøbning) venter. → `projects/project-reformation/CONTEXT.md`
- **Auto-chatlog:** v3 fungerer (~2500 beskeder, 30 sessions, subagent-abstracts). Mangler automatisering. → `projects/auto-chatlog/CONTEXT.md`

### Afsluttede moduler
- **M1-M3:** Git, VS Code, Terminal (SSH, extensions, WSL, Zsh, Starship)
- **M4:** Projektstruktur (~/dev/ layout, template, /new-project, /checkpoint, dotfiles-repo)

### Venter
- **M5 step 11-17:** Filsystem, X1 Carbon, .wslconfig, fonts, Dev Drive, Poppler, quick reference
- **M6:** Terminal-automatisering (workspace åbner med rigtige terminaler)
- **M7:** Context engineering (selvstændigt projekt, se `projects/backlog/brief.context-engineering.md`)
- **M8:** Skabeloner (nyt projekt på under 5 min)

## Hvad mangler
- [x] Reformation fase 6: oprydning — checkpoint/chatlog-search integreret, archive ryddet, template opdateret, skills rettet ✅
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
- Checkpoint-skill: integreret i auto-chatlog ✅

## Changelog
Komprimeret overblik. Fuld detalje i PROGRESS.md.

- **Session 14** (2026-03-13): Chatlog-engine v3, sessions samlet, checkpoint+chatlog-search integreret i auto-chatlog, archive ryddet, template opdateret, reformation fase 6 afsluttet. → PROGRESS.md#session-14
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
