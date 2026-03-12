# Context Engineering Research — Claude Code Session Continuity

**Dato:** 2026-03-11
**Formål:** Praktiske mønstre for at bevare kontekst på tværs af Claude Code sessioner
**Kilder:** Anthropic officiel dokumentation, Anthropic engineering blog, community patterns

---

## 1. Anthropic's Officielle Anbefalinger

### CLAUDE.md Struktur

**Kilde:** [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) + [How Claude remembers your project](https://code.claude.com/docs/en/memory)

**Nøgleprincip:** Context window er den vigtigste ressource. Alt i CLAUDE.md spiser tokens FØR arbejdet begynder.

**Størrelse:** Max ~200 linjer per CLAUDE.md. Længere filer = lavere adherence.

**Hvad der skal ind:**
- Bash-kommandoer Claude ikke kan gætte
- Code style-regler der afviger fra defaults
- Test-instruktioner og foretrukne test-runners
- Repo-etikette (branch naming, PR-konventioner)
- Arkitektur-beslutninger specifikke for projektet
- Dev environment quirks (required env vars)
- Gotchas og non-obvious behaviors

**Hvad der IKKE skal ind:**
- Noget Claude kan finde ud af ved at læse koden
- Standard language-konventioner Claude allerede kender
- Detaljeret API-dokumentation (link i stedet)
- Info der ændrer sig ofte
- Lange forklaringer eller tutorials
- Fil-for-fil beskrivelser af codebasen
- Self-evident practices som "write clean code"

**Tommelfingerregel:** For hver linje, spørg: "Ville Claude lave fejl uden denne instruktion?" Hvis nej, slet den.

### Filhierarki (Scope)

| Scope | Placering | Formål |
|-------|-----------|--------|
| Managed policy | `C:\Program Files\ClaudeCode\CLAUDE.md` | Org-wide (IT/DevOps) |
| Projekt | `./CLAUDE.md` eller `./.claude/CLAUDE.md` | Team-delt via git |
| Bruger | `~/.claude/CLAUDE.md` | Personlige prefs, alle projekter |

Mere specifik scope trumfer bredere scope. CLAUDE.md i parent directories indlæses ved launch. CLAUDE.md i subdirectories indlæses on-demand.

### @import Syntax

```markdown
See @README.md for project overview
@docs/git-instructions.md
@~/.claude/my-project-instructions.md  # Personligt, ikke i git
```

Max 5 niveauer deep. Relative paths resolver fra filen der importerer.

### .claude/rules/ — Modulær Instruktions-Arkitektur

```
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md      # Altid indlæst
    ├── testing.md          # Altid indlæst
    └── api-design.md       # Kan scopes med paths
```

**Path-specifik scoping** med YAML frontmatter:
```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All API endpoints must include input validation
```

Regler UDEN `paths` indlæses ved launch. Med `paths` triggers kun når Claude arbejder med matchende filer.

### Auto Memory

**Kilde:** [How Claude remembers your project](https://code.claude.com/docs/en/memory)

- Claude skriver noter til sig selv automatisk (build commands, debugging insights, arkitektur-noter)
- Gemmes i `~/.claude/projects/<project>/memory/MEMORY.md`
- Første 200 linjer indlæses ved session start
- Topic-filer (`debugging.md`, `api-conventions.md`) læses on-demand
- Alle worktrees i samme git repo deler memory-mappe
- `/memory` kommando viser hvad der er indlæst + toggle auto memory

**Struktur:**
```
~/.claude/projects/<project>/memory/
├── MEMORY.md              # Index, altid indlæst (max 200 linjer)
├── debugging.md           # Topic-fil, on-demand
├── api-conventions.md     # Topic-fil, on-demand
└── ...
```

### Session Management

- `claude --continue` — genoptag seneste samtale
- `claude --resume` — vælg fra nylige sessioner
- `/rename` — giv sessioner beskrivende navne
- `/clear` — nulstil kontekst mellem urelaterede opgaver
- `/compact <instructions>` — komprimér med fokus, f.eks. `/compact Focus on the API changes`
- `/rewind` — gendan til checkpoint (samtale, kode, eller begge)
- `/btw` — side-spørgsmål der ikke forurener kontekst
- CLAUDE.md overlever compaction fuldt (genindlæses fra disk)

---

## 2. Anthropic Engineering Blog — Context Engineering Patterns

### Komprimering (Compaction)

**Kilde:** [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Prioritér recall først (fang ALT relevant), derefter precision (fjern overflødigt).

**Tool result clearing:** Fjern rå tool outputs dybt i historikken — sikker, letvægts-compaction.

**Claude Code's metode:** Modellen opsummerer kritiske detaljer (arkitekturbeslutninger, bugs, implementeringsspecifikke ting) mens redundante outputs fjernes, derefter fortsætter med komprimeret kontekst + 5 senest tilgåede filer.

**CLAUDE.md instruktion til compaction:**
```markdown
When compacting, always preserve the full list of modified files and any test commands
```

### Strukturerede Noter (Agentic Memory)

Agenten skriver persistente noter UDENFOR context window, hentes senere. Fordele:
- Tracker fremskridt i komplekse opgaver
- Vedligeholder kritiske afhængigheder der ellers tabes
- Muliggør multi-time kontinuitet

**Mønster:** Vedligehold en NOTES.md eller todo-liste. Pokémon-eksemplet: "precise tallies across thousands of game steps."

### Sub-Agent Arkitektur

Specialiserede sub-agents med rene context windows → kondenserede opsummeringer (1000-2000 tokens) til hovedagent.

**Konkret brug:** `"Use subagents to investigate how our auth system handles token refresh"` — sub-agenten udforsker, læser filer, rapporterer. Hovedkontekst forbliver ren.

### Multi-Context Window Handoff

**Kilde:** [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**claude-progress.txt mønster:** Kronologisk log af agent-handlinger. Nye sessioner læser denne fil for at forstå hvad der er sket.

**To-fase arkitektur:**
1. **Initializer** — etablerer fundament (scripts, feature list, baseline commit)
2. **Coding agents** — modtager anden prompt men samme tooling, laver "incremental progress in every session, while leaving clear artifacts"

**Session-initialiserings-protokol:**
1. Læs current directory og environment state
2. Gennemgå progress notes og git history
3. Læs feature list, vælg højest-prioritet ufærdig opgave
4. Kør init.sh for at verificere working state
5. Kør end-to-end tests før nyt arbejde

**Feature tracking i JSON** (agenten ændrer kun `passes` feltet):
```json
{
  "category": "functional",
  "description": "feature description",
  "steps": ["step 1", "step 2"],
  "passes": false
}
```

---

## 3. Progressive Disclosure — Det Centrale Mønster

### Tre-lags Arkitektur

**Kilde:** [Stop Bloating Your CLAUDE.md](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/) + [Skills as engineering pattern](https://glenrhodes.com/claude-skills-and-progressive-context-disclosure-as-a-real-engineering-pattern-not-prompt-engineering/)

**Lag 1: CLAUDE.md (altid indlæst) — ~50 linjer**
```markdown
# Project Name
Brief description (2-3 sentences).

## Commands
pnpm dev          # Start dev server
pnpm lint:fix     # Auto-fix linting issues

## Stack
- Nuxt 4, @nuxt/content v3

## Further Reading
**IMPORTANT:** Read relevant docs below before starting any task.
- @docs/architecture.md
- @docs/testing-strategy.md
```

**Lag 2: /docs eller .claude/rules/ (on-demand)**
```
docs/
├── nuxt-content-gotchas.md    # Non-obvious situationsspecifikke patterns
├── testing-strategy.md        # Hvornår hvilken test-type
└── SYSTEM_KNOWLEDGE_MAP.md    # Arkitekturoversigt
```

**Lag 3: .claude/skills/ (aktiveres ved behov)**
```
.claude/skills/
├── fix-issue/SKILL.md
├── api-conventions/SKILL.md
└── deploy/SKILL.md
```

### Kritisk Instruktion i CLAUDE.md

Uden denne linje læser Claude IKKE automatisk supplerende docs:
```markdown
**IMPORTANT:** Before starting any task, identify which docs are relevant and read them first.
```

### Skills Struktur

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true   # Kun manuelt triggeret
---
```

- `disable-model-invocation: true` = kun via `/skill-name` (workflows med side effects)
- Uden dette flag: Claude aktiverer automatisk når relevant
- Hold SKILL.md under 500 linjer, split references til separate filer

### Hvad der IKKE skal i CLAUDE.md

> "If a tool can enforce it, don't write prose about it."

- Style-regler som ESLint/Prettier håndhæver
- Type-konventioner som TypeScript håndterer
- Formatering i config-filer

---

## 4. Community Patterns — Hvad der Virker i Praksis

### Hybrid Memory (3-lags)

**Kilde:** [3 ways to fix Claude Code's memory](https://dev.to/gonewx/i-tried-3-different-ways-to-fix-claude-codes-memory-problem-heres-what-actually-worked-30fk)

| Tilgang | Styrke | Svaghed |
|---------|--------|---------|
| CLAUDE.md + daterede noter | Claude absorberer godt skrevne opsummeringer | Kræver disciplin (skippes ~40% af tiden) |
| SQLite via MCP | Persistent knowledge, overlever alt | Claude bruger det ikke autonomt uden prompting |
| Session replay + git state | Tids-rejse debugging, finder præcist øjeblik | Kræver manual review |

**Bedste kombination:** Alle tre sammen → ~80% kontinuitet.

### Living Artifacts > Conversation History

**Kilde:** [Context Engineering for Claude Code](https://clune.org/posts/anthropic-context-engineering/)

**Nøgleindsigt:** Forsøg ikke at bevare fuld samtalehistorik. Skab i stedet **living artifacts** (scripts, tests, dokumentation) som nye context windows kan læse og udvide.

- **Scripts** — automatiserede tools indlejrer viden permanent
- **JSON filer** — modeller har modstand mod at omskrive JSON (behandler det som "kode")
- **Git commits** — checkpoint arbejde ved context window-grænser
- **Foretruk fresh start over compaction** — nulstil kontekst, brug git

### Context Rot — Fire Typer

**Kilde:** [Context Engineering Secrets from Anthropic](https://01.me/en/2025/12/context-engineering-from-claude/)

| Type | Problem |
|------|---------|
| **Context Poisoning** | Forkert/forældet info korrumperer reasoning |
| **Context Distraction** | Irrelevant info reducerer fokus |
| **Context Confusion** | Lignende men distinkt info blandes sammen |
| **Context Clash** | Modstridende info skaber usikkerhed |

**Løsning:** Regelmæssig pruning af CLAUDE.md og memory-filer. Behandl dem som kode — review, prune, test om adfærd ændrer sig.

### /learn Feedback Loop

**Kilde:** [Stop Bloating Your CLAUDE.md](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/)

1. Claude laver fejl under udvikling
2. Fix det sammen i samtalen
3. Kør `/learn` (eller manuelt) for at ekstrahere reusable insight
4. Gem i relevant `/docs` fil
5. Næste session indlæser doc automatisk

Skaber en "curated knowledge base of exactly the things AI coding tools get wrong" i din specifikke codebase.

---

## 5. Konkrete Anbefalinger for Basic Setup

Baseret på al research, her er hvad der er relevant for dette projekts nuværende state:

### A. CLAUDE.md Pruning

Nuværende `~/CLAUDE.md` og projekt-CLAUDE.md er begge fornuftige men kan strammes. Check:
- Er der linjer Claude ville følge alligevel? (slet dem)
- Er der konflikter mellem de to filer? (fjern overlap)
- Kan detaljerede sektioner flyttes til `.claude/rules/` med path-scoping?

### B. NOW.md som Progress File

NOW.md-mønsteret ligner Anthropic's `claude-progress.txt` mønster for multi-context handoff. Det er korrekt arkitektur. Forbedring:
- Tilføj eksplicit instruktion i CLAUDE.md: `Read NOW.md at session start for current state`
- Hold "Næste step" sektionen som det FØRSTE i filen
- Overvej at splitte "hvad sessionen producerede" til separat fil (det fylder i context)

### C. Auto Memory Audit

Tjek `~/.claude/projects/*/memory/MEMORY.md` — den eksisterer allerede og indlæses. Sørg for at den ikke konflikter med manuelle CLAUDE.md instruktioner.

### D. Skills som Progressive Disclosure

De 6 eksisterende skills i `.claude/skills/` følger allerede best practice. Overvej:
- Er der instruktioner i CLAUDE.md der kun er relevante for specifikke tasks? → Flyt til skills
- `disable-model-invocation: true` for skills med side effects

### E. Session-Kontinuitet uden Hooks

PC har ingen auto-save hook. Tre pragmatiske løsninger:
1. **Compaction-instruktion i CLAUDE.md:** `When compacting, always preserve current task state and modified files list`
2. **Git som checkpoint:** Commit hyppigt med beskrivende messages — nye sessioner kan `git log --oneline`
3. **claude --continue:** Brug det aktivt i stedet for at starte fra scratch

---

## Kilder

- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — Anthropic officiel
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — Anthropic officiel
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic Engineering Blog
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Anthropic Engineering Blog
- [Stop Bloating Your CLAUDE.md](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/) — alexop.dev
- [Claude Skills as engineering pattern](https://glenrhodes.com/claude-skills-and-progressive-context-disclosure-as-a-real-engineering-pattern-not-prompt-engineering/) — Glen Rhodes
- [Context Engineering for Claude Code](https://clune.org/posts/anthropic-context-engineering/) — Arthur Clune
- [Context Engineering Secrets from Anthropic](https://01.me/en/2025/12/context-engineering-from-claude/) — Bojie Li
- [3 ways to fix Claude Code's memory](https://dev.to/gonewx/i-tried-3-different-ways-to-fix-claude-codes-memory-problem-heres-what-actually-worked-30fk) — DEV Community
- [Claude Code Session Memory](https://claudefa.st/blog/guide/mechanics/session-memory) — claudefa.st
- [Skills architecture](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Anthropic Platform Docs
