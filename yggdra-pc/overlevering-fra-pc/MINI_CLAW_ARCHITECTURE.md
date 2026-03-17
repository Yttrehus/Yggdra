# Mini-Claw Arkitektur: Checkpoint Agent

**Dato:** 2026-03-16
**Kontekst:** OpenClaw-inspireret, bygget på Yggdras eksisterende hooks og zero-token principper.

---

## 1. Hvad er en Mini-Claw?

En letvægts-agent der kører autonomt med ét formål, read-only som default, og med eksplicit kill-switch. Inspireret af OpenClaw's heartbeat pattern, men i Python, uden Node.js, og til ~$0/dag via Groq.

**Princip:** Deterministiske checks først. LLM kun når der er et signal.

---

## 2. Checkpoint Agent — Oversigt

| Aspekt | Design |
|--------|--------|
| **Formål** | Destillér sessioner, opdatér projektstatus, vedligehold episodisk hukommelse |
| **Trigger** | Claude Code hooks (Stop, PreCompact, Notification) + cron fallback |
| **Model** | Groq llama-3.3-70b-versatile ($0) |
| **Sikkerhed** | Budget-cap, timeout (120s), throttle (600s), kill-switch fil |
| **Status** | 80% ALLEREDE BYGGET i save_checkpoint.py + load_checkpoint.sh |

---

## 3. Trigger-mekanismer

### Allerede implementeret
| Hook | Trigger | Hvad sker |
|------|---------|-----------|
| **Stop** | Session slutter | Groq destillerer → episode + NOW.md + projekt-NOW.md |
| **PreCompact** | Context window komprimeres | Groq extraherer FACTS/DECISIONS/ACTIONS → episode |
| **Notification** | Periodic (throttled 10 min) | NOW.md update, INGEN Groq-kald |
| **SessionStart** | Ny session åbner | Læser projekter, episoder, parallel sessions |

### Mangler (GAP)
| Feature | Beskrivelse | Prioritet |
|---------|-------------|-----------|
| **HEARTBEAT.md config** | Markdown-fil der definerer hvad heartbeat tjekker — behavior-as-config | Høj |
| **Telegram input** | Polling af Telegram-beskeder → dispatch til relevante scripts | Medium |
| **Proaktiv follow-up** | Morning brief refererer gårsdagens episoder og foreslår næste skridt | Lav |

---

## 4. Data Flow

```
SESSION SLUTTER
     │
     ▼
save_checkpoint.py (trigger: Stop)
     │
     ├── 1. Læs transcript (sidste 15 beskeder, 500 chars/besked)
     ├── 2. Skriv data/NOW.md (global snapshot)
     ├── 3. Append data/checkpoints/{dato}.md (80KB cap)
     ├── 4. Groq: destillér → 3-5 linjer episode (200 tokens)
     ├── 5. Groq: identificér projekt (10 tokens)
     ├── 6. Append data/episodes.jsonl
     └── 7. Opdatér projects/{projekt}/NOW.md
```

```
NY SESSION STARTER
     │
     ▼
load_checkpoint.sh (trigger: SessionStart)
     │
     ├── 1. Læs projects/*/NOW.md (aktive sektioner, max 5+3 linjer)
     ├── 2. Læs data/NOW.md (hvis <48 timer gammel)
     ├── 3. Læs data/NOW_{parallel_id}.md (parallelle sessioner)
     ├── 4. Læs sidste 5 episoder fra episodes.jsonl
     └── 5. Output JSON → Claude Code context injection
```

---

## 5. Hvad skal BYGGES for at gøre det til en "rigtig" mini-claw

### 5.1 HEARTBEAT.md (config-fil)

```markdown
# HEARTBEAT.md — Checkpoint Agent Configuration

enabled: true
interval: 30m
time_window: 08:00-22:00 CET
model: groq/llama-3.3-70b-versatile
budget_daily_tokens: 50000
kill_file: /tmp/heartbeat_kill

## Checks (deterministiske, 0 tokens)
- [ ] Gmail: nye mails siden sidst
- [ ] Google Calendar: events næste 2 timer
- [ ] Google Tasks: nye/ændrede tasks
- [ ] Voice pipeline: nye filer i inbox

## Signals (kun hvis check finder noget)
- mail_urgent: LLM vurderer → Telegram notifikation
- calendar_soon: Regelbaseret → Telegram påmindelse
- task_new: Log → morning brief
- voice_new: Trigger transkription pipeline
```

**Fordel:** Ændring af behavior kræver kun redigering af en markdown-fil, ikke kode.

### 5.2 Daglig token-tracking

```python
# I save_checkpoint.py, tilføj efter Groq-kald:
TOKEN_LOG = "data/token_usage.jsonl"
def log_tokens(model, prompt_tokens, completion_tokens, purpose):
    entry = {
        "ts": datetime.now().isoformat(),
        "model": model,
        "prompt": prompt_tokens,
        "completion": completion_tokens,
        "purpose": purpose  # "episode", "project_id", "precompact"
    }
    with open(TOKEN_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

### 5.3 Kill-switch

```python
KILL_FILE = "/tmp/heartbeat_kill"
if os.path.exists(KILL_FILE):
    sys.exit(0)  # Stille exit, ingen fejl
```

Allerede delvist til stede via `cron_guard.sh` (lockfile + timeout), men eksplicit kill-fil er tydeligere.

---

## 6. Model-valg og token-cost

| Opgave | Model | Tokens/kald | Kald/dag | Daglig cost |
|--------|-------|-------------|----------|-------------|
| Episode destillering | Groq (free) | ~600 | 3-8 | $0 |
| Projekt-identifikation | Groq (free) | ~100 | 3-8 | $0 |
| PreCompact flush | Groq (free) | ~800 | 1-3 | $0 |
| Heartbeat signal (sjældent) | Groq (free) | ~500 | 0-5 | $0 |
| Morning brief | Groq (free) | ~2000 | 1 | $0 |
| **Total** | | | | **~$0/dag** |

**Hvis Groq free tier forsvinder:**
- Haiku fallback: ~$0.005/dag
- Sonnet fallback: ~$0.05/dag
- Opus: ALDRIG for heartbeat ($0.50+ per kald)

**Zero-token gating er ikke optional.** Uden deterministiske checks før LLM-kald kan heartbeat-costs eskalere ukontrolleret. OpenClaw-fællesskabet rapporterer costs fra $6-13/mdr (sparsom brug) til $150+/mdr (Opus hvert 30. min) — se OpenClaw GitHub discussions og `/root/Yggdra/research/openclaw_deep_dive_2026-03-15.md` for detaljer. [Specifikke dollar-beløb stammer fra community-rapporter i OpenClaw Discord/GitHub, verificeret mod Anthropic pricing: Opus input $15/MTok, output $75/MTok (Anthropic, 2025).]

---

## 7. Sikkerhedsmekanismer

| Mekanisme | Status | Implementation |
|-----------|--------|----------------|
| **Read-only default** | DELVIST | Heartbeat læser kun. save_checkpoint skriver. Ingen skriver til app/ eller scripts/. |
| **Timeout** | DONE | cron_guard.sh (120s for heartbeat, 300s for checkpoint) |
| **Throttle** | DONE | 600s mellem Notification-hooks |
| **Tidsvindue** | DONE | 08:00-22:00 dansk tid i heartbeat.py |
| **Dedup** | DONE | Hash-baseret i checkpoint, state-baseret i heartbeat |
| **File size cap** | DONE | 80KB daglig log, 500 chars/besked |
| **Kill-switch** | MANGLER | Tilføj `/tmp/heartbeat_kill` check |
| **Budget-cap** | MANGLER | Tilføj token_usage.jsonl + daglig grænse |
| **HEARTBEAT.md config** | MANGLER | Behavior-as-config i stedet for hardcoded |
| **Dagbog** | MANGLER | Mini-claw skriver sin egen log: hvad den gjorde, hvad den fandt |

---

## 8. Bygge-rækkefølge (inkrementel)

### Fase 1: Styrk det eksisterende (1-2 timer)
1. **Token-tracking** — tilføj `log_tokens()` i save_checkpoint.py (15 linjer)
2. **Kill-switch** — tilføj kill-fil check i heartbeat.py + save_checkpoint.py (5 linjer)
3. **Budget-cap** — læs token_usage.jsonl, stop hvis daglig grænse overskredet (20 linjer)

### Fase 2: HEARTBEAT.md config (2-3 timer)
4. **Skriv HEARTBEAT.md** — definér checks, signals, thresholds
5. **Refaktorér heartbeat.py** — læs config fra HEARTBEAT.md i stedet for hardcoded sources
6. **Mini-claw dagbog** — heartbeat skriver til `data/heartbeat_log.jsonl`

### Fase 3: Intelligent gating (2-3 timer)
7. **Signal-baseret LLM** — kun kald Groq når et check finder noget nyt
8. **Proaktiv follow-up** — morning brief refererer gårsdagens episoder
9. **Telegram input** — polling + dispatch til relevante scripts

### Total estimat: ~6-8 timer arbejde for en fuld mini-claw

---

## 9. Hvad dette IKKE er

- Ikke en autonom agent der tager beslutninger
- Ikke et framework der kræver installation
- Ikke OpenClaw (430K linjer, Node.js, $2-5K/måned)
- Ikke en erstatning for Claude Code sessions

Det er: **3-4 Python scripts der allerede eksisterer, styrket med config-fil, token-tracking, og bedre gating.** Den billigste vej fra "hooks der kører" til "mini-claw der vedligeholder sig selv."

---

## 11. Kilder og referencer

### Primærkilder (Yggdra-intern research, verificerbar på disk)
- OpenClaw deep dive: `research/openclaw_deep_dive_2026-03-15.md` — heartbeat-pattern, 3-lags hukommelse, cost-analyse
- Agents & automation destillat: `research/DESTILLAT_agents_automation.md` — L0-L5 automationsspektrum, compounding reliability
- Zero-token pipelines: `research/zero_token_pipeline_architecture.md` — gate-keeper pattern, cost-estimater
- Memory & autonomi research: `research/memory_autonomy_research_2026-02-23.md` — Mem0/LightRAG/OpenClaw evaluering
- Voice memo transkription: `data/inbox/voice_260316_transcript.txt` — mini-claw vision, filesystem-watcher design

### Ekstern prissætning (verificerbar)
- Anthropic. (2025). Claude API pricing. https://www.anthropic.com/pricing — Opus: $15/MTok input, $75/MTok output
- Groq. (2026). API pricing: Free tier. https://groq.com/pricing — llama-3.3-70b-versatile gratis på free tier

### Kodebase-referencer (verificerbar via `git log`)
- `scripts/save_checkpoint.py` — Stop/PreCompact hook implementation
- `scripts/load_checkpoint.sh` — SessionStart hook
- `scripts/heartbeat.py` — Eksisterende regelbaseret heartbeat
- `data/HEARTBEAT.md` — Config-fil (oprettet i denne session)

### Transparens
- Arkitekturforslaget er forfatterens (Claude/Yggdra) analyse baseret på ovenstående kilder
- Token-cost estimater er beregnet ud fra observeret brug i save_checkpoint.py (Groq usage API-response)
- Adversarial vurdering (sektion 10) er forfatterens kritiske analyse, ikke eksternt verificeret

---

## 10. Adversarial vurdering

### Steelman
- Bygger på 80% eksisterende kode — minimal ny kompleksitet
- $0/dag via Groq — ingen cost-risiko
- HEARTBEAT.md som config = behavior-ændring uden deploy
- Kill-switch + budget-cap = sikker at eksperimentere med

### Red team
- **"Mini-claw" er bare et fancy navn for cron + scripts** — ja, og det er pointen. I praksis dækker regelbaseret automation (cron + state-filer) langt de fleste vedligeholdelsesbehov uden LLM-involvering (se automationsspektrum L0-L5 i `research/DESTILLAT_agents_automation.md`, afsnit 1.2).
- **Groq free tier kan forsvinde** — Haiku fallback er $0.005/dag, acceptabelt.
- **HEARTBEAT.md kan blive stale** — tilføj "last_updated" check, advar hvis >7 dage gammel.
- **612 episoder i episodes.jsonl vokser ubegrænset** — tilføj rotation (behold 90 dage, arkivér resten).

### Neutral vurdering
Arkitekturen er sund fordi den respekterer zero-token princippet og bygger inkrementelt. Den største risiko er ikke teknisk men adoption — bruges det faktisk dagligt? Fase 1 (token-tracking + kill-switch) bør deployes og evalueres før fase 2-3.
