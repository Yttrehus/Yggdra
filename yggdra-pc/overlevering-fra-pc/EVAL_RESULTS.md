# Eval Results — Knowledge Collection (Dense Search Only)

**Date:** 2026-03-16 11:09  
**Collection:** knowledge (984 points)  
**Model:** text-embedding-3-small (1536d)  
**Search:** Dense vectors only (sparse/BM25 not available from VPS — no tokenizer)  
**Limit:** Top 5 results per query  

## Aggregate Scores

| Metric | Score | Count |
|--------|-------|-------|
| Hit@1 | 38.9% | 7/18 |
| Hit@3 | 55.6% | 10/18 |
| Hit@5 | 61.1% | 11/18 |

**Negative queries (should-not-match, threshold < 0.45):** 2/2 passed

## Per-Query Results

| # | Type | Query | Expected | Top-1 Result (score) | Hit@1 | Hit@3 | Hit@5 |
|---|------|-------|----------|---------------------|-------|-------|-------|
| 1 | exact | Ebbinghaus glemselskurve retention procent | DESTILLAT_memory_retrieval.md | DESTILLAT_memory_retrieval.md (0.588) | Y | Y | Y |
| 2 | exact | Vehicle Routing Problem Google Maps Route Opt... | solo_dev_google_maps_ai_2026.md | solo_dev_google_maps_ai_2026.md (0.471) | Y | Y | Y |
| 3 | exact | Pete Walker fawn-respons fjerde traumerespons | hyperempati_klinisk_psykologi.md | klinisk_profilering_frameworks.md (0.444) | — | Y | Y |
| 4 | exact | Groq Whisper v3 Turbo pris per minut audio | whisper_pricing_2026.md | COMPARISON.md (0.421) | — | — | — |
| 5 | exact | Pittenger 1993 MBTI test-retest reliabilitet ... | mbti_vs_big_five_evidens.md | mbti_vs_big_five_evidens.md (0.605) | Y | Y | Y |
| 6 | semantic | Hvordan fungerer hukommelse i AI-systemer sam... | DESTILLAT_memory_retrieval.md | DESTILLAT_memory_retrieval.md (0.749) | Y | Y | Y |
| 7 | semantic | Hvad er forskellen mellem en workflow og en a... | DESTILLAT_agents_automation.md | DESTILLAT_agents_automation.md (0.745) | Y | Y | Y |
| 8 | semantic | Hvordan kan en solo-udvikler bygge datapipeli... | zero_token_pipeline_architecture.md | zero_token_pipeline_architecture.md (0.682) | Y | Y | Y |
| 9 | semantic | Hvilke open source frameworks kan man bruge t... | agents_framework_comparison.md | agent-teams.md (0.651) | — | — | — |
| 10 | semantic | Hvordan bygger man personlig videnssøgning me... | personal_data_pipeline_best_practices.md | personal_data_pipeline_best_practices.md (0.604) | Y | Y | Y |
| 11 | cross-topic | heartbeat daemon proaktiv AI overvågning | openclaw_deep_dive_2026-03-15.md | WHAT_IF.md (0.530) | — | — | Y |
| 12 | cross-topic | context window begrænsninger og workarounds f... | context_window_workarounds_2026.md | context-engineering-research.md (0.535) | — | — | — |
| 13 | cross-topic | RAG evaluering metrics precision faithfulness | CH5_RAG_PRODUCTION.md | memory-systems.md (0.534) | — | — | — |
| 14 | cross-topic | Armin Ronacher Flask PI minimal agent tools f... | armin_ronacher_agent_philosophy_2026.md | agent-architectures.md (0.538) | — | — | — |
| 15 | cross-topic | Dogsheep SQLite Willison embeddings personlig... | personal_data_pipeline_best_practices.md | zero_token_pipeline_architecture.md (0.586) | — | Y | Y |
| 16 | negative | blockchain cryptocurrency trading bitcoin | — | zero_token_pipeline_architecture.md (0.199) | n/a | n/a | PASS |
| 17 | negative | opskrift på rugbrød med surdej | — | DESTILLAT_memory_retrieval.md (0.367) | n/a | n/a | PASS |
| 18 | negative | memory | DESTILLAT_memory_retrieval.md | memory-systems.md (0.417) | — | Y | Y |
| 19 | negative | agent framework comparison benchmark cost per... | agents_framework_comparison.md | DESTILLAT_agents_automation.md (0.483) | — | — | — |
| 20 | negative | Nate Jones intent gap agenter fejler | NATE_JONES_ANALYSE.md | DESTILLAT_agents_automation.md (0.517) | — | — | — |

## Full Result Details

### Query 1: Ebbinghaus glemselskurve retention procent

- **Type:** exact  
- **Expected:** DESTILLAT_memory_retrieval.md  
- **Relevance target:** top-1  
- **Hit@1:** YES | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `DESTILLAT_memory_retrieval.md` (score: 0.5884) **<-- MATCH**
  2. `DESTILLAT_memory_retrieval.md` (score: 0.5337) **<-- MATCH**
  3. `DESTILLAT_memory_retrieval.md` (score: 0.5270) **<-- MATCH**
  4. `DESTILLAT_memory_retrieval.md` (score: 0.5265) **<-- MATCH**
  5. `DESTILLAT_memory_retrieval.md` (score: 0.5153) **<-- MATCH**

### Query 2: Vehicle Routing Problem Google Maps Route Optimization API

- **Type:** exact  
- **Expected:** solo_dev_google_maps_ai_2026.md  
- **Relevance target:** top-1  
- **Hit@1:** YES | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `solo_dev_google_maps_ai_2026.md` (score: 0.4712) **<-- MATCH**
  2. `solo_dev_google_maps_ai_2026.md` (score: 0.4484) **<-- MATCH**
  3. `solo_dev_google_maps_ai_2026.md` (score: 0.4359) **<-- MATCH**
  4. `solo_dev_google_maps_ai_2026.md` (score: 0.4265) **<-- MATCH**
  5. `anthropic_building_effective_agents.md` (score: 0.3833)

### Query 3: Pete Walker fawn-respons fjerde traumerespons

- **Type:** exact  
- **Expected:** hyperempati_klinisk_psykologi.md  
- **Relevance target:** top-1  
- **Hit@1:** NO | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `klinisk_profilering_frameworks.md` (score: 0.4437)
  2. `hyperempati_klinisk_psykologi.md` (score: 0.4366) **<-- MATCH**
  3. `hyperempati_klinisk_psykologi.md` (score: 0.4206) **<-- MATCH**
  4. `hyperempati_klinisk_psykologi.md` (score: 0.3992) **<-- MATCH**
  5. `hyperempati_klinisk_psykologi.md` (score: 0.3929) **<-- MATCH**

### Query 4: Groq Whisper v3 Turbo pris per minut audio

- **Type:** exact  
- **Expected:** whisper_pricing_2026.md  
- **Relevance target:** top-1  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** NO  
- **Top 5 results:**
  1. `COMPARISON.md` (score: 0.4209)
  2. `openclaw_deep_dive_2026-03-15.md` (score: 0.4208)
  3. `openai.md` (score: 0.4172)
  4. `openclaw_deep_dive_2026-03-15.md` (score: 0.4103)
  5. `COMPARISON.md` (score: 0.4069)

### Query 5: Pittenger 1993 MBTI test-retest reliabilitet 50 procent

- **Type:** exact  
- **Expected:** mbti_vs_big_five_evidens.md  
- **Relevance target:** top-1  
- **Hit@1:** YES | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `mbti_vs_big_five_evidens.md` (score: 0.6052) **<-- MATCH**
  2. `mbti_vs_big_five_evidens.md` (score: 0.5867) **<-- MATCH**
  3. `mbti_vs_big_five_evidens.md` (score: 0.5820) **<-- MATCH**
  4. `mbti_vs_big_five_evidens.md` (score: 0.5362) **<-- MATCH**
  5. `mbti_vs_big_five_evidens.md` (score: 0.5188) **<-- MATCH**

### Query 6: Hvordan fungerer hukommelse i AI-systemer sammenlignet med mennesker?

- **Type:** semantic  
- **Expected:** DESTILLAT_memory_retrieval.md  
- **Relevance target:** top-3  
- **Hit@1:** YES | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `DESTILLAT_memory_retrieval.md` (score: 0.7490) **<-- MATCH**
  2. `DESTILLAT_memory_retrieval.md` (score: 0.6650) **<-- MATCH**
  3. `memory-systems.md` (score: 0.6561)
  4. `DESTILLAT_memory_retrieval.md` (score: 0.6539) **<-- MATCH**
  5. `DESTILLAT_memory_retrieval.md` (score: 0.6514) **<-- MATCH**

### Query 7: Hvad er forskellen mellem en workflow og en agent?

- **Type:** semantic  
- **Expected:** DESTILLAT_agents_automation.md  
- **Relevance target:** top-1  
- **Hit@1:** YES | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `DESTILLAT_agents_automation.md` (score: 0.7453) **<-- MATCH**
  2. `agent-architectures.md` (score: 0.7155)
  3. `DESTILLAT_agents_automation.md` (score: 0.6751) **<-- MATCH**
  4. `agent-teams.md` (score: 0.6317)
  5. `agent-architectures.md` (score: 0.5692)

### Query 8: Hvordan kan en solo-udvikler bygge datapipelines uden at bruge LLM tokens?

- **Type:** semantic  
- **Expected:** zero_token_pipeline_architecture.md  
- **Relevance target:** top-1  
- **Hit@1:** YES | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `zero_token_pipeline_architecture.md` (score: 0.6821) **<-- MATCH**
  2. `zero_token_pipeline_architecture.md` (score: 0.6503) **<-- MATCH**
  3. `zero_token_pipeline_architecture.md` (score: 0.6413) **<-- MATCH**
  4. `personal_data_pipeline_best_practices.md` (score: 0.6380)
  5. `zero_token_pipeline_architecture.md` (score: 0.6281) **<-- MATCH**

### Query 9: Hvilke open source frameworks kan man bruge til at bygge multi-agent systemer?

- **Type:** semantic  
- **Expected:** agents_framework_comparison.md  
- **Relevance target:** top-3  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** NO  
- **Top 5 results:**
  1. `agent-teams.md` (score: 0.6509)
  2. `agent-teams.md` (score: 0.6338)
  3. `agent-teams.md` (score: 0.6321)
  4. `agent-teams.md` (score: 0.6319)
  5. `DESTILLAT_agents_automation.md` (score: 0.6270)

### Query 10: Hvordan bygger man personlig videnssøgning med embeddings og vektor-databaser?

- **Type:** semantic  
- **Expected:** personal_data_pipeline_best_practices.md  
- **Relevance target:** top-3  
- **Hit@1:** YES | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `personal_data_pipeline_best_practices.md` (score: 0.6035) **<-- MATCH**
  2. `memory-systems.md` (score: 0.6032)
  3. `memory-systems.md` (score: 0.5866)
  4. `personal_data_pipeline_best_practices.md` (score: 0.5697) **<-- MATCH**
  5. `DESTILLAT_memory_retrieval.md` (score: 0.5681)

### Query 11: heartbeat daemon proaktiv AI overvågning

- **Type:** cross-topic  
- **Expected:** openclaw_deep_dive_2026-03-15.md  
- **Relevance target:** top-3  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** YES  
- **Top 5 results:**
  1. `WHAT_IF.md` (score: 0.5303)
  2. `DESTILLAT_memory_retrieval.md` (score: 0.5256)
  3. `GAPS.md` (score: 0.5120)
  4. `openclaw_deep_dive_2026-03-15.md` (score: 0.4732) **<-- MATCH**
  5. `automation-patterns.md` (score: 0.4707)

### Query 12: context window begrænsninger og workarounds for lange samtaler

- **Type:** cross-topic  
- **Expected:** context_window_workarounds_2026.md  
- **Relevance target:** top-3  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** NO  
- **Top 5 results:**
  1. `context-engineering-research.md` (score: 0.5353)
  2. `context-engineering-research.md` (score: 0.5352)
  3. `context-engineering-research.md` (score: 0.5347)
  4. `context-engineering-research.md` (score: 0.5149)
  5. `agent-teams.md` (score: 0.4977)

### Query 13: RAG evaluering metrics precision faithfulness

- **Type:** cross-topic  
- **Expected:** CH5_RAG_PRODUCTION.md  
- **Relevance target:** top-3  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** NO  
- **Top 5 results:**
  1. `memory-systems.md` (score: 0.5343)
  2. `DESTILLAT_memory_retrieval.md` (score: 0.5292)
  3. `memory-systems.md` (score: 0.4954)
  4. `DESTILLAT_memory_retrieval.md` (score: 0.4896)
  5. `GAPS.md` (score: 0.4875)

### Query 14: Armin Ronacher Flask PI minimal agent tools filosofi

- **Type:** cross-topic  
- **Expected:** armin_ronacher_agent_philosophy_2026.md  
- **Relevance target:** top-3  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** NO  
- **Top 5 results:**
  1. `agent-architectures.md` (score: 0.5383)
  2. `DESTILLAT_agents_automation.md` (score: 0.5354)
  3. `DESTILLAT_agents_automation.md` (score: 0.5183)
  4. `DESTILLAT_agents_automation.md` (score: 0.5119)
  5. `DESTILLAT_agents_automation.md` (score: 0.4959)

### Query 15: Dogsheep SQLite Willison embeddings personlig data

- **Type:** cross-topic  
- **Expected:** personal_data_pipeline_best_practices.md  
- **Relevance target:** top-3  
- **Hit@1:** NO | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `zero_token_pipeline_architecture.md` (score: 0.5861)
  2. `personal_data_pipeline_best_practices.md` (score: 0.5616) **<-- MATCH**
  3. `DESTILLAT_memory_retrieval.md` (score: 0.4945)
  4. `zero_token_pipeline_architecture.md` (score: 0.4838)
  5. `DESTILLAT_memory_retrieval.md` (score: 0.4453)

### Query 16: blockchain cryptocurrency trading bitcoin

- **Type:** negative  
- **Expected:** None (negative)  
- **Relevance target:** should-not-match  
- **Max score:** 0.1994 — PASS (below threshold)  
- **Top 5 results:**
  1. `zero_token_pipeline_architecture.md` (score: 0.1994)
  2. `zero_token_pipeline_architecture.md` (score: 0.1836)
  3. `automation-patterns.md` (score: 0.1836)
  4. `claude-code-organization.md` (score: 0.1811)
  5. `zero_token_pipeline_architecture.md` (score: 0.1749)

### Query 17: opskrift på rugbrød med surdej

- **Type:** negative  
- **Expected:** None (negative)  
- **Relevance target:** should-not-match  
- **Max score:** 0.3670 — PASS (below threshold)  
- **Top 5 results:**
  1. `DESTILLAT_memory_retrieval.md` (score: 0.3670)
  2. `PIPELINE_DESIGN.md` (score: 0.3534)
  3. `solo_dev_google_maps_ai_2026.md` (score: 0.3476)
  4. `REFLEKSION.md` (score: 0.3435)
  5. `yggdra-gold.md` (score: 0.3423)

### Query 18: memory

- **Type:** negative  
- **Expected:** DESTILLAT_memory_retrieval.md  
- **Relevance target:** top-5  
- **Hit@1:** NO | **Hit@3:** YES | **Hit@5:** YES  
- **Top 5 results:**
  1. `memory-systems.md` (score: 0.4168)
  2. `DESTILLAT_memory_retrieval.md` (score: 0.3981) **<-- MATCH**
  3. `DESTILLAT_memory_retrieval.md` (score: 0.3924) **<-- MATCH**
  4. `memory-systems.md` (score: 0.3887)
  5. `anthropic_context_engineering.md` (score: 0.3800)

### Query 19: agent framework comparison benchmark cost performance

- **Type:** negative  
- **Expected:** agents_framework_comparison.md  
- **Relevance target:** top-5  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** NO  
- **Top 5 results:**
  1. `DESTILLAT_agents_automation.md` (score: 0.4829)
  2. `anthropic_building_effective_agents.md` (score: 0.4740)
  3. `agent-teams.md` (score: 0.4702)
  4. `anthropic_building_effective_agents.md` (score: 0.4589)
  5. `agent-teams.md` (score: 0.4472)

### Query 20: Nate Jones intent gap agenter fejler

- **Type:** negative  
- **Expected:** NATE_JONES_ANALYSE.md  
- **Relevance target:** top-3  
- **Hit@1:** NO | **Hit@3:** NO | **Hit@5:** NO  
- **Top 5 results:**
  1. `DESTILLAT_agents_automation.md` (score: 0.5173)
  2. `RED_TEAM_EVALUERING_2026-03-15.md` (score: 0.4212)
  3. `DESTILLAT_memory_retrieval.md` (score: 0.3982)
  4. `RESEARCH_CATALOG.md` (score: 0.3843)
  5. `automation-patterns.md` (score: 0.3817)

