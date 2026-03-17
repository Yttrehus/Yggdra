# VPS Sundhedstjek — 16. marts 2026

**Formål:** Komplet status-rapport til PC-session. Alt PC behøver vide for at fortsætte.
**Genereret af:** Opus 4.6 (VPS), mens PC er offline.

---

## 1. Infrastruktur

### Disk
| Metrik | Værdi | Bemærkning |
|--------|-------|------------|
| Disk total | 96 GB | |
| Brugt | ~64 GB (67%) | Var 71 GB (74%) inden cleanup — 7 GB frigjort (torch/nvidia/triton + .bak filer) |
| Ledigt | ~32 GB | |
| `/root/Yggdra/` | ~3 GB | scripts/venv renset for GPU-pakker (7.6→~0.9 GB) |
| `/root/Yggdra/data/` | 1.8 GB | Heraf gdrive_import ~1.1 GB |

**Status:** 7 GB frigjort i session 7e1bfc05 (torch/nvidia/triton + .bak filer). Disk vokser ~2 GB/uge. Kandidater for yderligere oprydning: `data/gdrive_import/` (1.1 GB), `data/checkpoints/`, gamle backup-filer.

### Docker (5 containere)
| Container | Status | Bemærkning |
|-----------|--------|------------|
| traefik | Up 2 weeks | HTTPS + routing |
| webapp (nginx) | Up 22 hours | Genstartet i går (CSS-fix?) |
| qdrant | Up 2 weeks | **5 collections, ~47K vektorer** (sessions+conversations slettet, docs→knowledge migreret) |
| api-logger | Up 2 weeks | TransportIntra proxy |
| tor-proxy | Up 2 weeks (healthy) | YouTube transcript pipeline |

### Qdrant (opdateret efter parallel session bf0fae7a + e01ce27b)
| Collection | Points | Status |
|------------|--------|--------|
| routes | 40,053 | ✓ BEHOLD — TransportIntra |
| **knowledge** | **6,626** | ✓ BEHOLD — migreret fra docs (1.466) + ingestet research (3.171) + docs (1.005) |
| advisor_brain | 453 | ✓ BEHOLD — unik, Miessler/Nate Jones/Practitioner's Bible |
| miessler_bible | 102 | ✓ BEHOLD — original kildemateriale |
| episodes | ~80 | ✓ BEHOLD — vokser ~30/dag |
| ~~sessions~~ | ~~43,511~~ | **SLETTET** — terminal noise, 27% SKIP |
| ~~conversations~~ | ~~81~~ | **SLETTET** — duplikerede episodes |
| ~~docs~~ | ~~1,466~~ | **MIGRERET** til knowledge |

**Total: ~47K vektorer (ned fra ~87K).** 46% reduktion, højere kvalitet.

### Retrieval-benchmark (session e01ce27b)
| Metode | Hit@5 |
|--------|-------|
| **Dense-only** | **83%** |
| Hybrid RRF (dense+sparse) | 61% |

**Konklusion:** Dense-only er bedre. Hybrid RRF skader fordi sparse-noise diluter gode dense-resultater. Hybrid undersøges videre men bruges IKKE som default.

---

## 2. Hooks & Automation

### Hooks (config korrekt, men strukturelle problemer)
| Hook | Script | Status |
|------|--------|--------|
| SessionStart | `load_checkpoint.sh` | ✓ Config korrekt — men output-format bør verificeres |
| Stop | `save_checkpoint.py` | ✓ Virker — Groq destillering → episode + NOW.md |
| PreCompact | `save_checkpoint.py` | ✓ Virker |
| Notification | (tom) | Fjernet — var throttled 10 min |

**NOW.md note fra automation-projektet siger "Fix SessionStart hook (peger på echo, ikke load_checkpoint.sh)"** — dette er FORÆLDET. Hooket peger korrekt på load_checkpoint.sh. NOW.md er opdateret.

### Kritiske Cron-Fejl (fra audit-agent)

| Problem | Severity | Detalje |
|---------|----------|---------|
| **session_log TIMEOUT** | KRITISK | Circuit breaker tripped 15/3 kl. 18:10. Genstartet, nu failure 2/3. 600s timeout for stram. |
| **youtube_monitor TIMEOUT** | HØJ | Første timeout 16/3 kl. 07:05. 300s timeout — sandsynligvis Tor rate-limiting. |
| **35% episoder uden projekt** | STRUKTUREL | 216/614 episoder har `project: unknown`. Groq kun kaldt ved Stop, ikke Notification. |

### Episodes
- 614 episoder i `data/episodes.jsonl`
- Seneste: i dag kl. 11:04 (session bf0fae7a)
- **216 (35%) har ingen projekt-tildeling** — forurener projekt-NOW.md routing
- `rotate_episodes.py` oprettet (session e01ce27b) — 90-dages retention, klar til brug.

### Cron (17 aktive jobs)

| Job | Tid | Status | Bemærkning |
|-----|-----|--------|------------|
| backup_offsite | 04:00 daglig | ✓ | Kritisk — behold |
| embed_advisor_brain | 05:00 søndag | ⚠️ | Duplikerer? PC har knowledge collection |
| embed_docs | 05:00 søndag | ⚠️ | Duplikerer knowledge — **BØR DEAKTIVERES** (docs→knowledge migration DONE) |
| weekly_audit | 06:00 søndag | ✓ | Producerer audit-rapporter |
| ai_intelligence | 06:30 daglig | ✓ | Daily briefing |
| ai_intelligence --weekly | 06:15 søndag | ✓ | Weekly briefing |
| cruft_detector | 06:30 søndag | ✓ | Kill condition: fjern når bedre monitoring |
| youtube_monitor | 07:00 daglig | ⚠️ | TIMEOUT 16/3 — failure 1/3, circuit breaker snart |
| morning_brief | 07:00 daglig | ✓ | Groq-baseret morgenrapport |
| source_discovery | 08:00 søndag | ✓ | Nye kilder |
| daily_sweep | 08:00 daglig | ✓ | Oprydning |
| hotmail_autosort | 08:45/13:45/18:45 | ✓ | 3x daglig |
| heartbeat | */30 min, 08-21 | ✓ | Gmail, kalender, tasks check |
| process_session_log | */6 timer | ❌ | CIRCUIT BREAKER TRIPPED — timeout 600s for stram |
| prompt_miner | 06:30 daglig | ✓ NY | Prompt-mining fra sessioner (27K script) |
| rotate_episodes | 05:30 søndag | ✓ NY | 90-dages episode retention |
| auto_dagbog | 23:55 daglig | ✓ | Dagbogsindlæg |

**Cron-ændringer 16/3 (aften-sessioner):**
- `embed_docs` → **DEAKTIVERET** (migration done, duplikerede knowledge)
- `prompt_miner` → **TILFØJET** dagligt kl. 06:30 (scanner sessioner for genanvendelige prompts)
- `rotate_episodes` → **TILFØJET** søndag kl. 05:30 (90-dages retention)

**Cron-anbefaling:**
- `process_session_log` → EVALUER om den stadig producerer nyttigt output
- `embed_advisor_brain` → BEHOLD (advisor_brain er separat domæne)

---

## 3. Projekter — Samlet Status

| Projekt | Status | Seneste aktivitet | Næste handling |
|---------|--------|-------------------|----------------|
| **arkitektur** | Aktiv | 16/3 — projekt-struktur, hooks | Konsolidér brain/ → projects/ |
| **automation** | Aktiv | 16/3 — Mini-Claw Fase 1 DONE | Fase 2: multi-collection HEARTBEAT, token-dashboard |
| **transport** | Parkeret | 15/3 — sterilisering | Stop-beskrivelser, ikoner |
| **forskning** | Fundament | 16/3 — research loops | Definér første research-projekt |
| **assistent** | Fundament | 14/3 — gdrive access | Ryd op gdrive_import (1.1 GB) |
| **notion** | Fundament | 8/3 — MCP connector | Konsolidér workspaces |
| **research-architecture** | Fundament | 8/3 — scope defineret | Kortlæg ekspert-frameworks |
| **bogfoering** | Parkeret | 8/3 | Aktiveres ved behov |
| **rejse** | Parkeret | 15/3 | Aktiveres ved næste rejse |

**Alle 9 projekter har CONTEXT.md + NOW.md.** Struktur er komplet.

---

## 4. Research — Komplet Inventory

### /research/ (VPS) — 200 filer, 8.4 MB
- **97 .md-filer** (7.6 MB) + 103 supplementære (PNG, mermaid, LaTeX, Python, JSON)
- RESEARCH_CATALOG.md eksisterer men dækker kun 79/97 filer

**Kategorier (fra fuld audit):**

| Kategori | Antal .md | Størrelse | Highlights |
|----------|-----------|-----------|------------|
| AI Agents & Automation | 15 | ~250K | CH6 = 50K (størst fil). OpenClaw, LangGraph, PI agent |
| Memory & Retrieval | 11 | ~270K | DESTILLAT_memory = kompakt konsolideret |
| Bog-projekt (CH1-CH10) | 25 | ~650K | 10 kapitler + 9 praksis-versioner + 6 research-filer |
| Claude Code & Anthropic | 5 | ~110K | claude_code_ecosystem = 44K (25+ repos) |
| Prompting & Context | 9 | ~170K | Anti-patterns research stærkest |
| Infrastructure | 11 | ~170K | Whisper pricing, hardware, dev env |
| Visualization & Design | 9 | ~200K | Brainmap v1+v2, knowledge viz survey |
| Psykologi | 3 | ~66K | NYT (15/3): hyperempati, MBTI, klinisk profilering |
| Meta & Methodology | 8 | ~180K | Layer 1→2 progression, RESEARCH_DEEP_STUDY |
| Destillater | 3 | ~85K | DESTILLAT_memory, DESTILLAT_agents, RED_TEAM |

**Strukturelle problemer:**
- Navngivning inkonsistent (`CH7_ADVANCED_PROMPTING.md` vs `ch7_prompting_antipatterns_research.md`)
- Ingen arkiv-segment — gamle filer blandet med nye
- HOW_TO_BUILD_AGENTS har 4 versioner (.md, _pandoc.md, .pdf, .tex)
- Psykologi-filer (15/3) er standalone, ikke integreret i nogen kategori

### data/research/ (VPS) — 18 filer, 784 KB
- 6 .md-filer + 12 JSON-filer (arXiv/Semantic Scholar søgeresultater)
- Overlapper delvist med /research/

### PC-side (fra CONTEXT.md)
- **LIB.research/** — llm-landskab (7 profiler), ai-frontier (5 topics), videns-vedligeholdelse (6 filer)
- **LIB.ydrasil/** — VPS-æra research + docs (89+73 filer)

**Anbefaling:** Research eksisterer i 3+ lokationer. Konsolidering bør være en PC-opgave. Lavthængende frugt: opdater RESEARCH_CATALOG.md med de 18 manglende filer.

---

## 5. Memory Cleanup — DONE

| Metrik | Før | Efter |
|--------|-----|-------|
| MEMORY.md linjer | 221 (over 200-grænsen) | 74 |
| Topic-filer | 2 | 4 |

**Hvad blev gjort:**
- Forældede facts opdateret ("Kris har INGEN PC" → PC ankommet 4/3)
- "Deep Research 23/2" (36 linjer) → `project_continuous_memory.md`
- "Key Learnings" (62 linjer) → `reference_technical_learnings.md`
- Trello-detaljer trimmet (Trello droppet 4/3)
- Færdige items komprimeret

**Topic-filer:**
1. `project_continuous_memory.md` — OpenClaw byggeplan
2. `reference_technical_learnings.md` — VitePress, YouTube/Tor, Qdrant, TI API
3. `book_writing.md` — AI Practitioner's Bible (uændret)
4. `feedback_security_env.md` — .env fix (uændret)
5. `feedback_loops_metoden.md` — Loops-metoden (uændret)

---

## 6. Parallel Session Status (bf0fae7a + e01ce27b)

Session bf0fae7a leverede **5 rapporter** i `yggdra-pc/overlevering-fra-pc/` + implementerede alt fra Mini-Claw. Session e01ce27b fortsatte med knowledge ingest og retrieval eval.

1. ✅ `QDRANT_LEGACY_AUDIT.md` — sessions+conversations SLETTET, docs MIGRERET
2. ✅ `EVAL_SUITE.json` — 20 test-queries for memory.py
3. ✅ `MINI_CLAW_ARCHITECTURE.md` — **IMPLEMENTERET** (token-tracking + kill-switch + budget-cap + HEARTBEAT.md)
4. ✅ `BACKLOG_STRUCTURE_PROPOSAL.md` — 3 præfikser (active/ref/_archive) vs "gør ingenting"
5. ✅ `RESEARCH_KVALITETSFRAMEWORK.md` — PhD-niveau referencekrav, kvalitetskriterier

---

## 7. PC-Session Anbefalinger — Prioriteret

### Skal gøres (høj ROI, lav risiko)
1. ~~**Slet Qdrant legacy**~~ — **DONE** (session bf0fae7a): sessions (43K) + conversations (81) slettet. docs (1.466) migreret til knowledge.
2. **Kør eval-suite:** Test memory.py search med de 20 queries fra EVAL_SUITE.json
3. **Deaktiver embed_docs cron:** Duplikerer knowledge collection. `crontab -e`, kommenter linje ud.

### Bør gøres (medium ROI)
4. ~~**Mini-Claw Fase 1**~~ — **DONE** (session bf0fae7a): token-tracking + kill-switch + budget-cap i save_checkpoint.py + heartbeat.py
5. ~~**Migrer docs → knowledge**~~ — **DONE** (session bf0fae7a): 1.466 points migreret, knowledge nu 6.626 points
6. **Opdater RESEARCH_CATALOG.md:** 97 filer nu, katalog dækker kun 79

### Kan vente
7. **Obsidian:** Parkeret (PC beslutning). Fase 0 = 5 min test.
8. **Research-konsolidering:** 3 lokationer → 1. Lav risiko, lav urgency.
9. **Episodes rotation:** 614 episoder, vokser ubegrænset. Implementer 90-dages retention.
10. **Disk-oprydning:** gdrive_import (1.1 GB) er den lavthængende frugt.

---

## 8. Kendte Fejl / Forældede State

| Problem | Lokation | Fix |
|---------|----------|-----|
| NOW.md sagde "Fix SessionStart hook" | projects/automation/NOW.md | FIXED — hooket var korrekt, NOW.md opdateret |
| MEMORY.md sagde "Kris har INGEN PC" | MEMORY.md | FIXED i denne session |
| **session_log CIRCUIT BREAKER** | cron (process_session_log.py) | Øg timeout fra 600s→900s, eller fix OOM i scriptet |
| **youtube_monitor TIMEOUT** | cron (youtube_monitor.py) | Øg timeout fra 300s→600s, tjek Tor circuit |
| **35% episoder uden projekt** | data/episodes.jsonl | Kald Groq project-ID også ved Notification-events |
| RESEARCH_CATALOG dækker 79/97 filer | research/RESEARCH_CATALOG.md | Opdater med 18 nye filer |
| embed_docs cron duplikerer knowledge | crontab | **DEAKTIVERET** 16/3 |
| Notification hook tom | .claude/settings.local.json | Bevidst — var problematisk |
| **prompt_miner i HEARTBEAT men ikke i kode** | heartbeat.py | **FIXED** 16/3 — check_prompt_miner() tilføjet |
| **Substack aldrig i briefings** | ai_intelligence.py | substack_api ikke installeret, ingen fetch_rss() |
| **Loops fejlmønstre (F5, F7)** | Systemisk | Planer ≠ produkter, research > building. Se LOOPS rapport |

---

## 9. Fil-liste: Alt oprettet/ændret i denne session

| Handling | Fil | Beskrivelse |
|----------|-----|-------------|
| OPRETTET | `yggdra-pc/overlevering-fra-vps/VPS_SUNDHEDSTJEK_2026-03-16.md` | Denne rapport |
| OPDATERET | `projects/automation/NOW.md` | Fjernet forældet bug, tilføjet Mini-Claw næste-skridt |
| OPDATERET | `~/.claude/.../memory/MEMORY.md` | 221→74 linjer |
| OPRETTET | `~/.claude/.../memory/project_continuous_memory.md` | OpenClaw byggeplan (fra MEMORY.md) |
| OPRETTET | `~/.claude/.../memory/reference_technical_learnings.md` | Tekniske learnings (fra MEMORY.md) |
| OPRETTET | `~/.claude/.../memory/feedback_friktion_case_study_260316.md` | TI-app friktion: 45 min spildt |
| OPRETTET | `scripts/prompt_miner.py` | Prompt-mining fra sessioner (27K) |
| OPRETTET | `scripts/integrations/termux_voice_sync.sh` | Telefon→VPS voice memo sync |
| OPRETTET | `research/LOOPS_PIPELINE_EJERSKAB_2026-03-16.md` | Loops-analyse, 7 fejltyper, framework v2 |
| OPDATERET | `scripts/heartbeat.py` | `check_prompt_miner()` tilføjet |
| OPDATERET | `scripts/api_logger.py` | `/api/recovery` endpoint tilføjet |
| OPDATERET | `app/nginx.conf` | Route til `/api/recovery` |
| OPDATERET | `crontab` | +prompt_miner (06:30), +rotate_episodes (05:30 søn), -embed_docs |

---

*Rapport genereret kl. 12:10, mandag 16. marts 2026. VPS session (Opus 4.6).*
*3 parallelle research-agenter brugt: repo-scan, research-kortlægning, hooks/automation audit.*
