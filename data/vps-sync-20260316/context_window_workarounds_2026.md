# Arbejde RUNDT om LLM Context Window Begrænsningen
## Research-rapport — Februar 2026

---

## Indholdsfortegnelse

1. [Problemet](#problemet)
2. [Sliding Window / Compaction](#1-sliding-window--compaction)
3. [Hierarkisk Summarization](#2-hierarkisk-summarization)
4. [Ekstern Hukommelse (Vector DB, Knowledge Graphs, SQL)](#3-ekstern-hukommelse)
5. [MemGPT/Letta — Virtuel Kontekst-styring](#4-memgptletta--virtuel-kontekst-styring)
6. [RAG-baseret Hukommelse](#5-rag-baseret-hukommelse)
7. [Multi-agent Arkitekturer](#6-multi-agent-arkitekturer)
8. [Nye Tilgange (2025-2026)](#7-nye-tilgange-2025-2026)
9. [Sammenligningstabel](#sammenligningstabel)
10. [Konklusion og Anbefalinger](#konklusion)
11. [Kilder](#kilder)

---

## Problemet

Selv med context windows på 200K+ tokens (Claude), 1M+ (Gemini) og 128K (GPT-4o) rammer persistente AI-agenter fundamentale begrænsninger:

- **Kostnad:** 100:1 input-to-output ratio i produktionsagenter (Manus). Hver token i konteksten koster ved *hvert* API-kald.
- **Kvalitetsforringelse:** "Lost in the middle"-fænomenet — modeller bruger start og slut af konteksten bedre end midten.
- **Sessionsgræns:** Konteksten nulstilles mellem sessioner. Ingen naturlig langtidshukommelse.
- **Latency:** Længere kontekst = langsommere time-to-first-token.

Spørgsmålet er ikke "hvordan får vi et større vindue?" men **"hvordan giver vi illusionen af uendelig hukommelse inden for et begrænset vindue?"**

---

## 1. Sliding Window / Compaction

### Sådan virker det

Konteksten behandles som et vindue der glider hen over samtalens historie. Ældre beskeder komprimeres eller fjernes, mens nyere bevares i fuld detalje.

**Google ADK's implementation** (v1.16.0+) er et konkret eksempel:

```python
EventsCompactionConfig(
    compaction_interval=3,  # Komprimer hver 3 events
    overlap_size=1          # Bevar 1 event som overlap
)
```

Hver gang 3 nye events er afsluttet, opsummerer systemet de ældre events til et summary og beholder 1 overlappende event for kontekstforankring.

**Manus' tilgang** er mere sofistikeret: de udskifter fulde tool-resultater med komprimerede versioner, men beholder nok metadata (f.eks. URLs, filstier) til at det fulde resultat kan genhentes. Kompression er altid *reversibel*.

### Tradeoffs

| Fordel | Ulempe |
|--------|--------|
| Simpelt at implementere | Informationstab ved hvert komprimeringsskridt |
| Forudsigeligt token-forbrug | Kumulativt tab over lange sessioner |
| Lav latency-overhead | Overlap-størrelse er en kritisk afvejning |
| KV-cache-venligt (append-only) | Intet langtidshukommelse på tværs af sessioner |

### Produktionsmodenhed

**Bevist i produktion.** Manus bruger dette som kernestrategi. Google ADK har det som built-in feature. Det er den mest udbredte tilgang i 2026.

### Effekt vs. flad kontekst

Reducerer token-forbrug med 60-80% ved lange sessioner. Manus rapporterer at de opretholder agent-kvalitet over 50+ tool calls med denne strategi.

---

## 2. Hierarkisk Summarization

### Sådan virker det

Kontekst organiseres i lag med stigende abstraktionsniveau:

```
Tier 1: Rå kontekst (seneste 5-10 beskeder) — fuld detalje
Tier 2: Kort-tids-summaries (session-niveau) — nøglebeslutninger, fakta
Tier 3: Lang-tids-summaries (på tværs af sessioner) — destilleret viden
Tier 4: Permanent viden (fakta, præferencer, regler)
```

Ved hvert lag reduceres tokens, men kerneinformationen bevares. NEXUSSUM-paperet demonstrerer at hierarkisk summarization kan give **op til 30% forbedring** i kvalitet sammenlignet med flat truncation, specielt på lange narrative tekster (BookSum-benchmark).

**LangMem's tilgang** skelner mellem tre hukommelsestyper:
- **Semantisk hukommelse** — fakta og viden (collections eller profiles)
- **Episodisk hukommelse** — succesfulde interaktioner som eksempler
- **Procedural hukommelse** — adfærdsregler via system prompts der evolverer

### Tradeoffs

| Fordel | Ulempe |
|--------|--------|
| Bevarer vigtig info over lange perioder | Summarization er fejlbehæftet — LLM'en kan miste nuancer |
| Skalerbar til uendelige sessioner | Hvert summarization-skridt koster et LLM-kald |
| Tættere på menneskelig hukommelse | Svært at vide hvad der er "vigtigt" på forhånd |
| Kan kombineres med alle andre tilgange | Hierarki-design kræver omhyggelig tuning |

### Produktionsmodenhed

**Bevist i produktion.** ChatGPT's hukommelse bruger en variant (automatisk ekstraktion af fakta). Claude Code's `CLAUDE.md` + `MEMORY.md` er en manuelt-kurateret version. Mem0 automatiserer det med 91% lavere latency end naive tilgange.

### Effekt vs. flad kontekst

30% kvalitetsforbedring over truncation (NEXUSSUM). Mem0 rapporterer 26% forbedring i LLM-as-Judge metrics over OpenAI's egen hukommelse.

---

## 3. Ekstern Hukommelse

### 3a. Vector Database (Qdrant, Pinecone, Chroma)

Semantisk søgning over embeddings. Konverterer tekst til vektorer, gemmer i database, henter relevante chunks ved behov.

**Styrke:** Skalerer til millioner af dokumenter. God til "find lignende kontekst."
**Svaghed:** Semantisk søgning forstår ikke relationer, tidslighed eller kausalitet. "Find lignende" ≠ "find relevant."

### 3b. Knowledge Graphs (Neo4j, FalkorDB, Microsoft GraphRAG)

Strukturerede relationer mellem entiteter. **Microsoft GraphRAG** bygger automatisk en knowledge graph fra ustruktureret tekst, laver community-summaries, og bruger dem ved retrieval.

**Nøgletal:**
- FalkorDB: **90% reduktion i hallucinationer** vs. traditionel RAG
- LinkedIn: **63% hurtigere ticket-resolution** (40 timer → 15 timer)
- LightRAG: **10x token-reduktion** med sammenlignelig kvalitet

**Styrke:** Forstår relationer ("Kris kører rute 256" → "rute 256 er i Aarhus" → "Aarhus har organisk affald"). Deterministisk op til 99% nøjagtighed.
**Svaghed:** Dyrt at bygge og vedligeholde. Kræver entity extraction pipeline.

### 3c. SQL/Key-Value Stores

Struktureret data med eksakt lookup. Bruges til bruger-profiler, præferencer, session state.

**Styrke:** Deterministisk, hurtigt, billigt.
**Svaghed:** Ingen semantisk forståelse. Kræver foruddefineret skema.

### Produktionsmodenhed

Vector DB: **Fuld produktion** (Qdrant, Pinecone, Chroma — tusindvis af deployments).
Knowledge Graphs: **Tidlig produktion** (Microsoft, LinkedIn, Neo4j bruger det; kræver stadig ekspertise).
SQL: **Fuld produktion** (fundamentalt, men begrænset til struktureret data).

### Effekt vs. flad kontekst

Afhænger af retrieval-kvalitet. God RAG pipeline leverer relevante chunks der ville være umulige at finde i flat context. Dårlig RAG pipeline henter støj der forvirrer modellen.

---

## 4. MemGPT/Letta — Virtuel Kontekst-styring

### Sådan virker det

MemGPT behandler LLM'ens context window som **RAM** i et operativsystem. Ligesom et OS pager hukommelse mellem RAM og disk, pager MemGPT information mellem context window og ekstern storage.

**Arkitekturen:**

```
┌─────────────────────────────────────┐
│         LLM Context Window          │  ← "RAM"
│  ┌─────────────────────────────┐    │
│  │ System prompt               │    │
│  │ Core memory (user bio,      │    │
│  │   agent persona)            │    │
│  │ Working memory (recent msgs)│    │
│  │ Message buffer              │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│    Recall Storage (vector DB)       │  ← "Disk" (conversation history)
│    Archival Storage (vector DB)     │  ← "Disk" (long-term knowledge)
└─────────────────────────────────────┘
```

**Memory pressure** trigger: Når token-brug nærmer sig en tærskel (f.eks. 70%), begynder agenten autonomt at:
1. Opsummere ældre beskeder
2. Skrive vigtige fakta til core memory
3. Arkivere detaljeret kontekst til archival storage
4. Frigøre plads i context window

Agenten har **eksplicitte funktionskald** til at læse/skrive hukommelse:
- `core_memory_append()` / `core_memory_replace()` — redigér permanent hukommelse
- `archival_memory_search()` / `archival_memory_insert()` — søg/gem i langtidsarkiv
- `conversation_search()` — søg i samtalehistorik

### Tradeoffs

| Fordel | Ulempe |
|--------|--------|
| Elegant abstraktion — illusionen af uendelig kontekst | Agenten bruger "kognitivt båndbredde" på hukommelsesadministration |
| Selvstyrende — agenten bestemmer hvad der er vigtigt | Ustruktureret storage begrænser komplekse forespørgsler |
| Skalerer til arbitrært lange interaktioner | Ekstra LLM-kald til hukommelsesoperationer = højere kostnad |
| Persistent på tværs af sessioner | Kræver pålidelig function-calling kapabilitet |

### Produktionsmodenhed

**Tidlig produktion.** Letta (MemGPT's kommercielle videreudvikling) tilbyder en hosted platform og open-source framework. DeepLearning.AI har lavet et kursus med Andrew Ng om det. Det er #1 model-agnostic open source agent på Terminal-Bench (coding benchmark).

Nyeste feature (2025-2026): **Context Repositories** — git-baseret versionering af hukommelse med programmatisk kontekst-styring.

### Effekt vs. flad kontekst

Muliggør interaktioner der ellers ville være umulige (dage/uger af kontinuitet). Kvaliteten afhænger af agentens evne til at vælge hvad der er vigtigt at huske — en form for "judgment" der varierer mellem modeller.

---

## 5. RAG-baseret Hukommelse

### Sådan virker det

I stedet for at proppe alt ind i konteksten, hentes kun det relevante ved behov:

```
Bruger stiller spørgsmål
    → Embed spørgsmålet
    → Søg i vector DB for relevante chunks
    → Injicer top-K resultater i konteksten
    → LLM svarer med den ekstra kontekst
```

**Agentic RAG** (2025-2026) går videre: agenten selv beslutter *hvornår* og *hvad* der skal retrieves, bruger planlægning og refleksion, og kan iterere over flere retrieval-runder.

**A-RAG** (Hierarchical Retrieval, arXiv feb. 2026) tilføjer hierarkiske retrieval-interfaces der skalerer til enterprise-niveau.

### Tradeoffs

| Fordel | Ulempe |
|--------|--------|
| Kun relevante tokens i konteksten | Retrieval-kvalitet er flaskehalsen |
| Skalerer til millioner af dokumenter | Semantic search fanger ikke altid det relevante |
| Velforstået teknologi med mange tools | Chunking-strategi er kritisk og svær at perfektionere |
| Kombinerer godt med alle andre tilgange | Latency fra embedding + søgning + re-ranking |

### Produktionsmodenhed

**Fuld produktion.** RAG er den mest modne og udbredte tilgang. Qdrant, Pinecone, Chroma, Weaviate har tusindvis af produktions-deployments. Næsten alle chatbots med domain-viden bruger RAG i en eller anden form.

Men industrien bevæger sig fra "RAG" mod "Context Engine" — RAG som én komponent i en bredere kontekst-styringspipeline.

### Effekt vs. flad kontekst

Dramatisk forbedring for domain-specifik viden. Reducer hallucinationer med 60-90% sammenlignet med ren parametrisk viden. Men kræver investering i retrieval-pipeline kvalitet.

---

## 6. Multi-agent Arkitekturer

### Sådan virker det

I stedet for én agent med ét stort context window, bruger man **specialiserede agenter med separate kontekster:**

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Planlægger   │────▶│ Researcher   │────▶│ Eksekutør    │
│ (strategi)   │     │ (RAG/search) │     │ (handling)   │
└──────────────┘     └──────────────┘     └──────────────┘
       │                                         │
       └──────────────┐     ┌────────────────────┘
                      ▼     ▼
              ┌──────────────────┐
              │ Delt Hukommelse  │
              │ (Redis/DB/Graph) │
              └──────────────────┘
```

**Hukommelses-scoping** er den vigtigste designbeslutning:
- **Isoleret hukommelse:** Hver agent har sin egen kontekst. Sikkerhed, men risiko for duplikeret arbejde.
- **Delt hukommelse:** Agenter læser/skriver til fælles store. Koordination, men risiko for "memory contamination."
- **Hybrid:** Privat arbejdshukommelse + delt faktabase.

**Framework-implementationer:**
- **LangGraph:** In-thread memory (session) + cross-thread memory (persistent). MemorySaver + InMemoryStore.
- **CrewAI:** ChromaDB (short-term), SQLite (task results), vector embeddings (entity memory).
- **Autogen:** Pluggable memory backends med developer-styret write-back.

### Tradeoffs

| Fordel | Ulempe |
|--------|--------|
| Hvert vindue fokuserer på sin opgave | Koordinations-overhead mellem agenter |
| Naturlig parallelisering | Memory contamination ved delt hukommelse |
| Specialisering → højere kvalitet per opgave | Kompleks at debugge og monitorere |
| Skalerer horisontalt | Token-kostnad multipliceres med antal agenter |

### Produktionsmodenhed

**Tidlig produktion.** LangGraph, CrewAI og Autogen er i brug i produktion, men kræver betydelig engineering. Redis, MongoDB og PostgreSQL som backends er veldokumenterede. MAGMA (Multi-Graph based Agentic Memory Architecture, januar 2026) er cutting-edge research.

### Effekt vs. flad kontekst

Muliggør opgaver der kræver mere kontekst end noget enkelt vindue kan rumme. Men overhead-kostnaden er reel — simpel single-agent med god compaction slår ofte multi-agent for moderate opgaver.

---

## 7. Nye Tilgange (2025-2026)

### 7a. Infini-attention (Google, 2024)

Indbygger en **compressive memory** direkte i attention-mekanismen. Gemmer hele historikken i en fixed-size Memory Matrix i stedet for lineært voksende KV-cache.

- **114x reduktion** i GPU VRAM vs. Memorising Transformers
- Klarer passkey retrieval op til **1 million tokens**
- State-of-the-art på 500K token bog-summarization

**Status:** Research. Ikke tilgængelig i kommercielle modeller endnu, men Google bruger sandsynligvis varianter internt.

### 7b. EM-LLM — Episodisk Hukommelse inspireret af hjernen

Integrerer aspekter af menneskelig episodisk hukommelse i LLM'er **uden fine-tuning**. Virker out-of-the-box med enhver Transformer-model.

**Status:** Research/eksperimentel.

### 7c. Megalodon (Meta, 2024-2025)

Ny arkitektur med **lineær** computational complexity (i stedet for kvadratisk) relative til input-længde. Designet til ubegrænset context length.

**Status:** Research. Ingen kommerciel deployment.

### 7d. Mem0 — Universal Memory Layer

Managed memory-as-a-service. Ekstraherer, konsoliderer og retriever salient information automatisk.

- **26% forbedring** i LLM-as-Judge over OpenAI's hukommelse
- **91% lavere p95 latency**
- **90%+ token-besparelse**
- 41.000+ GitHub stars, 14M+ PyPI downloads
- AWS valgte Mem0 som eksklusiv memory provider for deres Agent SDK
- Raised $24M (Series A, oktober 2025)

**Status:** **Fuld produktion.** Bruges af CrewAI, Flowise, Langflow, Fortune 500 virksomheder.

### 7e. Agentic Memory (AgeMem, januar 2026)

Unified framework der integrerer lang- og korttidshukommelse direkte i agentens policy. Hukommelsesoperationer er eksponeret som tool-kald: store, retrieve, update, summarize, discard.

**Status:** Research (arXiv 2601.01885).

### 7f. Manus' Context Engineering (2025)

Ikke ét trick men en **samlet disciplin:**

- KV-cache hit rate som den vigtigste produktionsmetrik (10x omkostningsreduktion)
- Logit masking i stedet for dynamisk tool-fjernelse (bevarer cache)
- Filsystemet som ubegrænset ekstern hukommelse
- `todo.md` recitation mod goal drift
- Fejl bevares i konteksten (belief updates)

**Status:** **Fuld produktion.** Manus er en af de mest avancerede produktionsagenter.

### 7g. Memoria (december 2025)

Skalerbar agentic memory framework til personaliseret konversations-AI (arXiv 2512.12686).

**Status:** Research/tidlig adoption.

---

## Sammenligningstabel

| Tilgang | Kompleksitet | Produktion? | Token-besparelse | Langtid? | Bedst til |
|---------|-------------|-------------|------------------|----------|-----------|
| Sliding Window/Compaction | Lav | Ja | 60-80% | Nej (session) | Lange single-session samtaler |
| Hierarkisk Summarization | Medium | Ja | 70-90% | Ja | Multi-session kontinuitet |
| Vector DB (RAG) | Medium | Ja | 80-95% | Ja | Domain-viden, search |
| Knowledge Graph | Høj | Delvis | 80-95% | Ja | Relationsforståelse |
| MemGPT/Letta | Høj | Delvis | Variabel | Ja | Autonome agenter |
| Multi-agent | Høj | Delvis | Variabel | Ja | Komplekse workflows |
| Mem0 (managed) | Lav | Ja | 90%+ | Ja | Plug-and-play personalisering |
| Infini-attention | N/A | Nej | 114x VRAM | Ja | Næste gen modeller |

---

## Konklusion

### Hvad virker i produktion LIGE NU (februar 2026)

1. **Compaction + hierarkisk summarization** er baseline. Alle seriøse produktionssystemer bruger det. Google ADK, Manus og Claude Code implementerer varianter.

2. **RAG er modent men evolverer.** Vector search alene er utilstrækkeligt — industrien bevæger sig mod Agentic RAG (agenten styrer retrieval) og GraphRAG (relations-forståelse).

3. **Mem0 er den hurtigste vej til produktion.** Managed service, bred framework-integration, dokumenterede forbedringer. Hvis man vil have langtidshukommelse uden at bygge det selv.

4. **Manus' context engineering** er state-of-the-art for produktionsagenter. Kerneindsigten: **KV-cache hit rate er vigtigere end raw context management.** 10x omkostningsreduktion ved stabile prompt-prefixes.

5. **MemGPT/Letta** er den mest elegante abstraktion men stadig krævende at operere. God til autonome agenter der skal køre i dage/uger.

### Anbefaling til Ydrasil

Ydrasil bruger allerede Qdrant (vector DB) + CLAUDE.md (manuelt kurateret kontekst) + session logging. Det er et solidt fundament. De næste skridt efter stigende kompleksitet:

1. **Automatisk compaction** — implementér sliding window summarization i checkpoint-systemet (lav, høj gevinst)
2. **Mem0 integration** — erstat/supplér Qdrant med Mem0 for personlig hukommelse (lav, høj gevinst)
3. **GraphRAG** — byg relationer oven på Qdrant-data for bedre retrieval (medium, medium gevinst)
4. **MemGPT-inspireret memory pressure** — lad agenten selv styre sin hukommelse (høj, høj gevinst for autonomi)

---

## Kilder

### Papers
- [Infini-attention: Leave No Context Behind](https://arxiv.org/abs/2404.07143) — Google, april 2024
- [MemGPT: Towards LLMs as Operating Systems](https://research.memgpt.ai/) — UC Berkeley, 2023
- [Agentic Memory (AgeMem)](https://arxiv.org/abs/2601.01885) — januar 2026
- [Memoria: Scalable Agentic Memory](https://arxiv.org/abs/2512.12686) — december 2025
- [Agentic RAG Survey](https://arxiv.org/abs/2501.09136) — januar 2025
- [A-RAG: Hierarchical Retrieval](https://arxiv.org/html/2602.03442) — februar 2026
- [Memory in the Age of AI Agents (survey)](https://arxiv.org/abs/2512.13564) — december 2025
- [Personalized Long-term Interactions via Persistent Memory](https://arxiv.org/abs/2510.07925) — oktober 2025
- [Microsoft GraphRAG](https://arxiv.org/abs/2404.16130) — april 2024
- [EM-LLM: Human-Inspired Episodic Memory](https://em-llm.github.io/) — 2024
- [NEXUSSUM: Hierarchical LLM Agents for Long-Form Summarization](https://aclanthology.org/2025.acl-long.500.pdf) — ACL 2025

### Frameworks og tools
- [Letta (MemGPT)](https://www.letta.com/) — Stateful AI agents med persistent memory
- [Mem0](https://mem0.ai/) — Universal memory layer ($24M Series A)
- [Google ADK Compaction](https://google.github.io/adk-docs/context/compaction/) — Built-in context compaction
- [LangMem SDK](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/) — LangChain's memory framework
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag) — Graph-based RAG
- [Agent Memory Paper List](https://github.com/Shichun-Liu/Agent-Memory-Paper-List) — Kurateret papirliste

### Blog posts og artikler
- [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — Manus, 2025
- [Design Patterns for Long-Term Memory in LLM Architectures](https://serokell.io/blog/design-patterns-for-long-term-memory-in-llm-powered-architectures) — Serokell
- [Context Engineering for AI Agents: Part 2](https://www.philschmid.de/context-engineering-part-2) — Phil Schmid
- [How LLMs Handle Infinite Context With Finite Memory](https://towardsdatascience.com/llms-can-now-process-infinite-context-windows/) — Towards Data Science
- [Advancing Long-Context LLM Performance in 2025](https://flow-ai.com/blog/advancing-long-context-llm-performance-in-2025) — Flow AI
- [Stateful AI Agents: Deep Dive into Letta Memory Models](https://medium.com/@piyush.jhamb4u/stateful-ai-agents-a-deep-dive-into-letta-memgpt-memory-models-a2ffc01a7ea1) — Medium, feb 2026
- [Context Engineering in Manus](https://rlancemartin.github.io/2025/10/15/manus/) — Lance Martin
- [Mem0 Research: 26% Accuracy Boost](https://mem0.ai/research) — Mem0
- [LLM Chat History Summarization Guide](https://mem0.ai/blog/llm-chat-history-summarization-guide-2025) — Mem0, 2025
- [Context Engineering Turns AI Agents From Goldfish Into Assistants](https://blog.suryas.org/p/context-engineering-sessions-memory) — Surya
- [AI Agent Architecture: Build Systems That Work in 2026](https://redis.io/blog/ai-agent-architecture/) — Redis
- [Compaction: The Missing Design Principle](https://medium.com/data-science-collective/compaction-the-missing-design-principle-for-scalable-llm-applications-3e9c831a72e0) — Medium, feb 2026
- [From RAG to Context: 2025 Year-End Review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context) — RAGFlow
