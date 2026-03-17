# Context — VPS Yggdra pr. 16. marts 2026

Current state af alt der kører, mangler, og venter.

---

## Infrastruktur

### Docker (5 services, alle stabile)
- **traefik** — reverse proxy + TLS (2 ugers uptime)
- **webapp** — nginx, volume-mounted til `/root/Ydrasil/app` (LIVE produktion)
- **qdrant** — vector DB, kun localhost:6333 (5 collections, ~47K vektorer — sessions+conversations slettet, docs→knowledge migreret)
- **api-logger** — custom Python, port 3003
- **tor-proxy** — separat container, port 9150/9151

### Cron (17 aktive jobs — se SUNDHEDSTJEK for komplet liste)
- `backup_offsite.sh` — 04:00 daglig (KRITISK)
- `morning_brief.py` — 07:00 daglig
- `heartbeat.py` — */30 min (08-21)
- `ai_intelligence.py` — 06:30 daglig + 06:15 søndag (weekly)
- `daily_sweep.py` — 08:00 daglig
- `weekly_audit.py` — 06:00 søndag
- `youtube_monitor.py` — 07:00 daglig ⚠️ (timeout)
- `source_discovery.py` — 08:00 søndag
- `cruft_detector.py` — 06:30 søndag
- `embed_docs.py` — 05:00 søndag ⚠️ (BØR DEAKTIVERES — migration done)
- `embed_advisor_brain.py` — 05:00 søndag
- `hotmail_sort.py` — 3x/dag (08:45, 13:45, 18:45)
- `process_session_log` — */6 timer ❌ (circuit breaker tripped)
- `prompt_miner` — 06:30 daglig (NY 16/3 — scanner sessioner for prompts)
- `rotate_episodes` — 05:30 søndag (NY 16/3 — 90-dages retention)
- `auto_dagbog` — 23:55 daglig

### Disabled
- `embed_docs` — DEAKTIVERET 16/3 (duplikerede knowledge collection efter migration)
- tmux pipe-pane (15/3 — "logs nobody reads")
- Trello sync (14/3 — Trello droppet)
- Voice memo pipeline (14/3)
- Navigator (lang tid)

### Hooks
- **PreCompact + Stop** → `save_checkpoint.py` — destillerer session via Groq
- **SessionStart** → `load_checkpoint.sh` — injicerer projekters NOW.md + episoder

## Sikkerhed

### Fikset 15/3
- Nginx dot-fil blokering tilføjet (`location ~ /\. { deny all; }`)
- `.env` var offentligt tilgængelig — nu 404

### VENTER: Nøglerotation
- Anthropic API key
- OpenAI API key
- Groq API key
- ElevenLabs API key
- Alle har været offentligt tilgængelige i ukendt tid

### Kendte risici
- **API-nøgler IKKE roteret endnu** — Anthropic, OpenAI, Groq, ElevenLabs. Skal gøres manuelt fra dashboards.
- Traefik API er `insecure=true`
- Alt kører som root
- Ingen firewall-regler dokumenteret
- API-logger har ingen auth
- **Substack-data aldrig indgået i briefings** — `substack_api` ikke installeret i venv (fundet i session 1f86132c)

## Research (80+ filer, ~28K linjer)

### Produceret denne weekend (17 filer)
| Fil | Kategori | Linjer |
|-----|----------|--------|
| `DESTILLAT_memory_retrieval.md` | Memory | 553 |
| `DESTILLAT_agents_automation.md` | Agents | 501 |
| `zero_token_pipeline_architecture.md` | Pipeline | 498 |
| `visual_llm_landscape_2026.md` | Visual AI | 386 |
| `klinisk_profilering_frameworks.md` | Psykologi | 450 |
| `RESEARCH_DEEP_STUDY_2026-03-15.md` | Meta | 303 |
| `skattepenge_ekspertkilder_2026.md` | Politik | 300 |
| `RESEARCH_CATALOG.md` | Meta | 222 |
| `RED_TEAM_EVALUERING_2026-03-15.md` | Evaluering | 200 |
| `hyperempati_klinisk_psykologi.md` | Psykologi | 180 |
| `mbti_vs_big_five_evidens.md` | Psykologi | 170 |
| `openclaw_deep_dive_2026-03-15.md` | Agents | 150 |
| `solo_dev_google_maps_ai_2026.md` | Transport | 150 |
| `personal_data_pipeline_best_practices.md` | Pipeline | 215 |
| `HOW_TO_BUILD_AGENTS.md` | Agents | 1075 |
| `claude_code_ecosystem_2026.md` | Tools | 740 |
| `automation_deep_audit_2026-03-15.md` | Audit | ~100 |

### Red team vurdering
- Automation audit: 9/10 (bedst — finder og fikser reelle problemer)
- Visual LLM landscape: 8/10 (bedste research-rapport)
- Destillater: 7/10 (solid men for lange — 500+ linjer er rapporter, ikke destillater)
- Research catalog: 6/10 (svagest — mangler definerede kvalitetskriterier)

## Hvad mangler (VPS-side)

### Kritisk
1. **API-nøgler bør roteres** — har været offentlige
2. **process_session_log timeout** — circuit tripped, 600s timeout, 3/3 failures

### Høj prioritet
3. **Dead scripts oprydning** — ~20 af 51 scripts er dead code
4. **Heartbeat verificering** — Telegram token fikset, men bør bekræftes at beskeder ankommer
5. **Commit alt** — massiv uncommitted state

### Middel prioritet
6. **Fact extraction PoC** — 50 linjer i save_checkpoint.py (Groq fact extraction)
7. ~~**SessionStart hook**~~ — FIKSET, peger korrekt på load_checkpoint.sh
8. ~~**6.7 GB GPU-pakker**~~ — SLETTET (session 7e1bfc05), 7 GB frigjort
9. **Dead Trello-kode** — i 5 scripts, klar til oprydning
10. **Substack-data mangler** — `pip install substack-api` + `fetch_rss()` i ai_intelligence.py
11. **Termux voice sync** — script klar (`scripts/integrations/termux_voice_sync.sh`), mangler installation på telefon
12. **Loops Framework v2** — dokumenteret i `research/LOOPS_PIPELINE_EJERSKAB_2026-03-16.md`, endnu ikke implementeret som skill/hook

### Opdateringer fra 16/3 sessioner (9 parallelle sessioner)
- **Mini-Claw Fase 1 DONE:** token-tracking + kill-switch + budget-cap i save_checkpoint.py og heartbeat.py
- **HEARTBEAT.md config-fil oprettet** — Trello deaktiveret, dynamisk behavior
- **get_context.py v3:** hybrid flags, auto-detection, fjernet refs til slettede collections
- **memory.py kopieret fra PC** til scripts/ — fungerer på VPS
- **rotate_episodes.py oprettet** — 90-dages retention, i cron søndag 05:30
- **prompt_miner.py oprettet** (27K) — scanner sessioner for prompts, i cron dagligt 06:30
- **heartbeat.py:** `check_prompt_miner()` tilføjet — kill condition 14 dage ubrugt
- **termux_voice_sync.sh** oprettet i scripts/integrations/ — `vm` alias til telefon→VPS voice sync
- **LOOPS_PIPELINE_EJERSKAB_2026-03-16.md** — loops-analyse med 7 fejltyper, framework v2
- **API-logger:** recovery endpoint (`/api/recovery`) tilføjet, nginx config opdateret
- **embed_docs cron DEAKTIVERET** — docs→knowledge migration fuldført
- **Dense > Hybrid:** 83% vs 61% Hit@5 — hybrid RRF bruges IKKE som default
- **Disk: 67%** (ned fra 74% efter torch/nvidia cleanup)
- **Friktion case study:** TI-app recovery bygget i 45 min til et problem der ikke eksisterede

## Hvad mangler (PC-side, fra SESSION_22_PLAN.md)

- P1: Taxonomy migration (git mv 2_research → LIB.research)
- P2: Terminal-automatisering (tasks.json)
- P3: Notion-spejling (database + kanban)
- P4: Automation-index PC-side
- P5: Webscraping-audit (allerede lukket)
- P6: Luk briefs (peer-review, github-workflow → arkiv)
- P7: Context-engineering hooks

## Repo-vurdering (ærlig)

| Dimension | Score |
|-----------|-------|
| Kodeorganisering | 5/10 |
| Dokumentation | 7/10 |
| Sikkerhed | 4/10 (forbedret fra 3) |
| Vedligeholdelse | 5/10 |
| Automatisering | 7/10 |

## Obsidian-bro (ny analyse)

**Status:** Analyseret, ikke implementeret. Anbefaling: BETINGET JA.
**Rapport:** `OBSIDIAN_BRO_ANALYSE.md` i denne mappe (484 linjer, 7 loops)
**Kernekonklusion:** ~200 markdown-filer er vault-egnede, ~440 wiki-links giver mening. Graph view + Dataview er de eneste genuint nye kapabiliteter. Red teams hårdeste argument: "Obsidian løser et problem Kristoffer ikke har bevist at han har."
**Dag 1 plugins:** Graph View (built-in), Dataview, Obsidian Git, Smart Connections
**Kill condition:** Fjernes efter 2 uger hvis < 3 åbninger/uge

## Aktive projekter (VPS projects/)

| Projekt | Status |
|---------|--------|
| transport | Intet — sterilisering har prioritet |
| assistent | Fundament-fase |
| automation | Hook-system under opdatering |
| bogfoering | Parkeret |
| forskning | Fundament-fase |
| notion | MCP reconnected, mangler konsolidering |
| rejse | Parkeret |
| research-architecture | Oprettet, fundament-fase |
| arkitektur | Under opbygning |
