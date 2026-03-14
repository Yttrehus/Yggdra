# Work Intake

**Dato:** 2026-03-14
**Status:** Backlog
**Priority:** Medium-high (enabler for alt andet arbejde)

## Opsummering
- Prioriteret overblik over briefs og projekter i en enkelt fil — "hvad er vigtigst, og hvad er klar?"
- Modenhedstags i briefs (sketch → spec'd → ready) så man kan se forskel uden at åbne filen
- Synlige afhængigheder ("X blokerer Y") ét sted
- Session-forslag: baseret på prioritet + modenhed, hvad giver mening at tage fat på næste gang?

## Problem Statement
12 briefs i en mappe. Ingen rækkefølge. Prioritering sker i hovedet, afhængigheder lever i memory-filer (session 19: MCP/Skills ventede på Ydrasil INDEX.md). "Hvad skal næste session handle om?" er en beslutning uden systematisk input.

## Hvad det IKKE er
- Ikke sprints, ikke Jira-light, ikke acceptance criteria per task
- Ikke project-taxonomy (det dækker livscyklus — hvad et projekt ER. Dette dækker rækkefølge — hvad du GØR)
- Ikke et framework der kræver vedligeholdelse. Hvis det tager længere at opdatere end at gøre arbejdet, er det forkert

## Deliverables
1. **TRIAGE.md** i `projects/0_backlog/` — sorteret liste med modenhed + prioritet + afhængigheder. Én fil, flat, scanbar på 10 sekunder
2. **Frontmatter-tags** i eksisterende briefs — `maturity: sketch|brief|spec'd|ready` og `blocks: [...]` / `blocked-by: [...]`
3. **Triage-rytme** — ikke et møde, bare en vane: start af session → scan TRIAGE.md → vælg

## Skitse: TRIAGE.md format
```markdown
# Triage — Prioriteret overblik

Sidst opdateret: YYYY-MM-DD

## Klar
| Brief | Modenhed | Blokerer | Noter |
|-------|----------|----------|-------|
| research-architecture | ready | context-engineering | Kører på VPS sandbox v2 |

## Næste op
| Brief | Modenhed | Blokeret af | Mangler |
|-------|----------|-------------|---------|
| context-engineering | spec'd | research-architecture | Venter på INDEX.md |

## Ideer (ingen tidspres)
| Brief | Modenhed | One-liner |
|-------|----------|-----------|
| voice-integration | sketch | Voice memos → struktureret input |
```

## Scope-check
- Løser det et reelt problem? Ja — session-start beslutninger er uinformerede
- Er det værd at investere tid? Ja, men KUN hvis det forbliver en flad fil + et par tags. Minutters vedligeholdelse, ikke timers
- Overlap med project-taxonomy? Nej — taxonomy = livscyklus, dette = prioritering og rækkefølge

## Kill condition
Hvis TRIAGE.md ikke konsulteres i 5 sessioner efter oprettelse, slet den. Den skal være nyttig nok til at du faktisk åbner den.

## Origin Story
Session 20. Yttre delte en Google-guide om backlog management med Claude Code. 80% var ting Yggdra allerede gør. De 20% der manglede kogte ned til: der er ingen sorteret liste, ingen synlige afhængigheder, og "hvad skal jeg lave?" er en hovedbeslutning.
