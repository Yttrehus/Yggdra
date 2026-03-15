# VPS Ralph Loop — Videns-vedligeholdelse

Deploy til `/root/Yggdra/yggdra-pc/videns-vedligeholdelse/`.
5 iterationer. Korer EFTER llm-landskab + ai-frontier (bruger deres output).

---

## CLAUDE.md

```markdown
# Videns-vedligeholdelse — Sandbox

Du korer autonomt i en Ralph loop. Yttre er ikke tilgaengelig.
Hver iteration er et `claude --print` kald.

## Boot-sekvens

1. Dit iterationsnummer er givet i prompten
2. Laes LOOP_STATE.md — check ## Blokkere
3. Laes den relevante iteration i LOOP_PLAN.md
4. VALIDER INPUT: Check at filer fra forrige iteration eksisterer
5. Udfor opgaven. Skriv output til disk
6. Verificer output med kommandoer (ls, wc -l, head)
7. Opdater LOOP_STATE.md
8. Stop

## LOOP_STATE format

```
# Loop State
## Blokkere
(ingen / liste)

## Filregister
(kumulativ liste af producerede filer)

## Iteration [N-1] (seneste)
Opgave: ...
Output: ...
Done: ... -> PASS/FAIL

## Iteration [N-2]
(slet aeldre end N-2)

## Naeste: Iteration N
```

## Projekt

Design et system til at holde AI-viden aktuel. Decay-detection, kilde-registrering, vedligeholdelsesprotokoller. Bygger videre paa eksisterende ai_intelligence.py + youtube_monitor.py.

## Input fra andre loops

Disse filer kan eksistere fra parallelle loops:
- `../llm-landskab/COMPARISON.md` — provider-sammenligning (brug til kilde-prioritering)
- `../ai-frontier/GAPS.md` — huller i Yttres setup (brug til decay-prioritering)
Hvis de ikke eksisterer: arbejd uden dem.

## Yggdra PC repo

Klonet til `/root/Yggdra/yggdra-pc/yggdra-repo/`. Det er Yttres PC-side af Yggdra — projekter, backlog, research, skills, state-filer.
Brug det i iteration 5-6 til at forstaa helheden. Laes IKKE hele filer >200 linjer — brug head/grep.

## Regler

### Token-bevidsthed
- Laes ALDRIG filer >500 linjer i helhed. Brug head, tail, grep
- Max 3 parallelle subagents
- Skriv kompakt

### Build > Research
- Hver iteration SKAL producere filer paa disk
- Design der kan implementeres, ikke akademisk kategorisering

### Done = Verified
- Test med kommandoer
- Spot-check at pipeline-design refererer til eksisterende scripts korrekt

### Miljo
- Du er PAA VPS'en. ALDRIG ssh til dig selv
- SOG IKKE paa nettet
- Eksisterende scripts: /root/Yggdra/scripts/ai_intelligence.py, youtube_monitor.py
- Kilde-config: /root/Yggdra/data/intelligence_sources.json
- Cron: `crontab -l` for at se hvad der korer
- Substack: /root/Yggdra/data/substack_cookies.json (virker, testet)

### Anti-patterns
- Ikke abstrakte kategorier uden konkrete eksempler
- Ikke pipeline-design der kraever nye services (brug eksisterende Python + cron)
- Ikke >10 kilder i en kategori (collector's trap)
```

---

## LOOP_PLAN.md

```markdown
# Loop Plan — Videns-vedligeholdelse (7 iterationer)

## Iteration 1 — Audit eksisterende pipelines
**Opgave:** Komplet inventar af hvad der korer i dag
**Metode:** 2 subagents:
- Sub A: `crontab -l` + `head -50` af ai_intelligence.py og youtube_monitor.py. Hvad gor de, hvornaar, hvad fanger de
- Sub B: `cat /root/Yggdra/data/intelligence_sources.json` + ls /var/log/ydrasil/. Hvad er konfigureret, hvad er output
**Output:** `_audit.md` — tabel med [pipeline, frekvens, kilder, output, kvalitet, gaps]
**Done:** _audit.md >50 linjer, alle pipelines dokumenteret

## Iteration 2 — DECAY_MODEL.md + SOURCE_REGISTRY.md
**Opgave:** Kategoriser al viden efter halveringstid. List alle kilder med metadata
**Input:** _audit.md + ../llm-landskab/COMPARISON.md (hvis den eksisterer) + ../ai-frontier/GAPS.md (hvis den eksisterer)
**DECAY_MODEL.md format:**
```
| Kategori | Halveringstid | Eksempler | Nuvaerende daekning |
|----------|---------------|-----------|---------------------|
| Model benchmarks | ~3 mdr | Elo, MMLU, HumanEval | youtube_monitor |
```
**SOURCE_REGISTRY.md format:**
```
| Kilde | Type | Frekvens | Kvalitet (1-5) | Daekning | URL/Metode |
|-------|------|----------|----------------|----------|------------|
| Import AI | Substack | Ugentlig | 5 | Bred AI | fetch_substack() |
```
**Done:** Begge filer >50 linjer, >5 decay-kategorier, >15 kilder registreret

## Iteration 3 — PIPELINE_DESIGN.md
**Opgave:** Design udvidelser af eksisterende pipelines
**Input:** _audit.md + SOURCE_REGISTRY.md + DECAY_MODEL.md
**Daek:**
- Substack-integration: allerede implementeret — dokumenter workflow
- Blog-RSS: Simon Willison, Anthropic blog, OpenAI blog — design fetch-funktion
- Proaktiv re-scan: decay-baseret prioritering (hvad skal re-scannes forst?)
- Alerting: naar noget kritisk aendrer sig (ny model, prisaendring, breaking change)
**Format per udvidelse:**
```
### [Udvidelse]
**Effort:** Timer/Dage
**Aendringer i:** [eksisterende fil]
**Ny kode:** [pseudokode, max 20 linjer]
**Test:** [hvordan verificeres det virker]
```
**Done:** PIPELINE_DESIGN.md >80 linjer, >3 udvidelser med pseudokode

## Iteration 4 — MAINTENANCE_PROTOCOL.md
**Opgave:** Hvornaar re-scan, hvornaar arkiver, hvornaar slet
**Input:** DECAY_MODEL.md + PIPELINE_DESIGN.md
**Daek:**
- Re-scan triggers: tidsbaseret (decay) + event-baseret (ny model release)
- Arkiverings-politik: hvad flyttes til archive/, hvad slettes
- Kvalitetskontrol: hvordan vurderes om en kilde stadig er vaerdifuld
- Vedligeholdelses-kalender: ugentligt, maanedligt, kvartalsvist
**Done:** MAINTENANCE_PROTOCOL.md >60 linjer, konkret nok til at folge som checkliste

## Iteration 5 — Yggdra PC scan
**Opgave:** Scan Yttres PC-repo for helhedsbillede
**Input:** /root/Yggdra/yggdra-pc/yggdra-repo/ (klonet fra GitHub)
**Metode:** 3 subagents:
- Sub A: Laes CONTEXT.md + BLUEPRINT.md + CLAUDE.md. Forstaa systemets state og arkitektur
- Sub B: Laes alle briefs i projects/0_backlog/ (head -15 af hver). Forstaa backlog-prioriteter. Laes TRIAGE.md
- Sub C: Laes CONTEXT.md i hvert projekt under projects/ (head -20 af hver). Forstaa hvad der eksisterer
Merger til YGGDRA_SCAN.md: hvad er systemet, hvad er prioriteterne, hvad er aktivt, hvad mangler
**Done:** YGGDRA_SCAN.md >80 linjer, daekker system-state + projekter + backlog + prioriteter

## Iteration 6 — Holistisk evaluering
**Opgave:** Evaluer ALLE 4 loops' output i kontekst af hele Yggdra
**Input:** YGGDRA_SCAN.md + alt output fra:
- ../llm-landskab/ (profiler, COMPARISON.md, RECOMMENDATION.md)
- ../ai-frontier/ (topics/, WHAT_IF.md, GAPS.md)
- Denne loop (DECAY_MODEL, SOURCE_REGISTRY, PIPELINE_DESIGN, MAINTENANCE_PROTOCOL)
- ../youtube-pipeline-v2/ (hvis den har koert)
**Skriv HOLISTIC_EVALUATION.md:**
- Hvad fylder hullerne vi fandt i GAPS.md?
- Hvad overlapper mellem loops (redundans)?
- Hvad mangler stadig — hvad har INGEN loop adresseret?
- Konkrete anbefalinger: hvad boer Yttre goere foerst? (prioriteret liste, max 7 punkter)
- Hvor staar Yggdra som system? Styrker, svagheder, blinde pletter
**Vaer aerlig og kritisk. Ingen smiger. Sandhed.**
**Done:** HOLISTIC_EVALUATION.md >100 linjer, alle 4 loops refereret, prioriteret handlingsliste

## Iteration 7 — Review
**Opgave:** 3 Reviewer-subagents
- Reviewer A: Er pipeline-design implementerbart? Refererer det til korrekte filstier og funktioner?
- Reviewer B: Er decay-model realistisk? Er kilde-registrering komplet?
- Reviewer C: Er HOLISTIC_EVALUATION.md aerlig? Spot-check 3 claims mod kilderne. Er handlingslisten realistisk?
**Done:** EVALUATION.md med aerlig vurdering af hele loopet
```

---

## LOOP_STATE.md (initial)

```markdown
# Loop State

## Blokkere
(ingen)

## Filregister
(tomt)

## Naeste: Iteration 1
Audit eksisterende pipelines
```

---

## Start-kommando

```bash
cd /root/Yggdra/yggdra-pc/videns-vedligeholdelse

for i in $(seq 1 7); do
  echo "=== Iteration $i === $(date)"
  if grep -q "BLOCKED\|FAILED" LOOP_STATE.md 2>/dev/null; then
    echo "=== HALTED ==="
    cat LOOP_STATE.md | head -10
    break
  fi
  timeout 600 /root/.local/bin/claude --print \
    "Du er iteration $i af 7. Folg CLAUDE.md boot-sekvens."
  if ! grep -q "Iteration $i" LOOP_STATE.md 2>/dev/null; then
    echo "=== WARNING: iteration $i opdaterede ikke state ==="
  fi
  echo "=== Iteration $i done === $(date)"
  sleep 10
done
```

---

## Review fra telefon

```bash
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/videns-vedligeholdelse/LOOP_STATE.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/videns-vedligeholdelse/PIPELINE_DESIGN.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/videns-vedligeholdelse/SOURCE_REGISTRY.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/videns-vedligeholdelse/HOLISTIC_EVALUATION.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/videns-vedligeholdelse/YGGDRA_SCAN.md"
```
