# Decay Model — Videnshalveringstid

Viden forældes med forskellig hastighed. Denne model kategoriserer AI-viden efter halveringstid og angiver nuværende dækning i Yggdra.

## Kategorier

| Kategori | Halveringstid | Eksempler | Nuværende dækning | Pipeline |
|----------|---------------|-----------|---------------------|----------|
| Model releases & benchmarks | ~2-4 uger | Ny model, Elo-ændringer, SWE-bench scores | GOD — ai_intelligence fanger GitHub releases + HN + Reddit | ai_intelligence.py |
| API pricing & rate limits | ~1-3 måneder | Prisændringer, nye tiers, context window ændringer | MIDDEL — fanger announcements men ikke stille ændringer | ai_intelligence.py (indirekte via HN) |
| Tool/framework versioner | ~2-4 uger | Claude Code updates, MCP spec, Qdrant releases | GOD — GitHub release watch på 8 repos | ai_intelligence.py |
| Agent arkitekturer & patterns | ~3-6 måneder | Nye agent-patterns, workflow-design, prompt engineering | MIDDEL — YouTube kanaler + Reddit, men ingen systematisk re-scan | youtube_monitor.py |
| Research papers & breakthroughs | ~6-12 måneder | Nye teknikker (RAG, reasoning, memory), fundamentale papers | SVAG — arXiv scan er overfladisk (top 20 pr dag), ingen citation tracking | ai_intelligence.py (arXiv) |
| Provider strategi & konkurrence | ~3-6 måneder | Opkøb, partnerships, produkt-roadmaps, markedspositionering | SVAG — ingen dedikeret pipeline, afhænger af HN og Reddit | — |
| Infrastruktur best practices | ~6-12 måneder | Docker configs, Qdrant tuning, backup-strategier, deployment | INGEN — ren manual viden, ingen automatisk opdatering | — |
| Personlig setup-viden | ~1-3 måneder | Kris' credentials, server-config, script-stier, cron-jobs | GOD — checkpoint hooks, men ingen decay-markering | save_checkpoint.py |
| Lovgivning & compliance | ~12-24 måneder | EU AI Act, GDPR ændringer, copyright-lovgivning | INGEN — ikke tracket | — |
| Priser & abonnementer | ~1-3 måneder | SaaS-priser (Anthropic, hosting, domains, tools) | SVAG — kun fanget som side-effekt af andre pipelines | — |

## Decay-hastighed Visualisering

```
TIMER    DAGE     UGER     MÅNEDER    ÅR
|--------|--------|--------|----------|------>
         ▓▓▓ Model releases (2-4 uger)
                  ▓▓▓▓ API pricing (1-3 mdr)
         ▓▓▓ Tool versioner (2-4 uger)
                  ▓▓▓▓▓▓▓ Agent patterns (3-6 mdr)
                           ▓▓▓▓▓▓▓▓ Research papers (6-12 mdr)
                  ▓▓▓▓▓▓▓ Provider strategi (3-6 mdr)
                           ▓▓▓▓▓▓▓▓ Infra best practices (6-12 mdr)
                  ▓▓▓▓ Personal setup (1-3 mdr)
                                    ▓▓▓▓▓▓▓ Lovgivning (12-24 mdr)
                  ▓▓▓▓ Priser (1-3 mdr)
```

## Re-scan Prioritering

Baseret på halveringstid × nuværende dækning → prioritet:

| Prioritet | Kategori | Begrundelse |
|-----------|----------|-------------|
| **KRITISK** | Provider strategi | Kort halveringstid + INGEN dækning. Misser opkøb, pivots, pricing moves |
| **HØJ** | API pricing & rate limits | Stille ændringer fanges ikke. Kris betaler potentielt for meget |
| **HØJ** | Priser & abonnementer | Relateret til ovenstående men bredere (hosting, SaaS) |
| **MIDDEL** | Research papers | Lang halveringstid redder os, men arXiv-scan er overfladisk |
| **MIDDEL** | Agent patterns | YouTube dækker delvist, men ingen re-scan af ældre viden |
| **LAV** | Infrastruktur | Ændrer sig langsomt, manual viden holder |
| **LAV** | Lovgivning | Lang halveringstid, ikke akut relevant for Kris' setup |

## Implikationer for Pipeline-design

1. **Hurtig decay (uger):** Kræver daglig/ugentlig scanning. AI_intelligence håndterer dette rimeligt.
2. **Medium decay (måneder):** Kræver periodisk re-scan. MANGLER helt i nuværende setup. Bør trigges af tidsbaserede checks.
3. **Langsom decay (år):** Kan håndteres kvartalsvist via manual review. Lav prioritet for automatisering.
4. **Kritisk gap:** Stille ændringer (pricing, rate limits, API deprecations) fanges ikke af nogen pipeline. Disse er farlige fordi de ikke genererer nyheder.
