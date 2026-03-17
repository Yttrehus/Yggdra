# Qdrant Legacy Collections — Migration Audit

**Dato:** 2026-03-16
**Metode:** REST API sampling (5-10 points per collection), metadata-analyse, overlap-check

## Overblik

| Collection | Points | Dim | Content Type | Anbefaling |
|---|---|---|---|---|
| sessions | 43,511 | 1536 | Tmux/Claude session chunks | DELETE |
| advisor_brain | 453 | 1536 | Nate Jones + Miessler + Practitioner Bible | KEEP AS-IS |
| docs | 1,466 | 1536 | docs/ + research/ markdown chunks | MIGRATE TO KNOWLEDGE |
| miessler_bible | 102 | 1536 | danielmiessler.com blog posts | KEEP AS-IS |
| conversations | 81 | 1536 | Tidlige chatlog-beskeder | DELETE |
| **knowledge** | **984** | 1536 | PC-ingesteret research + projekter | NY — beholdes |
| **episodes** | **59** | 1536 | Voice memos, chatlogs, session plans | NY — beholdes |
| routes | 40,053 | 1536 | TransportIntra rutedata | KEEP AS-IS (separat domæne) |

**Total:** 86,649 points. Anbefalet efter migration: ~42,074 points (-51%).

---

## 1. sessions (43,511 points) — ANBEFALING: DELETE

### Indhold
Chunked tmux session logs og Claude Code session JSONL-filer. Hvert punkt har:
- `summary` — Groq/Haiku-genereret opsummering af en chunk
- `raw_preview` — rå terminal-output (inkl. ANSI-koder, kode-diffs, noise)
- `date` — session-dato (2026-01-28 til 2026-02-23)
- `source` — `tmux_session` (91%) eller `claude_code` (9%)
- `source_file` — logfilnavn (tmux-YYYY-MM-DD.log eller UUID.jsonl)
- `chunk_index`, `processed_at`

### Kvalitet
**Lav.** 27% af stikprøven har `SKIP` som summary (= ren noise/ANSI-koder). De resterende summaries er overfladiske ("Docker genstartet", "kode-diff uden kontekst"). Raw previews indeholder terminalkontrol-sekvenser der er ubrugelige som søgeresultater.

### Overlap med knowledge/episodes
**Minimal direkte overlap.** Knowledge indeholder PC-ingesterede research-filer (helt andre kilder). Episodes indeholder destillerede chatlogs og voice memos fra marts 2026. Sessions dækker jan-feb 2026 terminal-output — men den information der var vigtig er allerede fanget i DAGBOG.md, MEMORY.md og episodes.jsonl.

### Begrundelse for DELETE
- 43K points bruger ~67% af al Qdrant-storage
- Summaries er maskinelt genererede af billig-modeller og overfladiske
- Raw previews er terminal-noise, ikke søgbar viden
- Vigtig information fra disse sessioner er allerede destilleret til DAGBOG.md, MEMORY.md, episodes.jsonl
- `ctx`-søgninger mod sessions returnerer primært noise

---

## 2. advisor_brain (453 points) — ANBEFALING: KEEP AS-IS

### Indhold
Chunked tekst fra tre syntetiske "bøger" sammensat af rådgiver-indhold:
- **"The Builder's Edge"** (author: `nate_jones`) — Nate Jones' YouTube-videoer destilleret til bogkapitler
- **"Become Yourself"** (author: `miessler`) — Daniel Miessler blog/YouTube destilleret til bog
- **"AI Practitioner's Bible"** (author: `practitioner_bible`) — Kris-specifik syntese af begge + egne erfaringer

Payload-felter: `type` (advisor_content), `author`, `book`, `chapter`, `section`, `text`, `content` (preview)

### Kvalitet
**Høj.** Velstruktureret, manuelt kurateret indhold. Kapitler og sektioner giver god kontekst. Content er indholdsmæssigt rigt — AI-arkitektur, prompt engineering, RAG, automation, sikkerhed, filosofi.

### Overlap med knowledge/episodes
**Ingen.** Knowledge indeholder ingen advisor-relaterede filer. Advisor_brain er den eneste kilde til dette destillerede rådgiver-materiale.

### Begrundelse for KEEP
- Unik, høj-kvalitets vidensbase der bruges aktivt via `ctx --advisor`
- Ingen duplikering andre steder
- 453 points er minimalt storage-forbrug
- Velstrukturerede metadata muliggør filtrering på author/book/chapter

---

## 3. docs (1,466 points) — ANBEFALING: MIGRATE TO KNOWLEDGE

### Indhold
Markdown-filer fra `/docs/` og `/research/` embeddet med header-baseret chunking:
- **Type `documentation`** (21 filer): DAGBOG, KRIS_PROFILE, GDRIVE_OVERBLIK, PC_SETUP, TRANSPORTINTRA_PROFIL, ATLAS, div. audits
- **Type `research`** (50 filer): HOW_TO_BUILD_AGENTS, academic_writing, agent_architectures, claude_code_ecosystem, memory research, whisper pricing, m.fl.

Payload-felter: `source` (docs:FILE eller research:FILE), `type`, `file`, `header`, `content`, `summary`

### Kvalitet
**Medium-høj.** Indholdet er reelt og nyttigt. Chunking er header-baseret (bedre end sessions' vilkårlige chunking). Men mange filer er fra feb 2026 og kan være forældede.

### Overlap med knowledge/episodes
**Indirekte.** Knowledge (PC) indeholder 53 filer — ingen direkte fil-navne-overlap med docs. Men tematisk overlap er sandsynligt (context engineering, agent architectures, research methodology eksisterer begge steder i forskellige versioner).

### Begrundelse for MIGRATE
- Indholdet er værdifuldt men bør re-embeddes med knowledge-collectionens nyere pipeline (UUID-baserede IDs, content_hash, confidence-felter, created_at/indexed_at timestamps)
- Docs bruger numeriske IDs og ældre payload-format — inkompatibelt med knowledge-pipelinen
- Efter migration: docs kan slettes, og `ctx` kun søger i knowledge + advisor_brain
- Migration giver mulighed for at fjerne forældede filer og opdatere med nyeste versioner

---

## 4. miessler_bible (102 points) — ANBEFALING: KEEP AS-IS

### Indhold
Blog posts fra danielmiessler.com, scraped via VitePress API:
- 102 chunks fra blogposts dateret 2025-08-01 til 2026-01-17
- Emner: AI, cybersecurity, business, creativity, philosophy, prompt injection, Claude Code

Payload-felter: `title`, `date`, `url`, `tags` (pipe-separerede), `source` (blog), `chunk_index`, `total_chunks`, `file`, `text`, `embedded_at`

### Kvalitet
**Høj.** Originalt kildemateriale med gode metadata (URL, dato, tags). Chunking er per-blogpost med chunk_index.

### Overlap med knowledge/episodes
**Ingen.** Knowledge indeholder ingen Miessler blog-posts. Advisor_brain indeholder destillerede versioner, men miessler_bible har original-teksten.

### Begrundelse for KEEP
- Unik kilde — original blog-tekster (ikke destillerede)
- Komplementerer advisor_brain (original vs. destilleret)
- 102 points er negligibelt storage
- Bruges af `ctx --advisor` pipeline

---

## 5. conversations (81 points) — ANBEFALING: DELETE

### Indhold
Rå chatlog-beskeder fra de allerførste sessioner (28. jan - 2. feb 2026):
- 81 individuelle chat-turns (user + assistant)
- Sekventielle numeriske IDs (0, 1, 2, ...)
- Payload: `role`, `content`, `date`, `source` (chatlog)

### Kvalitet
**Lav for søgning.** Individuelle chat-beskeder uden kontekst. Brugerens korte spørgsmål ("hej fortæl mig hvor var slap?") og assistentens svar. Ingen chunking — hver besked er ét punkt.

### Overlap med knowledge/episodes
**Ja, indirekte.** Episodes har allerede destillerede chatlogs (chatlog.md fra PC). Den vigtige information fra disse tidlige samtaler er fanget i DAGBOG.md og MEMORY.md.

### Begrundelse for DELETE
- 81 points — negligibelt storage, men forurener søgeresultater
- Individuelle chat-turns er dårlige søge-enheder (for korte, ingen kontekst)
- Historisk information allerede fanget i episodes og DAGBOG
- Ingen unik viden der ikke findes andetsteds

---

## 6. knowledge (984 points) — NY COLLECTION, BEHOLDES

### Indhold
PC-ingesterede markdown-filer fra Yggdra PC-repoet (projects/, research/):
- 53 unikke filer: research-rapporter, arkitektur-docs, AI frontier topics, psykologi, skattepenge, system-scans
- UUID-baserede IDs, moderne payload med `content_hash`, `confidence`, `created_at`, `indexed_at`
- Confidence-niveauer: `established`, `research`, `draft`, `unknown`

### Status
Aktivt i brug. Nyeste indexed_at: 2026-03-16. Ingen oprydning nødvendig.

---

## 7. episodes (59 points) — NY COLLECTION, BEHOLDES

### Indhold
Voice memos, chatlogs, session plans og progress-noter:
- 4 kildefiler: voice_260316_053647.md, chatlog.md, SESSION_22_PLAN.md, progress.md
- Samtlige fra marts 2026 sessioner
- Samme moderne payload-format som knowledge

### Status
Aktivt i brug. Komplementerer knowledge med episodisk/tidsmæssig kontekst.

---

## Migrationsplan (opsummering)

### Fase 1: DELETE (frigivelse af ~51% storage)
1. `sessions` — 43,511 points. Verificér at DAGBOG.md + episodes.jsonl dækker.
2. `conversations` — 81 points. Ingen unik viden.

### Fase 2: MIGRATE docs → knowledge
1. Re-embed docs-filerne med knowledge-pipelinens format (UUID, content_hash, confidence)
2. Fjern forældede filer (audits fra feb 2026, duplikerede versioner)
3. Slet docs-collection efter verifikation

### Fase 3: KEEP
- `advisor_brain` (453) — unik rådgiver-vidensbase
- `miessler_bible` (102) — original blog-kildemateriale
- `routes` (40,053) — separat domæne (TransportIntra)
- `knowledge` (984) — ny primary collection
- `episodes` (59) — ny episodisk collection

### Resultat efter migration
- **Fra 8 collections → 5 collections**
- **Fra ~86K points → ~42K points**
- `ctx` søger i: knowledge + advisor_brain + miessler_bible
- `ctx --advisor` søger i: advisor_brain + miessler_bible
- routes forbliver separat (TransportIntra)
