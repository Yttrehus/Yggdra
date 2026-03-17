# Loops-analyse, Pipeline-arkitektur & Ejerskab

**Dato:** 16. marts 2026
**Kilde:** 31-min voice memo + analyse af 148 loop-episoder fra 8.–16. marts
**Metode:** 4 loops (dataindsamling → mønster-analyse → framework-design → red team)

---

## Del 1: Mønster-analyse — Hvad går galt i loops?

### Datamængde analyseret
- 148 episoder med loop-nøgleord fra `episodes.jsonl` (643 total)
- 25 filer i `overlevering-fra-vps/`
- 4 primære session-JSONL'er (89c484f6, 94a9d938, 1f86132c, 525d1317)
- 9 verificerede "missed/found-later"-hændelser

### De 7 systematiske fejltyper

| # | Fejltype | Eksempel | Først fanget i |
|---|----------|---------|----------------|
| F1 | **Config/prerequisites antaget** | settings.local.json mangler → `claude --print` suspenderer | Loop 4 (flagget i loop 2) |
| F2 | **Vendor-claim bias** | Anthropic "54%", Mem0 "26%", claude-mem "10x" — ukritisk gengivet | Red team (dedikeret) |
| F3 | **Kun syntese, ingen nye kilder** | Loops syntetiserer eksisterende viden, henter ikke ny fra web | Retrospektiv (post-loop) |
| F4 | **Stille infrastruktur-fejl** | Heartbeat brugte forkert Telegram-token i uger, youtube_monitor crashet | Audit-loop |
| F5 | **Leverance-gap** | Planer skrevet men deliverables aldrig bygget (TRIAGE.md) | Reviewer loop 2+ |
| F6 | **Reviewer ignoreret** | Reviewer flagger, builder fikser ikke i 3+ iterationer | Loop 4-5 |
| F7 | **Research > Building** | "Du researcher når du burde bygge" — surfacede uafhængigt 3 gange | Red team |

### Nøgleindsigt: Hvorfor kræver det 4 loops?

**Root cause:** Loop 1 er konstruktiv og optimistisk. Den antager:
1. At config og services virker (F1, F4)
2. At eksisterende viden er tilstrækkelig (F3)
3. At vendor-claims er sande (F2)
4. At planer ≈ leverancer (F5, F7)

Disse antagelser afsløres først ved **adversarial gennemgang** (red team) eller **runtime execution** (smoke test). Begge sker typisk i loop 3-4.

**Den matematiske årsag:** Enhver loop der ikke eksplicit adresserer alle 7 fejltyper vil misse noget. En loop der kun er konstruktiv kan ikke finde F2, F6 eller F7.

---

## Del 2: Loops Framework v2 — Fra 4 til 2

### Princip: Dual-Nature Loop

Hver loop har **to faser** i stedet for at være enten konstruktiv ELLER adversarial:

```
Loop N = Byg-fase (60%) + Udfordre-fase (40%)
```

### Loop 1: Byg + Verificér

**Pre-flight checklist** (eliminerer F1, F4):
- [ ] Config/permissions: eksisterer nødvendige filer? (`settings.local.json`, `.env`, API keys)
- [ ] Services: er afhængigheder oppe? (Qdrant, Docker, cron)
- [ ] State: er der stale state der bør ryddes? (`.seen_items.json`, gamle logs)
- [ ] Scope: er outputtet et **produkt** eller en **plan**? (Kun produkter accepteres → eliminerer F5, F7)

**Byg-fase (60% af tid):**
- Parallelle agenter: research + implementation SAMTIDIG
- Mindst N nye kilder fra web (eliminerer F3)
- Hver agent producerer deliverable, ikke rapport

**Udfordre-fase (40% af tid):**
- Reviewer med **veto-ret** — kan blokere loop-completion (eliminerer F6)
- Vendor-claim audit: er tal verificerede? (eliminerer F2)
- Smoke test: kør det der er bygget, verificér output

**Loop 1 output:** Deliverable der virker + reviewer-vurdering med PASS/FAIL

### Loop 2: Red Team + Polish

**Kun nødvendig hvis Loop 1 Reviewer markerer CONDITIONAL PASS eller FAIL.**

- Steelman: bedste argument FOR den valgte tilgang
- Red team: bedste argument IMOD — specifikt:
  - Er der alternative tilgange der er billigere/simplere?
  - Er der bias i fremstillingen?
  - Er leverancen reel eller "research der ligner leverance"?
- Neutral: anbefaling med implementeringsplan

**Loop 2 output:** Endelig leverance + adversarial evaluering

### Hvornår er 2 loops nok?

| Signal | Loops nødvendigt |
|--------|-----------------|
| Loop 1 Reviewer: PASS + smoke test OK | 1 loop |
| Loop 1 Reviewer: CONDITIONAL PASS | 2 loops |
| Loop 1 Reviewer: FAIL | 2 loops (med scope-reduktion) |
| Ny domæne-viden påkrævet (ingen eksisterende research) | 2 loops |

### Pre-flight Checklist (copy-paste skabelon)

```markdown
## Pre-flight — [opgave-navn]
- [ ] Config: [list nødvendige filer]
- [ ] Services: [list afhængigheder + quick test]
- [ ] State: [stale state der bør ryddes?]
- [ ] Scope: Output er [PRODUKT/PLAN] — kun PRODUKT accepteres
- [ ] Kilder: Minimum [N] nye web-kilder påkrævet
- [ ] Reviewer: Har veto-ret. PASS/CONDITIONAL/FAIL.
```

### Loop-tabel skabelon

```markdown
| Loop | Faser | Agenter | Formål | Reviewer-krav |
|------|-------|---------|--------|---------------|
| 1 | Byg (60%) + Udfordre (40%) | [N parallelle] | [deliverable] | PASS/CONDITIONAL/FAIL |
| 2 | Red team + Polish | 3 (steelman/red/neutral) | Adversarial + endelig leverance | Kun ved CONDITIONAL/FAIL |
```

---

## Del 3: Pipeline-arkitektur — 95% rent guld for 0 tokens

### Kerneindsigt fra eksisterende research

- **70-90% af pipeline-arbejde er token-fri** (zero_token_pipeline_architecture.md)
- **L0-L3 bør eje 80% af pipelines** — kun det der kræver "forstå hvad dette betyder" tilhører L4+ (DESTILLAT)
- **Gate-keeper-mønstret:** Data → regelbaseret filter → signal? → nej: 0 tokens → ja: LLM aktiveres
- **JSONL som solo-dev's Kafka** — append-only, atomisk, `jq` for queries

### VAR-kamera-princippet

Hvert pipeline-trin producerer **to outputs:**

```
Step A → [resultat_A] + [log_A.jsonl]
Step B → [resultat_B] + [log_B.jsonl]
Step C → [resultat_C] + [log_C.jsonl]
```

**Log-format (standardiseret):**
```json
{
  "timestamp": "2026-03-16T16:00:00Z",
  "pipeline": "ai_intelligence",
  "step": "keyword_filter",
  "input_count": 47,
  "output_count": 12,
  "filtered_count": 35,
  "duration_ms": 230,
  "decision": "35 items scored 0, discarded without LLM"
}
```

**Logging destination:** `data/pipeline_logs/` (JSONL per pipeline per dag). Friskeste 7 dage på disk, ældre embeddes i Qdrant `pipeline-events` collection.

### Tredje Qdrant collection: `pipeline-events`

**Anbefaling: JA** — men først når de 4 pipelines kører stabilt.

- **Formål:** Sporbarhed. "Hvornår så vi sidst denne RSS-kilde?" "Hvorfor blev denne artikel filtreret fra?"
- **Payload:** pipeline, step, decision, timestamp, content_hash
- **Retention:** 90 dage, derefter automatisk sletning
- **Kill condition:** Hvis ingen query rammer collection i 30 dage → slet

### De 4 pipelines

#### Pipeline 1: AI Intelligence Pre-filter (L1→L4) — ★ START HER

**Nuværende:** ai_intelligence.py sender alle RSS-items til Groq.
**Forbedring:** Deterministisk pre-filter FØR Groq.

```
RSS-fetch → alle items
  → hash-check mod .seen_items.json (ALLEREDE IMPLEMENTERET)
  → keyword-score filter (ALLEREDE IMPLEMENTERET: RELEVANCE_KEYWORDS)
  → score == 0 → discard + LOG → 0 tokens
  → score 1-3 → gem i daily JSONL + LOG → 0 tokens
  → score 4+ → Groq summarization + LOG → tokens kun her
```

**Effort:** ~1 time (refaktorering, ikke nybygning)
**Besparelse:** 60-80% af Groq-tokens

#### Pipeline 2: ctx Temporal Decay (L1) — ★ START HER

**Nuværende:** `ctx` returnerer stale og friske resultater med samme score.
**Forbedring:** Post-processing decay.

```python
age_days = (now - result.payload.get("created_at", now)).days
result.score *= 1 / (1 + age_days * 0.01)
```

**Effort:** 30 minutter
**Gevinst:** Friskere retrieval for alt der bruger `ctx`

#### Pipeline 3: Heartbeat Gate-keeper (L2→L4)

**Nuværende:** heartbeat.py kalder potentielt API'er selv uden signal.
**Forbedring:** Shell pre-check der kun aktiverer heartbeat ved ændring.

```
cron */30 8-21
  → bash: tjek Gmail-labels, Tasks, Kalender (API calls, men ingen LLM)
  → hash mod data/heartbeat_state.json
  → ingen ændring → HEARTBEAT_OK, 0 tokens, LOG
  → ændring → heartbeat.py med kun relevant check + LOG
```

**Effort:** 2 timer
**Besparelse:** 90%+ af heartbeat-tokens
**Bonus:** Fjern Trello-integration (droppet 4/3)

#### Pipeline 4: Inkrementel Ingestion (L1)

**Nuværende:** embed_docs disabled. Ingen løbende indexering.
**Forbedring:** Daglig inkrementel ingestion med hash-check.

```
cron 06:00 dagligt
  → find nye/ændrede filer (mtime > last_ingest)
  → SHA256 per fil → sammenlign mod Qdrant content_hash
  → uændret → skip, 0 tokens
  → ændret → chunk + embed + upsert (idempotent) + LOG
```

**Effort:** 3 timer
**Gevinst:** Retrieval af nyeste research i `ctx`

### Prioritering

| # | Pipeline | Tokens sparet | Effort | Hvornår |
|---|----------|--------------|--------|---------|
| 1 | AI Intelligence pre-filter | 60-80% Groq | 1 time | I dag |
| 2 | ctx temporal decay | Bedre kvalitet | 30 min | I dag |
| 3 | Heartbeat gate-keeper | 90%+ heartbeat | 2 timer | I morgen |
| 4 | Inkrementel ingestion | Friskere ctx | 3 timer | Denne uge |

---

## Del 4: Ejerskab — Lokal server med open-source LLM

### Hvad kan lokalt vs. hvad kræver API

| Opgave | Lokal model | Kvalitet vs. API | Anbefalet model |
|--------|-------------|-----------------|-----------------|
| Filtrering/klassificering | ★★★ | 87-97% | Phi-3 Mini (3.8B) — kører på VPS nu |
| Embeddings | ★★★ | 95%+ | Allerede lokalt i Qdrant |
| Whisper transskription | ★★★ | 98%+ | Large v3 Turbo |
| Summarisering | ★★☆ | 80-90% | Mistral Small 3 / DeepSeek R1 32B |
| Simpel kode | ★★☆ | 70-80% | DeepSeek R1 Distill 32B |
| **Kompleks kodning** | ★☆☆ | 30-50% | **API påkrævet (Opus 4.6)** |
| **Lang-kontekst (>100K)** | ★☆☆ | 20-40% | **API påkrævet** |
| **Dyb ræsonnering** | ★☆☆ | 40-60% | **API påkrævet** |
| **Multi-agent koordination** | ☆☆☆ | N/A | **API påkrævet** |

### Hardware-anbefaling

**"Penge er ikke et problem" → To-trins investering:**

**Trin 1 (nu): Brugt PC + RTX 3090 — ~9.000 DKK**
- 24 GB VRAM → kører 32B modeller på 30-40 t/s
- Whisper Large v3 Turbo: 10 min lyd → 36 sek
- Kan køre Ollama som altid-tændt service
- Break-even vs. RunPod: ~15 måneder
- Strøm: ~2.190 DKK/år ved 4t daglig brug

**Trin 2 (om 3-6 måneder): Evaluer 70B-kapabilitet**
- Beelink GTR9 Pro (128GB, ~14.800 DKK) — når ROCm-drivere modner
- Eller dobbelt RTX 3090 setup (48GB VRAM)
- Eller afvent næste generation hardware (H2 2026)

**Mac Mini M4 Pro frarådes** — Kris har allerede Lenovo X1 Carbon + VPS. Endnu en Apple-enhed tilføjer kompleksitet uden at løse et problem.

### Total cost of ownership

| Scenarie | År 1 | År 2 | År 3 | 3-års total |
|----------|------|------|------|-------------|
| **Kun API (nuværende)** | ~6.000 DKK | ~6.000 DKK | ~6.000 DKK | ~18.000 DKK |
| **RTX 3090 + hybrid** | 9.000 + 2.190 + 2.000 API | 2.190 + 2.000 | 2.190 + 2.000 | ~21.570 DKK |
| **RTX 3090 + aggressiv lokal** | 9.000 + 2.190 + 1.000 API | 2.190 + 1.000 | 2.190 + 1.000 | ~18.570 DKK |

**Break-even:** ~18 måneder ved aggressiv lokal routing. Men den reelle gevinst er **ejerskab og uafhængighed**, ikke pris.

### Kan det erstatte Claude Code-abonnementet?

**Nej — men det kan reducere afhængigheden med 30-70%.**

- Pipeline-filtrering, embeddings, Whisper, summarisering → lokalt
- Claude Code til kompleks kodning, lang-kontekst, multi-agent → uundværligt
- **Hybrid-routing er svaret:** 80-95% af kald lokalt, 5-20% via API

### Implementeringsplan

| Fase | Hvad | Hvornår |
|------|------|---------|
| 0 | Ollama på VPS (CPU-only) til pipeline-filtrering | Kan gøres nu |
| 1 | Køb brugt RTX 3090 PC | Når det giver mening |
| 2 | Ollama + Whisper på GPU-maskine | Dag 1 med hardware |
| 3 | Hybrid-routing: lokalt default, API for frontier | Uge 1-2 |
| 4 | Evaluér 70B modeller / næste-gen hardware | 3-6 måneder |

---

## Del 5: Tværgående — Systemets sammenhæng

### De tre emner er ét system

```
Loops-framework (hvordan Claude arbejder)
    ↓ optimerer
Pipeline-arkitektur (hvad der sker mellem sessioner)
    ↓ drives af
Lokal LLM (ejerskab over begge)
```

**Meta-observation:** Denne rapport er selv et eksempel på pipeline-tænkning:
1. Voice memo → Whisper (pipeline-trin 1)
2. Rå transskription → renskrevet prompt (pipeline-trin 2, LLM-assisteret)
3. Prompt → ny session med struktureret analyse (pipeline-trin 3)
4. Analyse → konsolideret rapport (pipeline-trin 4)

Hvert trin producerede et output + en log (voice memo, renskrevet markdown, session-episodes, denne rapport).

### VPS-reformation hænger sammen

VPS skal ligne PC. Pipelines er en del af den arkitektur:
- **VPS ejer drift:** cron, pipelines, heartbeat, ingestion
- **PC ejer udvikling:** kode, research, design
- **GPU-maskine (fremtidig):** lokal LLM, Whisper, embeddings
- **SSH er broen** mellem alle tre

---

---

## Del 6: Red Team + Steelman

### STEELMAN — Hvad er genuint stærkt

1. **F1-F7 fejltaxonomien er empirisk**, ikke spekuleret. Udledt af 148 episoder. Specielt F6 (reviewer ignoreret) og F7 (research > building) er sjældent formuleret så klart.
2. **Pipeline 1 og 2 er konkrete og billige.** 1 time + 30 min for verificerbar ROI. Består enhver cost-benefit analyse.
3. **VAR-kamera-princippet løser F4** (stille infrastruktur-fejl). Standardiseret log-format er idempotent at tilføje.
4. **Dual-nature loop (60/40) er en simpel mental model** der kan operationaliseres uden overhead.
5. **Hardware-analysen er ærlig om sine grænser.** Siger eksplicit at Claude Code er uundværligt.

### RED TEAM — Hvad er galt

**Loops Framework:**
- "Kun produkter accepteres" er et ønske, ikke en mekanisme. En 300-linjer analyserapport vil kalde sig selv et produkt. **Denne rapport er selv eksemplet.**
- PASS/CONDITIONAL/FAIL har ingen operationelle kriterier. Uden kriterier er reviewer-veto symbolsk.
- "Mindst N nye kilder" — N er ikke specificeret.
- **80% løsning:** En enkelt regel: *Ingen session afsluttes uden at producere en fil der kan køres eller testes.* Pre-flight reduceret til 3 spørgsmål: Virker credentials? Kører services? Er output en kommando eller en markdown-fil?

**Pipeline-arkitektur:**
- Tredje Qdrant collection (`pipeline-events`) er arkitektur der tjener arkitektur. JSONL i `data/pipeline_logs/` gør præcis det samme.
- Pipeline 3 (Heartbeat) erstatter én fragilitet (LLM-kald) med en anden (OAuth API-kald). Ingen retry-logik specificeret.
- Pipeline 4 bruger `mtime` som gate — giver falske positiver med symlinks og git ops. SHA256 alene er korrekt.
- "ALLEREDE IMPLEMENTERET" — men dokumentet ved ikke om keyword-filter faktisk er integreret i flowet. **Plan skrevet uden at læse koden.**

**Ejerskab:**
- TCO-tabellen bruger 6.000 DKK/år som API-baseline **uden kilde**. Faktisk forbrug er ukendt.
- Kvalitetstal (87-97%, 98%+) har ingen kilde — præcis F2 (vendor-claim bias) som rapporten selv identificerer. **Ironisk.**
- 3 maskiner (VPS + laptop + GPU-server) = vedligeholdsbyrde for en fuldtidsbuschauffør. Ikke adresseret.

### OVERSETE MULIGHEDER

1. **Session-budget som primitive** — hard token-budget per session defineret FØR start. Ingen framework nødvendig.
2. **episodes.jsonl som feedback-loop** — 643 episoder. Hvornår er loops produktive vs. uproduktive? Mønster-analyse af tidspunkt, varighed, outcome.
3. **Voice memo som pipeline-input** — daglige voice memos bør embeddes direkte i `ctx`, ikke kun bruges som kilde.
4. **Pre-commit hook som leverance-gate** — afvis commits der kun indeholder `.md` uden tilhørende `.py`/config. Eliminerer F5+F7 operationelt.
5. **Kompaktering = checkpoint** — når Claude kompakterer, stop og evaluer: "bygger jeg eller researcher jeg?" Naturlig gate der allerede eksisterer.

### NEUTRAL VERDICT

**Gør nu (næste 2 timer):**
- Pipeline 2: ctx temporal decay — 4 linjer kode, 30 min, ingen risiko
- Pipeline 1: AI Intelligence pre-filter — 1 time, men LÆS koden først

**Gør denne uge:**
- Tilføj til CLAUDE.md: "Ingen session afsluttes uden kørbar fil. Reviewer har veto. Smoke test er obligatorisk." (Frameworkets essens i 30 ord)

**Udskyd:**
- Pipeline 3 (Heartbeat gate-keeper) — mål faktisk token-forbrug først
- Pipeline 4 (Ingestion) — fix mtime-problemet i designet

**Dræb:**
- Tredje Qdrant collection — JSONL gør jobbet
- RTX 3090-beslutningen nu — dokumentér faktiske API-udgifter i 30 dage, kør Phi-3 Mini på VPS (CPU) i samme periode, tag beslutning med data

**Dom:** Rapporten er 60% genuint nyttig og 40% research der ligner leverance (F7). Det bedste den producerer er Pipeline 1+2, F1-F7 taxonomien, og pre-flight checklistens kerne. Alt andet bør gentjekkes mod faktisk kode og data.

---

*Genereret kl. 16:51, red team tilføjet kl. 17:02, 16. marts 2026. Baseret på 148 episoder, 25 overleverings-filer, 4 session-JSONL'er, 6 research-rapporter.*
