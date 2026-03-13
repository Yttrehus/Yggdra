# Context Engineering

**Dato:** 2026-03-12
**Klar til:** Backlog (research udført, klar til PoC/DLR)

## Opsummering
- Systematisér hvordan Claude Code bruges effektivt: CLAUDE.md, compaction, skills, session-management, subagents
- Research udført med 8 kilder (Anthropic officiel + community) — gemt i research/_ARC/context-engineering-research.md
- Trukket ud af PLAN.md M7 som selvstændigt pipeline-projekt

## Origin Story
Startede som M7 i PLAN.md: "Context engineering — Systematisér hvordan Claude Code bruges effektivt." I session 10 blev det klart at dette var for stort til et modul og blev trukket ud som selvstændigt projekt. Research udført: @import syntax, .claude/rules/, compaction-instruktioner, ~80% kontinuitet er realistisk mål. Tæt relateret til session-drift-pipeline (hooks) og research-architecture (praksis).

## Rå input
**Research:** research/_ARC/context-engineering-research.md (8 kilder, session 10)

**Fra PLAN.md M7:**
> Formål: Systematisér hvordan Claude Code bruges effektivt. Samler indsigter fra alle moduler.
> 1. CLAUDE.md best practices (under 200 linjer, progressive disclosure)
> 2. Compaction-strategi (hvornår, hvordan, hooks)
> 3. Skills-arkitektur (hvad er et skill, hvornår laves et nyt)
> 4. Session-management (NOW.md, plan-filer, hooks)
> 5. Subagent-strategi

**Fra ADR backlog:**
> Context engineering som selvstændigt projekt — research i research/_ARC/context-engineering-research.md
