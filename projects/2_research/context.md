# Context — VPS Yggdra pr. 16. marts 2026

Current state af alt der kører, mangler, og venter.

---

## Infrastruktur

### Docker (4 services, alle stabile)
- **traefik** — reverse proxy + TLS (2 ugers uptime)
- **webapp** — nginx, volume-mounted til `/root/Ydrasil/app` (LIVE produktion)
- **qdrant** — vector DB, kun localhost:6333 (7 collections, 84K+ vektorer)
- **api-logger** — custom Python, port 3003
- **tor-proxy** — separat container, port 9150/9151

### Cron (11 aktive jobs)
- `morning_brief.py` — daglig kl. 07:00
- `heartbeat.py` — hvert 30 min (08-21)
- `ai_intelligence.py` — daglig kl. 06:00
- `daily_sweep.py` — daglig kl. 05:00
- `weekly_audit.py` — søndag kl. 04:00
- `youtube_monitor.py` — daglig kl. 03:00
- `source_discovery.py` — daglig kl. 02:00
- `cost_guardian.py` — daglig kl. 01:00
- `embed_docs.py` — daglig kl. 23:00
- `embed_advisor_brain.py` — daglig kl. 22:00
- `hotmail_sort.py` — 3x/dag (08:45, 13:45, 18:45)

### Disabled
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
- Traefik API er `insecure=true`
- Alt kører som root
- Ingen firewall-regler dokumenteret
- API-logger har ingen auth

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
7. **SessionStart hook** — peger muligvis på echo, ikke load_checkpoint.sh
8. **6.7 GB GPU-pakker** — nvidia/torch/triton på GPU-løs VPS, kan fjernes
9. **Dead Trello-kode** — i 5 scripts, klar til oprydning

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
