# LLM Landskab

**Dato:** 2026-03-14
**Klar til:** Backlog — VPS Ralph loop
**Prioritet:** Høj

## Opsummering
Per-provider intelligence om AI-udbydere. Advocacy + red team for hver. Deliverable: konkret anbefaling om Yttre skal bruge mere end Anthropic, og til hvad.

## Hvorfor
AI-landskabet ændrer sig ugentligt. Yttre bruger kun Anthropic i dag. Det er måske optimalt — måske ikke. Uden systematisk viden om alternativerne er det et gæt. Projektet bygger vidensgrundlaget for informerede beslutninger om multi-provider strategi.

## Scope

**Inden for:**
- Provider-profiler: Anthropic, OpenAI, Google DeepMind, xAI, Meta AI, Mistral, Perplexity
- Styrker/svagheder per provider (reasoning, code, vision, tool use, context window, pris)
- Komparativ matrix med konkrete benchmarks og erfaringer
- "Hvad ville Yttre vinde/miste ved at tilføje provider X?"

**Uden for:**
- Implementation af multi-provider setup (separat projekt)
- Hardware/on-premise modeller (Llama lokalt etc.)
- Provider-intern arkitektur (hvordan de træner modeller)

## Deliverables

1. `providers/anthropic.md` — profil, styrker, svagheder, pricing, roadmap, kilder
2. `providers/openai.md` — samme format
3. `providers/google.md` — samme format
4. `providers/xai.md` — samme format
5. `providers/meta.md` — samme format (open source vinkel)
6. `providers/mistral.md` — samme format (EU vinkel)
7. `providers/perplexity.md` — samme format (search vinkel)
8. `COMPARISON.md` — komparativ matrix (pris, context, tool use, code, reasoning, vision)
9. `RECOMMENDATION.md` — "til Yttres setup: hvad giver mening ud over Anthropic?"

## VPS-metode (Ralph loop, 10 iterationer)

### Iteration 1-2: Anthropic + OpenAI profiler
2 subagents per provider: Advocate (steelman) + Critic (svagheder). Merger til profil.
**Kilder:** Officielle docs, pricing pages, changelogs, seneste blog posts.
**Done:** Begge profiler >80 linjer med kilder.

### Iteration 3-4: Google + xAI profiler
Samme metode.
**Done:** Begge profiler >60 linjer med kilder.

### Iteration 5-6: Meta + Mistral + Perplexity profiler
3 providers, mindre dybde. Meta: open source fokus. Mistral: EU/sovereignty. Perplexity: search-first.
**Done:** Alle 3 profiler >40 linjer.

### Iteration 7-8: COMPARISON.md
Syntetisér alle profiler til komparativ matrix. Dimensioner: pris per million tokens (input/output), context window, tool use kvalitet, code generation, reasoning, vision, API stabilitet, community/ecosystem.
**Done:** Matrix med alle 7 providers, >100 linjer, alle felter udfyldt.

### Iteration 9: RECOMMENDATION.md
Baseret på Yttres setup (Claude Code, VPS, Qdrant, voice, automation) — hvad giver mening?
Scenarier: "kun Anthropic", "Anthropic + OpenAI embeddings", "Anthropic + Gemini til vision", "fuld multi-provider".
**Done:** >60 linjer, mindst 3 scenarier med pro/con.

### Iteration 10: Review
3 Reviewer-subagents: fakta-check mod kilder, konsistens mellem profiler, anbefaling matcher data.
**Done:** EVALUATION.md med ærlig vurdering.

## Kilder
- Officielle: anthropic.com, openai.com, ai.google.dev, x.ai, ai.meta.com, mistral.ai, perplexity.ai
- Benchmarks: chatbot-arena, LMSYS leaderboard, Artificial Analysis
- Community: r/LocalLLaMA, r/ClaudeAI, HN
- Eksisterende VPS research: /root/Yggdra/research/CH4_LLM_LANDSCAPE.md

## Kill condition
Hvis profiler mest bliver gengivelse af marketing-materiale uden reel substans → kill efter iteration 4.
