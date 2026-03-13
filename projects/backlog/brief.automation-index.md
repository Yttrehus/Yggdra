# Automation Index

**Dato:** 2026-03-12
**Klar til:** Backlog

## Opsummering
- Levende index over alle automatiske hooks, workflows, cronjobs der kører uden brugerens vidende
- Formål: overblik og cruft-forebyggelse — vide hvad der kører, og hvornår noget bør slettes
- Erstatter den forældede references/automation.md (nu i research/_ARC/)

## Origin Story
Opstod i session 12 under fil-audit. automation.md eksisterede i references/ men var forældet og dækkede ikke det nuværende system. Yttre vil have et index der giver overblik over alt der kører automatisk — hooks på PC, cronjobs på VPS, scheduled tasks — så intet køres i skyggen. Cruft-forebyggelse: hvis noget kører men aldrig bruges, skal det opdages og fjernes.

## Rå input
**Eksisterende fil:** research/_ARC/automation.md (forældet, pre-reformation)

**Fra session 12 diskussion:**
> automation.md burde fungere som et index over igangværende automatiske hooks/workflows/cronjobs etc som kører uden at brugeren har mulighed for at se det uden at spørge. Det er for overblikkets skyld og for cruft-forebyggelse.
