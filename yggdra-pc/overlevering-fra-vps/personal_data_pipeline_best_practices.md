# Personal Data Pipeline — Best Practices fra Praktikere

**Dato:** 2026-03-15
**Formål:** Actionable teknikker til personligt vidensystem med Qdrant, Python, cron, embeddings.

---

## 1. De Store Navne og Deres Tilgange

### Simon Willison — Datasette + Dogsheep + LLM CLI
Den mest relevante praktiker. Bygger personlige datapipelines med:
- **Dogsheep-arkitektur:** Hvert datakilde → dedikeret `X-to-sqlite` konverter → unified SQLite → faceted search via Datasette
- **`llm` CLI-værktøj:** Kør embeddings + LLM-kald direkte fra terminalen. Modulært, composable, scriptbart.
- **Search-based RAG:** Brug full-text search (FTS5 i SQLite) til at hente kontekst, IKKE kun embeddings. Hybrid > enten-eller.
- **Evals er essentielle:** "Good RAG systems are backed by evals." Test retrieval-kvalitet systematisk.
- **Open-weight modeller:** Brug altid modeller du kan køre selv. Proprietære API'er lukker ned → dine embeddings bliver værdiløse.
- Kilde: simonwillison.net/tags/embeddings, datasette.io

### Karlicoss (Dmitrii Gerasimov) — HPI (Human Programming Interface)
Python-pakke der samler personlig data fra 30+ tjenester:
- **Nøgleprincip:** Data forbliver i kildeformat på disk. HPI normaliserer on-the-fly til Python-objekter.
- **Multi-source merging:** `my.github.all` kombinerer GDPR-eksport + API-data til ét view.
- **Lazy loading + caching:** Skjuler parsing/error-handling. Du arbejder med rene objekter.
- **Timezone-normalisering:** Dedikerede moduler til at fikse timezone-naive timestamps.
- **Ingen central database:** Filer på disk ER databasen. Scripts transformerer on-demand.
- Kilde: github.com/karlicoss/HPI, beepb00p.xyz/pkm-search

### Linus Lee (thesephist) — Monocle Personal Search
Bygget personlig søgemaskine over 10.000+ dokumenter:
- **Modulær ingestion:** Hvert datakilde har eget modul → standardiseret Doc-schema (ID, tokens, tekst, titel, link)
- **Source-level dedup:** Prefix-baserede ID'er (tw- for tweets, etc.) sikrer unikhed
- **Pre-compiled indexes:** Byg indexes ved build-time, IKKE runtime. Hurtigere søgning.
- **Cross-source retrieval:** Søg på tværs af alle kilder samtidig — ingen siloer.
- Kilde: thesephist.com/posts/browser, github.com/thesephist/monocle

### Steph Ango (Obsidian CEO) — File Over App
- **Filformater > apps:** Brug åbne formater (markdown, JSON, plaintext). Apps dør, filer overlever.
- **"If you want your writing still readable in 2060, it must be readable on a computer from 1960."**
- **Lokal-først:** Filer på din harddisk, ikke i skyen.
- Kilde: stephango.com/file-over-app

### Maggie Appleton — Digital Gardens
- **Evergreen notes:** Skriv noter der holder over tid, revider løbende.
- **Daily notes som friktionsfri input:** Lav barriere for at fange viden.
- **Bidirektionale links:** Skab kontekstuelle forbindelser mellem noter.
- Kilde: maggieappleton.com/garden

### Geoffrey Litt — LLM End-User Programming
- **LLM som "lokal udvikler":** Brug AI til at bygge one-off scripts og custom GUIs.
- **Hybrid model:** Direkte manipulation (spreadsheet-stil) + AI til ændringer.
- **Build don't buy:** Skræddersy værktøjer i stedet for generisk SaaS.
- Kilde: geoffreylitt.com/2023/03/25/llm-end-user-programming

---

## 2. Teknikker for Datakvalitet

### Deduplication
| Teknik | Hvornår | Kilde |
|--------|---------|-------|
| Source-prefix ID'er (tw-123, gh-456) | Ved ingestion | Linus Lee/Monocle |
| Content hash (SHA256 af tekst) | Før embedding | Willison |
| Merge fra multiple sources pr. entitet | GDPR + API kombination | Karlicoss/HPI |
| Idempotent upsert med payload-hash | Ved Qdrant insert | Qdrant best practice |

### Data Freshness
- **Timestamp på alle punkter:** Gem `indexed_at` og `source_updated_at` i payload
- **Temporal decay:** Nyere data scorer højere. Formel: `score * (1 / (1 + days_since_update * decay_rate))`
- **Re-embed schedule:** Kør re-indexering på ændrede filer, IKKE alt. Brug filsystem-timestamps.
- **TTL-baseret cleanup:** Slet punkter ældre end X dage for flygtige kilder (chat, notifications)

### Relevance Scoring
- **Hybrid search (vektor + BM25):** Qdrant understøtter det. Reciprocal Rank Fusion (RRF) til at kombinere.
- **Reranking:** Hent 50 kandidater med billig søgning → rerank top-10 med dyrere model (ColBERT, cross-encoder)
- **Kontekstuel embedding:** Tilføj LLM-genereret kontekst til chunks FØR embedding. Dramatisk bedre retrieval.
- **Matryoshka embeddings:** Start med lave dimensioner for grov filtrering → højere dimensioner for reranking.

---

## 3. Best-in-Class Pipeline for Solo Developer + Qdrant

### Arkitektur (inspireret af Dogsheep + HPI + Monocle)

```
KILDER                    INGESTION              STORAGE           RETRIEVAL
─────────────────────────────────────────────────────────────────────────────
Markdown-filer    ─┐
YouTube transcripts─┤  source_module.py  ──→  Qdrant collection
Chat-logs          ─┤  (normalisér til Doc)    + SQLite metadata
Voice memos        ─┤
API-data           ─┘
                         ↓
                    Chunking + Embedding
                    (med kontekst-prefix)
                         ↓
                    Upsert med hash-check
                    (skip uændrede docs)
```

### Konkrete Anbefalinger

**1. Standardisér Doc-format (fra Monocle)**
```python
@dataclass
class Doc:
    id: str          # source_prefix + source_id
    source: str      # "youtube", "markdown", "chat"
    text: str        # ren tekst
    title: str
    url: str | None
    created_at: datetime
    indexed_at: datetime
    content_hash: str  # SHA256 af text
```

**2. Idempotent ingestion (fra HPI)**
```python
def upsert_if_changed(doc: Doc, collection: str):
    existing = qdrant.retrieve(collection, [doc.id])
    if existing and existing[0].payload["content_hash"] == doc.content_hash:
        return  # Skip — uændret
    vector = embed(doc.text)
    qdrant.upsert(collection, [PointStruct(id=doc.id, vector=vector, payload=doc.__dict__)])
```

**3. Hybrid search (fra Qdrant + Willison)**
```python
# Kombiner vektor + sparse (BM25) med Reciprocal Rank Fusion
results = qdrant.query_points(
    collection_name="knowledge",
    prefetch=[
        Prefetch(query=dense_vector, using="dense", limit=50),
        Prefetch(query=sparse_vector, using="sparse", limit=50),
    ],
    query=FusionQuery(fusion=Fusion.RRF),
    limit=10,
)
```

**4. Kontekstuel chunking (fra Willison/Anthropic)**
- Chunk → send til billig LLM med dokumentets titel/kontekst → få 1-2 sætningers kontekst → prepend til chunk → embed
- Koster lidt ekstra men løfter retrieval-kvalitet markant

**5. Temporal decay i scoring**
```python
def apply_decay(results, decay_rate=0.01):
    now = datetime.now()
    for r in results:
        age_days = (now - r.payload["created_at"]).days
        r.score *= 1 / (1 + age_days * decay_rate)
    return sorted(results, key=lambda r: r.score, reverse=True)
```

---

## 4. Automationsmønstre

### Self-Healing Pipelines
- **Retry med exponential backoff:** Alle API-kald. Max 3 forsøg.
- **Dead letter queue:** Fejlede docs → `data/failed_ingestion.jsonl` → retry ved næste kørsel.
- **Health check i cron:** Tjek Qdrant er op + collection count stabil. Alert ved >10% fald.
- **Idempotens overalt:** Ethvert script kan køres N gange med samme resultat.

### Mini-Agenter (fra Willison + Litt)
- **One-off scripts via LLM:** Brug Claude/LLM til at generere engangscripts til datarensning.
- **Scheduled summarization:** Cron → hent nye docs → destillér med Groq/Haiku → gem i episodes.
- **Proaktiv retrieval:** Morning brief-script søger automatisk efter relevante docs baseret på dagens kalender/tasks.

### Cron-Strategi
```
# Tier 1: Real-time (hvert 5-15 min)
*/15 * * * *  heartbeat.py          # Tjek systemstatus

# Tier 2: Daglig (morgen)
0 7 * * *     morning_brief.py      # Daglig briefing
0 6 * * *     ingest_new_sources.py  # Indexér nye filer

# Tier 3: Ugentlig
0 3 * * 0     reindex_changed.py    # Re-embed ændrede docs
0 4 * * 0     cleanup_stale.py      # Fjern forældede vektorer
```

---

## 5. Anti-Patterns (fra praktikerne)

1. **Embed ALDRIG alt på én gang.** Inkrementel ingestion med hash-check. (Willison)
2. **Stol ALDRIG kun på vektor-søgning.** Hybrid search (vektor + keyword) slår begge alene. (Qdrant, Willison)
3. **Brug ALDRIG kun én embedding-model.** Hold modellen udskiftelig. Gem model-navn i metadata. (Willison)
4. **Byg ALDRIG monolitisk.** Hvert datakilde = eget script/modul. Composable > monolitisk. (Dogsheep, HPI)
5. **Ignorer ALDRIG timestamps.** Temporal metadata er kritisk for relevans. (HPI, Monocle)
6. **Test ALDRIG RAG uden evals.** Lav 20-30 test-queries med forventede svar. Mål precision@5. (Willison)

---

## 6. Direkte Relevans for Yggdra

### Allerede gjort rigtigt
- File-over-app (markdown, JSON på disk) ✓
- Python scripts, composable ✓
- Qdrant med embeddings ✓
- Cron-baseret automation ✓

### Mangler / Næste Skridt
1. **Hybrid search i Qdrant** — tilføj sparse vectors (BM25) til eksisterende collections
2. **Content hash ved upsert** — undgå re-embedding af uændrede docs
3. **Temporal decay** — implementér i `ctx`-søgning
4. **Standardisér Doc-format** — ensartet payload-struktur på tværs af alle collections
5. **Eval-suite** — 20-30 test-queries der kører ugentligt og måler retrieval-kvalitet
6. **Kontekstuel chunking** — prepend kontekst til chunks før embedding
7. **Dead letter queue** — fang fejlede ingestions i stedet for at miste dem stille

---

*Kilder: Simon Willison (simonwillison.net), Karlicoss/HPI (github.com/karlicoss/HPI), Linus Lee/Monocle (thesephist.com), Steph Ango (stephango.com), Maggie Appleton (maggieappleton.com), Geoffrey Litt (geoffreylitt.com), Qdrant (qdrant.tech/articles/hybrid-search), beepb00p.xyz/pkm-search*
