# Automation Patterns — Inventar & State of the Art (marts 2026)

**Kilder:** crontab -l, automation-audit.md, CH6_AGENTS_AUTOMATION.md, autonomous_ai_setup.md, CLAUDE.md

---

## 1. Yttres Automation Inventar

### Docker Services (always-on)
| Service | Funktion | Status |
|---------|----------|--------|
| traefik | Reverse proxy, TLS | Aktiv |
| webapp (nginx) | TransportIntra webapp | Aktiv |
| qdrant | Vector DB (7 coll, ~84K points) | Aktiv |
| api-logger | Logger API-kald | Aktiv |
| tor-proxy | YouTube/privacy proxy (port 9150) | Aktiv (system service) |

### Cron Jobs (aktive)
| Tid | Script | Type | Cost |
|-----|--------|------|------|
| 04:00 | backup_offsite.sh | L1: Backup | $0 |
| 06:15 søn | ai_intelligence.py --weekly | L4: LLM digest | Groq (gratis) |
| 06:30 | ai_intelligence.py | L4: LLM intelligence | Groq |
| 06:30 søn | cruft_detector.py | L1: Filsystem scan | $0 |
| 06:00 søn | weekly_audit.py | L1: 22-punkt audit | $0 |
| 05:00 søn | embed_advisor_brain.py | L1: Re-embedding | OpenAI ($<0.10) |
| 05:00 søn | embed_docs.py | L1: Re-embedding | OpenAI ($<0.10) |
| 07:00 | youtube_monitor.py | L4: YT + embed | OpenAI |
| 08:00 | daily_sweep.py | L4: Autonom sweep | Groq |
| 08:00 søn | source_discovery.py | L4: Kilde-søgning | OpenAI |
| 23:55 | auto_dagbog.py | L4: Session→dagbog | Groq |
| Hver time | process_session_log.py (6h) | L1: Log parsing | $0 |
| Hver time | tmux pipe-pane rotation | L1: Logging | $0 |
| Hver time :45 | hotmail_autosort.py | L4: Mail-sortering | API |

### Cron Jobs (disabled)
| Script | Årsag |
|--------|-------|
| morning_brief.py | Disabled session3 |
| score_knowledge_batch.py | Disabled session3 |
| heartbeat.py | Disabled session3 |
| sync_inbox.py | Trello droppet |
| voice_memo_pipeline.py | Voice memos ikke aktive |
| navigator.py | Deaktiveret 2026-02-01 |

### Claude Code Hooks
| Event | Script | Funktion |
|-------|--------|----------|
| SessionStart | load_checkpoint.sh | Injicerer NOW.md + episoder |
| Stop | save_checkpoint.py | Destillerer session → episodes.jsonl + NOW.md |
| PreCompact | save_checkpoint.py | Pre-compaction flush |
| Notification | check_trello_pending.sh | Trello → kontekst (Trello droppet) |

**Total:** 4 Docker services, ~12 aktive cron jobs, ~5 disabled, 4 hooks.

---

## 2. Automation Patterns (teori)

### Pattern 1: Scheduled Batch (L1)
Cron + Python script. Kør på tidsplan, processér batch, skriv resultat til disk.
- **Yttres brug:** backup, embedding, audit, dagbog
- **Styrke:** 100% reliability, $0, ingen dependencies
- **Svaghed:** Ingen realtime, ingen kontekst-bevidsthed

### Pattern 2: Event-Driven (L2)
Webhook/file-watcher trigger → script kører.
- **Yttres brug:** Claude Code hooks (SessionStart, Stop, PreCompact)
- **Styrke:** Reagerer på reelle events, ikke tidsplan
- **Svaghed:** Kræver hook-infrastruktur

### Pattern 3: Polling (L2)
Periodisk check for ændringer → reagér hvis nyt.
- **Yttres brug:** hotmail_autosort, youtube_monitor, source_discovery
- **Styrke:** Simpelt, robust
- **Svaghed:** Latency (polling interval), spild-kald

### Pattern 4: LLM-in-the-Loop (L4)
Deterministisk pipeline med ét LLM-beslutningspunkt.
- **Yttres brug:** daily_sweep (Groq klassificerer), ai_intelligence (Groq scorer)
- **Styrke:** Billigt (Groq gratis), reliability 90-95%
- **Svaghed:** LLM-fejl propagerer, ingen self-correction

### Pattern 5: Ralph Loop (L5)
`claude --print` i loop med LOOP_STATE.md som shared state.
- **Yttres brug:** Sandbox v1-v3, dette AI Frontier loop
- **Styrke:** Fuld Claude-capability, alt på disk, fuld visibility
- **Svaghed:** Ingen auto-recovery, context loss over iterationer, dyrt

### Pattern 6: Heartbeat Daemon (L4-L5)
Periodisk check af inboxes → spawn agent ved arbejde.
- **Yttres brug:** heartbeat.py (disabled)
- **Styrke:** Proaktiv, bruger kun tokens når der er noget at gøre
- **Svaghed:** Kræver polling-logik, risk for runaway

---

## 3. Automation Spectrum — Yttres Position

```
L0 Manual     ████████████████  (daglige opgaver)
L1 Cron       ████████████      (12 aktive jobs)
L2 Events     ████              (4 hooks)
L3 Workflow   ░░░░              (droppede n8n)
L4 LLM-loop   ████████          (intelligence, dagbog, sweep)
L5 Agent      ██                (Ralph loops, eksperimentelt)
```

**Observation:** Yttre har solid L1+L2+L4 men springer L3 over. n8n var der men blev droppet. Spørgsmålet er om L3 er nødvendigt eller om L1→L4 spring er fint.

**Svar:** For solo setup er L3 (workflow engine) unødvendigt. Bash scripts med LLM-kald (L4) giver samme funktionalitet uden ekstra service. L3 er mest værdifuldt ved team-brug og visual debugging.

---

## 4. Proaktiv AI — Hvad Andre Gør

### OpenClaw (430K LOC)
- Telegram/WhatsApp/Discord input
- Auto-PRs, Sentry integration, heartbeat
- **For stor for solo.** Men principper er gode: heartbeat + inbox polling.

### PicoClaw
- Enkelt binary, Groq Whisper, kører på $10 hardware
- **Relevant:** Minimal autonom agent

### MOM (Zechner/Ronacher)
- Slack-bot: log.jsonl + context.jsonl + MEMORY.md per kanal
- Selvforvaltende: installerer deps, skriver CLI-wrappers
- **Relevant:** State-per-kanal pattern

### Claude Code Scheduler
- NLP scheduling ("every weekday at 9am")
- Git worktree isolation
- **Relevant:** Laveste effort for bedre autonomi

---

## 5. Modenhedsvurdering

| Pattern | Modenhed | Relevans for Yttre | Effort |
|---------|----------|-------------------|--------|
| Cron + scripts (L1) | Production-ready | Allerede i brug | - |
| Event hooks (L2) | Production-ready | Allerede i brug | - |
| Workflow engine (L3) | Production-ready | Droppet (korrekt) | - |
| LLM-in-loop (L4) | Production-ready | Allerede i brug | - |
| Ralph loops (L5) | Early adopter | I brug, mangler guardrails | Timer |
| Heartbeat daemon | Early adopter | Disabled, bør genaktiveres | Timer |
| Proaktiv AI (full) | Eksperimentel | Nice to know | Uger |

---

## DEL 2: Miessler PAI & Nate Jones Principper

---

## 6. Miessler AIMM (AI Impact Maturity Model)

5 niveauer for AI-modenhed:

| Level | Navn | Beskrivelse | Yttre er her? |
|-------|------|-------------|---------------|
| 0 | Natural | Pre-AI. Alt manuelt. | Nej |
| 1 | Chatbots | Spørg → svar. Menneske handler. | Delvist |
| 2 | **Agentic** | Agenter med kontekst og handlingsevne. Menneske orkestrerer. | **JA** |
| 3 | Workflows | Permanente flows, automatiserede forretningsprocesser | Delvist (cron) |
| 4 | Managed | AI styrer alt, menneske overvåger | Nej |

**Yttre sidder primært på Level 2** med elementer af Level 3 (cron jobs, hooks).
Miessler: "Move as fast as possible to Level 2. Build an agentic platform. Get your context into it."

**PAIMM (Personal version):** 9 niveauer i 3 tiers (Chatbots → Agents → Assistants). Toppen (AS3) = den digitale assistent Miessler beskrev i 2016.

---

## 7. Miessler PAI Arkitektur

Miesslers PAI system ("Kai"):

### Kerneelementer
- **Multi-provider agents:** Claude researcher + Gemini researcher + Grok researcher, parallelt
- **Voice:** ElevenLabs stemmer til hvert agent-resultat
- **Visualization server:** Se agenter arbejde i realtid
- **Skills system:** Modulære capabilities (research, web scraping, art, entropy)
- **TELOS:** Goal management framework (GitHub repo) — definerer IDEAL STATE
- **Daemon:** "Giv alt et API" — execution layer

### The Last Algorithm
Miesslers kerneprincip:
```
Loop:
  1. Observér CURRENT STATE
  2. Sammenlign med IDEAL STATE
  3. Tag den optimale handling for at lukke gabet
  4. Gentag
```

**Direkte parallel til Yttre:** MISSION.md (ideal state) → NOW.md (current state) → session handling (lukke gap). Yttre gør dette allerede, men manuelt. Miessler automatiserer det.

### Hvad Yttre kan adoptere
1. **The Last Algorithm som cron:** Periodisk sammenlign NOW.md med MISSION.md → identificér gaps → prioritér
2. **Multi-provider research:** Brug Groq+OpenAI parallelt (allerede muligt via scripts)
3. **Skills som modulært system:** Allerede implementeret (.claude/skills/)

---

## 8. Nate Jones Principper

### De 5 Kerneindsigter (fra 5 videoer)

**1. Context Engineering > Domain Memory**
"Domain memory er biblioteket. Context engineering er hvad der ligger på skrivebordet."
→ Yttre gør dette: ctx --limit 5, skills-system, CLAUDE.md

**2. Human Throttle**
Reversibilitet afgør om AI kan handle autonomt. 5 primitiver:
- Comfort zones, undo-infrastruktur, human throttle, reversibilitet, bounded operations
→ Yttre: Git + backup + verify-princip. **Mangler:** staging-miljø

**3. Non-Engineer Builder**
"De der bygger AI-native systemer først, får uindhentelig fordel."
→ Yttre = præcis denne case: lastbilchauffør → AI-native system builder

**4. Compounding Gap**
Forskel mellem forberedte og uforberedte vokser eksponentielt.
→ Yttre er på den rigtige side — allerede 60+ research-filer, 84K vektorer

**5. Attention Drowning**
Selv med 100K+ tokens forringes reasoning. Signal drukner i støj.
→ Yttre addresserer dette via fokuseret retrieval (ctx --limit 5)

### Jones vs. Miessler — Sammenligning

| Dimension | Jones | Miessler | Yttre |
|-----------|-------|---------|-------|
| Fokus | Strategi, reversibilitet | Byg, automatisér | Hybrid |
| Modenhed | Enterprise-orienteret | Solo builder | Solo builder |
| Kernemetafor | "Human throttle" | "The Last Algorithm" | "Bash-first" |
| Arkitektur | Context engineering | Multi-agent + skills | Skills + hooks |

---

## 9. Samlet Automation Roadmap

### Allerede på plads (ingen handling)
- L1 cron (12 aktive jobs)
- L2 hooks (SessionStart, Stop, PreCompact)
- L4 LLM-in-loop (intelligence, dagbog, sweep)
- Skills system (.claude/skills/)
- Episodisk log (episodes.jsonl + NOW.md)

### Lav effort, høj impact (Timer)
1. **Genaktivér heartbeat.py** — proaktiv inbox-scanning
2. **Circuit breakers på Ralph loops** — max_turns, timeout, cost cap
3. **The Last Algorithm som weekly cron** — sammenlign NOW.md ↔ MISSION.md

### Moderat effort (Dage)
4. **Multi-provider research** — Groq + OpenAI parallelt i research.py
5. **Staging for webapp** — preview-system før produktion
6. **Bedre episodisk retrieval** — ctx-søg i stedet for seneste 5

### Fremtid (Uger)
7. **Voice-first interface** — Whisper + Claude + ElevenLabs (Miessler-style)
8. **Automatisk gap-detection** — The Last Algorithm automatiseret
9. **Event-driven arkitektur** — file watchers, webhook endpoints
