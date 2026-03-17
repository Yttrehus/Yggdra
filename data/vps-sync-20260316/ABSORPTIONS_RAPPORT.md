# Absorptions-rapport — VPS sync 16-17. marts 2026

Dækker: Alt produceret på VPS siden session 22 (15/3-2026). 9+ parallelle VPS-sessioner den 16/3.

---

## 1. Infrastruktur

**Qdrant oprydning:**
- 87K → 47K vektorer. `sessions` (43K) og `conversations` (81) slettet. `docs` (1.466) migreret til `knowledge`.
- `knowledge` er nu 6.626 points (op fra 984 på PC).
- `advisor_brain` (453) og `miessler_bible` (102) beholdes som separate collections.
- 7 GB disk frigjort (GPU-pakker fjernet). Disk 67% (var 74%).

**Kritisk finding: Dense > Hybrid.**
VPS-benchmark viser dense-only 83% Hit@5 vs. hybrid RRF 61%. Sparse-noise diluter gode resultater. PC's `memory.py` bruger hybrid som default — bør skifte til dense-only.

**Mini-Claw Fase 1:**
Token-tracking, kill-switch og budget-cap tilføjet i `save_checkpoint.py` og `heartbeat.py`. Budget: 100K tokens/dag.

**API-nøgler IKKE roteret** — Anthropic, OpenAI, Groq, ElevenLabs var eksponeret (nginx dot-fil-fix lavet, men nøglerne er de samme).

---

## 2. Automation & Scripts

**Nye/opdaterede scripts:**
- `prompt_miner.py` (27K) — scanner session-JSONL for genanvendelige prompts. Regelbaseret klassifikation + Groq-scoring. Dagligt kl. 06:30.
- `rotate_episodes.py` — 90-dages retention. Søndag 05:30.
- `termux_voice_sync.sh` — `vm` alias: telefon→VPS voice sync.
- `credentials.py` — centraliseret API-nøgle-modul med rate-limiting (Groq: 25 req/min, 10K/dag).
- `save_checkpoint.py` — nu med PreCompact-flush, budget-cap, og Groq-baseret projekt-routing.
- `heartbeat.py` — 30 min interval, 08-21 dansk tid, prompt_miner kill-condition check tilføjet.

**Crontab:** 17+ aktive jobs. Deaktiverede: navigator, voice_memo_pipeline, embed_docs, score_knowledge_batch, sync_inbox.

**Kendte fejl:**
- `process_session_log` circuit breaker tripped (3/3 failures, 600s timeout for stram).
- `youtube_monitor` timeout (Tor rate-limiting).
- 35% episoder mangler projekt-tildeling (216/614 har `project: unknown`).
- Groq API returnerer 403 — prompt_miner kørte blind.

---

## 3. Research

**Prompt Mining (1.270 prompts analyseret):**
- 54% kommandoer (8 ord gns.), 29% kør-løs (55 ord), 11% meta/strukturerede (600+ ord), 6% korrektioner (844 ord — dyreste mønster).
- Top effektive mønstre: struktureret opgave med output-spec + anti-patterns (3,5% af prompts, næsten altid first-shot success), fil-referencer (13,6%), implement-this-plan.
- Top ineffektive: vage kommandoer (53,9%), Termux-tastefejl (35,8%), korrektions-kaskader (6,3%).
- 8 copy-paste skabeloner i PROMPT_KATALOG.md.

**To store destillater:**
- `DESTILLAT_agents_automation.md` (501 linjer, 13 filer konsolideret).
- `DESTILLAT_memory_retrieval.md` (553 linjer, 12 filer + akademisk litteratur).

**Loops Framework v2:**
- `LOOPS_PIPELINE_EJERSKAB_2026-03-16.md` — 148 episoder analyseret, 7 fejltyper. F5 (planer≠produkter) og F7 (research>building) er de vigtigste.
- Dual-nature loop + pre-flight checklist.

**Intelligence briefings:**
- Claude Code v2.1.76 med forbedret MCP-elicitation.
- "Agentic engineering" som begreb breder sig (Simon Willison).
- Structured Distillation paper: 11x token-reduktion med bevaret retrieval-kvalitet.
- "MCP is dead; long live MCP" sentiment-skift.

---

## 4. Arkitektoniske beslutninger

**VPS Reformation Blueprint:** "Shared Repo, Split State" — VPS og PC deler repo men har separat state. 6 åbne beslutninger. Ikke implementeret endnu.

**VPS-beslutning:** VPS skal spejle PC-opsætning — intet eget "personlighedssystem."

**MEMORY.md ryddet:** 221→74 linjer. Forældet fact korrigeret.

---

## 5. VPS-projektstatus (alle fra NOW-filer)

| Projekt | Status |
|---|---|
| transport | Sterilisering har prioritet, intet aktivt |
| assistent | Fundament-fase, gdrive_import 1,1 GB uryddet |
| rejse | Parkeret |
| bogfoering | Parkeret |
| forskning | Fundament, 60+ filer i /research/ uden struktur |
| arkitektur | Projekt-baseret struktur under opbygning |
| automation | Hook-system kører, Mini-Claw fase 1 planlagt |

---

## 6. Leveret til PC (overlevering-fra-pc/)

- `EVAL_SUITE.json` — 20 test-queries til memory.py
- `EVAL_RESULTS.md` + `EVAL_RESULTS_HYBRID.md` — benchmark-resultater
- `QDRANT_LEGACY_AUDIT.md` — cleanup-plan
- `MINI_CLAW_ARCHITECTURE.md` — design for token-tracking
- `BACKLOG_STRUCTURE_PROPOSAL.md` — forslag til backlog-reform
- `RESEARCH_KVALITETSFRAMEWORK.md` — kvalitetskriterier
- `SESSION_FRIE_TOJLER_2026-03-16.md` — session-analyse
- `KAPITELSTRUKTUR_FORSLAG.md` — forslag til kapitelstruktur
- `VPS_PLAN.md` + `NEXT_SESSION_PROMPT.md`

---

## 7. Hvad kræver handling fra PC

**Kritisk:** Roter API-nøgler (Anthropic, OpenAI, Groq, ElevenLabs).

**Høj:** Skift memory.py default fra hybrid til dense-only. Kør eval-suite. Fix process_session_log timeout.

**Medium:** Installer termux_voice_sync.sh. Forny Groq API-nøgle. Deaktivér embed_docs cron.

**Lav:** VPS_REFORMATION_BLUEPRINT diskussion. Research-konsolidering. Backlog-struktur.
