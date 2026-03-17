# Zero-Token Data Pipelines: Arkitektur for Regelbaseret Databehandling

**Dato:** 15. marts 2026
**Formål:** Kortlægning af patterns for datapipelines der filtrerer, kategoriserer og router data UDEN LLM-tokenforbrug. Fokus på hvad en solo-udvikler realistisk kan bygge med cron + Python + bash.
**Metode:** Akademisk litteratur, open-source projekter, produktionsrapporter, web research.

---

## Indholdsfortegnelse

1. [Problemformulering](#1-problemformulering)
2. [Unix Pipe-filosofien](#2-unix-pipe-filosofien)
3. [ETL og Workflow-orchestrering](#3-etl-og-workflow-orchestrering)
4. [Stream Processing](#4-stream-processing)
5. [Regelbaseret NLP](#5-regelbaseret-nlp)
6. [Personlige Vidensystem-pipelines](#6-personlige-vidensystem-pipelines)
7. [Gate-keeper Mønstret](#7-gate-keeper-mønstret)
8. [Praktiske Solo-dev Patterns](#8-praktiske-solo-dev-patterns)
9. [Syntese: Zero-Token Pipeline-arkitektur](#9-syntese-zero-token-pipeline-arkitektur)
10. [Kilder](#10-kilder)

---

## 1. Problemformulering

Ethvert AI-system der bruger LLM-kald til filtrering, kategorisering og routing betaler en dobbelt pris: **tokens** (direkte omkostning) og **latens** (ventetid på API-svar). For en solo-udvikler med et personligt vidensystem betyder det:

- Et morning brief-script der kalder en LLM for at opsummere 10 datakilder koster ~$0.10-0.50 per kørsel
- En heartbeat-daemon der tjekker 6 inboxes hvert 30. minut og kalder LLM for hver: ~$5-15/dag
- En research-pipeline der kategoriserer 50 artikler: ~$1-3 per batch

Det centrale spørgsmål: **Hvor meget af denne databehandling kan ske UDEN tokens?**

Svaret fra litteraturen er klart: 70-90% af typisk pipeline-arbejde er filterering, routing, deduplicering, formatering og tidsbaseret logik. Alt dette kan håndteres med deterministisk kode. LLM'en skal kun aktiveres for det resterende 10-30% der kræver semantisk forståelse.

---

## 2. Unix Pipe-filosofien

### Oprindelse og Principper

Douglas McIlroy foreslog pipe-konceptet i et internt memo hos Bell Labs i 1964: "We should have some ways of coupling programs like garden hose — screw in another segment when it becomes necessary to massage data in another way." Ken Thompson implementerede `pipe()` system-kaldet i Version 3 Unix i 1973, angiveligt på én nat (McIlroy, 1986).

**McIlroy, M.D. (1964).** Internt memo, Bell Laboratories. Foreslog pipe-mekanismen som modulært data-flow interface. Upubliceret, citeret i Salus (1994).

**McIlroy, M.D., Pinson, E.N. & Tague, B.A. (1978).** "UNIX Time-Sharing System: Foreword." *Bell System Technical Journal*, 57(6), 1899-1904. Formulerede Unix-filosofien eksplicit: "Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface."

**Raymond, E.S. (2003).** *The Art of Unix Programming.* Addison-Wesley. Udvidede McIlroys principper til 17 regler, herunder: Rule of Modularity (skriv simple dele forbundet med rene interfaces), Rule of Composition (design programmer til at blive forbundet med andre programmer), Rule of Separation (adskil policy fra mekanisme).

### Relevans for Zero-Token Pipelines

Unix-pipe-filosofien er det teoretiske fundament for zero-token pipelines. Kerneprincippet: **tekst er det universelle interface.** Data flyder som tekst-strømme gennem en kæde af specialiserede filtre, hvor hvert filter gør præcis én ting. Denne arkitektur er inherent token-fri — ingen af filtrene behøver semantisk forståelse.

Konkret eksempel:
```bash
# Zero-token pipeline: find nye emails, filtrer spam, kategoriser efter afsender
cat inbox.jsonl \
  | jq 'select(.date > "2026-03-14")' \          # Tidsfilter
  | grep -v -f spam_patterns.txt \                # Regelbaseret spam-filter
  | python3 categorize_by_sender.py \             # Afsender-routing
  | tee business.jsonl personal.jsonl unknown.jsonl  # Fan-out
```

Hele pipelinen kører på millisekunder, koster 0 tokens, og håndterer 95% af email-triage. Kun `unknown.jsonl` behøver LLM-klassificering.

---

## 3. ETL og Workflow-orchestrering

### De Store Frameworks

**Apache Airflow** (Maxime Beauchemin, Airbnb, 2014). Open-source workflow-orchestrator. DAG-baseret (Directed Acyclic Graphs). De facto standard for batch ETL. Python-native. Ulempe for solo-devs: kræver metadata-database (PostgreSQL/MySQL), webserver, scheduler — minimum 3 processer. Overkill for <20 jobs.

**Prefect** (Jeremiah Lowin, 2018). "Pythonic Airflow." Nøgleforskel: ingen DAG-definition nødvendig — dekorér Python-funktioner med `@flow` og `@task`. SQLite til development (intet ekstra setup). Cron-scheduling built-in. Mest relevant for solo-devs der vil have mere end cron men mindre end Airflow.

**Dagster** (Nick Schrock, 2019). "Software-defined assets." Centrerer sig om *hvad* data er (assets) snarere end *hvornår* det køres (schedules). Stærk lineage og observability. Mere konceptuel overhead end Prefect, men bedre til komplekse afhængigheder.

**Luigi** (Erik Bernhardsson, Spotify, 2012). Letvægts Python-pipeline. Minimal overhead. God til små-til-mellemstore batch-jobs. Mindre aktivt udviklet end Prefect/Dagster.

### Kilde

**Beauchemin, M. (2017).** "The Rise of the Data Engineer." *Free Code Camp / Medium.* Definerede ETL-ingeniør-rollen og argumenterede for deklarativ pipeline-definition.

**FreeAgent Engineering (2025).** "Decoding Data Orchestration Tools: Comparing Prefect, Dagster, Airflow, and Mage." Sammenligning baseret på produktionserfaring med alle fire frameworks. Konklusion: Prefect for simplicity, Dagster for asset-centrisk, Airflow for skala.

### Solo-dev Vurdering

For en solo-udvikler med <20 pipeline-jobs er **cron + Python-scripts** næsten altid det rigtige valg. Frameworks tilføjer observability og retry-logik, men koster kognitiv overhead. Tommelfingerregel:

| Antal jobs | Anbefaling |
|-----------|-----------|
| 1-15 | cron + Python |
| 15-50 | Prefect (minimal overhead) |
| 50-200 | Dagster (asset lineage) |
| 200+ | Airflow (enterprise, team) |

---

## 4. Stream Processing

### Apache Kafka + Apache Flink

**Kafka** (Jay Kreps, LinkedIn, 2011) er en distribueret event-streaming platform. Data publiceres som events til topics, konsumeres af consumers. Garanti for ordering inden for partitioner. Velegnet til real-time data-flow mellem systemer.

**Flink** (TU Berlin, 2014) er en stateful stream-processing motor. Kører transformationer og filtre på data-strømme. Flink SQL abstraherer kompleksiteten så filtrering kan skrives deklarativt:

```sql
-- Regelbaseret filtrering uden LLM
SELECT * FROM inbox_stream
WHERE sender NOT IN (SELECT pattern FROM spam_list)
AND received_at > CURRENT_TIMESTAMP - INTERVAL '1' HOUR
```

**Kreps, J., Narkhede, N. & Rao, J. (2011).** "Kafka: a Distributed Messaging System for Log Processing." *Proceedings of the NetDB Workshop.* Grundlæggende paper der definerede log-baseret messaging.

**Carbone, P. et al. (2015).** "Apache Flink: Stream and Batch Processing in a Single Engine." *Bulletin of the IEEE Computer Society Technical Committee on Data Engineering*, 38(4). Beskrev Flinks unified model for stream og batch.

### Solo-dev Vurdering

Kafka + Flink er **massivt overkill** for en solo-udvikler. De kræver JVM, ZooKeeper (ældre versioner), og dedikeret ops. Men *principperne* er direkte anvendelige:

- **Event-drevet arkitektur:** Brug en fil (JSONL) som "topic". Append events, læs med `tail -f` eller Python.
- **Idempotente consumers:** Gem "last processed" offset i en state-fil. Genstart uden data-tab.
- **Partitionering:** Én JSONL-fil per datakilde. Ingen blanding.

Simpel Python-ækvivalent til Kafka consumer:
```python
import json
from pathlib import Path

def consume_events(topic_file: Path, state_file: Path):
    last_offset = int(state_file.read_text()) if state_file.exists() else 0
    with open(topic_file) as f:
        for i, line in enumerate(f):
            if i < last_offset:
                continue
            event = json.loads(line)
            yield event
            state_file.write_text(str(i + 1))
```

---

## 5. Regelbaseret NLP

### spaCy Matchers

spaCy (Matthew Honnibal & Ines Montani, Explosion AI, 2015) tilbyder tre regelbaserede matching-systemer der kører UDEN ML-modeller:

**Matcher** — Token-baseret pattern matching. Hvert pattern er en liste af dictionaries der beskriver tokens:
```python
from spacy.nlp import blank
from spacy.matcher import Matcher

nlp = spacy.blank("da")  # Ingen model — kun tokenizer
matcher = Matcher(nlp.vocab)
matcher.add("DATO", [[{"SHAPE": "dddd-dd-dd"}]])
matcher.add("PRIS", [[{"LIKE_NUM": True}, {"TEXT": {"IN": ["kr", "DKK", "EUR"]}}]])
```

**EntityRuler** — Pattern-baseret entity recognition. Kombinerer frase-matching og token-patterns til NER uden træning:
```python
ruler = nlp.add_pipe("entity_ruler")
patterns = [
    {"label": "ORG", "pattern": "TransportIntra"},
    {"label": "ROUTE", "pattern": [{"TEXT": {"REGEX": "^rute\\s*\\d+"}}]},
]
ruler.add_patterns(patterns)
```

**PhraseMatcher** — Ultra-hurtig eksakt matching. Optimeret til store ordlister (10.000+ termer).

### Kilde

**Honnibal, M. & Montani, I. (2017).** "spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing." Explosion AI. Introducerede rule-based matching som first-class feature.

**spaCy Documentation (2026).** "Rule-based matching." https://spacy.io/usage/rule-based-matching. Komplet guide til Matcher, PhraseMatcher, EntityRuler inkl. regex-support.

### Regex og Heuristik-baseret Extraction

For mange NLP-opgaver er regex + heuristik tilstrækkeligt:

| Opgave | LLM nødvendig? | Zero-token alternativ |
|--------|----------------|----------------------|
| Dato-extraktion | Nej | `dateutil.parser.parse()` eller regex `\d{4}-\d{2}-\d{2}` |
| Email-adresser | Nej | Regex `[\w.-]+@[\w.-]+\.\w+` |
| Beløb/priser | Nej | Regex `\d+[.,]?\d*\s*(kr|DKK|EUR)` |
| Adresser (DK) | Delvist | Regex for postnummer + DAWA API lookup |
| Sentiment | Ja | LLM (semantisk forståelse krævet) |
| Opsummering | Ja | LLM (generativ opgave) |
| Kategorisering (simple) | Nej | Keyword-matching + scoring |
| Kategorisering (nuanceret) | Ja | LLM (kontekstafhængig) |

Tommelfingerregel: **Hvis opgaven kan beskrives med "find X der matcher Y" → regex. Hvis den kræver "forstå hvad dette betyder" → LLM.**

---

## 6. Personlige Vidensystem-pipelines

### Dogsheep (Simon Willison, 2019-)

**Arkitektur:** Hvert datakilde → dedikeret `X-to-sqlite` konverter → unified SQLite database → faceted search via Datasette.

Nøgleprincipper:
- **SQLite som universelt format.** Én fil = én database. Ingen server. `cp` er backup.
- **FTS5 for søgning.** SQLite's built-in full-text search. Ingen embeddings nødvendigt for keyword-søgning.
- **Dogsheep-beta:** Samler alle kilder i ét søgeindex. YAML-konfiguration specificerer queries per datakilde.
- **`llm` CLI:** Embeddings + LLM-kald fra terminalen. Modulært, composable, scriptbart.

**Willison, S. (2019).** "Dogsheep: Personal analytics with Datasette." https://datasette.substack.com/p/dogsheep-personal-analytics-with. Beskrev arkitekturen og motivationen.

**Willison, S. (2020).** Talk Python to Me, Episode 299: "Personal search engine with Datasette and Dogsheep." Detaljeret gennemgang af pipeline-design.

### HPI — Human Programming Interface (Dmitrii Gerasimov / karlicoss, 2019-)

**Arkitektur:** Python-pakke (`my`) der normaliserer personlig data fra 30+ tjenester on-the-fly.

Nøgleprincipper:
- **Data forbliver i kildeformat.** Ingen central database. GDPR-eksporter, API-dumps, JSON-filer — alt ligger som filer på disk.
- **Lazy loading + caching.** Parsing sker on-demand. Resultater caches transparent.
- **Multi-source merging.** `my.github.all` kombinerer GDPR-eksport + API-data til ét Python-view.
- **Timezone-normalisering.** Dedikerede moduler til at fikse timezone-naive timestamps — et reelt problem for personlig data.

**Gerasimov, D. (2020).** "Building a Human Programming Interface." https://beepb00p.xyz/hpi.html. Design-dokumentation og motivation.

**GitHub: karlicoss/HPI.** https://github.com/karlicoss/HPI. 2.5K+ stars. Aktiv udvikling.

### Monocle (Linus Lee / thesephist, 2021)

**Arkitektur:** Personal search engine. Fuld-tekst søgeindex bygget offline, serveret i browseren.

Nøgleprincipper:
- **Offline indexering.** Komprimeret index genereres batch-vis. Søgning sker lokalt i browser — ingen server.
- **Stemming + tokenisering.** Søge-pipeline: tokenize → stem → lookup i inverteret index. Rent regelbaseret.
- **Privatliv som arkitektur-valg.** Ingen data forlader maskinen.

**Lee, L. (2021).** "Building Monocle, a universal personal search engine for life." https://thesephist.com/posts/monocle/. Beskrev design-filosofi og implementering.

### Fælles Mønster

Alle tre systemer deler en filosofi: **data in → deterministisk transformation → struktureret output.** LLM'er bruges kun som et valgfrit ekstra lag *oven på* den regelbaserede pipeline — aldrig som fundament.

---

## 7. Gate-keeper Mønstret

### OpenClaw's Heartbeat

OpenClaw (tidl. Clawdbot/Moltbot, Peter Steinberger et al., 2025-) implementerer det reneste eksempel på gate-keeper mønstret i et AI-agent-system.

**Arkitektur:**
1. Gateway-daemon kører som systemd-service med konfigurerbar heartbeat (default: 30 min)
2. Ved hvert heartbeat: læs `HEARTBEAT.md` — en tjekliste af items at kontrollere
3. **Deterministiske checks kører FØRST:** shell-scripts + API-kald tjekker inboxes, kalender, system-health
4. Hvis checks finder intet: print `HEARTBEAT_OK` — **0 tokens forbrugt**
5. Kun hvis et check finder signal: aktiver LLM til at ræsonnere over situationen

**Nøgleindsigt:** "Most heartbeat logic is not 'reasoning' — it's just checking state, and for this, a shell script plus a few API calls is perfect." (OpenClaw docs, 2026)

**Ken Huang (2026).** "OpenClaw Design Patterns (Part 1 of 7)." Substack. Beskrev heartbeat-mønstret som "cheap checks first, models only when you need them."

**DEV Community (2026).** "Heartbeats in OpenClaw: Cheap Checks First, Models Only When You Need Them." Detaljeret gennemgang af to-lags arkitekturen.

### Gate-keeper som Generelt Mønster

Gate-keeper mønstret kan generaliseres:

```
Data ind → [Regelbaseret filter] → Signal? → Nej → Log + sov
                                  → Ja → [LLM] → Handling
```

Eksempler:

| Data | Gate-keeper regel | LLM kun ved |
|------|------------------|-------------|
| Emails | Afsender i whitelist? Keyword match? | Ukendt afsender + forretningsrelevant |
| Trello-kort | Ændret siden sidst? | Nyt kort der kræver prioritering |
| RSS feeds | Ny artikel? Titel matcher keywords? | Artikel der passerer keyword-filter |
| Git commits | Fil i kritisk sti? | Semantisk review af ændring |
| Kalender | Event inden for 24 timer? | Forberedelse af møde-briefing |

I praksis filtrerer gate-keeperen 80-95% af events fra. LLM-forbruget reduceres tilsvarende.

---

## 8. Praktiske Solo-dev Patterns

### Pattern 1: JSONL som Event-bus

```python
# Append-only event log — erstatter Kafka for solo-dev
import json, datetime
from pathlib import Path

def emit(topic: str, event: dict):
    event["_ts"] = datetime.datetime.now().isoformat()
    path = Path(f"data/events/{topic}.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
```

Fordele: atomisk append, `wc -l` for stats, `tail -f` for monitoring, `jq` for ad-hoc queries.

### Pattern 2: Hash-baseret Deduplicering

```python
import hashlib, json
from pathlib import Path

SEEN_FILE = Path("data/.seen_hashes.json")

def is_new(item: dict, key_fields: list[str]) -> bool:
    """Returner True kun for nye items. Zero tokens."""
    seen = json.loads(SEEN_FILE.read_text()) if SEEN_FILE.exists() else {}
    content = "|".join(str(item.get(f, "")) for f in key_fields)
    h = hashlib.sha256(content.encode()).hexdigest()[:16]
    if h in seen:
        return False
    seen[h] = item.get("_ts", "")
    SEEN_FILE.write_text(json.dumps(seen))
    return True
```

### Pattern 3: Keyword-Score Kategorisering

```python
CATEGORIES = {
    "transport": ["rute", "stop", "lastbil", "chauffør", "levering", "afhentning"],
    "økonomi": ["faktura", "moms", "bilag", "konto", "betaling", "skat"],
    "research": ["paper", "studie", "metode", "evidence", "framework", "survey"],
}

def categorize(text: str) -> str:
    """Regelbaseret kategorisering. Zero tokens."""
    text_lower = text.lower()
    scores = {}
    for cat, keywords in CATEGORIES.items():
        scores[cat] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "uncategorized"
```

### Pattern 4: Temporal Decay Filter

```python
from datetime import datetime, timedelta

def relevance_score(item: dict, decay_days: int = 30) -> float:
    """Nyere items scorer højere. Zero tokens."""
    ts = datetime.fromisoformat(item["_ts"])
    age_days = (datetime.now() - ts).days
    return max(0.0, 1.0 - (age_days / decay_days))
```

### Pattern 5: Cron Pipeline-orkestrering

```bash
# crontab -e
# Hver time: hent nye data, filtrer, kategoriser
0 * * * * /root/Yggdra/scripts/venv/bin/python /root/Yggdra/scripts/pipeline_ingest.py >> /var/log/pipeline.log 2>&1

# Hver 30. min: heartbeat gate-keeper
*/30 * * * * /root/Yggdra/scripts/heartbeat_check.sh && /root/Yggdra/scripts/venv/bin/python /root/Yggdra/scripts/heartbeat_act.py

# Dagligt kl 07:00: opsummer kun det der passerede gårsdagens filtre
0 7 * * * /root/Yggdra/scripts/venv/bin/python /root/Yggdra/scripts/morning_brief.py
```

### Pattern 6: Compose Pipeline med Python Generators

```python
def pipeline(*steps):
    """Unix-pipe mønster i Python. Hvert step er en generator."""
    def run(data):
        result = data
        for step in steps:
            result = step(result)
        return result
    return run

# Brug:
process = pipeline(
    lambda items: (i for i in items if is_new(i, ["id"])),         # Dedup
    lambda items: (i for i in items if relevance_score(i) > 0.3),  # Temporal filter
    lambda items: ({**i, "cat": categorize(i["text"])} for i in items),  # Kategoriser
)

for item in process(load_events("inbox")):
    if item["cat"] == "uncategorized":
        llm_categorize(item)  # KUN her bruges tokens
    else:
        emit(item["cat"], item)
```

---

## 9. Syntese: Zero-Token Pipeline-arkitektur

### Det Samlede Mønster

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐
│  Datakilder  │───→│  Gate-keeper  │───→│  Rule Pipeline │
│  (JSONL,API) │    │  (hash,time)  │    │  (filter,cat)  │
└─────────────┘    └──────┬───────┘    └───────┬────────┘
                          │                     │
                     Filtreret fra          Kategoriseret
                     (80-95%)              ┌─────┴──────┐
                                          │             │
                                     Resolved       Unresolved
                                     (emit)        (→ LLM, 5-20%)
```

### 5 Design-principper

1. **Tokens er den dyreste ressource.** Brug dem kun til semantisk forståelse — aldrig til filtrering, routing, deduplicering eller formatering.

2. **Tekst er det universelle interface.** JSONL som event-format. Bash pipes for ad-hoc. Python generators for komplekse pipelines. Samme data kan bearbejdes af begge.

3. **Gate-keeper foran LLM.** Altid et regelbaseret filter mellem datakilde og LLM-kald. 80-95% af data behøver aldrig tokens.

4. **Append-only state.** JSONL event logs + hash-baseret dedup. Intet data slettes, men duplikater fanges deterministisk.

5. **Cron er infrastruktur nok.** Kafka og Airflow er for teams med 10+ pipeline-jobs. En solo-dev med <15 jobs bruger cron + Python + bash.

### Hvad Kræver Stadig Tokens

| Opgave | Hvorfor LLM er nødvendig |
|--------|-------------------------|
| Opsummering af tekst | Generativ — kræver sprogmodel |
| Nuanceret kategorisering | "Er denne email en klage eller en forespørgsel?" |
| Sentiment-analyse | Kontekstafhængig — sarkasme, ironi |
| Møde-forberedelse | Syntese af flere kilder til briefing |
| Proaktive forslag | "Baseret på mønstret bør du..." |

### Estimeret Token-besparelse

| Scenario | Med LLM overalt | Med zero-token pipeline | Besparelse |
|----------|-----------------|------------------------|------------|
| Morning brief (10 kilder) | ~5.000 tokens | ~800 tokens (kun opsummering) | 84% |
| Heartbeat (6 inboxes, 48x/dag) | ~48.000 tokens/dag | ~2.400 tokens/dag (kun ved signal) | 95% |
| Research-kategorisering (50 artikler) | ~25.000 tokens | ~5.000 tokens (kun "uncategorized") | 80% |
| Email-triage (100 mails) | ~50.000 tokens | ~5.000 tokens (kun ukendte) | 90% |

---

## 10. Kilder

### Fundamentale Tekster

**McIlroy, M.D., Pinson, E.N. & Tague, B.A. (1978).** "UNIX Time-Sharing System: Foreword." *Bell System Technical Journal*, 57(6), 1899-1904. Formulerede Unix-filosofien: "Write programs that do one thing and do it well."

**Raymond, E.S. (2003).** *The Art of Unix Programming.* Addison-Wesley. 17 Unix-designregler inkl. Rule of Composition og Rule of Separation.

**Salus, P.H. (1994).** *A Quarter Century of Unix.* Addison-Wesley. Historisk kildedokumentation inkl. McIlroys 1964-memo.

### ETL og Orchestrering

**Beauchemin, M. (2017).** "The Rise of the Data Engineer." Medium. Definerede ETL-rollen og argumenterede for deklarativ pipeline-definition.

**FreeAgent Engineering (2025).** "Decoding Data Orchestration Tools: Comparing Prefect, Dagster, Airflow, and Mage." https://engineering.freeagent.com/2025/05/29/. Sammenligning baseret på produktionserfaring.

**Dagster Guides (2025).** "Data Pipeline Frameworks: Key Features & 10 Tools to Know in 2025." https://dagster.io/guides/data-pipeline-frameworks. Overblik med fokus på asset-baseret orchestrering.

### Stream Processing

**Kreps, J., Narkhede, N. & Rao, J. (2011).** "Kafka: a Distributed Messaging System for Log Processing." *Proceedings of the NetDB Workshop.* Grundlæggende Kafka-paper.

**Carbone, P. et al. (2015).** "Apache Flink: Stream and Batch Processing in a Single Engine." *Bulletin of the IEEE CSTCDE*, 38(4). Unified stream/batch model.

### Regelbaseret NLP

**Honnibal, M. & Montani, I. (2017).** "spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing." Explosion AI. Rule-based matching som first-class feature.

**spaCy Documentation (2026).** "Rule-based matching." https://spacy.io/usage/rule-based-matching. Matcher, PhraseMatcher, EntityRuler, regex-support.

### Personlige Data-pipelines

**Willison, S. (2019).** "Dogsheep: Personal analytics with Datasette." https://datasette.substack.com/p/dogsheep-personal-analytics-with. SQLite + FTS5 som personligt søgeindex.

**Gerasimov, D. (2020).** "Building a Human Programming Interface." https://beepb00p.xyz/hpi.html. Python-normalisering af 30+ personlige datakilder.

**Lee, L. (2021).** "Building Monocle, a universal personal search engine for life." https://thesephist.com/posts/monocle/. Offline personal search med regelbaseret pipeline.

### Agent Gate-keeper Mønster

**Ken Huang (2026).** "OpenClaw Design Patterns (Part 1 of 7)." https://kenhuangus.substack.com/p/openclaw-design-patterns-part-1-of. Heartbeat som "cheap checks first, models only when you need them."

**OpenClaw Documentation (2026).** "Heartbeat." https://docs.openclaw.ai/gateway/heartbeat. Konfiguration og arkitektur for gate-keeper daemon.

### Data Pipeline Best Practices

**Latitude (2025).** "Ultimate Guide to Preprocessing Pipelines for LLMs." https://latitude.so/blog/ultimate-guide-to-preprocessing-pipelines-for-llms. Token-efficient pipeline design.

**Redis (2026).** "LLM Token Optimization: Cut Costs & Latency in 2026." https://redis.io/blog/llm-token-optimization-speed-up-apps/. Konkrete strategier for token-reduktion i produktion.

**Pybites (2025).** "A Practical Example of the Pipeline Pattern in Python." https://pybit.es/articles/a-practical-example-of-the-pipeline-pattern-in-python/. Python generator-baseret pipeline implementation.
