# Konvergens-vurdering — PC vs VPS

## Hvor er de i sync?

- **Qdrant som hukommelsesbackend** — begge bruger det, begge via SSH-tunnel fra PC.
- **memory.py** — PC-version er porteret til VPS (`scripts/memory.py`). Samme kodebase.
- **Episoder + knowledge** — begge bruger samme to collections. VPS har bare mere data (6.626 vs 984 knowledge points).
- **Voice memo pipeline** — begge sider virker (Groq Whisper på VPS, renskrivning på PC).
- **CLAUDE.md-ånden** — begge siger "sig det kort, bare gør det, state på disk."

## Hvor divergerer de?

| Dimension | PC | VPS | Gap |
|---|---|---|---|
| **Knowledge points** | 984 | 6.626 | VPS har 6x mere. PC har ikke ingestet VPS's docs-migration |
| **Search default** | Hybrid RRF | Dense-only (83% vs 61%) | PC bruger den dårligere metode |
| **State-management** | Manuelt CONTEXT.md | Auto NOW.md per projekt via hooks | VPS er automatiseret, PC er manuelt |
| **Hooks** | 2 (suggest-compact, check-git-commit) | Fuldt system (SessionStart, Stop, PreCompact, Notification) | PC mangler 80% af hook-systemet |
| **Projekt-navne** | Stage-præfiks (BMS./REF./LIB.) | Simple navne (transport/assistent/rejse) | Inkompatibelt |
| **Credentials** | Ikke centraliseret | credentials.py med rate-limiting | PC mangler |
| **Cron/automation** | Ingen | 17+ aktive jobs | VPS er selvkørende, PC er manuelt |
| **Prompt mining** | Ikke til stede | 1.270 prompts analyseret, daglig pipeline | Kun på VPS |
| **Session tracking** | chatlog-engine (v3, 3000 beskeder) | episodes.jsonl + daglig checkpoint | Forskellige systemer |

## VPS-beslutninger der påvirker PC-planer

**1. Dense > Hybrid** — PC's memory.py skal have dense-only som default. Hele eval-suiten (20 queries) skal køres mod dense, ikke hybrid. Dette invaliderer dele af session 24's arbejde.

**2. Reformation Blueprint** — VPS foreslår "Shared Repo, Split State" med 6 åbne beslutninger. Hvis dette vedtages, ændrer det:
- Projekt-navngivning (PC's BMS./REF. vs VPS's simple navne)
- State-filer (NOW_vps.md / NOW_pc.md split)
- Hook-systemet (portér VPS-hooks til PC)
- CLAUDE.md merge

**3. brief.memory-architecture.md er forældet** — v1 er live. Kan lukkes.

**4. VPS har allerede implementeret ting PC har i backlog:**
- `automation-index` → VPS har 17 cron jobs, heartbeat, prompt miner
- `context-engineering` → VPS har prompt mining, INSIGHTS.md, PROMPT_KATALOG.md
- `research-architecture` → VPS har INDEX.md-struktur, destillater

## Filer i PC-repoet der skal opdateres

| Fil | Ændring |
|---|---|
| `scripts/memory.py` | Default search: hybrid → dense-only |
| `CONTEXT.md` | Tilføj session 25 med VPS-sync, opdatér hukommelsesarkitektur-status |
| `projects/0_backlog/brief.memory-architecture.md` | Luk (v1 er live) |
| `projects/0_backlog/TRIAGE.md` | Opdatér: memory lukket, context-engineering er delvist dækket af VPS prompt mining |
| `projects/REF.prompt-skabeloner/` | Absorber VPS's PROMPT_KATALOG.md og INSIGHTS.md |

## Reformation Blueprint — er PC enig?

**Ja i retningen, nej i tempoet.**

Godt:
- Shared Repo, Split State er den rigtige arkitektur
- Maskin-ID i state-filer løser konflikter
- Qdrant centralt på VPS er allerede realiteten

Bekymringer:
- 6 åbne beslutninger kræver Yttres input — dette er ikke noget Claude kan beslutte
- Projekt-navngivning er en kulturel beslutning, ikke en teknisk
- Tempoet er forkert: hukommelsen virker, brug den først, reformér derefter
- "Spørg først" vs "bare gør det" er ikke binært — det afhænger af tillid til systemet

**Anbefaling:** Tag de 3 lavthængende: (1) dense-only default, (2) luk memory-brief, (3) absorber PROMPT_KATALOG. Parkér reformation til Yttre har levet med hukommelsen en uge.
