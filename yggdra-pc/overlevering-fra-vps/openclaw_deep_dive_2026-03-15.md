# OpenClaw Deep Dive — Hvad Det Er, Hvad Det Koster, Hvad Vi Stjæler

**Dato:** 15. marts 2026
**Formål:** Konkret analyse af OpenClaw-patterns relevante for Yttres VPS + Qdrant + Claude Code setup

---

## 1. Hvad Er OpenClaw Præcist

OpenClaw (tidl. Clawdbot/Moltbot) er en open-source autonom AI-agent bygget OVEN PÅ Claude Code. Den tilføjer tre ting Claude Code ikke har: **persistent hukommelse**, **heartbeat-daemon**, og **messaging-integration** (Telegram/WhatsApp/Slack). 430K+ linjer, TypeScript/Node.js. Peter Steinberger (Østrig) startede det, forlod projektet til OpenAI feb 2026 — nu community-drevet.

**Kerneforskel fra Claude Code:** Claude Code er reaktiv (du starter en session). OpenClaw er proaktiv (den vågner selv, checker inboxes, handler). Claude Code glemmer mellem sessions. OpenClaw husker via markdown-filer på disk.

---

## 2. Arkitektur — De 4 Byggeklodser

**SOUL.md** — Agentens identitet. Loades FØRST i system prompt. Svarer til vores CLAUDE.md.

**HEARTBEAT.md** — Tjekliste agenten gennemgår hvert 30. minut. "Check mail", "check Trello", "commit ændringer". Gateway-daemon (systemd) vækker agenten, den læser HEARTBEAT.md, beslutter om der er noget at gøre. Hvis nej: HEARTBEAT_OK (gratis). Hvis ja: handler.

**3-lags hukommelse:**
- **Tier 1 (always loaded):** MEMORY.md — maks ~100 linjer, kurateret. = Vores CLAUDE.md + MEMORY.md
- **Tier 2 (daily context):** `memory/YYYY-MM-DD.md` — daglige noter, auto-genereret. I dag + i går loades automatisk. = Vores episodes.jsonl
- **Tier 3 (deep knowledge):** `memory/people/`, `projects/`, `topics/` — søges via vektor-embeddings. = Vores Qdrant collections

**Cron vs. Heartbeat:** Cron = isolerede sessions, præcis tid, én opgave. Heartbeat = batch-check i hovedsession, kontekst-bevidst, fleksibel. OpenClaw bruger begge.

---

## 3. Heartbeat-Pattern i Detalje

Sådan virker det:
1. systemd/LaunchAgent kører gateway-daemon (always-on)
2. Hvert 30 min: daemon sender heartbeat-signal til agenten
3. Agent vågner, læser HEARTBEAT.md (tjekliste)
4. For hvert punkt: deterministisk check FØRST (API-kald, filcheck), LLM KUN hvis der er signal
5. Intet at gøre → HEARTBEAT_OK (ingen tokens brugt)
6. Noget at gøre → handler, evt. sender Telegram-besked

**Best practice:** Regel-baserede checks (Python/bash) som filter INDEN LLM. Kun kald Claude/Haiku når der er reelt signal at vurdere. Ellers brænder du $2-5/dag på "er der noget nyt? nej."

---

## 4. Mini-Claw Pattern

`mini-claw` (htlin222/mini-claw på GitHub) er en minimal Telegram-bot der bruger din Claude Pro/Max subscription direkte. Ingen API-cost. Persistent samtaler via Pi coding agent.

**Mønstret:** Én fokuseret agent, ét interface (Telegram), én opgave. Ikke 430K linjer men ~400-1000 linjer. Community bygger disse "micro-claws" til specifikke formål:
- Inbox-triage agent (sortér mail, foreslå svar)
- Research agent (overvåg RSS, opsummér nyt)
- DevOps agent (check logs, alerts)

**Relevans:** Yttre behøver ikke OpenClaw. Yttre behøver 3-4 mini-claws i Python.

---

## 5. Hukommelse — memsearch

Zilliz (folkene bag Milvus) extraherede OpenClaws hukommelsessystem som standalone library: **memsearch**. Det gør:
- Scanner markdown-mapper, splitter i chunks (heading-baseret)
- Embedder til Milvus (vektor DB)
- **Hybrid search: dense vektor + BM25 sparse + RRF reranking**
- Filer er source of truth, IKKE vector-indexet

**Kritisk indsigt:** OpenClaws hukommelse er IKKE magi. Det er markdown-filer + vektor-søgning + hybrid search. Præcis det vi allerede har med Qdrant + episodes.jsonl + MEMORY.md. Vi mangler bare: (1) hybrid search, (2) automatisk daily logs, (3) reranking.

---

## 6. Hvad Koster Det

| Setup | Kostnad/måned |
|-------|---------------|
| Personal, sparsom | $6-13 |
| Heartbeat hvert 30 min (Sonnet) | $30-90 |
| Heartbeat hvert 30 min (Opus) | $150+ |
| Heartbeat + cron jobs (heavy) | $100-300 |

**Pengeslugere:** Heartbeat der kalder LLM for at svare "nej, intet nyt" = $1-5/dag. Én bruger betalte $18.75 på én nat for Opus der spurgte "er det dag endnu?" hvert 30. minut.

**Yttres situation:** Claude Max subscription ($100/mo) + Groq (gratis) + OpenAI embeddings ($<5/mo). Heartbeat via Groq/Haiku = praktisk talt gratis. Heartbeat via Opus = katastrofe.

---

## 7. Hvad Yttre Skal STJÆLE (Ikke Installere)

### A. 3-lags hukommelse (allerede 80% på plads)
Vi har: MEMORY.md (Tier 1), episodes.jsonl (Tier 2), Qdrant (Tier 3).
**Mangler:** Automatiske daily markdown-logs (`memory/YYYY-MM-DD.md`). auto_dagbog.py gør dette delvist men output er i DAGBOG.md, ikke per-dag filer. **Fix: 10 linjer i save_checkpoint.py.**

### B. Heartbeat med regel-baseret filter (50 linjer Python)
```
heartbeat.py:
  1. Check ny mail (IMAP, ingen LLM) → flag hvis ny
  2. Check Google Tasks (API, ingen LLM) → flag hvis ny
  3. Check Telegram (polling, ingen LLM) → flag hvis ny
  4. HVIS noget flagget → kald Groq/Haiku: "opsummér og prioritér"
  5. HVIS intet flagget → exit (0 tokens brugt)
```
**Cost:** $0 ved intet nyt. ~$0.001 per Haiku-kald ved signal. Kør hvert 30 min via cron.

### C. HEARTBEAT.md som konfig (0 linjer kode)
Opret `/root/Yggdra/data/HEARTBEAT.md` med tjekliste. heartbeat.py læser den. Ændringer i behavior = rediger markdown, ikke kode.

### D. Hybrid search i Qdrant (konfiguration)
Qdrant supporterer sparse vectors (BM25) native. Vi bruger det ikke. memsearch-mønstret: dense + sparse + RRF reranking. **Effort: re-ingest med sparse vectors, ~1 dag.**

### E. Cron-isolerede sessions til tunge opgaver
OpenClaws cron kører i isolerede sessions (egen kontekst, billigere model). Vi gør dette allerede med `claude --print`. **Forbedring:** Tilføj model-override per job (Haiku til simpelt, Sonnet til komplekst).

---

## 8. Hvad Yttre IKKE Skal Gøre

- **Installere OpenClaw** — 430K linjer TypeScript, Node.js, massiv dependency. Vi har allerede 80% af værdien.
- **Installere memsearch** — kræver Milvus. Vi har Qdrant. Stjæl mønstret, ikke koden.
- **Heartbeat med Opus** — $5/dag for "er der noget nyt? nej." Brug Groq/Haiku.
- **Gateway-daemon** — systemd service der holder forbindelse. Overkill. Cron hvert 30 min gør det samme.
- **Multi-agent routing** — OpenClaws multi-agent er for teams. Solo = én agent med gode tools.

---

## 9. Konkret Handlingsplan for Yttre

| # | Handling | Effort | Impact |
|---|---------|--------|--------|
| 1 | Genaktivér heartbeat.py med regel-baseret filter | 2 timer | Proaktivitet uden LLM-cost |
| 2 | Opret HEARTBEAT.md som konfig-fil | 15 min | Behavior-as-config |
| 3 | Tilføj daily markdown-logs i save_checkpoint.py | 30 min | Tier 2 memory |
| 4 | Hybrid search i Qdrant (sparse vectors) | 1 dag | 15-25% bedre retrieval |
| 5 | Reranking i ctx (Cohere/cross-encoder) | 2 timer | Præcisere top-5 |
| 6 | Temporal decay i ctx-scoring | 30 min | Friskere resultater |

**Total effort:** ~2 dage. **Resultat:** 90% af OpenClaws værdi, 0% af dens kompleksitet.

---

## Kilder

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Docs: Cron vs Heartbeat](https://docs.openclaw.ai/automation/cron-vs-heartbeat)
- [OpenClaw Docs: Memory](https://docs.openclaw.ai/concepts/memory)
- [memsearch (Zilliz)](https://github.com/zilliztech/memsearch)
- [mini-claw](https://github.com/htlin222/mini-claw)
- [openclaw-config (TechNickAI)](https://github.com/TechNickAI/openclaw-config)
- [OpenClaw Memory Masterclass (VelvetShark)](https://velvetshark.com/openclaw-memory-masterclass)
- [Heartbeats: Cheap Checks First (DEV.to)](https://dev.to/damogallagher/heartbeats-in-openclaw-cheap-checks-first-models-only-when-you-need-them-4bfi)
- [OpenClaw Costs (Hostinger)](https://www.hostinger.com/tutorials/openclaw-costs)
- [OpenClaw Production Stack on $15 VPS (Medium)](https://medium.com/@rentierdigital/the-complete-openclaw-architecture-that-actually-scales-memory-cron-jobs-dashboard-and-the-c96e00ab3f35)
- [Milvus Blog: OpenClaw Guide](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
- [All Things Open: OpenClaw Anatomy](https://allthingsopen.org/articles/openclaw-viral-open-source-ai-agent-architecture)
