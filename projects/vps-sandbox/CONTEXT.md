# VPS Sandbox

## Metadata
- **Status:** V4 afsluttet (4 parallelle loops, 30 iterationer). Output evalueret, klar til hentning.
- **Sidst opdateret:** 2026-03-15 (session 21)

## Hvad er det
Autonom sandkasse på VPS (72.62.61.51) der kører Claude i Ralph loop — 10 iterationer per run, state på disk, ingen menneskelig interaktion undervejs. Producerer deliverables der evalueres og hentes til PC.

## Historik

### V1 (session 18-19)
6 iterationer. Producerede 5 research-rapporter (~2200 linjer), 4 hook-scripts, research INDEX.md. Kvalitetsaudit: direction-analysis 8/10, context-engineering 7.5/10, research-arch-report 6/10. Proces 5/10 — research spawning research, 6 iterationer at aktivere en JSON config.

### V2 (session 19-20)
10 iterationer, 3 projekter: Research Architecture, TransportIntra Arkiv, Prompt-skabeloner. Alle 10/10 iterationer gennemført, 45 filer, alle done-kriterier PASS. Stjerne-deliverables: TI PROGRESS.md (4 kausale kæder), TI INDEX.md (194L med crown jewels), 2 skills (session-resume, sitrep).

### V3 (session 20)
6 iterationer der uddybede V2's mediokre dele: Research INDEX.md fik 54 Key Insights, 4 TI subproject stubs uddybet (16L→30-40L), chatlog renset (0 artefakter), dialectic-pipeline skill bygget (120L), N8N archive med kausal kæde (93L). Review: 4×IMPROVED, 3×PASS, 0×FAIL.

### V4 (session 20-21)
4 parallelle Ralph loops, 30 iterationer total. Alle KOMPLET, alle PASS, nul FAIL.

| Loop | Iter | Filer | Linjer | Kerne-output |
|------|------|-------|--------|--------------|
| llm-landskab | 10 | 10 | ~875 | 7 provider-profiler, COMPARISON.md, RECOMMENDATION.md (Scenarie C) |
| ai-frontier | 10 | 8 | ~1.606 | 5 topic-filer, GAPS.md (8 gaps), WHAT_IF.md (10 forslag) |
| videns-vedligeholdelse | 7 | 8 | ~970 | DECAY_MODEL, PIPELINE_DESIGN (5 udvidelser), HOLISTIC_EVALUATION |
| youtube-pipeline-v2 | 3 | 5 | ~530 | frame_extractor.py (230L PoC), 3 nye kanaler tilføjet |

Nøglefund:
- RSS-bug fundet: feeds konfigureret i sources.json men aldrig kaldt i ai_intelligence.py (15 min fix)
- HOLISTIC_EVALUATION: ærlig, advarer mod analyse-paralyse, 7 prioriterede handlinger
- frame_extractor.py virker med lokale filer, VPS download blokeret (datacenter IP)
- 10/10 fact-checks i llm-landskab, 10/10 i ai-frontier. Ingen hallucination

## Hvad er hentet til PC
- 3 skills: dialectic-pipeline, session-resume, sitrep → `.claude/skills/`
- Research INDEX.md v3 (54 Key Insights) → `projects/research/INDEX.md`
- TI projekt (INDEX, PROGRESS, CONTEXT, 8 subprojects, research, archive) → `projects/transportintra/`
- BLUEPRINT.md → roden
- vps-pc-convergence.md → `projects/research/`
- MINING_RESULTS.md → `projects/prompt-skabeloner/`
- V3_EVALUATION.md → denne mappe

### V4 (hentet session 21)
19 filer hentet til `projects/research/`:
- `llm-landskab/` — COMPARISON.md, RECOMMENDATION.md, 7 provider-profiler
- `ai-frontier/` — GAPS.md, WHAT_IF.md, 5 topic-filer
- `videns-vedligeholdelse/` — HOLISTIC_EVALUATION.md, PIPELINE_DESIGN.md, DECAY_MODEL.md, SOURCE_REGISTRY.md, MAINTENANCE_PROTOCOL.md, YGGDRA_SCAN.md
- youtube-pipeline-v2: kode allerede på VPS (frame_extractor.py, udvidet youtube_monitor.py, 3 nye kanaler)

## Infrastruktur
- Placering: `/root/Yggdra/yggdra-pc/`
- Loop: `claude --print` i for-loop (10 iterationer)
- State: LOOP_STATE.md (rolling window, kun 2 seneste iterationer)
- Plan: LOOP_PLAN.md (iterationsplan med done-kriterier)
- Regler: CLAUDE.md (Build>Research, Done=Verified, token-bevidsthed)

## Prompt-design (vps-prompt-final.md)
Referenceeksemplar i `projects/0_backlog/vps-prompt-final.md`. Indeholder CLAUDE.md, LOOP_PLAN.md, LOOP_STATE.md, og start-kommando.

## Kill condition
Hvis VPS sandbox ikke bruges i 3 sessioner → arkivér. Sandbox er et værktøj, ikke et projekt.
