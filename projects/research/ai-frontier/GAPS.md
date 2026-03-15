# GAPS — Yttre vs. State of the Art

**Baseret på:** Alle topic-filer + WHAT_IF.md
**Format:** Gap → hvad state of the art gør → hvad Yttre har → effort at lukke

---

## Gap 1: Hybrid Search (Dense + Sparse)

**State of the art:** Produktions-RAG systemer bruger hybrid search (vektor + BM25) med 15-25% bedre retrieval. Qdrant, Weaviate, Pinecone supporterer det alle. Manus optimerer KV-cache med append-only context.

**Yttre har:** Dense-only vektor search (text-embedding-3-small, 1536 dim, cosine). 84K points. Ingen BM25, ingen sparse vectors.

**Gap:** Keyword-tunge queries (navne, adresser, rute-numre) performer dårligt med pure semantic search. "Rute 256 organisk" finder muligvis ikke det rette fordi dense embeddings lægger vægt på semantik, ikke nøgleord.

**Effort at lukke:** Dage. Re-ingest nødvendigt. ~$2-5 i embedding cost.
**Prioritet:** P2 (høj impact men kræver re-ingest)

---

## Gap 2: Reranking

**State of the art:** Reranking efter initial retrieval er standard. Cohere Rerank, BGE Reranker, cross-encoders. Op til 48% forbedring (Databricks). Manus bruger logit masking for tool selection.

**Yttre har:** Ingen reranking. Top-k dense results bruges direkte i ctx.

**Gap:** Top-5 fra Qdrant er "gode nok" men ikke optimale. Reranking ville sikre at de mest relevante chunks er i top-5.

**Effort at lukke:** Timer. Cohere API kald = 5 ekstra linjer kode.
**Prioritet:** P1 (laveste effort, høj impact)

---

## Gap 3: Evaluering og Måling

**State of the art:** Agent-systemer har eval pipelines: task completion rate, cost per task, error recovery rate. RAGAS for RAG. DeepEval for broader eval. METR viste at perceived ≠ actual productivity.

**Yttre har:** Ingen systematisk evaluering. "Det virker" er subjektivt. Ingen baseline-målinger. Ingen A/B tests. cost_daily.json tracker cost men ikke kvalitet.

**Gap:** Yttre ved ikke om forbedringer faktisk forbedrer. Kan ikke kvantificere om hybrid search er bedre end dense-only på Yttres data. Kan ikke bevise at agents hjælper (METR: 19% langsommere).

**Effort at lukke:** Dage-Uger. Kræver: 10-20 test queries med forventede svar, script der måler retrieval precision, cost tracking per task.
**Prioritet:** P2 (fundamentalt men stort)

---

## Gap 4: Temporal Decay / Recency Weighting

**State of the art:** Graphiti har bi-temporal model. Mem0 har automatisk decay. OpenClaw bruger temporal decay i retrieval. Menneskehjernens glemsel er en feature — ikke alt er lige relevant.

**Yttre har:** Ingen temporal awareness. Episode fra dag 1 scorer lige så højt som episode fra i går. Qdrant metadata har timestamps men de bruges ikke i scoring.

**Gap:** Gammel information forurener retrieval. "Hvad arbejder Yttre på?" returnerer muligvis 3 måneder gamle chunks over denne uges.

**Effort at lukke:** Timer. I ctx: multiplér score med recency_weight (e.g. exp(-age_days/30)).
**Prioritet:** P2 (lav effort, medium impact)

---

## Gap 5: Proaktiv AI / Always-On

**State of the art:** OpenClaw: heartbeat daemon + Telegram input polling + auto-PRs. MOM (Zechner): Slack-bot med per-kanal memory. Claude Code Scheduler: NLP scheduling med git worktree isolation. Miessler PAI: multi-agent research parallelt.

**Yttre har:** heartbeat.py (disabled). Claude Code hooks (reaktiv, ikke proaktiv). Cron jobs (tidsbaseret, ikke event-baseret). Ingen input-polling fra Telegram/mail.

**Gap:** Yttre reagerer kun når bruger starter session eller cron kører. Ingen evne til at proaktivt sige "Hey, der er noget nyt du bør vide" uden scheduled cron.

**Effort at lukke:** Timer (genaktivér heartbeat) til Dage (Telegram input polling).
**Prioritet:** P1 (heartbeat allerede bygget)

---

## Gap 6: Fact Extraction / Konsolidering

**State of the art:** Mem0: automatisk fact extraction → deduplicate → decay. Letta: core memory (always-in-context) med agent self-editing. A-MEM: Zettelkasten-inspireret auto-linking. Menneskehukommelse: episodisk → semantisk konsolidering under søvn.

**Yttre har:** save_checkpoint.py destillerer episodes. episodes.jsonl = 3-5 linjer per session. Men ingen automatisk fact extraction ("Kris foretrækker dansk", "Rute 256 = organisk affald"). Ingen konsolidering (episodisk → semantisk migration).

**Gap:** Yttre husker HVAD der skete (episodisk) men konverterer ikke til HVAD vi ved (semantisk). MEMORY.md fyldes manuelt. CLAUDE.md opdateres manuelt. Ingen automatisk knowledge accumulation.

**Effort at lukke:** Dage. 50 linjer Python (Groq extraction → Qdrant facts collection).
**Prioritet:** P3 (moderat effort, usikker impact)

---

## Gap 7: Context Engineering Discipline

**State of the art:** Manus: KV-cache optimering (append-only, stable prefixes, 10x billigere). Karpathy: "Context engineering is the new prompt engineering." Anthropic: cache breakpoints, restorable compression.

**Yttre har:** CLAUDE.md + skills/ + NOW.md injection. God struktur. Men ingen KV-cache bevidsthed. Ingen append-only context discipline. Todo.md attention pattern bruges ikke.

**Gap:** Yttre betaler fuld pris for context tokens der kunne caches. Ingen bevidst manipulation af attention via recitation (Manus' todo.md pattern).

**Effort at lukke:** Timer (todo.md pattern) til Dage (KV-cache optimering kræver prompt-redesign).
**Prioritet:** P3 (optimization, ikke fundament)

---

## Gap 8: Multi-Provider Resilience

**State of the art:** Pi (Zechner): provider-agnostisk, sessions kan flyttes mellem Claude, GPT, Gemini. Miessler PAI: parallel research med Claude + Gemini + Grok. smolagents: model-agnostisk.

**Yttre har:** Anthropic lock-in for agent-work (Claude Code). OpenAI for embeddings. Groq for billige tasks. Men ingen evne til at skifte mid-session eller køre parallelt.

**Gap:** Hvis Anthropic API er nede eller Claude kvalitet dropper, har Yttre ingen fallback for interaktiv agent-work. Embeddings og destillering er allerede multi-provider.

**Effort at lukke:** Uger (ville kræve alternativ til Claude Code). Lav prioritet — Anthropic er stabil.
**Prioritet:** P4 (langsigtet resilience)

---

## Opsummering

| Gap | State of Art | Yttre | Effort | Prioritet |
|-----|-------------|-------|--------|-----------|
| Reranking | Standard | Mangler | Timer | P1 |
| Proaktiv AI | Heartbeat+polling | Disabled | Timer | P1 |
| Hybrid search | Standard | Dense-only | Dage | P2 |
| Evaluering | Eval pipelines | Ingen | Dage-Uger | P2 |
| Temporal decay | Bi-temporal | Ingen recency | Timer | P2 |
| Fact extraction | Mem0 auto | Manuel | Dage | P3 |
| Context engineering | KV-cache opt | Ingen cache-bevidsthed | Timer-Dage | P3 |
| Multi-provider | Provider-agnostisk | Anthropic-locked | Uger | P4 |

**Konklusion:** Yttre er overraskende tæt på state of the art i fundamentet (skills, hooks, episodisk log, Qdrant). De største gaps er i **retrieval-kvalitet** (reranking, hybrid) og **proaktivitet** (heartbeat, event-driven). Ingen af de kritiske gaps kræver uger — de fleste lukkes i timer-dage.
