# Videns-vedligeholdelse

**Dato:** 2026-03-14
**Klar til:** Backlog — VPS Ralph loop (efter llm-landskab + ai-frontier)
**Prioritet:** Medium-høj — design-projekt, ikke research

## Opsummering
Design et system til at holde AI-viden aktuel. Decay-detection, automatisk re-scan, kilde-registrering, vedligeholdelsesprotokoller. Udvidelse af eksisterende ai_intelligence.py + youtube_monitor.py.

## Hvorfor
AI-viden har halveringstider fra uger til måneder. Model-benchmarks: ~3 mdr. Pricing: ~6 mdr. Arkitektur-principper: ~12 mdr. Uden systematisk vedligeholdelse akkumulerer Yggdra forældet viden der fører til dårlige beslutninger.

## Scope

**Inden for:**
- Decay-model: kategorisering af videns-halveringstid
- Kilde-registrering: alle kilder med type, frekvens, kvalitetsscore
- Pipeline-design: hvordan VPS proaktivt scanner og opdaterer
- Vedligeholdelsesprotokoller: hvornår re-scan, hvornår arkivér, hvornår slet
- Integration med eksisterende ai_intelligence.py + youtube_monitor.py

**Uden for:**
- Selve researchen (det er llm-landskab og ai-frontier)
- Implementation af nye pipelines (separat efter design)
- Qdrant-arkitektur (separat)

## Deliverables

1. `DECAY_MODEL.md` — kategorier af viden med halveringstider og eksempler
2. `SOURCE_REGISTRY.md` — alle kilder med type, frekvens, kvalitetsscore, URL/RSS
3. `PIPELINE_DESIGN.md` — udvidelse af ai_intelligence.py: nye kilder, Substack, blogs, proaktiv re-scan
4. `MAINTENANCE_PROTOCOL.md` — hvornår re-scannes, hvornår arkiveres, hvornår slettes

## VPS-metode (Ralph loop, 5 iterationer)

### Iteration 1: Audit eksisterende pipelines
Inventar: ai_intelligence.py, youtube_monitor.py, crontab, intelligence_sources.json. Hvad kører, hvornår, hvad fanger det, hvad misser det.
**Done:** _audit.md med komplet inventar + gap-analyse.

### Iteration 2: DECAY_MODEL.md + SOURCE_REGISTRY.md
Kategorisér al viden i Yggdra efter halveringstid. List alle kilder med metadata.
**Done:** Begge filer >50 linjer.

### Iteration 3-4: PIPELINE_DESIGN.md
Design udvidelser: Substack-integration (allerede implementeret), blog-RSS, proaktiv re-scan af ældre research, decay-baseret prioritering.
**Done:** >80 linjer, konkret nok til at implementere.

### Iteration 5: Review + MAINTENANCE_PROTOCOL.md
**Done:** Begge filer, ærlig vurdering.

## Kill condition
Hvis designet bliver mere komplekst end det problem det løser → simplificér radikalt eller kill.
