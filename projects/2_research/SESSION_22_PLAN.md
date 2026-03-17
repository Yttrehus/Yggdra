# Session 22 — Konsolideret Plan
**Dato:** 2026-03-15
**Basis:** 7 research-agenter, blue/red/neutral evaluering

---

## Kontekst

22 sessioner har produceret 16 briefs, 30+ research-filer og 3000+ linjer analyse. Konsolideringsanalysen viser at det meste handler om **2 konkrete problemer:**
1. ctx returnerer ikke gode nok resultater
2. Kontekst forsvinder mellem sessioner

Plus vedligeholdelse af det der allerede kører.

## Del 1: VPS — allerede gjort

| Opgave | Status |
|--------|--------|
| RSS feeds (6 stk) | ✅ V5 |
| Heartbeat (30 min) | ✅ V5 |
| Temporal decay | ✅ V5 |
| Reranking (cross-encoder) | ✅ V5 |
| Pipeline health check | ✅ V5 |
| Source cleanup | ✅ V5 |
| Circuit breakers | ✅ V5 |
| Qdrant indexes (5 collections) | ✅ Session 22 |
| Automation inventory | ✅ V6 |

## Del 2: Fix fundament (VPS)

| # | Opgave | Effort | Prioritet |
|---|--------|--------|-----------|
| 1 | Fix youtube_monitor.py (cred_text bug) | 30 min | KRITISK |
| 2 | Fix source_discovery.py (JSON-parse) | 30 min | KRITISK |
| 3 | Fix/slet process_session_log.py | 30 min | HØJ |
| 4 | Slet tmux pipe-pane fra crontab | 5 min | MIDDEL |
| 5 | Reducer hotmail til 3x/dag | 5 min | LAV |

## Del 3: Backlog konsolidering (PC)

### Arkivér (done/redundant)
- `brief.work-intake` → 9_archive (taxonomy er i brug)
- `brief.cross-session-peer-review` → 9_archive (praksis, ikke projekt)
- `raw.github-workflow` → 9_archive (marinerer = dead)

### Merge
- `RDY.context-engineering` → absorber i `DLR.session-blindhed` (samme problem)
- `memory-architecture` + `GAPS.md` + `WHAT_IF.md` → ét projekt: `SIP.retrieval`

### Minimal projektsæt (3 nye)
1. **SIP.retrieval** — hybrid search completion + fact extraction. Absorberer memory-architecture
2. **DLR.session-blindhed** (eksisterende) — hooks + compaction. Absorberer context-engineering
3. **research-architecture** (nedskaleret) — KUN research-praksis, IKKE ~/reference/ infra

### LIB.ydrasil cleanup
- **Behold ~30 filer** (7 crown jewels + agent/memory deep-dives + TI/voice/Nate)
- **Arkivér ~40 filer** (audits, rapporter, duplikater, process-meta)
- **Slet ~20 filer** (cruft: academic standards, plantegning v0.1, gamle chatlog-formater)
- **Opret 3 synteser:** agent_frameworks_reference.md, memory_implementation_guide.md, skills_inventory.md

## Del 4: Taxonomy migration (PC)
```bash
git mv projects/2_research projects/LIB.research
# Arkivér VPS prompt-filer
mkdir -p projects/9_archive/vps.prompt-drafts
git mv projects/0_backlog/vps-prompt-*.md projects/9_archive/vps.prompt-drafts/
git mv projects/0_backlog/vps-sandbox-v2.md projects/9_archive/vps.prompt-drafts/
# Opdatér refs i CONTEXT.md, CLAUDE.md, BLUEPRINT.md
```

## Del 5: Nye muligheder

### Google Maps + TI
- **VROOM** (Docker) — ruteoptimering, sammenlign med faktisk rækkefølge
- **Google Route Optimization API** — $200 gratis/måned
- **Heatmap** over stop-tæthed, vægt-distribution

### TI Økonomi
- Projekt oprettet: `REF.transportintra/subprojects/oekonomi/`
- Satser: 1 kr/kg organisk, 50 kr/spand, 40 kr plastpose
- Diesel: 39,4 L/100km gennemsnit
- Mangler: kg/dag og spande/dag for præcist regnestykke

### Obsidian
- Installer som read-only browser (5 min), lad Claude Code forblive primært
- Reel værdi: graph view + backlinks. Men ikke prioritet.

### Fabric
- Redundant med Yggdra. Brug patterns som inspiration for Claude Code skills.

### OpenClaw
- Principperne er allerede implementeret (heartbeat, episoder, MEMORY.md)
- Mangler: regel-baseret filter i heartbeat (tjek INDEN LLM-kald)

## Parkeret
- Hybrid search re-ingest (84K points, $2-5) — gør reranking-eval først
- Voice→Qdrant pipeline — kill-tegn: voice memos bruges ikke nok
- Mini-claws som arkitektur — byg on-demand, ikke som framework
- Skattekroner — marinerer

## Evaluering

**Blue team:** Analyse-fasen er overstået. 15 timers implementering > 15 timers analyse.
**Red team:** Fix broken cron jobs FØR nyt feature-arbejde. Fact extraction er ubevist.
**Neutral:** Red team har ret om prioritering. Dag 1 = fix fundament. Dag 2 = byg nyt.
