# Inventar — Prompt & Context Engineering Materiale

Pr. 17. marts 2026. Alt materiale Yggdra har om prompting, context engineering og agent-arkitektur.

---

## Kilder (10 filer i data/vps-sync-20260316/)

| Fil | Indhold | Vurdering |
|---|---|---|
| `sources/anthropic_context_engineering.md` | Anthropic Applied AI: context rot, attention budget, just-in-time retrieval, compaction | **Guld** — primær kilde |
| `sources/manus_context_engineering.md` | Manus: KV-cache, logit masking, filsystem som hukommelse, bevar fejl | **Guld** — produktionsviden |
| `sources/lance_martin_context_engineering.md` | LangChain: Write/Select/Compress/Isolate taxonomi, tool RAG | **Sølv** — god ramme, men sammenfatning af andre |
| `sources/anthropic_harnesses.md` | Long-running agents: feature list JSON, session-protokol, én feature per session | **Guld** til multi-session |
| `sources/zechner_minimal_agent.md` | pi: 4 tools, <1000 tokens system prompt, MCP koster 7-9% kontekst | **Guld** til Yggdra-arkitektur |
| `CH7_ADVANCED_PROMPTING.md` | Destillat af 30+ papers: context engineering, meta-prompting, Claude-specifikt | **Guld** |
| `CH7_PROMPTING_PRACTICE.md` | Anti-patterns, prompt injection, structured output, prompts-as-code | **Sølv** — 60-70% overlap med CH7_ADVANCED |
| `agents_context_engineering.md` | 5-lags stack: offload/reduce/isolate/progressive disclosure med kodeeksempler | **Guld** som implementeringsreference |
| `context_window_workarounds_2026.md` | Alle context management-tilgange sammenlignet (sliding window, MemGPT, Mem0, RAG) | **Sølv** — overblik, dækket bedre i sources/ |
| `LOOPS_PIPELINE_EJERSKAB_2026-03-16.md` | F1-F7 fejltaxonomi fra 148 episoder, pipeline-arkitektur, lokal LLM-ejerskab | **Guld** — empirisk, Yggdra-specifik |

## VPS Destillater (2 filer i yggdra-pc/overlevering-fra-vps/)

| Fil | Indhold | Vurdering |
|---|---|---|
| `DESTILLAT_agents_automation.md` | L0-L5 automationsspektrum, framework-benchmarks, METR-studie, OpenClaw gap | **Guld** — 501 linjer, 13 filer konsolideret |
| `DESTILLAT_memory_retrieval.md` | Kognitionsvidenskab (CLS, FSRS), 3-lags arkitektur, chunking er 80% af RAG | **Guld** — 553 linjer, akademisk forankret |

## Prompt Mining Output (4 filer i data/vps-sync-20260316/prompt_mining/)

| Fil | Indhold | Vurdering |
|---|---|---|
| `INSIGHTS.md` | 1.270 prompts analyseret, mønstre, effektivitetsfordeling | **Guld** — empirisk, egne data |
| `PROMPT_KATALOG.md` | 8 copy-paste skabeloner med eksempler og DONE-kriterier | **Guld** — operationel, klar til brug |
| `analysis.jsonl` | Rå analyse-data per prompt | Referencedata |
| `daily_report.md` | Seneste daglige rapport | Operationelt |

## PC Eksisterende (5 filer i projects/REF.prompt-skabeloner/)

| Fil | Indhold | Vurdering |
|---|---|---|
| `CONTEXT.md` | Projektdefinition, 5 mønstre, 2 skills besluttet | Aktuel |
| `MINING_RESULTS.md` | Chatlog-mining: 972 beskeder, 6 mønstre, 2 skills valgt | Aktuel |
| `VPS_HANDOFF.md` | Cross-session koordinering (session 19-era) | **Forældet** |
| `BESKED_FRA_ANDEN_SESSION.md` | Cross-session besked, absorberet | **Forældet** |
| `CLAUDE.md` | Projekt-lokal CLAUDE.md | Minimal |

## PC Research (i projects/2_research/sources/)

Disse filer overlapper med data/vps-sync-20260316/sources/ — sandsynligvis tidligere kopier:
- `anthropic_context_engineering.md`, `manus_context_engineering.md`, `lance_martin_context_engineering.md`, `anthropic_harnesses.md`, `zechner_minimal_agent.md`, `anthropic_building_effective_agents.md`, `vercel_removed_tools.md`

---

## Hvad er guld, hvad er støj?

**Guld (11 filer):** De 7 sources + 2 destillater + INSIGHTS + PROMPT_KATALOG. Disse indeholder actionable viden.

**Sølv (3 filer):** CH7_PROMPTING_PRACTICE (overlap), lance_martin (sammenfatning), context_window_workarounds (overblik). Brugbare som reference, men kernen er dækket bedre andetsteds.

**Forældet (2 filer):** VPS_HANDOFF.md, BESKED_FRA_ANDEN_SESSION.md — historiske koordineringsfiler.

**Duplikater:** projects/2_research/sources/ ≈ data/vps-sync-20260316/sources/ (7 filer).

## Nate B Jones (tilføjet post-inventar)

| Fil | Indhold | Vurdering |
|---|---|---|
| `yggdra-pc/overlevering-fra-vps/CLAUDE_CODE_SIKKERHED_NATE_JONES.md` | Terraform-case + 5 management skills + 5-Layer QA + hook-arkitektur. Opdateret med transkript 17/3 | **Guld** — operationelt, direkte relevant |
| `data/vps-sync-20260316/NATE_JONES_ANALYSE.md` | 30-video analyse (jan 2026): intent gap, convergence loops, context engineering, high agency | **Guld** — bredeste Nate-analyse |
| `data/vps-sync-20260316/nate_jones_transcript.en.vtt` | Rå VTT fra "Agent Management for Vibe Coders" | Referencedata |

## Hvad overlapper?

- CH7_ADVANCED + CH7_PRACTICE: 60-70% overlap. Merge eller vælg én.
- anthropic_context_engineering + agents_context_engineering: samme principper, første er teori, anden er implementering. Begge nyttige.
- lance_martin sammenfatter anthropic + manus. Redundant hvis man har originalerne.
- DESTILLAT_memory_retrieval siger hybrid 15-25% bedre end dense. VPS eval siger dense 83% vs hybrid 61%. **Modsigelelse** — kontekst-afhængig (generel litteratur vs. Yggdra-specifik benchmark).

## Hvad modsiger hinanden?

**Hybrid vs. dense search:** Litteraturen (DESTILLAT_memory_retrieval) siger hybrid vinder generelt. Yttres egen benchmark siger dense vinder på Yttres data. **Løsning:** Trust egne benchmarks over generel litteratur. Dense-only default, hybrid som fallback.
