# Yggdra

## Metadata
- **Status:** Session 21. VPS V4 (4 research loops, 30 iter) afsluttet og hentet. 19 research-filer til PC. TRIAGE.md opdateret med V4 handlinger.
- **Sidst opdateret:** 2026-03-15 (session 21)

## Hvad er det
Personligt udvikler-fundament. Startede som "Basic Setup" (Windows-opsætning), vokset til framework for hvordan Yttre arbejder med AI og kode.

## Hvor er vi

### Seneste session (21 — 2026-03-15)
VPS V4 research loops (4 parallelle, 30 iterationer, alle PASS) evalueret og hentet til PC:
- **llm-landskab:** 7 provider-profiler, COMPARISON.md, RECOMMENDATION.md → `projects/research/llm-landskab/`
- **ai-frontier:** 5 topic-filer, GAPS.md (8 gaps), WHAT_IF.md (10 forslag) → `projects/research/ai-frontier/`
- **videns-vedligeholdelse:** HOLISTIC_EVALUATION, PIPELINE_DESIGN, DECAY_MODEL, SOURCE_REGISTRY, MAINTENANCE_PROTOCOL, YGGDRA_SCAN → `projects/research/videns-vedligeholdelse/`
- **youtube-pipeline-v2:** frame_extractor.py PoC + 3 nye kanaler (på VPS, ikke hentet)
- **TRIAGE.md:** Opdateret med 7 V4 handlinger + 4 afsluttede briefs
- **Backlog:** 9 forbrugte VPS-filer arkiveret

### Session 20 (2026-03-14)
VPS sandbox v2 (10 iter) + v3 (6 iter) afsluttet og evalueret. Output hentet til PC:
3 nye skills (dialectic-pipeline, session-resume, sitrep), TI-projekt (INDEX+PROGRESS+8 subprojects+research+archive), research INDEX v3 (54 insights), BLUEPRINT.md, TRIAGE.md, vps-sandbox CONTEXT.md, reference-filer.

### Session 19 (2026-03-14)
VPS sandbox v2 designet og deployed. Tre projekter i Ralph loop (10 iterationer). VPS v1 kvalitetsauditeret. Prompt evalueret og justeret. Handoff fra github-workflow absorberet (prompt-skabeloner).

### Session 18 (2026-03-14)
Ydrasil-projekt startet: VPS research+docs indekseret (INDEX.md). MCP/Skills kompendium research gennemført (adversarial proces). Nye skills tilføjet (context-search, debugging-wizard, mcp-builder, spec-miner, strategic-compact, the-fool, verification-loop). Nye backlog briefs (project-taxonomy, session-blindhed). data/ og scripts/ mapper oprettet i roden. Checkpoint-skill rettet: chatlog-engine kører nu først. Underscore-prefix fjernet fra projektmapper.

### Session 17 (2026-03-14)
Skills-synlighed i VS Code: global vs projekt `.claude/skills/` afklaret — alt allerede synkroniseret i projekt-mappen. MCP/Skills kompendium opgraderet fra brief til projekt. Adversarial research-proces designet: context scout → parallel research (MCP-landskab, skills-landskab, Yggdra-behov) → steelman → red team → steelman red team → neutral evaluator.

### Session 16 (2026-03-15)
Backlog-audit: 14→11 briefs. context-engineering + session-drift-pipeline merged. webscraping-audit + terminal-automatisering → raw/. 6 briefs opdateret/skærpet (visualisering, mcp, integrationer, notion, peer-review, voice). VPS Ydrasil-æra research + docs downloaded til projects/research/ydrasil/ (89+73 filer, ~9MB). GDrive-duplikat slettet. Research-kvalitet vurderet: høj substans, men iterativt klutter (~30% duplikater fra CH-kapitler). Diskussion om prioritering: research-arkitektur → agent teams → hukommelse. Vision-briefs parkeret (transport-app, politik, LLM-uafhængighed).

### Session 15 (2026-03-14)
M5 step 11/13/14/17 gennemført: Downloads ryddet (225→2 filer), .wslconfig oprettet (8GB/4CPU), JetBrains Mono + ligaturer, quick reference. Chatlog-engine token-scanning tilføjet (heuristisk + subagent-verifikation, redact-patterns.json). M6/M7/M8 flyttet fra plan til backlog-briefs. Parallel tasks absorberet i briefs. Backlog-briefs evalueret og opdateret. "Basic Setup" referencer fjernet. architecture.R&D CONTEXT.md oprettet. Google AI samtale flyttet til architecture.R&D. Archive ryddet. Lektie: `rm` i bash bypasser papirkurven.

### Session 14 (2026-03-13)
Chatlog-engine v3: gap-sektioner, subagent-abstracts, danske datoer, secret-redaction. Sessions fra 5 projektmapper samlet i én (~2500 beskeder, 30 sessions). Checkpoint og chatlog-search integreret i auto-chatlog-projektet. Skills audit: forældede stier rettet, checkpoint/chatlog-search forenklet til pointere. Archive ryddet: journals, manuelle chatlogs, dump-scripts slettet (alt i git). Template opdateret: NOW.md+PLAN.md → CONTEXT.md. architecture.R&D fået CONTEXT.md.

### Session 13 (2026-03-13)
Manifest v4 implementeret. Tre iterationer af mappestruktur (pipeline/ → Development/ → projects/) landede på det simpleste: flad projects/-mappe, ét projekt = én mappe. ADR-terminologi og pipeline-stages droppet — erstattet af CONTEXT.md overalt med plain dansk status. Manuals og research ind under projects/. Rod reduceret til 2 mapper (projects/ + .claude/). CONTEXT.md template designet (rekursivt, skalerbart). NOW+PLAN+PROGRESS → CONTEXT.md + PROGRESS.md.

Chatlog v2 krav defineret: én fil (chatlog.md), komplet sessionsdata inkl. tænkeblokke og tool calls, session-baseret inddeling, navigationslinks. Hukommelsesarkitektur skitseret: markdown (nu) → vector DB (snart) → knowledge graph (senere). Claude Memory tilføjet til VS Code workspace.

### Struktur
```
Yggdra/
├── CONTEXT.md, PROGRESS.md, CLAUDE.md, BLUEPRINT.md, README.md
├── chatlog.md                ← genereret af auto-chatlog engine
├── data/                     ← data-filer
├── scripts/                  ← utility scripts
├── projects/
│   ├── 0_backlog/            ← 12 briefs + TRIAGE.md + raw/
│   ├── 1_archive/            ← afsluttede projekter
│   ├── auto-chatlog/         ← chatlog-engine + checkpoint + chatlog-search
│   ├── manuals/              ← git, vscode, terminal, git-concepts
│   ├── mcp-skills-kompendium/← MCP+skills research + kompendier
│   ├── prompt-skabeloner/    ← chatlog mining, MINING_RESULTS.md
│   ├── research/             ← INDEX.md v3, llm-landskab/, ai-frontier/, videns-vedligeholdelse/
│   ├── transportintra/       ← TI arkiv: INDEX, PROGRESS, 8 subprojects, research, archive
│   ├── vps-sandbox/          ← VPS sandbox proces-dokumentation
│   └── ydrasil/              ← VPS INDEX.md, research, sessions, docs
└── .claude/                  ← skills (13 stk), template, settings
```

### Aktive projekter
- **VPS Sandbox:** v1-v4 gennemført. V4 output hentet (19 filer). → `projects/vps-sandbox/CONTEXT.md`
- **Research:** V4 tilføjede llm-landskab (7 profiler), ai-frontier (5 topics+GAPS+WHAT_IF), videns-vedligeholdelse (6 filer). → `projects/research/`
- **Auto-chatlog:** v3 fungerer (~3000 beskeder, 39 sessions). → `projects/auto-chatlog/CONTEXT.md`
- **TransportIntra arkiv:** Komplet. → `projects/transportintra/CONTEXT.md`

### Afsluttede moduler
- **M1-M3:** Git, VS Code, Terminal (SSH, extensions, WSL, Zsh, Starship)
- **M4:** Projektstruktur (~/dev/ layout, template, /new-project, /checkpoint, dotfiles-repo)

### Venter
- **M5 step 12, 15:** X1 Carbon (BIOS, fysisk adgang), Dev Drive (GUI/admin)

## Hvad mangler
- [x] Reformation ✅
- [x] M5 step 11 — Downloads oprydning (225→2 filer) ✅
- [x] M5 step 13 — .wslconfig (8GB RAM, 4 CPU) ✅
- [x] M5 step 14 — JetBrains Mono + Mermaid Preview ✅
- [x] M5 step 16 — Poppler verificeret ✅
- [x] M5 step 17 — Quick reference ✅
- [ ] M5 step 12 — X1 Carbon (BIOS, Lenovo Vantage, 400 MHz bug — kræver fysisk adgang)
- [ ] M5 step 15 — Dev Drive (evaluer om det giver mening, kræver GUI/admin)
- M6, M7, M8 → backlog-briefs i `projects/0_backlog/`

## Beslutninger

**Rækkefølge:** M5 rest (12, 15 — begge kræver dig) → backlog-projekter efter prioritet

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
- Prettier mangler .prettierrc
- /new-project utestet i praksis
- chatlog-search: for tidligt at evaluere

## Changelog
Komprimeret overblik. Fuld detalje i PROGRESS.md.

- **Session 21** (2026-03-15): VPS V4 (4 loops, 30 iter) evalueret og hentet. 19 research-filer: llm-landskab (7 profiler+COMPARISON+RECOMMENDATION), ai-frontier (5 topics+GAPS+WHAT_IF), videns-vedligeholdelse (6 filer inkl. HOLISTIC_EVALUATION). TRIAGE.md opdateret med 7 handlinger. 9 forbrugte backlog-filer arkiveret. → PROGRESS.md#session-21
- **Session 20** (2026-03-14): VPS v2+v3 evalueret, output hentet til PC. 3 skills, TI-projekt, research INDEX v3, BLUEPRINT.md, TRIAGE.md, vps-sandbox CONTEXT.md. → PROGRESS.md#session-20
- **Session 19** (2026-03-14): VPS sandbox v2 deployed (3 projekter), v1 kvalitetsauditeret, prompt evalueret+justeret, github-workflow handoff absorberet. → PROGRESS.md#session-19
- **Session 18** (2026-03-14): Ydrasil-projekt startet, MCP/Skills kompendium research done, 7 skills tilføjet, checkpoint-skill rettet, underscore-prefix fjernet. → PROGRESS.md#session-18
- **Session 17** (2026-03-14): Skills-synlighed afklaret, MCP/Skills kompendium brief→projekt, adversarial research-proces designet. → PROGRESS.md#session-17
- **Session 16** (2026-03-15): Backlog-audit (14→11 briefs), VPS research downloaded, research-kvalitet vurderet, prioritering diskuteret. → PROGRESS.md#session-16
- **Session 15** (2026-03-14): M5 step 11/13/14/17 done, M6-M8→backlog, token-scanning, parallel tasks absorberet, archive ryddet. → PROGRESS.md#session-15
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
