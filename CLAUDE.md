# Basic Setup (→ Yggdra)

Personligt udvikler-fundament. Startede som Windows-opsætning, vokset til framework for hvordan Yttre arbejder med AI og kode.

@NOW.md

## Projekter

Alle projekter bor i `projects/`. Hvert projekt har en CONTEXT.md (samme format som rod-CONTEXT.md).
Idéer starter som briefs i `projects/backlog/`. Arkiv i `projects/archive/`.

## State-filer

- NOW.md — hvor vi er (start her)
- PLAN.md — hvad der skal gøres (moduler + rækkefølge)
- PROGRESS.md — hvorfor det ser ud som det gør (narrativ)

## Workflow

- PLAN.md opdateres efter hvert afsluttet step
- NOW.md opdateres automatisk — ved pauser, beslutninger, session-slut
- Commit + push efter hver logisk ændring
- State på disk — alt vigtigt overlever en session-crash
- Spørg før du bygger. Diskussion færdig → bekræftelse → kode.

## Kommunikation

- Brugeren gør tingene selv — Claude guider fra sidelinjen
- Ved multi-step: list alle steps kort → derefter ét step ad gangen
- Når Yttre stiller spørgsmål, vil han forstå — besvar ærligt

## Compaction

When compacting, always preserve: current task state, modified files, open decisions, active project context.
