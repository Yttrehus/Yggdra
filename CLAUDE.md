# Basic Setup (→ Yggdra)

Personligt udvikler-fundament. Startede som Windows-opsætning, vokset til framework for hvordan Yttre arbejder med AI og kode.

@CONTEXT.md

## Projekter

Alle projekter bor i `projects/`. Hvert projekt har en CONTEXT.md (samme format som rod-CONTEXT.md).
Idéer starter som briefs i `projects/backlog/`. Arkiv i `projects/archive/`.

## Hvad læses automatisk

Kun denne fil (CLAUDE.md) og CONTEXT.md (via @import). Alt andet læses efter behov.

## Kontekst-kilder (læses efter behov)

- PROGRESS.md — fuld narrativ per session, destilleret
- chatlog.md — komplet sessionsdata (roden, genereret af projects/auto-chatlog/chatlog-engine.js)
- projects/*/CONTEXT.md — projekt-specifik kontekst

## Workflow

- CONTEXT.md opdateres ved pauser, beslutninger, session-slut
- PROGRESS.md opdateres med fuld session-narrativ ved session-slut
- Commit + push efter hver logisk ændring
- State på disk — alt vigtigt overlever en session-crash
- Spørg før du bygger. Diskussion færdig → bekræftelse → kode.

## Kommunikation

- Brugeren gør tingene selv — Claude guider fra sidelinjen
- Ved multi-step: list alle steps kort → derefter ét step ad gangen
- Når Yttre stiller spørgsmål, vil han forstå — besvar ærligt

## Compaction

When compacting, always preserve: current task state, modified files, open decisions, active project context.
