# Session-drift Pipeline

**Dato:** 2026-03-10
**Klar til:** PoC-klar (mangler: implementation af MVP hooks)

## Opsummering
- Nul-friktions session-management via Claude Code hooks (SessionStart, PostToolUse, PreCompact, SessionEnd)
- Research viser: 17 lifecycle events tilgængelige, hooks kan udføre fil-operationer direkte
- Arkitektur i 4 lag: auto-capture → pre-compaction save → state-audit → cross-session timeline

## Origin Story
Opstod fra idé-parkering: "Session-drift pipeline (M7): Automatisér den daglige drift-loop." Yttre mister kontekst mellem sessioner fordi hooks kun *minder* men ikke *udfører*. VPS har fuldt hook-system (save_checkpoint.py + load_checkpoint.sh via Groq) — PC-løsningen skal gøre det samme uden ekstern API.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-06-session-drift-research.md (681 linjer, dato 2026-03-10). Indeholder: komplet lifecycle event-tabel (17 events), gap-analyse, hook-begrænsninger, arkitektur-forslag med kode-eksempler for alle 4 hooks, implementeringsplan i 4 faser, VPS-sammenligning, kilder.

**Fra PLAN.md idé-parkering:**
> Session-drift pipeline (M7): Automatisér den daglige drift-loop: state-capture (NOW.md, PROGRESS.md, chatlog) ved commits, session-kontinuitet ved start, og OODA-baseret løbende state-audit.
