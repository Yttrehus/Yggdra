# Holistisk Evaluering — Alle 4 Loops i Kontekst

**Dato:** 2026-03-15
**Input:** Output fra llm-landskab, ai-frontier, youtube-pipeline-v2, videns-vedligeholdelse + YGGDRA_SCAN.md

---

## Hvad de 4 loops producerede

| Loop | Iterationer | Filer | Kerne-deliverable |
|------|-------------|-------|-------------------|
| **llm-landskab** | 7 (alle PASS) | 7 profiler + COMPARISON.md + RECOMMENDATION.md + EVALUATION.md | Provider-valgfri strategi: Scenarie C (Anthropic + OpenAI + Gemini). 10/10 fact-checks. |
| **ai-frontier** | 10 (alle PASS) | 5 topic-filer + GAPS.md + WHAT_IF.md + EVALUATION.md | 8 gaps identificeret. Konkret handlingsliste. 10/10 spot-checks. |
| **youtube-pipeline-v2** | 3 (alle PASS) | frame_extractor.py (230L) + udvidet youtube_monitor.py (+63L) | Frame extraction PoC. VPS download blokeret men graceful degradation. |
| **videns-vedligeholdelse** | 6 (alle PASS) | _audit.md + DECAY_MODEL.md + SOURCE_REGISTRY.md + PIPELINE_DESIGN.md + MAINTENANCE_PROTOCOL.md + YGGDRA_SCAN.md | Pipeline-gaps kortlagt. 5 udvidelser designet. Bug fundet (RSS feeds konfigureret men aldrig kaldt). |

**Samlet output:** ~30 filer, ~3.000 linjer, 27 iterationer. Alle fact-checks PASS. Ingen hallucerede data.

---

## Overlap og redundans

### Positiv redundans (konsistenscheck)
- **Hybrid search** nævnes i GAPS.md (P2), WHAT_IF.md (#1), og COMPARISON.md (Qdrant kan det). Konsistent budskab: Qdrant supporterer det, Yttre bruger det ikke, effort er dage. Godt.
- **Temporal decay** nævnes i GAPS.md (P2), DECAY_MODEL.md (kritisk gap), og WHAT_IF.md. Konsistens.
- **Proaktiv AI** i GAPS.md (heartbeat disabled, P1) og _audit.md (morning_brief + heartbeat begge disabled).

### Negativ redundans (spild)
- **Provider-profiler** i llm-landskab og **source_registry** i videns-vedligeholdelse dækker delvist samme ground (hvilke LLM providers Yttre bruger). Men fokus er forskelligt (pricing vs. intelligence-kilder), så det er acceptabelt.
- **YouTube pipeline** i youtube-pipeline-v2 og youtube_monitor audit i videns-vedligeholdelse overlapper. Begge konstaterer: VPS download blokeret, Tor upålideligt. En PoC er bygget (frame_extractor.py) men det addresserer ikke det fundamentale problem: transcripts er svære at hente fra VPS.

---

## Hvad INGEN loop adresserede

1. **VPS-PC synkronisering.** Alle loops kører på VPS, producerer output på VPS, men PC har ingen automatisk måde at hente det. YGGDRA_SCAN.md nævner det som svaghed, men ingen loop designede en løsning. Git pull? Rsync? SSH-baseret sync?

2. **Kost-tracking og budget.** RECOMMENDATION.md foreslår Scenarie C (3 providers) men ingen loop estimerede den samlede månedlige kost eller designede tracking. cost_daily.json eksisterer men analyseres ikke systematisk.

3. **Evaluering af retrieval-kvalitet.** GAPS.md siger "Ingen systematisk evaluering" (P2). WHAT_IF.md foreslår 10 test queries. Ingen loop byggede dem. Det er stadig et gap.

4. **Yttre's faktiske brug.** Ingen loop undersøgte om Yttre rent faktisk læser intelligence output. daily_*.md produceres trofast men der er ingen feedback loop. Producerer vi output ingen bruger?

5. **Mobiladgang.** BLUEPRINT.md's lag 4 (tilgængelighed) er uadresseret. Yttre har kun Android telefon (ingen PC-adgang til VPS under arbejde). Intelligence output er markdown-filer på en VPS — usynlige fra telefonen.

---

## Ærlig kritik

### Styrker
- **Fakta-baseret.** Begge evaluerings-loops (llm-landskab, ai-frontier) scorede 10/10 på fact-checks mod lokale kilder. Ingen hallucination.
- **Konkret.** WHAT_IF.md og PIPELINE_DESIGN.md har pseudokode, effort-estimater, kill conditions. Ikke bare "vi burde gøre X".
- **Selvkritisk.** GAPS.md er ærlig om Yttre's svagheder. Ingen smiger.
- **Arkitekturelt sammenhængende.** DECAY_MODEL.md → SOURCE_REGISTRY.md → PIPELINE_DESIGN.md → MAINTENANCE_PROTOCOL.md er en logisk kæde.

### Svagheder
- **Alt er design, intet er implementeret.** 4 loops, ~3.000 linjer output, men nul linjer kode i produktion (undtagen frame_extractor.py PoC og 3 nye YouTube kanaler). Risiko: analyse-paralyse.
- **Loop-isolation.** Loops kørte parallelt men refererer ikke til hinandens output (undtagen denne evaluering). PIPELINE_DESIGN.md burde have refereret til GAPS.md's P1-prioriteter. RECOMMENDATION.md burde have informeret SOURCE_REGISTRY.md.
- **Scope creep.** Videns-vedligeholdelse loopet voksede fra "pipeline design" til at inkludere YGGDRA_SCAN.md (systemscan). Det er nyttigt men fortynder fokus.
- **RSS-bug fundet men ikke fikset.** _audit.md og PIPELINE_DESIGN.md dokumenterer at RSS feeds er konfigureret i sources.json men aldrig kaldt i ai_intelligence.py. Det ville tage 5 minutter at fixe. I stedet skrev vi et 251-linje design-dokument.

### Blinde pletter
- **Ingen bruger-validering.** Vi antager at disse analyser er nyttige. Yttre har ikke valideret en eneste anbefaling.
- **Timing-bias.** Alle data er baseret på lokale research-filer der selv kan være forældede. COMPARISON.md bruger Elo-scores og priser der ændrer sig. Self-referential cirkel.
- **Ingen cost-analyse af loops selv.** Disse 4 loops har brugt Anthropic API tokens. Hvad kostede det? Er ROI positiv? Ingen ved det.

---

## Prioriteret handlingsliste (max 7 punkter)

Baseret på alle 4 loops' output, sorteret efter impact × (1/effort):

| # | Handling | Effort | Kilde | Begrundelse |
|---|---------|--------|-------|-------------|
| 1 | **Fix RSS feed bug** — tilføj `fetch_rss_feeds()` kald i `collect_all_items()` i ai_intelligence.py. Feeds er allerede konfigureret. | 15 min | videns-vedligeholdelse/_audit.md | Gratis value. Allerede betalt for konfigurationen. |
| 2 | **Genaktivér heartbeat.py** — fjern DISABLED comment i crontab. Heartbeat er bygget og testet. | 5 min | ai-frontier/GAPS.md (P1) | Proaktiv AI er det Yttre mangler mest. Koden eksisterer. |
| 3 | **Tilføj reranking i ctx** — 5 linjer kode: Cohere API efter Qdrant top-20, returnér top-5. | 2-4 timer | ai-frontier/WHAT_IF.md (#2) | Op til 48% bedre retrieval. Minimal kode. |
| 4 | **Tilføj pipeline health check i daily_sweep.py** — alert hvis ai_intelligence eller youtube_monitor ikke har produceret output. | 2-3 timer | videns-vedligeholdelse/PIPELINE_DESIGN.md (#4) | Forhindrer tavse fejl. |
| 5 | **Implementér temporal decay i ctx** — `score *= exp(-age_days/30)` i get_context.py. | 1-2 timer | ai-frontier/GAPS.md (P2) + videns-vedligeholdelse/DECAY_MODEL.md | Gammel info forurener retrieval. Triviel fix. |
| 6 | **Tilføj Anthropic + OpenAI blog RSS** til rss_feeds i sources.json + implementér `fetch_rss_feeds()`. | 2-3 timer | videns-vedligeholdelse/PIPELINE_DESIGN.md (#1) | Lukker kritisk gap: officielle announcements fanges ikke direkte. |
| 7 | **Design VPS→PC sync** — git-baseret eller rsync. Intelligence output + NOW.md + episodes.jsonl. Implementér som cron job eller hook. | 4-6 timer | YGGDRA_SCAN.md, alle loops | Fundamentalt problem: PC og VPS divergerer. Alt loop-output er usynligt fra PC. |

### Fravalg (med begrundelse)
- **Hybrid search:** For dyrt nu (re-ingest 84K points). Gør reranking først, evaluer impact.
- **Pricing diff-checker:** Nice to have men Yttre's volume er lavt og priser ændrer sig sjældent.
- **Multi-provider resilience:** P4, Anthropic er stabil, effort er uger.
- **Fact extraction pipeline:** Usikker impact, moderat effort. Evaluer after reranking.

---

## Hvor står Yggdra som system?

**Fundamentet er overraskende stærkt.** 84K vektorer i Qdrant, 17 cron jobs, 4 hooks, 11 skills, daglig intelligence pipeline, episodisk log — det er mere infrastruktur end de fleste personlige AI-setups. Arkitekturmæssigt er Yggdra tættere på state of the art end Yttre sandsynligvis indser.

**Det svageste punkt er broen mellem produktion og forbrug.** Pipelines producerer trofast output (15 daglige digests i træk) men der er ingen evidens for at Yttre læser dem. Morning brief er disabled. Telegram-alerts er kun for kritiske events. Intelligence output akkumulerer som uåbnede filer.

**Det næst-svageste punkt er VPS-PC kløften.** To systemer der burde føles som ét. Alle 4 loops kørte på VPS, producerede ~30 filer, men PC'en ved det ikke. Næste session på PC starter uden denne viden. Det er det samme session-blindhedsproblem som BLUEPRINT.md's lag 2 forsøger at løse — men på tværs af maskiner, ikke bare sessioner.

**Risikoen er analyse-paralyse.** 4 loops har produceret 3.000 linjer analyse og 7 implementerings-anbefalinger. Hvis Yttre kører 4 flere loops i stedet for at implementere punkt 1-3 (samlet effort: 3-5 timer), er systemet i analyse-mode, ikke build-mode. Næste trin bør være implementering, ikke mere design.

---

## Loop-kvalitet Sammenligning

| Dimension | llm-landskab | ai-frontier | youtube-v2 | videns-vedl. |
|-----------|-------------|-------------|------------|--------------|
| Fact accuracy | 10/10 | 10/10 | N/A (PoC) | Verificeret |
| Actionability | Middel (anbefalinger) | Høj (WHAT_IF) | Høj (kode) | Middel (design) |
| Implementeret | 0 linjer | 0 linjer | 293 linjer | 0 linjer |
| Cross-loop refs | Nej | Nej | Nej | Ja (bruger COMPARISON) |
| Kritisk selvvurdering | Ja (EVALUATION) | Ja (EVALUATION) | Delvist | Ja (denne fil) |

**Stærkeste loop:** ai-frontier — 8 gaps med effort-estimater og prioritering er direkte brugbare.
**Svageste loop:** youtube-pipeline-v2 — blokeret af VPS download-problem. PoC virker men kan ikke bruges i produktion.
**Mest overraskende fund:** RSS feed bug i ai_intelligence.py. Konfigureret men aldrig kaldt. 15 minutters fix.
