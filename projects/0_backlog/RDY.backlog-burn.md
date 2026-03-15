# Backlog Burn — Session 22 Plan

**Dato:** 2026-03-15
**Status:** RDY
**Mål:** Luk max briefs i én session. VPS kører autonomt, PC kører bagefter.

---

## Del 1: VPS Ralph Loop (autonom, 7 iterationer)

Deployes til `/root/Yggdra/yggdra-pc/v6-backlog-burn/`.
Dækker: V4 handlinger 1-6 + automation-inventory.

### CLAUDE.md

```markdown
# V6 Backlog Burn — Sandbox

Du kører autonomt i en Ralph loop. Yttre er ikke tilgængelig.
Hver iteration er et `claude --print` kald.

## Boot-sekvens

1. Dit iterationsnummer er givet i prompten
2. Læs LOOP_STATE.md — check ## Blokkere
3. Læs den relevante iteration i LOOP_PLAN.md
4. VALIDÉR INPUT: Check at filer fra forrige iteration eksisterer
5. Udfør opgaven. Skriv/ændr kode
6. TEST med kommandoer (python3 -c "...", crontab -l, curl, grep)
7. Opdatér LOOP_STATE.md
8. Stop

## LOOP_STATE format

```
# Loop State
## Blokkere
(ingen / liste)

## Filregister
(kumulativ liste af ændrede filer)

## Iteration [N-1] (seneste)
Opgave: ...
Output: ...
Done: ... → PASS/FAIL

## Iteration [N-2]
(slet ældre end N-2)

## Næste: Iteration N
```

## Projekt

7 konkrete implementeringer. Alt baseret på V4 research (HOLISTIC_EVALUATION, PIPELINE_DESIGN, GAPS.md, WHAT_IF.md). Plus en automation-inventarisering. Koden eksisterer allerede — du udvider den.

## Regler

### Token-bevidsthed
- Læs ALDRIG filer >500 linjer i helhed. Brug head, tail, grep
- Max 3 parallelle subagents
- Skriv kompakt

### Build > Research
- Hver iteration SKAL ændre kode eller config på disk
- Ingen rapporter — kun kode, config, og test-resultater

### Done = Verified
- Test ALTID med `python3 -c "..."` eller direkte kørsel
- Verificér at ændringer ikke bryder eksisterende funktionalitet
- Kør eksisterende script med --test eller --dry-run hvis muligt

### Miljø
- Du er PÅ VPS'en. ALDRIG ssh til dig selv
- SØG IKKE på nettet
- Python venv: /root/Yggdra/scripts/venv/bin/python3
- Scripts: /root/Yggdra/scripts/
- Config: /root/Yggdra/data/intelligence_sources.json
- Crontab: `crontab -l` og `crontab -e` (brug `(crontab -l; echo "...") | crontab -`)
- Qdrant: curl localhost:6333/collections

### Anti-patterns
- OMSKRIV IKKE hele scripts — tilføj/ændr funktioner
- TEST før du ændrer crontab
- Tag BACKUP af filer du ændrer (`cp file file.bak`)
- Brug IKKE pip install uden at teste først
```

### LOOP_PLAN.md

```markdown
# Loop Plan — V6 Backlog Burn (7 iterationer)

## Iteration 1 — Fix RSS bug + genaktivér heartbeat
**Opgave:** To quick wins fra V4 HOLISTIC_EVALUATION.
**Metode:**
1. **RSS bug:** `grep -n 'fetch_rss' /root/Yggdra/scripts/ai_intelligence.py` — find hvor funktionen er defineret men aldrig kaldt
2. Find main-flow / scheduling-logik: `grep -n 'def main\|if __name__\|def run\|schedule' /root/Yggdra/scripts/ai_intelligence.py | head -20`
3. Tilføj `fetch_rss_feeds()` kald det rigtige sted i execution flow
4. Test: `/root/Yggdra/scripts/venv/bin/python3 -c "import sys; sys.path.insert(0,'/root/Yggdra/scripts'); from ai_intelligence import fetch_rss_feeds; items=fetch_rss_feeds(); print(len(items), 'items fetched')"`
5. **Heartbeat:** `crontab -l | grep heartbeat` — er den kommenteret ud?
6. Test heartbeat: `/root/Yggdra/scripts/venv/bin/python3 /root/Yggdra/scripts/heartbeat.py`
7. Hvis test OK: uncomment i crontab
8. Verificér: `crontab -l | grep -v '^#' | grep heartbeat`
**Done:** fetch_rss_feeds() kaldt i ai_intelligence.py main flow + heartbeat aktiv i crontab. Begge testet.

## Iteration 2 — Temporal decay i get_context.py
**Opgave:** Nyere viden scorer højere i ctx-søgning. Fra V4 GAPS P2 + memory-architecture fase 1.
**Metode:**
1. `cp /root/Yggdra/scripts/get_context.py /root/Yggdra/scripts/get_context.py.bak`
2. `grep -n 'def.*search\|def.*query\|score\|payload\|timestamp\|created\|date' /root/Yggdra/scripts/get_context.py` — find retrieval-logik og timestamp-felter
3. Find hvor scores returneres fra Qdrant
4. Tilføj decay-logik efter Qdrant-kald:
   ```python
   import math
   from datetime import datetime
   # For hvert resultat:
   timestamp = point.payload.get('timestamp') or point.payload.get('created_at') or point.payload.get('date')
   if timestamp:
       try:
           age_days = (datetime.now() - datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))).days
           point.score *= math.exp(-age_days / 30)
       except (ValueError, TypeError):
           pass  # Ingen decay for manglende/ugyldigt timestamp
   ```
5. Sortér resultater igen efter decay
6. Test: `cd /root/Yggdra/scripts && ./venv/bin/python3 get_context.py "test query" 2>&1 | head -20` — verificér at det stadig virker
7. Test: sammenlign output med og uden decay (brug .bak)
**Output:** Opdateret get_context.py med temporal decay
**Done:** get_context.py ændret, test viser at nyere resultater scorer relativt højere, eksisterende queries stadig virker

## Iteration 3 — Reranking i ctx (Cohere API)
**Opgave:** Rerank top-20 Qdrant-resultater med Cohere Rerank API → returner top-5. Fra V4 WHAT_IF #2 + memory-architecture fase 1.
**Metode:**
1. Check om cohere er installeret: `/root/Yggdra/scripts/venv/bin/python3 -c "import cohere; print(cohere.__version__)"` — hvis ikke: `./venv/bin/pip install cohere`
2. Check om API key findes: `grep -ri 'cohere\|CO_API_KEY\|COHERE' /root/Yggdra/data/ /root/Yggdra/scripts/.env /root/.env 2>/dev/null`
3. Hvis INGEN API key: skriv BLOCKED i state ("Cohere API key mangler — Yttre skal oprette konto på dashboard.cohere.com og sætte CO_API_KEY"). Stop.
4. Hvis API key findes:
   - `cp /root/Yggdra/scripts/get_context.py /root/Yggdra/scripts/get_context.py.bak2`
   - Tilføj reranking efter Qdrant top-20, før temporal decay:
   ```python
   import cohere
   co = cohere.ClientV2(api_key=os.environ.get('CO_API_KEY'))
   reranked = co.rerank(
       model="rerank-v3.5",
       query=query,
       documents=[r.payload.get('text', '') for r in results],
       top_n=5
   )
   results = [results[r.index] for r in reranked.results]
   ```
   - Wrap i try/except så det falder gracefully tilbage til uden reranking
5. Test: `CO_API_KEY=... ./venv/bin/python3 get_context.py "transport rute 256" 2>&1 | head -20`
**Output:** Opdateret get_context.py med Cohere reranking
**Done:** Reranking virker ELLER BLOCKED med klar besked om hvad Yttre skal gøre. Aldrig crash.

## Iteration 4 — Pipeline health check i daily_sweep.py
**Opgave:** Alert hvis intelligence pipelines ikke har produceret output. Fra V4 HOLISTIC_EVALUATION.
**Metode:**
1. `cp /root/Yggdra/scripts/daily_sweep.py /root/Yggdra/scripts/daily_sweep.py.bak`
2. `head -60 /root/Yggdra/scripts/daily_sweep.py` — forstå strukturen
3. Tilføj funktion `check_pipeline_health()`:
   - Check at `data/intelligence/daily_YYYY-MM-DD.md` eksisterer for i dag eller i går
   - Check at `data/intelligence/youtube_YYYY-MM-DD.md` eksisterer for i dag eller i går
   - Hvis BEGGE mangler for i dag OG i går: log WARNING til /var/log/ydrasil/sweep.log
   - Check /var/log/ydrasil/intelligence.log for "ERROR\|FAIL\|Traceback" i seneste 48 timer: `grep -c 'ERROR\|FAIL\|Traceback' /var/log/ydrasil/intelligence.log`
   - Return dict med status per pipeline
4. Tilføj kaldet i daily_sweep main-flow
5. Test: `/root/Yggdra/scripts/venv/bin/python3 /root/Yggdra/scripts/daily_sweep.py` (eller --dry-run hvis det eksisterer)
**Output:** Opdateret daily_sweep.py
**Done:** Health check kører, rapporterer korrekt status

## Iteration 5 — Blog RSS feeds + fix sources
**Opgave:** Tilføj 4 blog RSS feeds + rens discovered_sources. Fra V4 HOLISTIC_EVALUATION + videns-vedligeholdelse.
**Metode:**
1. `cp /root/Yggdra/data/intelligence_sources.json /root/Yggdra/data/intelligence_sources.json.bak`
2. `cat /root/Yggdra/data/intelligence_sources.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(list(d.keys()), indent=2))"` — forstå JSON-strukturen
3. Tilføj til rss_feeds-sektionen:
   - Anthropic Research: `https://www.anthropic.com/research/rss` (priority: high)
   - OpenAI Blog: `https://openai.com/blog/rss/` (priority: high)
   - Google DeepMind: `https://deepmind.google/blog/rss.xml` (priority: medium)
   - Hugging Face Blog: `https://huggingface.co/blog/feed.xml` (priority: medium)
4. Test HVER feed: `python3 -c "import feedparser; f=feedparser.parse('URL'); print(len(f.entries), f.entries[0].title if f.entries else 'EMPTY')"`
5. Rens discovered_sources: fjern entries med noise-navne ("prize", "Tools/Platforms", "Ukendt kanal", "ikke specificeret")
6. Verificér: `python3 -c "import json; d=json.load(open('/root/Yggdra/data/intelligence_sources.json')); print(len(d.get('rss_feeds',[])), 'feeds,', len(d.get('discovered_sources',[])), 'discovered')"`
**Output:** Opdateret intelligence_sources.json
**Done:** 4 nye feeds tilføjet og testet, discovered_sources renset

## Iteration 6 — Automation inventory (VPS)
**Opgave:** Komplet inventar over alt der kører automatisk på VPS. For automation-index briefen.
**Output-fil:** `/root/Yggdra/yggdra-pc/v6-backlog-burn/AUTOMATION_INVENTORY.md`
**Metode:**
1. **Crontab:** `crontab -l` — list alle jobs (aktive OG kommenterede)
2. **Systemd timers:** `systemctl list-timers --all 2>/dev/null`
3. **Docker:** `docker ps --format '{{.Names}}: {{.Status}}'` — kørende containere
4. **Scripts med scheduling:** `grep -rl 'schedule\|cron\|timer\|interval\|sleep.*while' /root/Yggdra/scripts/ 2>/dev/null`
5. **Hooks:** `ls -la /root/Yggdra/.claude/hooks/ 2>/dev/null` + `cat /root/Yggdra/.claude/settings.local.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('hooks',{}), indent=2))" 2>/dev/null`
6. **n8n workflows:** `ls /root/Yggdra/data/n8n/ 2>/dev/null` eller `curl -s localhost:5678/api/v1/workflows 2>/dev/null | python3 -c "import sys,json; wfs=json.load(sys.stdin).get('data',[]); [print(w['name'], w.get('active','?')) for w in wfs]" 2>/dev/null`
7. **Log-rotation:** `ls /etc/logrotate.d/ | grep -i ydrasil 2>/dev/null`
8. Skriv AUTOMATION_INVENTORY.md med tabeller:
   ```
   ## Cron Jobs
   | Schedule | Script | Formål | Status |

   ## Docker Services
   | Container | Image | Ports | Status |

   ## Claude Code Hooks
   | Event | Script | Formål |

   ## Andre
   | Type | Hvad | Status |

   ## Cruft-kandidater
   (ting der kører men muligvis ikke bruges)
   ```
**Done:** AUTOMATION_INVENTORY.md eksisterer, >50 linjer, dækker cron+docker+hooks+n8n

## Iteration 7 — Review alle ændringer
**Opgave:** Verificér iteration 1-6 og skriv REVIEW.md.
**Metode:**
1. `crontab -l | grep -v '^#'` — heartbeat aktiv?
2. `diff /root/Yggdra/scripts/get_context.py.bak /root/Yggdra/scripts/get_context.py | head -40` — decay + reranking
3. `diff /root/Yggdra/scripts/daily_sweep.py.bak /root/Yggdra/scripts/daily_sweep.py | head -40` — health check
4. `python3 -c "import json; d=json.load(open('/root/Yggdra/data/intelligence_sources.json')); print(len(d.get('rss_feeds',[])), 'feeds')"` — feeds tilføjet?
5. `wc -l /root/Yggdra/yggdra-pc/v6-backlog-burn/AUTOMATION_INVENTORY.md` — inventory komplet?
6. End-to-end test af ctx: `/root/Yggdra/scripts/venv/bin/python3 /root/Yggdra/scripts/get_context.py "rute 256 sortering"` — virker det stadig?
7. Skriv REVIEW.md:
   ```
   # V6 Backlog Burn — Review
   ## Status per iteration
   | # | Opgave | Status | Noter |

   ## Ændrede filer
   (komplet liste med diff-summary)

   ## Blokerede ting (til Yttre)
   (Cohere API key? Andre mangler?)

   ## Anbefaling til næste step
   ```
**Done:** REVIEW.md skrevet, alle iterationer verificeret
```

### LOOP_STATE.md (initial)

```markdown
# Loop State

## Blokkere
(ingen)

## Filregister
(tomt)

## Næste: Iteration 1
Fix RSS bug + genaktivér heartbeat
```

### Deploy-kommando

```bash
mkdir -p /root/Yggdra/yggdra-pc/v6-backlog-burn

# Deploy CLAUDE.md, LOOP_PLAN.md, LOOP_STATE.md til mappen FØRST
# (copy-paste indholdet ovenfor til filerne)

for i in $(seq 1 7); do
  echo "=== Iteration $i === $(date)"
  if grep -q "BLOCKED\|FAILED" LOOP_STATE.md 2>/dev/null; then
    echo "=== HALTED ==="
    cat LOOP_STATE.md | head -10
    break
  fi
  timeout 600 /root/.local/bin/claude --dangerously-skip-permissions --print \
    "Du er iteration $i af 7. Følg CLAUDE.md boot-sekvens."
  if ! grep -q "Iteration $i" LOOP_STATE.md 2>/dev/null; then
    echo "=== WARNING: iteration $i opdaterede ikke state ==="
  fi
  echo "=== Iteration $i done === $(date)"
  sleep 10
done

echo "=== Loop færdig ==="
cat LOOP_STATE.md
```

### Review fra telefon

```bash
# Quick status
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/v6-backlog-burn/LOOP_STATE.md"
# Fuld review
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/v6-backlog-burn/REVIEW.md"
# Automation inventory
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/v6-backlog-burn/AUTOMATION_INVENTORY.md"
# Diff ctx
ssh root@72.62.61.51 "diff /root/Yggdra/scripts/get_context.py.bak /root/Yggdra/scripts/get_context.py | head -40"
```

---

## Del 2: PC (Claude Code session, efter VPS)

Kører i næste session efter VPS loop er done. Ingen VPS-afhængigheder.

### P1: Taxonomy migration (30 min)

**Hvad:** `git mv projects/2_research projects/LIB.research` + arkivér forbrugte VPS-filer.

```bash
# Rename
git mv projects/2_research projects/LIB.research

# Arkivér forbrugte VPS prompt-filer
mkdir -p projects/9_archive/vps.prompt-drafts
git mv projects/0_backlog/vps-sandbox-v2.md projects/9_archive/vps.prompt-drafts/
git mv projects/0_backlog/vps-prompt-final-draft.md projects/9_archive/vps.prompt-drafts/
git mv projects/0_backlog/vps-prompt-final.md projects/9_archive/vps.prompt-drafts/
git mv projects/0_backlog/vps-prompt-v5-implementering.md projects/9_archive/vps.prompt-drafts/
```

**Opdatér refs i:**
- CONTEXT.md — `2_research/` → `LIB.research/`, `1_archive` → `9_archive`
- CLAUDE.md — verify `LIB.research/` i strukturen
- BLUEPRINT.md — `2_research/` → `LIB.research/`
- projects/0_backlog/TRIAGE.md — opdatér stier

**Lukker briefs:** work-intake (migration done), project-taxonomy (dækket af work-intake)

### P2: Terminal-automatisering (15 min)

**Hvad:** `.vscode/tasks.json` med `runOn: folderOpen` så terminaler starter automatisk.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Bash",
      "type": "shell",
      "command": "bash",
      "isBackground": true,
      "runOptions": { "runOn": "folderOpen" },
      "presentation": {
        "reveal": "silent",
        "panel": "dedicated",
        "group": "terminals"
      },
      "problemMatcher": []
    },
    {
      "label": "VPS SSH",
      "type": "shell",
      "command": "ssh root@72.62.61.51",
      "isBackground": true,
      "runOptions": { "runOn": "folderOpen" },
      "presentation": {
        "reveal": "silent",
        "panel": "dedicated",
        "group": "terminals"
      },
      "problemMatcher": []
    },
    {
      "label": "Qdrant Tunnel",
      "type": "shell",
      "command": "ssh -L 6333:localhost:6333 root@72.62.61.51",
      "isBackground": true,
      "runOptions": { "runOn": "folderOpen" },
      "presentation": {
        "reveal": "silent",
        "panel": "dedicated",
        "group": "terminals"
      },
      "problemMatcher": []
    }
  ]
}
```

**Test:** Luk og genåbn VS Code workspace. 3 terminaler skal starte automatisk.

**Lukker brief:** terminal-automatisering

### P3: Notion-spejling (45 min)

**Hvad:** Opret "Projekter" database i Notion via MCP, populér med reelle projekter.

**Steps:**
1. `notion-create-database` med properties:
   - Projektnavn (title)
   - Status (select: Aktiv/Pauset/Venter/Arkiveret)
   - Stage (select: BMS/REF/LIB/KNB/DLR/SIP/PoC)
   - Næste step (rich_text)
   - Type (select: Dev/Research/Setup/Rejseselskab/Personlig)
   - Sidst opdateret (date)
   - Noter (rich_text, Notion-only)

2. `notion-create-pages` — tilføj alle aktive projekter:
   - BMS.auto-chatlog → Aktiv, BMS, "v3 fungerer"
   - DLR.session-blindhed → Aktiv, DLR, "aktiv research"
   - KNB.manuals → Aktiv, KNB, "git+terminal+vscode guides"
   - LIB.research → Aktiv, LIB, "V4 output integreret"
   - LIB.ydrasil → Aktiv, LIB, "VPS-æra research"
   - REF.mcp-skills-kompendium → Aktiv, REF, "opslagsværk"
   - REF.prompt-skabeloner → Aktiv, REF, "templates"
   - REF.transportintra → Aktiv, REF, "komplet arkiv"
   - REF.vps-sandbox → Aktiv, REF, "v1-v4 historik"

3. Opret 3 views:
   - **Fokus:** Kanban grupperet på Status
   - **Alt:** Tabel
   - **Arkiv:** Filtreret Status=Arkiveret

4. Test mobiloplevelsen (Yttre checker selv)

**Lukker brief:** notion-spejling

### P4: Automation-index — PC-side (30 min)

**Hvad:** Inventorier PC hooks/tasks, merge med VPS AUTOMATION_INVENTORY.md fra V6.

**PC-inventar:**
```bash
# Claude Code hooks
cat .claude/settings.local.json | python -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('hooks',{}), indent=2))"

# VS Code tasks (efter P2)
cat .vscode/tasks.json

# Git hooks
ls .git/hooks/

# Scripts
ls scripts/
```

**Output:** `projects/0_backlog/` → nyt projekt `BMS.automation-index/` med:
- `INDEX.md` — samlet inventar (PC + VPS)
- `CONTEXT.md` — hvad er det, kill condition

**Lukker brief:** automation-index

### P5: Webscraping-audit (5 min)

**Hvad:** Konklusionen er allerede i briefen. Implementér "WebFetch først" som instruktion.

**Handling:** Firecrawl skill er allerede installeret og har `MUST replace WebFetch and WebSearch` i sin beskrivelse. Det ER allerede implementeret — Firecrawl-skillen IS the policy. Briefen er reelt lukket.

**Alternativt:** Hvis Yttre vil nedprioritere Firecrawl, fjern skillen fra `.claude/skills/`. Men det er en beslutning, ikke et task.

**Lukker brief:** webscraping-audit (allerede løst af Firecrawl skill install)

### P6: Luk briefs (5 min)

**cross-session-peer-review:** Lukkes med note: "PR-based self-review (github-workflow) + /the-fool skill + /dialectic-pipeline skill dækker dette. Ingen dedikeret tooling nødvendig."

**github-workflow:** Allerede "marinerer" status — tags, README, PR workflow done. Resten er vaner, ikke kode.

**Handling:** Flyt begge til `projects/9_archive/`:
```bash
git mv projects/0_backlog/brief.cross-session-peer-review.md projects/9_archive/
git mv projects/0_backlog/raw.github-workflow.md projects/9_archive/
```

### P7: Context-engineering fase 1 — session-drift hooks (2-4 timer)

**Hvad:** BLUEPRINT.md viser at 4 hooks ALLEREDE er aktive (SessionStart, PreCompact, UserPromptSubmit, Stop). Briefen beskriver præcis de samme hooks. Check om de allerede gør det briefen beskriver.

**Eksisterende hooks (fra BLUEPRINT.md):**
| Hook | Script | Hvad det gør |
|------|--------|-------------|
| SessionStart | session_start.sh | Injicerer CONTEXT.md + seneste episoder |
| PreCompact | pre_compact.sh | Skriver marker med projekt + state |
| UserPromptSubmit | post_session_check.sh | Tjekker marker, injicerer reminder |
| Stop | session_end.sh | Logger episode til episodes.jsonl |

**Briefens spec:**
| Hook | Formål |
|------|--------|
| SessionStart | Inject NOW.md i kontekst |
| PostToolUse (Bash/git commit) | Auto-dump chatlog |
| PreCompact | Gem state til NOW.md FØR context ryddes |
| SessionEnd | Arkivér session i PROGRESS.md |

**Gap-analyse:**
1. SessionStart — ALLEREDE DONE (injicerer CONTEXT.md, som ER NOW.md-ækvivalenten)
2. PostToolUse (chatlog dump) — check-git-commit.sh eksisterer som hook, men den minder om NOW.md, dumper ikke chatlog. Chatlog-engine kører via BMS.auto-chatlog. GAP: auto-trigger chatlog-dump ved commit?
3. PreCompact — ALLEREDE DONE (pre_compact.sh)
4. Stop/SessionEnd — ALLEREDE DONE (session_end.sh → episodes.jsonl)

**Reelt gap:** Kun PostToolUse chatlog-trigger. Og muligvis: forbedre pre_compact.sh til også at appende til PROGRESS.md.

**Steps:**
1. Læs alle 4 eksisterende scripts (scripts/session_start.sh, pre_compact.sh, post_session_check.sh, session_end.sh)
2. Læs .claude/settings.local.json for hook-registrering
3. Identificér præcise gaps vs. briefens spec
4. Implementér manglende hooks
5. Test

**Lukker brief:** context-engineering (fase 1)

---

## Del 3: Opdatér state (efter alt)

### TRIAGE.md

Fjern/opdatér:
- V4 handlinger 1-6: Done (VPS V6)
- automation-index: Done
- context-engineering fase 1: Done
- notion-spejling: Done
- Fjern lukkede briefs fra tabeller
- Tilføj ny sektion "Session 22 resultater"

### CONTEXT.md

- Session 22 sektion med alt der blev gjort
- Opdatér struktur (LIB.research, nye arkiverede filer)
- Opdatér "Aktive projekter" og "Afsluttede"

### Commit + push

```bash
git add -A
git commit -m "session 22: backlog burn — taxonomy migration, terminal-auto, notion, automation-index, context-eng hooks, 8 briefs lukket"
git push
```

---

## Samlet tæller (forventet)

| Kategori | Antal |
|----------|-------|
| Briefs lukket | 8 (work-intake, project-taxonomy, terminal-auto, notion, automation-index, webscraping-audit, cross-session-peer-review, github-workflow) |
| V4 handlinger done | 6 (RSS bug, heartbeat, decay, health check, blog feeds, reranking delvist) |
| Forbrugte filer arkiveret | 4 VPS prompt-filer |
| Nye ting live | Notion-database, terminal-auto, automation-index, evt. context-eng hooks |
| Afventer stadig | 6 briefs (visualisering, voice, integrationer, pdf-skill, abonnement, M5 12/15) |

---

## Risici

| Risiko | Sandsynlighed | Mitigation |
|--------|---------------|------------|
| Cohere API key mangler | Høj | VPS loop skriver BLOCKED, resten fortsætter |
| RSS feed URLs ændret | Lav | feedparser test per URL i iteration 5 |
| Notion MCP fejler | Medium | Opret manuelt, synk senere |
| Hooks bryder workflow | Lav | Alle hooks har allerede fallback (exit 0) |
| Taxonomy migration bryder refs | Medium | grep -r for alle stier før commit |
