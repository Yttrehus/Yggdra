# Memory Systems — RAG, Vector DB & Retrieval (marts 2026)

**Kilder:** AI_MEMORY_SYSTEMS_SURVEY.md, CH5_RAG_PRACTICE.md, CH5_RAG_PRODUCTION.md, CH5_EMBEDDINGS_VECTOR_DBS.md, memory_autonomy_research_2026-02-23.md, ai_memory_research.md

---

## 1. RAG: State of the Art

### Det kritiske tal
**73-80% af enterprise RAG-projekter fejler i produktion** (Analytics Vidhya 2025). Ikke fordi RAG er dårligt — men fordi teams ikke forstår failure surfaces.

RAG er ikke et produkt. Det er en arkitektur med mindst 5 failure points der multiplicerer:
chunking → embedding → retrieval → context assembly → generation.
95% accuracy per stage = 77% end-to-end.

### RAG vs. Long Context vs. Fine-tuning

| | RAG | Long Context | Fine-tuning |
|---|---|---|---|
| Cost/query | ~$0.00008 | ~$0.10 (1250x) | ~$0.001 |
| Latency | ~1s | 30-60s | Sub-second |
| Updatability | Tilføj docs løbende | Reload per query | Retrain (dage) |
| Kildeangivelse | Native | Mulig men svær | Ikke tilgængelig |
| Bedst til | Dynamisk viden, hyppige queries | Holistisk analyse, lille corpus | Adfærdsændring |

**"Long context kills RAG" debat:** Stanford "Lost in the Middle": LLMs bruger info i start/slut, ignorerer midten. 30%+ performance drop. Long context er komplementært til RAG, ikke erstatning.

---

## 2. RAG-arkitekturer (10 patterns)

### Naive RAG
Query → embed → top-k → prompt → generate. Baseline. Fungerer overraskende godt. 80% af RAG starter her.

### Advanced RAG
Pre-retrieval (query rewriting, HyDE) + hybrid search + reranking + post-retrieval filtrering. De fleste produktions-systemer.

### Hybrid Search
Vektor (dense) + keyword (BM25/sparse) kombineret. Typisk 70% vektor + 30% BM25.
**Modenhed:** Production-ready
**Relevans for Yttre:** Direkte brugbar — Qdrant supporterer det, Yttre bruger det ikke endnu

### GraphRAG
Knowledge graphs + vektor search. 26-97% færre tokens (Microsoft). Stærkt til multi-hop reasoning.
**Modenhed:** Eksperimentel
**Relevans:** Nice to know — for komplekst for solo setup

### Agentic RAG
AI-agent styrer retrieval-strategi dynamisk. Vælger mellem vektor, keyword, web, database.
**Modenhed:** Eksperimentel
**Relevans:** Indirekte relevant — ctx-kommandoen er en primitiv version

### HyDE
Generér hypotetisk svar → embed det → søg med det. Løser query-document length mismatch.
**Modenhed:** Production-ready
**Effort:** Timer (en ekstra LLM-kald per query)

---

## 3. Chunking: 80% af RAG-kvalitet

**CDC studie:** Naiv chunking = 0.47-0.51 faithfulness. Optimeret semantisk = 0.79-0.82. **60% forbedring fra chunking alene.**

### Hierarki af impact
1. **Chunking strategi** (største lever)
2. **Query formulering** (prompt engineering)
3. **Retrieval pipeline** (hybrid, reranking)
4. **Embedding model** (mindst vigtig af de 4)

### Strategier

| Strategi | Hvornår | Yttre bruger? |
|----------|---------|---------------|
| Fixed-size (256-1024 tokens, 10-20% overlap) | Prototyping | Ja (~2000 chars) |
| Recursive character splitting | Default for 80% | Delvist |
| Semantic chunking | Kvalitetsforbedring, koster embedding-kald | Nej |
| Page-level | PDF'er, formaterede docs | Nej |
| Proposition chunking | Høj præcision, flere chunks | Nej |
| Hierarchical (parent-child) | Bevar både granularitet og kontekst | Nej |

**Anbefaling for Yttre:** Skift fra fixed-size til recursive character splitting som baseline. Overvej semantic chunking for advisor_brain (453 points, høj værdi).

---

## 4. Embedding-modeller

### Impact-hierarki
Embedding model er den **mindst vigtige** af de 4 levers (chunking > query > pipeline > model). Gabet mellem billigste og dyreste er 4-5 MTEB-point — LLM kompenserer.

### Yttres valg: text-embedding-3-small (OpenAI)
- $0.02/M tokens, 1536 dim, cosine
- **Korrekt valg for solo setup.** Billigt, godt nok, bred support.

### Alternativer der er værd at kende

| Model | Cost | Dim | Vurdering |
|-------|------|-----|-----------|
| text-embedding-3-small (OpenAI) | $0.02/M | 1536 | Safe default. Yttre bruger. |
| voyage-3.5-lite | $0.02/M | 1024 | Bedre MTEB, 32K context. Dark horse. |
| BGE-M3 (open) | Gratis | 1024 | Bedste open-source. Lokal, ingen API. |
| Cohere embed-v4 | $0.10/M | 1024 | Højeste MTEB (65.2). |

### Gotchas
- **Model upgrade = fuld re-embedding.** Gem altid rå tekst ved siden af vektorer.
- **Multilingual gaps.** Engelsk > dansk i embedding-kvalitet. Observeret i Yttres advisor_brain.
- **Embedding ceiling.** Efter et vist kvalitetsniveau hjælper bedre embeddings ikke — fix chunking/retrieval i stedet.

---

## 5. Vector DB: Yttres Qdrant Setup

### Nuværende tilstand
7 collections, ~84.210 points, 1536 dim, Cosine, **dense-only**.

| Collection | Points | Formål |
|------------|--------|--------|
| routes | 40.053 | TransportIntra rutedata |
| sessions | 42.106 | Sessionshistorik |
| docs | 1.169 | Dokumentation |
| advisor_brain | 453 | Nate Jones + Miessler |
| knowledge | 246 | Generel viden |
| miessler_bible | 102 | Miessler blogs/bøger |
| conversations | 81 | Samtaler |

### Vector DB-landskab

| Scenario | Valg | Begrundelse |
|----------|------|-------------|
| Solo dev, produktion | **Qdrant (Docker)** ✓ | Self-hosted, kraftfuldt, gratis. Yttre er her. |
| Zero ops | Pinecone | Fuldt managed. Betaler for bekvemmelighed. |
| Allerede PostgreSQL | pgvector | Ingen ny service. Men bryder ved 5M vektorer. |
| Nativ hybrid search | Weaviate | Bedste BM25 + vektor i ét system. |

**Yttres valg er korrekt.** Qdrant er det rigtige for solo self-hosted. Intet behov for at skifte.

### Hvad Yttre mangler i Qdrant

**1. Hybrid Search (dense + sparse)**
Qdrant supporterer sparse vectors (BM25). Yttre bruger kun dense.
- **Impact:** 15-25% bedre retrieval for keyword-tunge queries
- **Effort:** Dage (tilføj sparse vectors til eksisterende collections)
- **How-to:** Tilføj `sparse` vector config + BM25 tokenizer + reranking

**2. Reranking**
Ingen reranking efter retrieval. Top-k dense results bruges direkte.
- **Impact:** Op til 48% forbedring (Databricks)
- **Effort:** Timer (Cohere Rerank API kald efter retrieval)
- **Cost:** $1/1000 queries (Cohere) eller gratis med BGE reranker lokalt

**3. Query Expansion**
Ingen query rewriting eller HyDE.
- **Impact:** Bedre recall for korte/vage queries
- **Effort:** Timer (en ekstra LLM-kald)

---

## 6. Retrieval-optimering

### Reranking (anbefalet næste skridt)

| Reranker | Cost | Kvalitet | Lokal? |
|----------|------|----------|--------|
| Cohere Rerank | $1/1K queries | Bedst | Nej |
| BGE Reranker | Gratis | Tæt på Cohere | Ja (GPU) |
| Cross-encoder (SBERT) | Gratis | God | Ja |
| RankGPT (LLM) | Dyrt | Nuanceret | Via API |

**Anbefaling:** Start med Cohere Rerank ($1/1K) i ctx-kommandoen. Hvis for dyrt: BGE lokalt.

### Hybrid Search Implementation

Qdrant hybrid search kræver:
1. Tilføj sparse vector config til collection
2. Generér BM25 sparse vectors ved ingest (Qdrant har `models.SparseVector`)
3. Query med både dense + sparse, kombiner via Reciprocal Rank Fusion
4. Vægtning: start med 0.7 dense + 0.3 sparse, tuner derfra

**Effort:** 1-2 dage for eksisterende collections (re-ingest nødvendigt)

---

## 7. Modenhedsvurdering

| Emne | Modenhed | Relevans for Yttre | Effort |
|------|----------|-------------------|--------|
| Naive RAG | Production-ready | Allerede i brug | - |
| Hybrid search | Production-ready | Direkte brugbar | Dage |
| Reranking | Production-ready | Direkte brugbar | Timer |
| HyDE | Production-ready | Direkte brugbar | Timer |
| Semantic chunking | Early adopter | Indirekte relevant | Dage |
| GraphRAG | Eksperimentel | Nice to know | Uger |
| Agentic RAG | Eksperimentel | Indirekte relevant | Uger |

---

## DEL 2: Knowledge Graphs, Session Persistence & Episodisk Hukommelse

---

## 8. Knowledge Graphs for AI Memory

### Hvornår Knowledge Graphs > Vector Search
- **Multi-hop reasoning:** "Hvilke kunder har samme adresse som rute 256's stop?" Vektor-search finder ikke dette.
- **Relationer:** Entiteter hænger sammen. Vektorer behandler alt som uafhængige chunks.
- **Temporal awareness:** Hvornår skete noget? Vektorer har ingen tidsmodel.

### Frameworks

| Framework | Stars | Approach | VPS-egnet? | Cost |
|-----------|-------|----------|------------|------|
| **LightRAG** | 28.5K | Auto knowledge graph ved ingest | Ja (NetworkX) | $25-40 for 80K chunks |
| **Graphiti/Zep** | 23K | Real-time temporal KG | Stramt (Neo4j) | Moderat |
| **GraphRAG** (MS) | - | Community detection, sensemaking | Nej (for dyrt) | Tusindvis af API-kald |
| **MAGMA** (2026) | - | 4 parallelle grafer | Research-only | - |

### LightRAG (mest realistisk for Yttre)
- Dual retrieval: Lokal (entiteter) + Global (temaer)
- NetworkX in-memory graf, ingen ekstra server
- 10x billigere end GraphRAG, sammenlignelig nøjagtighed
- **Red team:** Entity extraction kan hallucinere. Papiret trukket fra ICLR.
- **Effort:** 1 dag setup + API-cost for initial ingest

### Graphiti (mest sofistikeret)
- Bi-temporal model: ved HVORNÅR ting skete, invaliderer automatisk
- P95 latency: 300ms, ingen LLM-kald ved retrieval
- **Red team:** Kræver Neo4j/Kuzu. Claude er "second class citizen" (structured output).
- **Effort:** Uger (ekstra DB + integration)

### Vurdering
**Modenhed:** Eksperimentel (alle frameworks)
**Relevans for Yttre:** Indirekte relevant — LightRAG er interessant men evidensgrundlaget er svagt
**Anbefaling:** Vent. Hybrid search i Qdrant giver 80% af værdien til 10% af indsatsen.

---

## 9. Session Persistence & Compaction

### Problemet
Claude Code sessions har et context window (200K standard, 1M beta). Lange sessions → context rot → kvalitetsfald. Session-skift = alt glemt.

### Yttres Nuværende Løsning
- **PreCompact hook:** save_checkpoint.py kører FØR komprimering
- **Stop hook:** Destillerer session via Groq → NOW.md per projekt
- **SessionStart:** load_checkpoint.sh injicerer NOW.md + seneste episoder
- **episodes.jsonl:** 3-5 linjers destillat per session

### State of the Art

| Approach | Hvem | Styrke | Svaghed |
|----------|------|--------|---------|
| **File-based state** | Pi/Ronacher, Yttre | Simpelt, versionerbart, synligt | Manuelt, ingen automatisk retrieval |
| **MEMORY.md** | Claude Code auto-memory | Zero-effort, officiel | Begrænset størrelse (200 linjer), ingen struktur |
| **Sessions API** | Claude Agent SDK | Resumable, forkable | Claude-only, ingen ekstern access |
| **Checkpointing** | LangGraph | Pause/resume/fork/replay | Kræver LangGraph |
| **Context repos** | Letta V1 | Git-baseret versionering | Tungt, overkill for solo |
| **KV-cache** | Manus | 10x billigere, append-only | Kræver stabile prefixes |

### Yttres Styrke (ofte undervurderet)
Yttre har faktisk en **bedre session-persistence end de fleste frameworks:**
1. NOW.md per projekt = kontekst-injection ved session start
2. episodes.jsonl = episodisk log
3. CLAUDE.md = permanent instruktionsset
4. Skills/ = domæneviden on demand
5. Git = fuld versionering

**Hvad mangler:** Automatisk retrieval af relevante episoder (i stedet for seneste 5). Temporal decay (nyere > ældre).

---

## 10. Episodisk Hukommelse

### Menneske → AI Mapping

| Menneskehukommelse | AI-implementation | Yttre har? |
|-------------------|-------------------|------------|
| Episodisk (begivenheder) | Session logs, episodes.jsonl | Ja (basalt) |
| Semantisk (fakta) | Qdrant vektorer, CLAUDE.md | Ja |
| Procedural (skills) | .claude/skills/, scripts | Ja |
| Arbejdshukommelse | Context window | Ja (200K) |

### Hvad forskningen siger
**Complementary Learning Systems (CLS):** Hjernen har to systemer — hippocampus (hurtig, specifik) og neocortex (langsom, generaliseret). AI-parallel: RAG (hurtig) + model weights (langsom). Intelligente agenter **behøver begge** (Kumaran et al. 2016).

**Glemsel er en feature:** Hjernen glemmer aktivt for at prioritere. AI-systemer der husker alt → context pollution. Temporal decay og relevance scoring er nødvendige.

**Reconsolidation:** Hver gang en erindring hentes, kan den ændres. Parallel: memory updates ved retrieval (Mem0's update phase).

### Memory Frameworks

| Framework | Approach | Ydrasil-relevant? |
|-----------|----------|-------------------|
| **Mem0** | Extract → deduplicate → decay | Ja — simpelt API, Qdrant native |
| **Letta/MemGPT** | OS-metafor: core/archival/recall | Delvist — overkill, men gode koncepter |
| **A-MEM** | Zettelkasten-inspireret auto-linking | Research-only |
| **Claude auto-memory** | MEMORY.md, automatisk vedligehold | Allerede i brug |

### Mem0 Assessment
- **Styrker:** Qdrant native, simpelt API (`add/search/update`), automatisk decay/dedup
- **Red team:** "26% bedre" er eget benchmark. LLM-kald per extraction = cost. Open-source har færre features.
- **Realistisk:** "3 prompts oven på vector DB" — kan bygges i 50 linjer Python
- **Effort:** Timer-dage

### Yttres Episodiske Hukommelse (nuværende)
```
Session → save_checkpoint.py → Groq destillat → episodes.jsonl (3-5 linjer)
                                                → NOW.md (projekt-state)
load_checkpoint.sh → injicerer NOW.md + seneste 5 episoder
```

**Hvad der virker:** Simpelt, billigt (Groq), alt på disk, git-versioneret.
**Hvad der mangler:**
1. Retrieval er dumb (seneste 5, ikke mest relevante)
2. Ingen temporal decay (episode fra dag 1 = episode fra i går)
3. Ingen konsolidering (episodisk → semantisk migration)
4. Ingen automatisk fact-extraction (Mem0's kernefunktion)

---

## 11. Anbefalinger (prioriteret)

### Lav indsats, høj impact (Timer)
1. **Reranking i ctx** — Cohere Rerank efter Qdrant retrieval
2. **HyDE i ctx** — generer hypotetisk svar, embed det, søg med det
3. **Episodisk retrieval** — ctx-søg i episodes.jsonl i stedet for seneste 5

### Moderat indsats, høj impact (Dage)
4. **Hybrid search** — tilføj BM25 sparse vectors til Qdrant
5. **Mem0-inspireret extraction** — 50 linjer: extract facts fra session → Qdrant
6. **Temporal decay** — score = relevance × recency_weight

### Høj indsats, usikker impact (Uger)
7. **LightRAG** — knowledge graph over eksisterende data
8. **Letta-koncepter** — core memory (always-in-context) vs archival
9. **Konsolidering** — automatisk episodisk→semantisk migration

### Fravalg (med begrundelse)
- **GraphRAG:** For dyrt, for komplekst for solo
- **Letta/MemGPT:** Overkill for 1 bruger, tung arkitektur
- **1M context:** $10/prompt, context rot efter ~100K
- **Full Mem0 hosted:** Vendor lock-in, open-source version er nok
