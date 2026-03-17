# Overlevering fra VPS — 8.–16. marts 2026

Alt der blev produceret og diskuteret på VPS-instansen. Samlet her til PC-Claude.

---

## Dokumentation (denne mappe)

### Nye (16. marts — session med Opus 4.6)
| Fil | Hvad |
|-----|------|
| **VPS_SUNDHEDSTJEK_2026-03-16.md** | Komplet infrastruktur-rapport: disk, Docker, Qdrant, cron, hooks, projekter, research, fejl. 236 linjer. |
| **VPS_REFORMATION_BLUEPRINT.md** | Arkitekturdesign for VPS≈PC. "Shared Repo, Split State". 6 åbne beslutninger. Migrations-plan i 4 faser. |

### Tidligere (8.–15. marts)
| Fil | Hvad |
|-----|------|
| **progress.md** | Narrativ dagbog — hvad skete, i hvilken rækkefølge, og hvorfor |
| **context.md** | Current state — infrastruktur, sikkerhed, research, hvad der mangler |
| **chatlog.md** | Kondenseret chatlog fra alle 12 sessions |
| **REFLEKSION.md** | Hvad VPS-Claude lærte om Kristoffer — personligt, ærligt, ufiltreret |
| **SESSION_22_PLAN.md** | Konsolideret plan fra session 22 med blue/red/neutral evaluering |
| **OBSIDIAN_BRO_ANALYSE.md** | Obsidian som bro til Yggdra — arkitektur, steelman, red team, anbefaling (484 linjer) |

## Rapporter til PC (`overlevering-fra-pc/`)

Produceret af session bf0fae7a + e01ce27b som leverancer til PC-sessionen:

| Fil | Indhold |
|-----|---------|
| `QDRANT_LEGACY_AUDIT.md` | Audit af alle collections, slet/behold/migrer-anbefalinger |
| `MINI_CLAW_ARCHITECTURE.md` | Mini-Claw design — nu IMPLEMENTERET (Fase 1) |
| `EVAL_SUITE.json` | 20 test-queries for memory.py retrieval |
| `EVAL_RESULTS.md` + `EVAL_RESULTS_HYBRID.md` | Dense 83% vs Hybrid 61% Hit@5 |
| `BACKLOG_STRUCTURE_PROPOSAL.md` | Forslag til projekt-præfikser |
| `RESEARCH_KVALITETSFRAMEWORK.md` | PhD-niveau referencekrav |
| `NEXT_SESSION_PROMPT.md` | Prompt til session e01ce27b (frie tøjler) |
| `SESSION_FRIE_TOJLER_2026-03-16.md` | Resultater fra frie-tøjler sessionen |
| `KAPITELSTRUKTUR_FORSLAG.md` | Forslag til backlog-kapitelstruktur (parkeret) |

## Session-filer (JSONL)

Rå Claude Code session-data. Kan parses med `python3 -c "import json; ..."`.

| Fil | Dato | Størrelse | Indhold |
|-----|------|-----------|---------|
| `aff0966e...2026-03-14.jsonl` | 8.–10. mar | 6.5 MB | "How to Build Agents" — research, manual, PDF-produktion |
| `1f86132c...2026-03-16.jsonl` | 15.–16. mar | 4.2 MB | Den store session — personlig besked, psykologi, research, sikkerhed |
| `f9506441...2026-03-14.jsonl` | 8.–10. mar | 1.3 MB | Claude Code Ecosystem rapport (PDF) |
| `89c484f6...2026-03-14.jsonl` | 14. mar | 1.1 MB | V1-loop + autonom delegation |
| `22ea4223...2026-03-14.jsonl` | 14. mar | 637 KB | V2-loop continuation, VPS-admin |
| `172373bf...2026-03-14.jsonl` | 9. mar | 606 KB | AI-biografi (ChatGPT-integration) |
| `94b3eadb...2026-03-14.jsonl` | 14. mar | 473 KB | TI kildeindeksering |
| `525d1317...2026-03-14.jsonl` | 14. mar | 353 KB | Ralph Loop V2 (10 iterationer, 45 filer) |
| `7041cf04...2026-03-14.jsonl` | 14. mar | 159 KB | Qdrant-guide til PC |
| `0b39188c...2026-03-14.jsonl` | 14. mar | 68 KB | Research-agenter (Notion + metodik) |
| `b2a02afb...2026-03-15.jsonl` | 15. mar | 32 KB | Usage-check ($16.68 total) |
| `cea36c18...2026-03-14.jsonl` | 14. mar | 4 KB | Fejlet session (auth error) |

## Research-filer (MD)

### Psykologi & Personlighed
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `klinisk_profilering_frameworks.md` | 450 | Tilknytningsteori, skematerapi, IFS, polyvagal, mentalisering, ACE — 45+ kilder |
| `mbti_vs_big_five_evidens.md` | 170 | MBTI er pseudovidenskab, Big Five er evidensbaseret, INFJ-fælden |
| `hyperempati_klinisk_psykologi.md` | 180 | C-PTSD, parentificering, hypervigilans, fawn-respons |

### AI Agents & Memory
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `DESTILLAT_memory_retrieval.md` | 553 | Konsolidering af 12 filer, 70+ kilder, evidensniveauer markeret |
| `DESTILLAT_agents_automation.md` | 501 | Konsolidering af 13 filer, frameworks, compounding reliability |

### Pipeline & Arkitektur
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `zero_token_pipeline_architecture.md` | 498 | Regelbaserede pipelines uden tokenforbrug, kørbar Python-kode |
| `personal_data_pipeline_best_practices.md` | 215 | Willison/Dogsheep, karlicoss/HPI, praktiske patterns |

### Visual AI
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `visual_llm_landscape_2026.md` | 386 | Multimodale modeller: generering stærk, forståelse fake. Steelman+red team |

### Politik & Økonomi
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `skattepenge_ekspertkilder_2026.md` | 300 | Danske institutioner, akademikere, åbne datasæt, CPI er perceptionsbaseret |

### Meta & Evaluering
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `RESEARCH_DEEP_STUDY_2026-03-15.md` | 303 | Hvad vi ved, mangler, overlapper + 20 nye kilder |
| `RESEARCH_CATALOG.md` | 222 | 79 filer kategoriseret, 3 duplikater, 63% HIGH kvalitet |
| `RED_TEAM_EVALUERING_2026-03-15.md` | 200 | Brutal vurdering af alt output |

### Domæne
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `openclaw_deep_dive_2026-03-15.md` | 150 | OpenClaw arkitektur, 90% allerede implementeret i Yggdra |
| `solo_dev_google_maps_ai_2026.md` | 150 | VROOM, Route Optimization API, Google Cloud |

### Loops & Metodik
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `LOOPS_PIPELINE_EJERSKAB_2026-03-16.md` | ~500 | 7 fejltyper (F1-F7), dual-nature loop framework, pipeline-arkitektur, ejerskabs-matrix |

### Audit
| Fil | Linjer | Indhold |
|-----|--------|---------|
| `automation_deep_audit_2026-03-15.md` | 100 | 18 cron jobs, 5 Docker, fixes, anbefalinger |
| `audit_2026-03-15.md` | ~50 | Ugentlig audit |

---

## Hvad VPS-sessionerne 16/3 har gjort (5 parallelle sessioner)

### Session 7e1bfc05 — VPS vedligehold & overlevering
- **7 GB disk frigjort** — GPU packages (torch/nvidia/triton) fjernet, ingen scripts brugte dem
- **19 .bak filer slettet** — alt i git history
- **MEMORY.md renset** — 221→74 linjer, 2 nye topic-filer (intet indhold tabt)
- **automation/NOW.md opdateret** — forældet "fix SessionStart hook" bug fjernet
- **3 research-filer fikset** — kildehenvisninger tilføjet/udvidet
- **VPS_SUNDHEDSTJEK_2026-03-16.md** + **VPS_REFORMATION_BLUEPRINT.md** skrevet

### Session bf0fae7a — Qdrant-audit, Mini-Claw, eval-suite
- **Qdrant oprydning:** sessions (43K) + conversations (81) SLETTET. docs (1.466) MIGRERET til knowledge
- **Mini-Claw Fase 1 DONE:** token-tracking + kill-switch + budget-cap i `save_checkpoint.py` + `heartbeat.py`
- **HEARTBEAT.md** oprettet som config-fil (behavior-as-config)
- **get_context.py v3:** hybrid search flags, auto-detection, oprydning af dead collections
- **5 rapporter** skrevet til `overlevering-fra-pc/` (QDRANT_LEGACY_AUDIT, EVAL_SUITE, MINI_CLAW_ARCHITECTURE, BACKLOG_STRUCTURE_PROPOSAL, RESEARCH_KVALITETSFRAMEWORK)
- **memory.py** kopieret fra PC til `scripts/`

### Session e01ce27b — Knowledge ingest & retrieval eval
- **Knowledge collection:** 2.450 → 6.626 points (research/ + docs/ ingestet)
- **Stale sessions slettet** (198 ANSI-støjfyldte points)
- **Retrieval benchmark:** Dense-only 83% Hit@5 vs Hybrid RRF 61% — **dense vinder**
- **advisor_brain analyseret:** 453 points, 3 kilder — BEHOLD separat
- **rotate_episodes.py** oprettet (90-dages retention)
- **get_context.py** fjernet refs til slettede collections

### Session 1f86132c — Research, sikkerhed, Obsidian
- **V3/V5 loops** med research-konsolidering (destillater, catalog, deep study)
- **Sikkerhedsfix:** nginx dot-fil blokering — `.env` med 4 API-nøgler var offentlig
- **OBSIDIAN_BRO_ANALYSE.md** (484 linjer, 7 loops) — betinget ja

### Kritiske fund
1. **API-nøgler IKKE roteret** — Anthropic, OpenAI, Groq, ElevenLabs var offentlige
2. **Dense > Hybrid RRF** — 83% vs 61% Hit@5. Hybrid bruges IKKE som default.
3. **Qdrant: 87K → 47K vektorer** — 46% reduktion, højere kvalitet
4. **Disk: 74% → 67%** efter 7 GB cleanup
5. **SSH PasswordAuthentication er YES** — venter på godkendelse
6. **Friktion case study** — 45 min spildt pga. antagelse (TI-app data "tabt") uden verifikation
7. **Substack-data aldrig indgået i briefings** — `substack_api` ikke installeret i venv
8. **Loops-analyse:** 7 fejltyper identificeret fra 148 episoder — F5 (planer ≠ produkter) og F7 (research > building) er de vigtigste

### Session 39336706 — Loops-analyse + Pipeline-arkitektur
- **LOOPS_PIPELINE_EJERSKAB_2026-03-16.md** skrevet (~500 linjer, 6 dele) — analyse af 148 episoder, 7 fejltyper (F1-F7), dual-nature loop framework, pipeline-arkitektur, ejerskabs-matrix
- **Loops Framework v2:** Hver loop er 60% byg + 40% udfordre. Reducerer 4→2 loops. Pre-flight checklist.
- **Memory opdateret:** `feedback_loops_metoden.md` udvidet med optimerings-vision

### Session b1720cb5 — Prompt-mining + perfekte prompts
- **prompt_miner.py** oprettet (27K) — scanner alle Claude Code sessioner for prompts, scorer dem, gemmer i `data/prompt_mining/`
- **5 prompt-versioner** genereret til fremtidige sessioner (overlevering, loops-analyse, research, voice memo, frie tøjler)
- **Termux voice sync** designet — `vm` alias for telefon→VPS voice memo transfer

### Session 1fd0c7b4 — Heartbeat alignment + cron
- **heartbeat.py:** `check_prompt_miner()` funktion tilføjet — checker kill condition (14 dage ubrugt)
- **2 nye cron jobs:** `prompt_miner.py daily` kl. 06:30 + `rotate_episodes.py` kl. 05:30 søndag
- **embed_docs cron DEAKTIVERET** — duplikerede knowledge collection
- **Overleveringsdokumenter opdateret** via parallelle agenter

### Session 661d7d2f — TI-app data recovery + friktion
- **API-logger recovery endpoint** tilføjet (`/api/recovery`) — modtager localStorage fra JS-appen
- **Docker/nginx config ændret:** nginx.conf opdateret til at route `/api/recovery` til api-logger
- **Friktion case study** dokumenteret — 45 min brugt på at bygge recovery-system til et problem der ikke eksisterede (data var allerede nået igennem til TI-serveren)
- **Kerneregel:** Verificér problemet eksisterer FØR du bygger løsningen
- **Termux voice sync script** (`scripts/integrations/termux_voice_sync.sh`) — klar til installation

### Ikke gjort (bevidst, pga. planlagt reformation)
- Cron-fixes (youtube_monitor, session_log) — reformeres alligevel
- Shebang/Trello cleanup i scripts — reformeres alligevel
- Episode backfill — episode-system ændres måske
