# WHAT IF — Hvad Kan Yttre Implementere I Morgen?

**Baseret på:** agent-architectures.md, agent-teams.md, memory-systems.md, automation-patterns.md
**Prioriteret efter:** Impact × (1/Effort) — høj impact, lav effort først

---

## 1. Hybrid Search i Qdrant

**Effort:** Dage (1-2 dage)
**Impact:** Høj — 15-25% bedre retrieval for keyword-tunge queries
**Kræver:** Sparse vector config i Qdrant, BM25 tokenizer, re-ingest af eksisterende data
**Risiko:** Re-ingest af 84K points tager tid + OpenAI embedding cost (~$2-5). Kan mislykkes hvis sparse vectors bruger for meget hukommelse.
**How-to:**
1. Tilføj sparse vector config til Qdrant collections (routes, docs, advisor_brain)
2. Implementér BM25 sparse vector generation i embed-scripts
3. Re-ingest med både dense + sparse vectors
4. Opdatér ctx/get_context.py til hybrid query (0.7 dense + 0.3 sparse)
5. Test: sammenlign retrieval-kvalitet før/efter på 10 kendte queries

**Modenhed:** Production-ready (Qdrant supporterer det native)

---

## 2. Reranking i ctx-kommandoen

**Effort:** Timer (2-4 timer)
**Impact:** Høj — op til 48% bedre retrieval precision
**Kræver:** Cohere Rerank API key ($1/1000 queries) ELLER lokal BGE reranker
**Risiko:** Ekstra latency (~200-500ms per query). Cohere API kan være nede.
**How-to:**
1. `pip install cohere` i venv
2. I get_context.py: efter Qdrant top-20 retrieval, send til Cohere Rerank
3. Returnér top-5 efter reranking
4. Fallback til uden reranking hvis Cohere timeout
5. Test: sammenlign top-5 kvalitet på 10 queries

**Modenhed:** Production-ready

---

## 3. Circuit Breakers på Ralph Loops

**Effort:** Timer (1-2 timer)
**Impact:** Medium — forebyg runaway agents, $47K horror stories
**Kræver:** Ændring i loop-scripts (start_claude_tmux.sh eller wrapper)
**Risiko:** Minimal. Værste case: loop stopper for tidligt.
**How-to:**
1. Tilføj `MAX_ITERATIONS=15` og `MAX_COST_USD=5.0` til loop-wrapper
2. Tjek Anthropic API usage efter hver iteration
3. Stop loop hvis grænse nået, skriv til LOOP_STATE.md
4. Send Telegram-notifikation ved forced stop
5. Test: kør loop med MAX_ITERATIONS=3, verificér det stopper

**Modenhed:** Production-ready (trivielt)

---

## 4. The Last Algorithm som Weekly Cron

**Effort:** Timer (3-4 timer)
**Impact:** Medium-Høj — proaktiv gap-detection mellem current og ideal state
**Kræver:** MISSION.md + alle NOW.md filer + Groq LLM
**Risiko:** LLM-kvalitet af gap-detection kan være lav. Kan producere noise.
**How-to:**
1. Nyt script: `scripts/gap_detector.py`
2. Læs MISSION.md + PRIORITIES.md + alle projects/*/NOW.md
3. Send til Groq: "Sammenlign current state med ideal state. Identificér top 3 gaps."
4. Output: `data/intelligence/weekly_gaps.md`
5. Tilføj til søndags-cron kl. 07:30

**Modenhed:** Early adopter (concept proven af Miessler)

---

## 5. Genaktivér Heartbeat Daemon

**Effort:** Timer (1 time — allerede bygget)
**Impact:** Medium — proaktiv check af inboxes → spawn agent ved arbejde
**Kræver:** heartbeat.py eksisterer allerede, bare enable i crontab
**Risiko:** Kan generere noise (for mange checks). Kan spawne unødvendige sessions.
**How-to:**
1. Uncomment heartbeat.py i crontab
2. Verificér at Telegram notifikation virker
3. Tilføj filter: kun notificér ved HIGH priority items
4. Monitor i 1 uge, justér interval

**Modenhed:** Early adopter (bygget, ikke testet i produktion)

---

## 6. Episodisk Retrieval (Smart Episode Loading)

**Effort:** Timer-Dage (4-8 timer)
**Impact:** Medium — bedre kontekst-injection ved session start
**Kræver:** Ændring i load_checkpoint.sh + muligvis embedding af episoder
**Risiko:** Kan gøre session start langsommere. Forkert episode-match = irrelevant kontekst.
**How-to:**
1. Embed episodes.jsonl i Qdrant collection `episodes`
2. I load_checkpoint.sh: ctx-søg baseret på projekt-kontekst
3. Injicér de 5 mest relevante episoder, ikke de 5 seneste
4. Fallback: seneste 5 hvis ctx fejler
5. Test: starter ny session, verificér episoder er relevante

**Modenhed:** Early adopter

---

## 7. Mem0-Inspireret Fact Extraction

**Effort:** Dage (1-2 dage)
**Impact:** Medium-Høj — automatisk fact-extraction fra sessions
**Kræver:** 50 linjer Python + Groq/OpenAI for extraction
**Risiko:** Fact-extraction kan hallucinere. Duplikater. Cost.
**How-to:**
1. I save_checkpoint.py: efter episode-destillering, extract facts
2. Groq prompt: "Ekstrakt 3-5 fakta fra denne session (navn, dato, beslutning, præference)"
3. Gem i Qdrant collection `facts` med metadata (dato, session_id, projekt)
4. Dedupliker mod eksisterende facts (cosine similarity > 0.95 = skip)
5. Brug i load_checkpoint.sh: hent relevante facts ved session start

**Modenhed:** Eksperimentel (Mem0 beviser konceptet, men egen impl. er utestet)

---

## 8. Multi-Provider Research

**Effort:** Dage (1-2 dage)
**Impact:** Medium — bredere perspektiv, undgå single-provider bias
**Kræver:** research.py udvidelse + Groq API
**Risiko:** Kompleksitet. To providers = to failure modes. Cost.
**How-to:**
1. I research.py: tilføj `--multi` flag
2. Kør query mod arXiv + OpenAlex + Semantic Scholar parallelt (allerede muligt)
3. Tilføj Groq som summarizer (gratis) efter retrieval
4. Kombiner resultater med deduplicering
5. Output: markdown med kilder markeret per provider

**Modenhed:** Production-ready (komponenterne eksisterer)

---

## 9. Webapp Staging/Preview

**Effort:** Dage (1-2 dage)
**Impact:** Medium — undgå produktion-uheld
**Kræver:** Ekstra nginx config + Docker service
**Risiko:** Dobbelt vedligeholdelse. Disk space.
**How-to:**
1. Tilføj `webapp-staging` service i docker-compose.yml
2. Mount til `app-staging/` i stedet for `app/`
3. Traefik route: staging.app.srv1181537.hstgr.cloud
4. Test ændringer i staging → kopier til produktion
5. Kill condition: fjern hvis aldrig brugt efter 2 uger

**Modenhed:** Production-ready (standard pattern)

---

## 10. Hvad Hvis Yttre Skifter Codebase?

### Cursor / Windsurf / Aider
Alle tre er IDE-baserede. Yttre kører headless (VPS + Android + PC).
- **Cursor:** Bedst til reel kodning med autocomplete. Kræver VS Code. Ikke relevant for headless.
- **Windsurf:** Fork af VS Code med AI. Samme problem.
- **Aider:** CLI-baseret. Ville fungere på VPS. Men Claude Code gør det samme bedre (hooks, skills, sessions).

**Vurdering:** Intet skift nødvendigt. Claude Code er det rigtige valg for Yttres setup.

### Multi-Provider
Yttre er Anthropic-locked (Claude Code). Risikoen:
- Hvis Anthropic hæver priser dramatisk
- Hvis Claude kvalitet falder
- Hvis en konkurrent leverer bedre agent-capabilities

**Mitigation:** Groq som fallback til billige tasks (allerede brugt). OpenAI til embeddings (allerede brugt). Kerneintelligensen er i CLAUDE.md + scripts, ikke i Claude-specifik kode.

---

## Prioriteret Rækkefølge

| # | Forslag | Effort | Impact | Prioritet |
|---|---------|--------|--------|-----------|
| 1 | Reranking i ctx | Timer | Høj | **P1** |
| 2 | Circuit breakers | Timer | Medium | **P1** |
| 3 | Genaktivér heartbeat | Timer | Medium | **P1** |
| 4 | Hybrid search | Dage | Høj | **P2** |
| 5 | The Last Algorithm cron | Timer | Medium-Høj | **P2** |
| 6 | Episodisk retrieval | Timer-Dage | Medium | **P2** |
| 7 | Fact extraction | Dage | Medium-Høj | **P3** |
| 8 | Multi-provider research | Dage | Medium | **P3** |
| 9 | Webapp staging | Dage | Medium | **P3** |
