# Vedligeholdelses-protokol — Videns-pipelines

Operationel checkliste for at holde Yggdra's videns-pipelines sunde og aktuelle.

---

## 1. Re-scan Triggers

### Tidsbaserede (automatiske)

| Kategori | Interval | Trigger | Handling |
|----------|----------|---------|----------|
| Model releases | 7 dage | Decay-check i daily run | Scan GitHub releases + HN |
| API pricing | 14 dage | Pricing diff-checker | Hash-sammenlign pricing pages |
| Tool versioner | 7 dage | GitHub release watch | Allerede dækket af ai_intelligence |
| Agent patterns | 30 dage | Decay-check | Re-scan YouTube + Substack |
| Research papers | 30 dage | Decay-check | Dybere arXiv scan (top 50 i stedet for 20) |
| Kilde-kvalitet | 90 dage | Kvartalsvis audit | Gennemgå SOURCE_REGISTRY.md |

### Event-baserede (manuelle/semi-auto)

| Event | Trigger | Handling |
|-------|---------|----------|
| Ny Claude model | CRITICAL_PATTERNS match | Telegram alert + umiddelbar research |
| Ny MCP spec version | GitHub release | Opdatér MCP-viden i Qdrant |
| Prisændring hos provider | Pricing diff-checker | Opdatér COMPARISON.md |
| YouTube kanal stopper | 0 videoer i 60 dage | Overvej fjernelse fra sources.json |
| Pipeline crash | Health monitor (daily_sweep) | Telegram alert + fix inden 24 timer |
| Yttre nævner nyt emne | Manual | Tilføj relevance keywords + evt. nye kilder |

---

## 2. Arkiverings-politik

### Hvad arkiveres

| Type | Arkiveringsregel | Destination |
|------|-----------------|-------------|
| Daily digests (md + json) | Behold 30 dage, arkivér ældre | data/intelligence/archive/YYYY-MM/ |
| Weekly digests | Behold 12 uger, arkivér ældre | data/intelligence/archive/ |
| Discovery rapporter | Behold 90 dage | data/intelligence/archive/ |
| YouTube transcripts | Behold permanent i Qdrant | Qdrant (sessions collection) |
| .seen_items.json | Trim til seneste 1000 entries | In-place (undgå OOM) |
| Pricing snapshots | Behold alle (diff-historik) | data/intelligence/pricing_snapshots/ |

### Hvad slettes

| Type | Slettepolitik |
|------|---------------|
| discovered_sources noise | Rens ved tilføjelse (quality filter) |
| Tomme/fejlede daglige filer | Slet efter 7 dage |
| Log-filer >100MB | Rotér (allerede via tmux pipe-pane) |

### Arkiverings-script (pseudokode)
```bash
# Kør månedligt, f.eks. 1. i hver måned
ARCHIVE_DIR="data/intelligence/archive/$(date +%Y-%m)"
mkdir -p $ARCHIVE_DIR
find data/intelligence/ -name "daily_*.md" -mtime +30 -exec mv {} $ARCHIVE_DIR/ \;
find data/intelligence/ -name "daily_*.json" -mtime +30 -exec mv {} $ARCHIVE_DIR/ \;
```

---

## 3. Kvalitetskontrol

### Ugentlig (søndag, efter ai_intelligence --weekly)

- [ ] Åbn ugens weekly digest. Indeholder den actionable information?
- [ ] Check top-5 items: er scoring korrekt? (false positives / false negatives)
- [ ] Check YouTube monitor: har den fundet nye videoer fra high-priority kanaler?
- [ ] Check .seen_items.json størrelse (bør ikke overstige 5000 entries)

### Månedlig (1. i måneden)

- [ ] Gennemgå SOURCE_REGISTRY.md: er alle kilder stadig aktive?
- [ ] Check om nye relevans-keywords bør tilføjes (baseret på Yttre's seneste interesser)
- [ ] Kør `wc -l data/intelligence/daily_*.md | sort -n` — er output-volumen stabil?
- [ ] Check intelligence.log for fejl: `grep -c "fejl\|FEJL\|error\|Error" /var/log/ydrasil/intelligence.log`

### Kvartalsvis (marts, juni, september, december)

- [ ] Full source review: fjern kilder med kvalitet ≤2 der ikke har produceret nyttigt output
- [ ] Evaluer om nye kilder bør tilføjes (tjek hvad Yttre har læst/brugt)
- [ ] Opdatér DECAY_MODEL.md hvis kategorier har vist sig at have anderledes halveringstid
- [ ] Sammenlign kost vs. værdi: hvad koster source_discovery.py (OpenAI embeddings)?

---

## 4. Vedligeholdelses-kalender

### Dagligt (automatisk, kl. 06:30-08:00)

| Tid | Pipeline | Script |
|-----|----------|--------|
| 06:30 | AI Intelligence daglig | ai_intelligence.py |
| 07:00 | YouTube monitor | youtube_monitor.py |
| 08:00 | Daily sweep (inkl. health check) | daily_sweep.py |

### Ugentligt (søndag)

| Tid | Pipeline | Script |
|-----|----------|--------|
| 06:15 | AI Intelligence ugentlig digest | ai_intelligence.py --weekly |
| 06:30 | Cruft detector | cruft_detector.py |
| 08:00 | Source discovery | source_discovery.py |
| — | Manual: check ugens digest kvalitet | Yttre |

### Månedligt (1. i måneden)

| Opgave | Ansvarlig |
|--------|-----------|
| Arkivér daglige filer >30 dage | Cron (når implementeret) |
| Source review | Yttre/Claude session |
| Keyword-review | Yttre/Claude session |
| Trim .seen_items.json | Automatisk (når implementeret) |

### Kvartalsvist

| Opgave | Ansvarlig |
|--------|-----------|
| Full source audit | Yttre/Claude session |
| Decay model review | Yttre/Claude session |
| Cost-analyse af pipelines | Yttre/Claude session |
| Fjern døde kilder | Yttre/Claude session |

---

## 5. Eskalerings-regler

| Situation | Handling |
|-----------|----------|
| Pipeline producerer ikke output i 2+ dage | Telegram alert (automatisk via health monitor) |
| Ny Claude model released | Telegram alert (automatisk via CRITICAL_PATTERNS) |
| Kilde returnerer 0 items i 4 uger | Markér som "stale" i SOURCE_REGISTRY, overvej fjernelse |
| .seen_items.json >10MB | Trim automatisk til seneste 1000 entries |
| intelligence.log >50MB | Rotér: `mv intelligence.log intelligence.log.1` |
| Groq free tier limit hit | Switch til Gemini Flash (billigst alternativ) |
| OpenAI embedding cost >$5/md | Reducér source_discovery frekvens eller switch til lokal model |
