# Eval Results — Hybrid Search vs Dense-only

**Dato:** 2026-03-16 12:29
**Collection:** knowledge (5621 points)
**Metode:** Hybrid = dense (text-embedding-3-small) + sparse (BM25-ish) + RRF fusion

## Summary

### Hit@k (med eval-suitens strenge k-værdier: top-1, top-3, top-5)

| Metode | Hit@k | Procent |
|--------|-------|---------|
| **Hybrid (dense+sparse+RRF)** | 8/18 | **44%** |
| Dense-only | 9/18 | 50% |

### Hit@5 (ensartet k=5 for alle queries — fair sammenligning med baseline)

| Metode | Hit@5 | Procent |
|--------|-------|---------|
| Baseline (dense-only, 2450 pts) | ~11/18 | **61%** |
| **Dense-only (5621 pts)** | 15/18 | **83%** |
| Hybrid RRF (5621 pts) | 11/18 | 61% |

### Konklusion

1. **Mere data hjalp:** Dense-only gik fra 61% → 83% med 3171 nye research-chunks
2. **Hybrid RRF skader:** RRF fusion diluter gode dense-resultater med mediokre sparse-matches (83% → 61%)
3. **Anbefaling:** Brug **dense-only** som primær search. Sparse/BM25 kan bruges som fallback for exact-match queries

## Per-query resultater

| # | Type | Query | Expected | Hybrid | Dense |
|---|------|-------|----------|--------|-------|
| 1 | exact | Ebbinghaus glemselskurve retention proce | DESTILLAT_memory_retrieva | MISS (#>5) | MISS (#4) |
| 2 | exact | Vehicle Routing Problem Google Maps Rout | solo_dev_google_maps_ai_2 | MISS (#5) | MISS (#3) |
| 3 | exact | Pete Walker fawn-respons fjerde traumere | hyperempati_klinisk_psyko | MISS (#>5) | MISS (#3) |
| 4 | exact | Groq Whisper v3 Turbo pris per minut aud | whisper_pricing_2026.md | MISS (#4) | MISS (#2) |
| 5 | exact | Pittenger 1993 MBTI test-retest reliabil | mbti_vs_big_five_evidens. | HIT (#1) | HIT (#1) |
| 6 | semantic | Hvordan fungerer hukommelse i AI-systeme | DESTILLAT_memory_retrieva | MISS (#>5) | MISS (#4) |
| 7 | semantic | Hvad er forskellen mellem en workflow og | DESTILLAT_agents_automati | HIT (#1) | HIT (#1) |
| 8 | semantic | Hvordan kan en solo-udvikler bygge datap | zero_token_pipeline_archi | HIT (#1) | HIT (#1) |
| 9 | semantic | Hvilke open source frameworks kan man br | agents_framework_comparis | HIT (#1) | HIT (#1) |
| 10 | semantic | Hvordan bygger man personlig videnssøgni | personal_data_pipeline_be | MISS (#>5) | MISS (#>5) |
| 11 | cross-topic | heartbeat daemon proaktiv AI overvågning | openclaw_deep_dive_2026-0 | MISS (#>5) | MISS (#>5) |
| 12 | cross-topic | context window begrænsninger og workarou | context_window_workaround | HIT (#3) | HIT (#2) |
| 13 | cross-topic | RAG evaluering metrics precision faithfu | CH5_RAG_PRODUCTION.md | MISS (#>5) | MISS (#4) |
| 14 | cross-topic | Armin Ronacher Flask PI minimal agent to | armin_ronacher_agent_phil | HIT (#2) | HIT (#1) |
| 15 | cross-topic | Dogsheep SQLite Willison embeddings pers | personal_data_pipeline_be | MISS (#5) | HIT (#3) |
| 16 | negative | blockchain cryptocurrency trading bitcoi | NONE | score=0.5 | score=0.2284 |
| 17 | negative | opskrift på rugbrød med surdej | NONE | score=0.5 | score=0.385 |
| 18 | negative | memory | DESTILLAT_memory_retrieva | MISS (#>5) | MISS (#>5) |
| 19 | negative | agent framework comparison benchmark cos | agents_framework_comparis | HIT (#3) | HIT (#2) |
| 20 | negative | Nate Jones intent gap agenter fejler | NATE_JONES_ANALYSE.md | HIT (#1) | HIT (#1) |

## Detaljeret analyse

### Hybrid misses
- **#1** `Ebbinghaus glemselskurve retention procent` — forventet `DESTILLAT_memory_retrieval.md`, top-5: ['human_memory_research.md', 'project-structure.md', 'human_memory_research.md', 'AI_MEMORY_SYSTEMS_SURVEY.md', 'AI_MEMORY_SYSTEMS_SURVEY.md']
- **#2** `Vehicle Routing Problem Google Maps Route Optimiza` — forventet `solo_dev_google_maps_ai_2026.md`, top-5: ['IMAGE_TOOLS_RESEARCH_2026.md', 'academic_writing_standards.md', 'academic_writing_standards.md', 'DESTILLAT_memory_retrieval.md', 'solo_dev_google_maps_ai_2026.md']
- **#3** `Pete Walker fawn-respons fjerde traumerespons` — forventet `hyperempati_klinisk_psykologi.md`, top-5: ['LAYER1_PASS2_WITH_ABSTRACTS.md', 'klinisk_profilering_frameworks.md', 'klinisk_profilering_frameworks.md', 'PIPELINE_DESIGN.md', 'armin_ronacher_agent_philosophy_2026.md']
- **#4** `Groq Whisper v3 Turbo pris per minut audio` — forventet `whisper_pricing_2026.md`, top-5: ['notion-best-practices.md', 'LOCAL_AI_HARDWARE_OPTIONS_2026.md', 'SOFTWARE_ENGINEERING_PRINCIPLES_SURVEY.md', 'whisper_pricing_2026.md', 'whisper_pricing_2026.md']
- **#6** `Hvordan fungerer hukommelse i AI-systemer sammenli` — forventet `DESTILLAT_memory_retrieval.md`, top-5: ['CH3_CLAUDE_CODE.md', 'human_memory_research.md', 'skattepenge_ekspertkilder_2026.md', 'human_memory_research.md', 'human_memory_research.md']
- **#10** `Hvordan bygger man personlig videnssøgning med emb` — forventet `personal_data_pipeline_best_practices.md`, top-5: ['PRE_DEEP_RESEARCH_REPORT.md', 'claude_code_ecosystem_2026.md', 'CH3_CLAUDE_CODE.md', 'LAYER1_PASS2_WITH_ABSTRACTS.md', 'LAYER1_PASS2_WITH_ABSTRACTS.md']
- **#11** `heartbeat daemon proaktiv AI overvågning` — forventet `openclaw_deep_dive_2026-03-15.md`, top-5: ['klinisk_profilering_frameworks.md', 'WHAT_IF.md', 'visual_llm_landscape_2026.md', 'DESTILLAT_memory_retrieval.md', 'visual_llm_landscape_2026.md']
- **#13** `RAG evaluering metrics precision faithfulness` — forventet `CH5_RAG_PRODUCTION.md`, top-5: ['DESTILLAT_memory_retrieval.md', 'CH5_RAG_EMBEDDINGS.md', 'AI_MEMORY_SYSTEMS_SURVEY.md', 'claude_code_ecosystem_2026.md', 'ch7_prompting_antipatterns_research.md']
- **#15** `Dogsheep SQLite Willison embeddings personlig data` — forventet `personal_data_pipeline_best_practices.md`, top-5: ['zero_token_pipeline_architecture.md', 'solo_dev_google_maps_ai_2026.md', 'DESTILLAT_memory_retrieval.md', 'zero_token_pipeline_architecture.md', 'personal_data_pipeline_best_practices.md']
- **#18** `memory` — forventet `DESTILLAT_memory_retrieval.md`, top-5: ['ARCHITECTURE_CONTINUOUS_MEMORY.md', 'brainmap_research_report_v2.md', 'visual_llm_landscape_2026.md', 'human_memory_research.md', 'LAYER2_PASS1_SOURCES.md']

*Genereret af eval_hybrid_search.py kl. 2026-03-16 12:29*