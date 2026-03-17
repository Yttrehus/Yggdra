# Destillat: AI Agent Memory & Retrieval

**Dato:** 15. marts 2026
**Formål:** Skarpeste samlede overblik over menneskehukommelse, AI-hukommelsessystemer, retrieval-teknikker og praktisk arkitektur for solo-udvikler.
**Metode:** Destillation af 12 primærkilder (feb-marts 2026), krydsvalideret mod akademisk litteratur.
**Evidensniveauer:** SOLID = peer-reviewed/replikeret. ANEKDOTISK = open-source community/blog. VENDOR = eget benchmark/marketing.

---

## Indholdsfortegnelse

1. [Menneskehukommelse — Kognitionsvidenskab](#1-menneskehukommelse)
2. [AI-Hukommelse State of the Art](#2-ai-hukommelse-state-of-the-art)
3. [OpenClaw-Principper](#3-openclaw-principper)
4. [Zero-Token Patterns](#4-zero-token-patterns)
5. [Retrieval — Fra Naiv RAG til Hybrid Search](#5-retrieval)
6. [Praktisk Arkitektur for Solo-Udvikler](#6-praktisk-arkitektur)
7. [Åbne Spørgsmål](#7-aabne-spoergsmaal)
8. [Samlet Litteraturliste](#8-samlet-litteraturliste)

---

## 1. Menneskehukommelse

### 1.1 Fire Hukommelsessystemer

Menneskehukommelsen er ikke ét system men et samspil mellem specialiserede subsystemer. Atkinson & Shiffrins (1968) modale model (sensorisk → korttid → langtid) er forenklet; nyere forskning viser fire funktionelt distinkte systemer:

| System | Funktion | Neuralt grundlag | AI-parallel |
|--------|----------|-----------------|-------------|
| **Episodisk** | Personligt oplevede begivenheder, bundet til tid/sted | Hippocampus | Session logs, episodes.jsonl |
| **Semantisk** | Fakta og begreber, frigjort fra kontekst | Neocortex (distribueret) | Qdrant vektorer, CLAUDE.md |
| **Procedural** | Know-how, motoriske/kognitive færdigheder | Basalganglier, cerebellum | Skills/, finjusterede modeller |
| **Arbejdshukommelse** | Korttidslagring + manipulation, ~4 chunks (Cowan 2001) | Præfrontal cortex | Context window |

**Complementary Learning Systems (CLS):** McClelland, McNaughton & O'Reilly (1995) demonstrerede at hjernen har to komplementære systemer — hippocampus for hurtig, specifik læring og neocortex for langsom, struktureret læring. Kumaran, Hassabis & McClelland (2016) opdaterede CLS-teorien: intelligente agenter behøver *nødvendigvis* begge. AI-parallel: RAG (hurtig, specifik) + model weights (langsom, generaliseret). **[SOLID]**

### 1.2 Encoding — Dybde Bestemmer Retention

Craik & Lockhart (1972) viste at hukommelseskvalitet afhænger af processerings*dybde*:
- Overfladisk (sensorisk) → dårlig retention
- Fonologisk (lyd) → middel retention
- Semantisk (betydning) → stærk retention

Craik & Tulving (1975) bekræftede eksperimentelt. Paivio (1971) tilføjede Dual Coding Theory: information kodet i *både* verbal og visuel form huskes markant bedre. **[SOLID]**

**Implikation for AI:** Rå tekst → embedding er overfladisk processering. Bedre: generér resumé (semantisk processing) + tilføj relationsmetadata (elaboration) + kontekst-metadata (encoding specificity). Embed resuméet *sammen med* indholdet.

### 1.3 Retrieval — Rekonstruktiv, Ikke Reproduktiv

Retrieval er en aktiv, rekonstruktiv proces, ikke en simpel lookup:

- **Encoding Specificity Principle** (Tulving & Thomson 1973): En hukommelse kan kun hentes hvis retrieval-cuen matcher konteksten hvori informationen blev kodet. Godden & Baddeley (1975) bekræftede med dykkereksperimentet. **[SOLID]**
- **Pattern Completion:** Hippocampus rekonstruerer fulde erindringer fra delvise cues. Horner et al. (2015, Nature Communications) viste holistisk genkaldelse via pattern completion, udfolder sig over 500-1500 ms i neocortex. **[SOLID]**
- **Spreading Activation** (Collins & Loftus 1975): Semantisk hukommelse er organiseret som netværk. Aktivering af én node spreder sig til relaterede noder. **[SOLID]**
- **Testing Effect** (Roediger & Karpicke 2006): At hente information *styrker* den — mere end gentagelse. Retrieval er ikke neutral aflæsning men aktiv læringsproces. **[SOLID]**

**Implikation for AI:** Top-K cosine similarity er cue-dependent recall. Men vi mangler spreading activation (2. ordens retrieval) og pattern completion (returnér hele dokumenter fra partielle hits). En graph-layer over Qdrant ville løse dette.

### 1.4 Glemsel — En Feature, Ikke en Bug

**Ebbinghaus' Glemselskurve** (1885, replikeret af Murre & Dros 2015): Ikke-lineær — 42% glemt efter 20 min, 66% efter 1 dag, 79% efter 1 måned. **[SOLID]**

**Interferens** er primær mekanisme (ikke passivt forfald):
- Retroaktiv interferens: ny læring forstyrrer gammel hukommelse (Müller & Pilzecker 1900)
- Proaktiv interferens: gammel læring forstyrrer ny encoding
- Retrieval-Induced Forgetting: at hente én hukommelse *undertrykker* relaterede (Anderson, Bjork & Bjork 1994) — aktiv inhibition, ikke konkurrence **[SOLID]**

**Adaptiv glemsel** beskytter mod overload, opdaterer forældet info, og muliggør generalisering. Nate Jones formulerer det præcist: "Forgetting is a useful technology for us. AI systems don't have any of that. They either accumulate or they purge, but they do not decay."

**Implikation for AI:** AI-systemer i dag glemmer intet — alt forbliver med samme vægt. Nødvendigt: temporal decay (FSRS-inspireret), access-based scoring, conflict resolution (nyere > ældre), periodisk arkivering.

### 1.5 Emotionel Vægtning og Salience

Amygdala-hippocampus-interaktion forstærker emotionelt signifikante erindringer via stresshormoner og synaptisk plasticitet. Girardeau et al. (2017, Nature Neuroscience) viste at hippocampus-amygdala kredsløb reaktiveres under non-REM søvn. Yerkes-Dodson-loven: moderat arousal optimerer hukommelse; ekstrem arousal kan fragmentere. **[SOLID]**

**Implikation for AI:** Alle chunks behandles ens. Et `salience`-felt bør differéntiere: kritiske fejl (0.9), beslutninger med konsekvenser (0.7), rutinelogs (0.3).

### 1.6 Konsolidering Under Søvn

Systems Consolidation Theory: Nye oplevelser kodes hurtigt i hippocampus (vågen), genafspilles og overføres til neocortex under søvn (SWR + sleep spindles + slow oscillations). Born & Wilhelm (2012), Diekelmann & Born (2023), Tambini & Davachi (2019) viste at bevidst gennemgang før søvn initierer systemkonsolidering. **[SOLID]**

**Implikation for AI:** En nightly pipeline der re-processerer dagens sessioner = primitiv hippocampal replay. Mangler: kompression (verbose → koncist), cross-linking (nye → eksisterende), pruning (redundans), migration (episodisk → semantisk ved gentagelse).

### 1.7 Reconsolidation

Nader et al. (2000): Konsoliderede hukommelser der hentes bliver midlertidigt ustabile og kræver ny proteinsyntese for at restabilisere. Hver retrieval åbner et "edit window" for opdatering. Betingelser: prediction error + begrænset tidsvindue (~6 timer) + ny information. **[SOLID]**

**Implikation for AI:** Retrieval bør være aktiv opdatering, ikke passiv aflæsning. Ved retrieval: opdatér access_count og last_accessed. Ved mismatch (bruger modsiger chunk): flag for re-embedding.

### 1.8 Ekspert-Chunking

Chase & Simon (1973): Skakmestre genkender konfigurationer som store chunks, nybegyndere ser individuelle brikker. ~50.000 chunk-patterns for ekspert-niveau (Gobet & Simon 1998). Generaliseret til medicinsk diagnose, programmering, musik, brandbekæmpelse (Klein 1998). **[SOLID]**

**Implikation for AI:** Domæne-specialiserede collections med domæne-specifik chunking. Hierarkisk chunking (resumé linket til detaljer). Cluster-baseret retrieval (semantiske clusters, ikke isolerede hits).

### 1.9 Spaced Repetition — FSRS-Modellen

FSRS (Free Spaced Repetition Scheduler, 2022-2025) modellerer hukommelse med tre variable: Stability (S), Difficulty (D), Retrievability (R). Glemselskurven approksimeres med power-funktion: `R = (1 + t/S)^(-1)`. Direkte implementerbar i vector database scoring. **[SOLID for den matematiske model]**

```python
def memory_score(similarity, days_since_access, stability=30, salience=0.5):
    retrievability = (1 + days_since_access / stability) ** (-1)
    return similarity * 0.7 + retrievability * 0.2 + salience * 0.1
```

---

## 2. AI-Hukommelse State of the Art

### 2.1 Taxonomi

Liu et al. (arXiv 2512.13564, jan 2026) foreslår en 3D-taxonomi: **form** (token/parametric/latent) × **funktion** (factual/experiential/working) × **dynamik** (formation/evolution/retrieval). Den gamle opdeling "short-term vs long-term" er utilstrækkelig. **[SOLID — bred survey, 100+ papers]**

Nate Jones (YouTube, 2026) tilføjer en praktisk dimension: hukommelse er MULTIPLE problemer — preferences (permanent KV), facts (struktureret, kræver opdatering), knowledge (parametrisk), episodic (temporal, ephemeral), procedural (exemplarer). "Treating this problem as one problem guarantees you solve none well." **[ANEKDOTISK — men bredt anerkendt i community]**

### 2.2 Frameworks — Hvad Virker, Hvad er Hype

#### MemGPT / Letta (21K stars)
OS-analogi: context window = RAM, ekstern storage = disk. Core memory (always-in-context, self-editing) + Recall (samtalehistorik) + Archival (vector DB). Letta V1 (feb 2026) tilføjer Context Repositories (git-baseret memory versionering).
- **Styrke:** Elegant abstraktion, agent-styret hukommelse
- **Svaghed:** Bruger LLM-kald til memory-ops (dyre tokens), kompleks arkitektur
- **Vurdering:** Overkill for 1 bruger. Koncepterne (tiered memory, memory pressure) er værdifulde at stjæle.
- **Evidens:** DeepLearning.AI-kursus med Andrew Ng, #1 på Terminal-Bench. **[ANEKDOTISK]**

#### Mem0 (47.8K stars)
Memory orchestration layer: extraction phase (LLM udtrækker kandidat-memories) + update phase (tilføj/opdatér/slet/behold). Qdrant som default vector store.
- **Påstået performance:** 26% accuracy-forbedring, 91% lavere p95 latency, 90%+ token-besparelse
- **Styrke:** Simpelt API (add/search/update), direkte Qdrant-integration, automatisk dedup+decay
- **Svaghed:** Tal fra eget paper (arXiv 2504.19413), ikke uafhængigt verificeret. Open-source version har færre features.
- **Vurdering:** Bedste match for eksisterende stack. Men kan bygges i ~50 linjer Python: "3 prompts oven på vector DB."
- **Evidens:** AWS eksklusiv memory provider, $24M Series A. **[VENDOR-CLAIMS for performance-tal]**

#### Zep / Graphiti (23K stars)
Temporal knowledge graph. Bi-temporal model — ved HVORNÅR ting skete, invaliderer forældet info. Graphiti engine. P95 latency 300ms, ingen LLM-kald ved retrieval.
- **Styrke:** Relationsforståelse, temporal awareness
- **Svaghed:** Kræver Neo4j/Kuzu (1-2GB RAM ekstra). Claude er "second class citizen" (Structured Output).
- **Vurdering:** For tungt for 4GB VPS med Qdrant. **[VENDOR-CLAIMS + SOLID (arXiv 2501.13956)]**

#### Cognee (6K stars)
ECL pipeline (Extract, Cognify, Load) → knowledge graphs. 30+ datakilder, MCP-server.
- **Vurdering:** Lovende men v0.3, for tidlig for produktion. **[ANEKDOTISK]**

#### A-MEM (NeurIPS 2025)
Zettelkasten-inspireret: atomiske noter med auto-linking. Selvorganiserende vidensnetværk.
- **Styrke:** Elegant design, akademisk valideret (NeurIPS)
- **Svaghed:** Forskningsprojekt, ikke production-ready. LLM-kald per memory-link.
- **Vurdering:** Som inspiration, ikke implementation. **[SOLID — arXiv 2502.12110, NeurIPS 2025]**

#### LightRAG (28.5K stars)
Letvægts auto-genereret knowledge graph. Dual retrieval: lokal (entiteter) + global (temaer). NetworkX in-memory.
- **Påstået:** 10x billigere end GraphRAG, sammenlignelig nøjagtighed
- **Svaghed:** Entity extraction kan hallucinere. Paper trukket fra ICLR.
- **Vurdering:** Interessant men svagt evidensgrundlag. **[VENDOR-CLAIMS — trukket paper er et rødt flag]**

#### MAGMA (jan 2026)
4 parallelle grafer (semantic, temporal, causal, entity). 45.5% bedre reasoning.
- **Vurdering:** Cutting-edge research, ikke production-ready. **[SOLID — arXiv 2601.03236]**

### 2.3 Konsolideringsoverblik

| Framework | Qdrant-support | RAM | Kompleksitet | Production | Solo-dev egnet |
|-----------|---------------|-----|-------------|------------|----------------|
| Mem0 | Ja (default) | ~200MB | Lav | Ja | **Ja** |
| Letta/MemGPT | Ja (archival) | ~500MB | Høj | Ja | Delvist |
| Zep/Graphiti | Nej (graph DB) | 2GB+ | Høj | Ja | Nej |
| Cognee | Delvist | Høj | Medium | Beta | Nej |
| A-MEM | Custom | Lav | Medium | Nej | Som inspiration |
| LightRAG | Ja (Qdrant) | ~512MB | Medium | Delvist | Muligvis |

### 2.4 RAG — Moden Men Ikke Perfekt

**73-80% af enterprise RAG-projekter fejler** (Analytics Vidhya 2025). Ikke fordi RAG er dårligt, men fordi teams ikke forstår failure surfaces: chunking × embedding × retrieval × context assembly × generation. 95% accuracy per stage = 77% end-to-end. **[ANEKDOTISK — industri-observation]**

Stanford "Lost in the Middle": LLMs bruger info i start/slut af kontekst, ignorerer midten. 30%+ performance drop. Long context er komplementært til RAG, ikke erstatning. **[SOLID]**

**Chunking er 80% af RAG-kvalitet.** CDC-studie: naiv chunking = 0.47-0.51 faithfulness, optimeret semantisk = 0.79-0.82. 60% forbedring fra chunking alene. Impact-hierarki: chunking > query formulering > retrieval pipeline > embedding model. **[SOLID]**

**Hybrid Search (vektor + BM25)** er production-ready og giver 15-25% bedre retrieval end dense-only. Qdrant supporterer det nativt. Reciprocal Rank Fusion (RRF) til kombination. Typisk 70% vektor + 30% BM25. **[SOLID — bred produktion]**

**Reranking** forbedrer op til 48% (Databricks). Cohere Rerank ($1/1K queries) er de facto standard. BGE Reranker er gratis alternativ. **[SOLID — Databricks benchmark]**

---

## 3. OpenClaw-Principper

OpenClaw (430K+ linjer TypeScript, Peter Steinberger → open-source feb 2026) er for stort til at installere, men principperne er guld.

### 3.1 3-Lags Hukommelse

| Lag | Hvad | Livscyklus | Ydrasil-parallel |
|-----|------|-----------|-----------------|
| **Tier 1** | MEMORY.md (~100 linjer, kurateret) | Permanent | CLAUDE.md + MEMORY.md |
| **Tier 2** | `memory/YYYY-MM-DD.md` (daglige noter) | I dag + i går | episodes.jsonl |
| **Tier 3** | `memory/people/`, `projects/`, `topics/` (vektor-søgbar) | Evergreen | Qdrant collections |

### 3.2 Heartbeat-Daemon

1. systemd/cron kører gateway hvert 30 min
2. Agent læser HEARTBEAT.md (tjekliste)
3. **Deterministiske checks FØRST** (API-kald, filcheck) — ingen LLM
4. Intet at gøre → HEARTBEAT_OK (0 tokens)
5. Signal fundet → LLM evaluerer og handler

**Kritisk indsigt:** Regel-baserede checks som filter INDEN LLM. En bruger betalte $18.75 på én nat for Opus der spurgte "er det dag endnu?" hvert 30 min. Brug Groq/Haiku, aldrig Opus, til heartbeat. **[ANEKDOTISK]**

### 3.3 memsearch (Zilliz)

Standalone library extraheret fra OpenClaws hukommelse:
- Scanner markdown-mapper, splitter i chunks (heading-baseret)
- **Hybrid search: dense vektor + BM25 sparse + RRF reranking**
- Filer er source of truth, IKKE vector-indexet

OpenClaws hukommelse er ikke magi. Det er markdown-filer + vektor-søgning + hybrid search. **[ANEKDOTISK]**

### 3.4 Hvad Der Skal Stjæles

1. **Heartbeat med regel-baseret filter** — cron hvert 30 min, deterministisk check, LLM kun ved signal
2. **HEARTBEAT.md som konfig** — behavior-as-config, ændring = rediger markdown
3. **Hybrid search** — dense + sparse + RRF
4. **Temporal decay** — `score × e^(-ln2/halflife × age_days)`, halflife 30 dage for samtaler, no decay for identitet
5. **Pre-compaction flush** — gem vigtig viden til disk FØR context komprimering
6. **Files in git > fancy databases** — markdown/JSONL for session memory, Qdrant for heterogen ekstern viden

---

## 4. Zero-Token Patterns

### 4.1 Kerneprincippet

70-90% af typisk pipeline-arbejde (filtrering, routing, deduplicering, formatering, tidsbaseret logik) kan håndteres med deterministisk kode. LLM'en skal kun aktiveres for de resterende 10-30% der kræver semantisk forståelse.

Fundament: Unix pipe-filosofien (McIlroy 1964/1978, Raymond 2003). Tekst er det universelle interface. Data flyder som tekst-strømme gennem specialiserede filtre.

### 4.2 Gate-keeper Mønstret

```
Data ind → [Regelbaseret filter] → Signal? → Nej → Log + sov
                                  → Ja  → [LLM] → Handling
```

| Data | Gate-keeper regel | LLM kun ved |
|------|------------------|-------------|
| Emails | Afsender i whitelist? Keyword? | Ukendt + forretningsrelevant |
| Trello | Ændret siden sidst? | Nyt kort der kræver prioritering |
| RSS | Ny artikel? Titel matcher keywords? | Passerer keyword-filter |
| Git | Fil i kritisk sti? | Semantisk review |
| Kalender | Event inden for 24h? | Møde-briefing |

Gate-keeperen filtrerer 80-95% af events. **[ANEKDOTISK — OpenClaw docs, bred praksis]**

### 4.3 JSONL som Event-bus

Erstatter Kafka for solo-dev: append-only, `wc -l` for stats, `tail -f` for monitoring, `jq` for ad-hoc queries. Idempotente consumers med offset-tracking i state-fil. Én JSONL per datakilde.

### 4.4 Hash-baseret Deduplicering

Content hash (SHA256) ved ingestion. Source-prefix ID'er (tw-123, yt-456) for unikhed. Idempotent upsert med payload-hash i Qdrant. Inspireret af Willison/Dogsheep, Karlicoss/HPI, Linus Lee/Monocle. **[ANEKDOTISK — bred praksis]**

### 4.5 Estimeret Token-besparelse

| Scenario | Med LLM overalt | Med zero-token pipeline | Besparelse |
|----------|-----------------|------------------------|------------|
| Morning brief (10 kilder) | ~5.000 tokens | ~800 tokens | 84% |
| Heartbeat (6 inboxes, 48×/dag) | ~48.000 tokens/dag | ~2.400 tokens/dag | 95% |
| Research-kategorisering (50 artikler) | ~25.000 tokens | ~5.000 tokens | 80% |

---

## 5. Retrieval

### 5.1 RAG-Arkitekturer (Modenhedsoverblik)

| Arkitektur | Modenhed | Indsats | Gevinst |
|-----------|---------|--------|---------|
| Naive RAG (top-k + prompt) | Production | Allerede i brug | Baseline |
| Hybrid Search (vektor + BM25) | Production | Dage | 15-25% bedre |
| Reranking (cross-encoder/Cohere) | Production | Timer | Op til 48% |
| HyDE (hypotetisk dokument) | Production | Timer | Bedre recall |
| Semantic Chunking | Early adopter | Dage | 60% over naiv |
| RAG-Fusion (multi-query + RRF) | Production | Timer | ~14% (MQRF-RAG 2025) |
| GraphRAG | Eksperimentel | Uger | Multi-hop reasoning |
| Agentic RAG | Eksperimentel | Uger | Dynamisk strategi |

### 5.2 Chunking — Den Vigtigste Lever

CDC-studie: chunking strategi har størst impact på RAG-kvalitet. Hierarki:

1. **Fixed-size** (~500 tokens, 10-20% overlap): Baseline. Simpelt. Ydrasil bruger dette.
2. **Recursive character splitting**: Default for 80%. LangChains industristandard.
3. **Semantic chunking**: 256-512 tokens, embedding-baseret split-detection. 60% over naiv.
4. **Proposition chunking**: Selvstændige udsagn. Højeste præcision per chunk.
5. **Hierarchical (parent-child)**: Retrieval på detalje-niveau, kontekst fra forælder.

**Kontekstuel chunking** (Willison/Anthropic): Send chunk + dokument-titel til billig LLM → få 1-2 sætningers kontekst → prepend → embed. Markant bedre retrieval. **[ANEKDOTISK — bredt anbefalet]**

### 5.3 Embedding-Modeller

Embedding model er den **mindst vigtige** lever (chunking > query > pipeline > model). Gabet mellem billigste og dyreste er 4-5 MTEB-point. **[SOLID — Databricks benchmark]**

text-embedding-3-small (OpenAI, $0.02/M, 1536 dim) er korrekt valg for solo. Alternativer: voyage-3.5-lite (bedre MTEB, $0.02/M), BGE-M3 (gratis, bedste open-source). Model upgrade = fuld re-embedding — gem altid rå tekst.

### 5.4 Temporal Decay i Scoring

Stanford Generative Agents (Park et al. 2023): `score = recency × importance × relevance`. OpenClaw: `score × e^(-ln2/halflife × age_days)`, halflife 30 dage. Simpel implementation:

```python
def apply_decay(results, decay_rate=0.01):
    for r in results:
        age_days = (now - r.payload["created_at"]).days
        r.score *= 1 / (1 + age_days * decay_rate)
    return sorted(results, key=lambda r: r.score, reverse=True)
```

**[SOLID for Stanford; ANEKDOTISK for OpenClaw-parametrene]**

---

## 6. Praktisk Arkitektur for Solo-Udvikler

### 6.1 Det Universelle Mønster

Alle succesfulde systemer (OpenClaw, Gastown, Nemori, MemGPT, GitHub Copilot, Miessler PAI) konvergerer mod samme mønster:

```
LIVE SESSION
  Load: Identity (CLAUDE.md) + Episoder (seneste 5) + Hot context (NOW.md)
  Under samtale: Agent kan SEARCH og STORE memory
  Før compaction: Silent flush (gem vigtigt til disk)
  Ved session-slut: Destillér → 3-5 linjers episode

MEMORY LAYERS
  HOT   → NOW.md, SESSION_RESUME.md (altid i context, ~2K tokens)
  WARM  → episodes.jsonl (seneste 30 dage, BM25-søgbar, temporal decay)
  COLD  → Qdrant (advisor brain, ruter, viden — hybrid search, evergreen + decaying)

HEARTBEAT DAEMON
  Hvert 30 min (08:00-22:00):
  1. Læs HEARTBEAT.md tjekliste
  2. Deterministiske checks (mail, tasks, telegram)
  3. Intet → HEARTBEAT_OK (0 tokens)
  4. Signal → Notificér via Telegram
```

### 6.2 6 Designprincipper

1. **Segment first, distill second** (Nemori, arXiv 2508.03341): Rå samtale → episoder → semantisk viden. Batch, segmentér efter emne, destillér. Udtræk ikke fakta fra en strøm.

2. **Validate at retrieval, not storage** (GitHub Copilot-mønstret): Gem alt løst. Verificér ved retrieval om det stadig er sandt. Billigere og mere robust end kuratering ved write.

3. **Temporal decay med evergreen-undtagelser**: Halflife 30 dage for samtaler. No decay for identitet/advisor-viden. Tilgåede memories refreshes.

4. **Hybrid search = BM25 + vectors + RRF**: Agenter søger med keywords (BM25 vinder). Brugere søger med mening (vektorer vinder). Kombiner med RRF.

5. **Pre-compaction flush**: Før context komprimerer, gem vigtigt til disk. Udvid PreCompact hooks til at lade LLM vælge hvad der er vigtigt.

6. **Files in git > fancy databases**: For session memory — markdown/JSONL i git. BM25-søgbar, versionskontrolleret, menneskelæsbar. Reservér Qdrant til heterogen ekstern viden.

### 6.3 Data Pipeline Best Practices (fra Praktikerne)

**Simon Willison** (Dogsheep): Hvert datakilde → dedikeret konverter → SQLite → faceted search. Hybrid search (FTS5 + embeddings). "Good RAG systems are backed by evals." **[ANEKDOTISK — men fra den mest respekterede praktiker]**

**Karlicoss/HPI**: Data forbliver i kildeformat på disk. Normalisering on-the-fly. Multi-source merging. Ingen central database — filer ER databasen.

**Linus Lee/Monocle**: Standardiseret Doc-schema (ID, tokens, tekst, titel, link). Source-prefix ID'er for dedup. Offline indexering.

**Steph Ango** (Obsidian CEO): "If you want your writing still readable in 2060, it must be readable on a computer from 1960." Filer > apps. **[ANEKDOTISK — men princippet er uimodsigeligt]**

**Fælles mønster:** Data in → deterministisk transformation → struktureret output. LLM kun som valgfrit lag *oven på* regelbaseret pipeline.

### 6.4 Nate Jones' 8 Principper

1. **Memory er en arkitektur, ikke en feature.** Byg det selv, vent ikke på vendors.
2. **Separér efter livscyklus.** Permanent (præferencer) / midlertidigt (projektfakta) / ephemeral (session).
3. **Match storage til query-mønster.** KV for stil, relationelt for fakta, vektor for semantik, tidsserie for historik.
4. **Mode-aware kontekst.** Planlægning kræver bredde, eksekvering kræver præcision.
5. **Byg portabelt.** Overlev vendor-skift, model-skift, tool-skift.
6. **Komprimering er kuratering.** Gør komprimeringsarbejdet selv — dommekraften er menneskelig.
7. **Retrieval kræver verifikation.** To-trins: recall candidates → verificer mod ground truth.
8. **Struktureret hukommelse compound'er.** Tilfældig akkumulering skaber støj. **[ANEKDOTISK — men bredt citeret]**

### 6.5 Prioriteret Bygge-rækkefølge

| # | Komponent | Effort | Impact | Evidens |
|---|-----------|--------|--------|---------|
| 1 | **Hybrid search i Qdrant** (BM25 + dense + RRF) | 1-2 dage | 15-25% bedre retrieval | SOLID |
| 2 | **Temporal decay i ctx** | 30 min | Friskere resultater | SOLID (Stanford) |
| 3 | **Reranking** (Cohere eller BGE lokalt) | 2 timer | Op til 48% | SOLID (Databricks) |
| 4 | **Heartbeat med gate-keeper** | 2 timer | Proaktivitet, ~0 LLM-cost | ANEKDOTISK |
| 5 | **Content hash ved upsert** | 1 time | Undgå re-embedding | ANEKDOTISK |
| 6 | **Kontekstuel chunking** | 1 dag | Markant bedre encoding | ANEKDOTISK |
| 7 | **Mem0-inspireret extraction** (~50 linjer Python) | 2-4 timer | Auto fact-extraction | VENDOR-CLAIMS |
| 8 | **Eval-suite** (20-30 test-queries) | 1 dag | Verificerbar kvalitet | SOLID (Willison) |
| 9 | **Episodisk→semantisk migration** (nightly batch) | 1-2 dage | Langvarig værdi | SOLID (CLS-teori) |

### 6.6 Fravalg (med Begrundelse)

| Fravalg | Hvorfor |
|---------|---------|
| GraphRAG (Microsoft) | For dyrt (tusindvis af API-kald for 80K chunks) |
| Letta/MemGPT installation | Overkill for 1 bruger, tung arkitektur |
| OpenClaw installation | 430K linjer TypeScript, usikker vedligeholdelse |
| Full Mem0 hosted | Vendor lock-in, open-source version er nok |
| 1M token context | $10/prompt, context rot efter ~100K tokens |
| Graphiti/Zep | Kræver Neo4j (2GB+ RAM), Claude er second-class citizen |
| LightRAG | Trukket ICLR-paper, entity hallucination risiko |

### 6.7 Estimeret Omkostning

| Komponent | Månedlig |
|-----------|---------|
| Qdrant (allerede kørende) | $0 |
| Groq Whisper (gratis tier) | $0 |
| Haiku memory extraction (~100 ops) | $1-3 |
| OpenAI embeddings | $0.50 |
| Cohere Rerank (~1K queries) | $1 |
| **Total** | **$2-5/md** |

---

## 7. Åbne Spørgsmål

### 7.1 Ubesvaret i Litteraturen

1. **Optimal decay-rate for personligt vidensystem.** Stanford bruger 30 dage halflife for generative agents. Er det rigtigt for en solo-bruger med projekter der varer måneder? Ingen empirisk data.

2. **Konsolideringsfrekvens.** Hvor ofte bør episodisk viden migrere til semantisk? Dagligt, ugentligt, ved threshold? CLS-teorien foreskriver gradvis overføring, men giver ingen konkret tidsramme for AI-systemer.

3. **Retrieval-verifikation i praksis.** Nate Jones' princip 7 (retrieval kræver verifikation) er intuitivt rigtigt, men ingen har publiceret en simpel, billig implementation for solo-dev setups.

4. **Relevans ≠ similarity.** Nate Jones: "Semantisk lighed er kun en proxy for relevans." Ingen general algoritme for relevans. Mode-aware retrieval (planlægning vs. eksekvering) er ikke løst.

5. **Entity hallucination i graph-baserede systemer.** LightRAGs ICLR-paper blev trukket. Hvor pålidelig er automatisk entity extraction? Usikkert evidensgrundlag.

6. **Cross-session memory contamination.** Hvornår forurener gammel kontekst nye sessioner? Ingen systematisk studie af temporal interference i AI-hukommelsessystemer.

### 7.2 Ubesvaret for Ydrasil Specifikt

7. **Qdrant hybrid search performance på vores data.** 15-25% forbedring er benchmark-tal. Hvad er den reelle gevinst på 84K vektorer med blandet dansk/engelsk?

8. **Mem0 vs. DIY extraction.** Er Mem0 bedre end 50 linjer Python med Haiku? Intet benchmark på vores data.

9. **Eval-baseline mangler.** Vi har ingen systematisk måling af nuværende ctx-kvalitet. Uden baseline er forbedringer uverificerbare.

---

## 8. Samlet Litteraturliste

### Kognitionsvidenskab

- Anderson, M.C., Bjork, R.A. & Bjork, E.L. (1994). Remembering can cause forgetting: Retrieval dynamics in long-term memory. *Journal of Experimental Psychology*, 20(5), 1063-1087.
- Atkinson, R.C. & Shiffrin, R.M. (1968). Human memory: A proposed system and its control processes.
- Born, J. & Wilhelm, I. (2012). System consolidation of memory during sleep. *Psychological Research*, 76(2), 192-203.
- Brodt, S. et al. (2023/2025). Systems memory consolidation during sleep. *Current Opinion in Neurobiology.*
- Chase, W.G. & Simon, H.A. (1973). Perception in chess. *Cognitive Psychology*, 4(1), 55-81.
- Collins, A.M. & Loftus, E.F. (1975). A spreading-activation theory of semantic processing. *Psychological Review*, 82(6), 407-428.
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*, 24(1), 87-114.
- Craik, F.I.M. & Lockhart, R.S. (1972). Levels of processing: A framework for memory research.
- Craik, F.I.M. & Tulving, E. (1975). Depth of processing and the retention of words in episodic memory.
- Diamond, D.M. et al. (2007). The temporal dynamics model of emotional memory processing. *Neural Plasticity.*
- Diekelmann, S. & Born, J. (2023). Sleep — A brain-state serving systems memory consolidation. *Neuron.*
- Ebbinghaus, H. (1885). Über das Gedächtnis.
- Girardeau, G. et al. (2017). Reactivations of emotional memory in the hippocampus-amygdala system during sleep. *Nature Neuroscience*, 20, 1634-1642.
- Gobet, F. & Simon, H.A. (1998). Expert chess memory: Revisiting the chunking hypothesis. *Memory*, 6(3), 225-255.
- Godden, D.R. & Baddeley, A.D. (1975). Context-dependent memory in two natural environments. *British Journal of Psychology*, 66, 325-331.
- Horner, A.J. et al. (2015). Evidence for holistic episodic recollection via hippocampal pattern completion. *Nature Communications*, 6, 7462.
- Klein, G. (1998). *Sources of Power: How People Make Decisions.* MIT Press.
- Kumaran, D., Hassabis, D. & McClelland, J.L. (2016). What learning systems do intelligent agents need? *Trends in Cognitive Sciences*, 20(7), 512-534.
- McClelland, J.L., McNaughton, B.L. & O'Reilly, R.C. (1995). Why there are complementary learning systems in the hippocampus and neocortex. *Psychological Review*, 102(3), 419-457.
- Miller, G.A. (1956). The magical number seven, plus or minus two.
- Müller, G.E. & Pilzecker, A. (1900). Experimentelle Beiträge zur Lehre vom Gedächtnis.
- Murre, J.M.J. & Dros, J. (2015). Replication and analysis of Ebbinghaus' forgetting curve. *PLOS ONE*, 10(7).
- Nader, K. et al. (2000). Fear memories require protein synthesis in the amygdala for reconsolidation after retrieval. *Nature*, 406, 722-726.
- Paivio, A. (1971). *Imagery and Verbal Processes.* Holt, Rinehart & Winston.
- Roediger, H.L. & Karpicke, J.D. (2006). The power of testing memory. *Perspectives on Psychological Science*, 1(3), 181-210.
- Tambini, A. & Davachi, L. (2019). Rehearsal initiates systems memory consolidation, sleep makes it last. *Science Advances*, 5(12).
- Tulving, E. & Thomson, D.M. (1973). Encoding specificity and retrieval processes in episodic memory.

### Spaced Repetition

- FSRS Algorithm (2022-2025). https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm
- Woźniak, P. (1987). SM-2 Algorithm. SuperMemo.

### AI-Hukommelse — Akademiske Papers

- Carbone, P. et al. (2015). Apache Flink: Stream and Batch Processing in a Single Engine. *Bulletin of the IEEE CSTCDE*, 38(4).
- Guo, Z. et al. (2025). A-MEM: Agentic Memory for LLM Agents. arXiv 2502.12110. NeurIPS 2025.
- Hu, C. et al. (2025). Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory. arXiv 2504.19413.
- Kreps, J. et al. (2011). Kafka: a Distributed Messaging System for Log Processing. *Proceedings of the NetDB Workshop.*
- Li, Y. et al. (2025). From Human Memory to AI Memory. arXiv 2504.15965.
- Liu, S. et al. (2026). Memory in the Age of AI Agents: A Survey. arXiv 2512.13564.
- Park, J.S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv 2304.03442.
- Rawal, A. et al. (2025). LightRAG: Simple and Fast Retrieval-Augmented Generation. arXiv 2410.05779.
- Rawal, A. et al. (2026). Agentic Memory (AgeMem). arXiv 2601.01885.
- Rawal, A. et al. (2026). Graph-based Agent Memory. arXiv 2602.05665.
- Rawal, A. et al. (2026). MAGMA: Multi-Graph Agentic Memory Architecture. arXiv 2601.03236.
- Souza, D. et al. (2025). Graphiti: Temporal Knowledge Graph Architecture. arXiv 2501.13956.
- Sundaresan, S. et al. (2024). Infini-attention: Leave No Context Behind. arXiv 2404.07143.
- Ye, J. et al. (2025). Nemori: Episode Segmentation + Distillation. arXiv 2508.03341.
- Zhang, A.L. et al. (2025). Recursive Language Models. arXiv 2512.24601.
- Zhang, R. et al. (2024). Survey on Memory Mechanism for LLM-based Agents. arXiv 2404.13501.
- NEXUSSUM (2025). Hierarchical LLM Agents for Long-Form Summarization. ACL 2025.
- Memoria (2025). Scalable Agentic Memory. arXiv 2512.12686.
- ICLR 2026 Workshop: MemAgents — Memory for LLM-Based Agentic Systems.

### Frameworks og Platforme

- Cognee: https://github.com/topoteretes/cognee
- CrewAI Memory: https://docs.crewai.com/en/concepts/memory
- Google ADK Compaction: https://google.github.io/adk-docs/context/compaction/
- LangMem SDK: https://langchain-ai.github.io/langmem/concepts/conceptual_guide/
- Letta/MemGPT: https://github.com/letta-ai/letta | https://docs.letta.com/concepts/memgpt/
- Mem0: https://github.com/mem0ai/mem0 | https://mem0.ai/
- memsearch (Zilliz): https://github.com/zilliztech/memsearch
- mini-claw: https://github.com/htlin222/mini-claw
- OpenClaw: https://github.com/openclaw/openclaw
- Qdrant: https://qdrant.tech/ | https://qdrant.tech/articles/hybrid-search

### Personlige Data-Pipelines

- Gerasimov, D. / karlicoss (2020). HPI: Human Programming Interface. https://beepb00p.xyz/hpi.html
- Lee, L. / thesephist (2021). Monocle: Universal Personal Search Engine. https://thesephist.com/posts/monocle/
- Willison, S. (2019). Dogsheep: Personal Analytics with Datasette. https://datasette.substack.com/
- Ango, S. / Obsidian CEO. File Over App. https://stephango.com/file-over-app

### Unix og Pipeline-teori

- McIlroy, M.D. et al. (1978). UNIX Time-Sharing System: Foreword. *Bell System Technical Journal*, 57(6).
- Raymond, E.S. (2003). *The Art of Unix Programming.* Addison-Wesley.
- Salus, P.H. (1994). *A Quarter Century of Unix.* Addison-Wesley.

### Regelbaseret NLP

- Honnibal, M. & Montani, I. (2017). spaCy 2. Explosion AI.

### Praktiker-Guides og Blog Posts

- Anthropic (2025). Effective Context Engineering for AI Agents.
- Huang, K. (2026). OpenClaw Design Patterns (Part 1 of 7). Substack.
- Jones, N. (2026). Memory er AI's største uløste problem. YouTube: https://youtu.be/JdJE6_OU3YA
- Manus (2025). Context Engineering for AI Agents.
- Ronacher, A. (2026). Agent Philosophy.
- VelvetShark (2026). OpenClaw Memory Masterclass.

### Industry Reports

- Analytics Vidhya (2025). 73-80% af enterprise RAG-projekter fejler.
- Databricks (2025). Reranking forbedrer op til 48%.
- Stanford (2023). Lost in the Middle: How Language Models Use Long Contexts.

---

*Destilleret 15. marts 2026 fra 12 primærkilder (4.500+ linjer → 500 linjer). Kildefiler bevaret i /root/Yggdra/research/.*
