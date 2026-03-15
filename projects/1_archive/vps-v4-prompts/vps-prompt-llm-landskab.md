# VPS Ralph Loop — LLM Landskab

Deploy til `/root/Yggdra/yggdra-pc/llm-landskab/`.
10 iterationer. Samme loop-infrastruktur som sandbox v2.

---

## CLAUDE.md

```markdown
# LLM Landskab — Sandbox

Du kører autonomt i en Ralph loop. Yttre er ikke tilgængelig.
Hver iteration er ét `claude --print` kald.

## Boot-sekvens

1. Dit iterationsnummer er givet i prompten
2. Læs LOOP_STATE.md — check ## Blokkere
3. Læs den relevante iteration i LOOP_PLAN.md
4. VALIDÉR INPUT: Check at filer fra forrige iteration eksisterer
5. Udfør opgaven. Skriv output til disk
6. Verificér output med kommandoer (ls, wc -l, head)
7. Opdatér LOOP_STATE.md
8. Stop

## LOOP_STATE format

```
# Loop State
## Blokkere
(ingen / liste)

## Filregister
(kumulativ liste af producerede filer)

## Iteration [N-1] (seneste)
Opgave: ...
Output: ...
Done: ... → PASS/FAIL

## Iteration [N-2]
(slet ældre end N-2)

## Næste: Iteration N
```

## Projekt

Per-provider AI intelligence. Profiler med advocacy + red team.
Output i `providers/` og rod-filer.

## Regler

### Token-bevidsthed
- Læs ALDRIG filer >500 linjer i helhed. Brug head, tail, grep
- Max 3 parallelle subagents
- Skriv kompakt

### Metode per provider
- **Advocate** (subagent): Steelman — hvad er denne provider bedst til? Hvad er deres unikke styrke? Brug officielle docs + blog
- **Critic** (subagent): Red team — hvad fejler? Hvad er dyrere/dårligere end alternativer? Brug community-sources
- **Orchestrator**: Merger til balanceret profil

### Profil-format
Hver profil følger dette format:
```
# [Provider]
## Identitet (hvem er de, hvad er deres mission)
## Modeller (aktuelle modeller med specs)
## Styrker (steelman — hvad er de bedst til)
## Svagheder (red team — hvad fejler)
## Pricing (input/output per million tokens, context window, rate limits)
## API & Developer Experience
## Relevans for Yttre (specifikt: Claude Code, VPS, Qdrant, voice, automation)
## Kilder
```

### Build > Research
- Hver iteration SKAL producere filer på disk
- Ingen rapporter der ikke direkte informerer et deliverable

### Done = Verified
- Test med kommandoer
- Spot-check 2 fakta mod kilden

### Miljø
- Du er PÅ VPS'en. ALDRIG ssh til dig selv
- SØG IKKE på nettet — brug kun kilder du kan læse lokalt eller via curl til officielle APIs/docs
- Eksisterende research: /root/Yggdra/research/CH4_LLM_LANDSCAPE.md
```

---

## LOOP_PLAN.md

```markdown
# Loop Plan — LLM Landskab (10 iterationer)

## Iteration 1 — Anthropic profil
**Opgave:** Byg providers/anthropic.md
**Metode:** 2 subagents (Advocate + Critic). Kilder: /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (sektion Anthropic), /root/Yggdra/research/AI_CLAUDE_ANTHROPIC_2026.md, /root/Yggdra/research/CH3_CLAUDE_CODE.md
**Done:** providers/anthropic.md >80 linjer, med pricing, modeller, styrker/svagheder

## Iteration 2 — OpenAI profil
**Opgave:** Byg providers/openai.md
**Metode:** 2 subagents. Kilder: CH4_LLM_LANDSCAPE.md (sektion OpenAI), eksisterende research
**Done:** providers/openai.md >80 linjer

## Iteration 3 — Google DeepMind profil
**Opgave:** Byg providers/google.md
**Metode:** 2 subagents. Kilder: CH4_LLM_LANDSCAPE.md, eksisterende research
**Done:** providers/google.md >60 linjer

## Iteration 4 — xAI profil
**Opgave:** Byg providers/xai.md
**Metode:** 2 subagents. Grok-modeller, Yttres erfaring (Grok var det første AI-tool han brugte)
**Done:** providers/xai.md >60 linjer

## Iteration 5 — Meta AI profil
**Opgave:** Byg providers/meta.md
**Metode:** Open source vinkel. Llama-modeller, community, self-hosting
**Done:** providers/meta.md >50 linjer

## Iteration 6 — Mistral + Perplexity profiler
**Opgave:** Byg providers/mistral.md + providers/perplexity.md
**Metode:** Mistral: EU/sovereignty vinkel. Perplexity: search-first vinkel
**Done:** Begge filer >40 linjer

## Iteration 7 — COMPARISON.md
**Opgave:** Komparativ matrix af alle 7 providers
**Input:** Alle provider-profiler
**Format:** Tabel med dimensioner: pris (input/output), context window, tool use, code gen, reasoning, vision, API stabilitet, ecosystem
**Done:** COMPARISON.md >100 linjer, alle felter udfyldt

## Iteration 8 — COMPARISON.md del 2 + kvalitetscheck
**Opgave:** Udvid COMPARISON.md med use-case scenarier. Spot-check 5 fakta
**Scenarier:** "bedste til code generation", "bedste til research/analyse", "bedste til vision", "bedste pris/ydelse", "bedste til agents/tool use"
**Done:** >5 scenarier tilføjet, fakta verified

## Iteration 9 — RECOMMENDATION.md
**Opgave:** Konkret anbefaling til Yttre
**Input:** COMPARISON.md + alle profiler
**Yttres setup:** Claude Code (CLI), VPS (Ubuntu, Python, Qdrant, cron), voice assistant (Whisper), TransportIntra webapp, automation scripts, Substack research
**Scenarier:** "kun Anthropic" / "Anthropic + OpenAI embeddings" / "Anthropic + Gemini vision" / "fuld multi-provider"
**Done:** RECOMMENDATION.md >60 linjer, mindst 3 scenarier med pro/con, ét klart "start her" forslag

## Iteration 10 — Review
**Opgave:** 3 Reviewer-subagents
- Reviewer A: Fakta-check 5 pricing/specs claims mod kilder
- Reviewer B: Konsistens mellem profiler (samme format, ingen modsigelser)
- Reviewer C: Er RECOMMENDATION.md actionable? Ville Yttre vide hvad han skal gøre?
**Done:** EVALUATION.md med ærlig vurdering
```

---

## LOOP_STATE.md (initial)

```markdown
# Loop State

## Blokkere
(ingen)

## Filregister
(tomt)

## Næste: Iteration 1
Anthropic profil
```

---

## Start-kommando

```bash
mkdir -p /root/Yggdra/yggdra-pc/llm-landskab/providers
cd /root/Yggdra/yggdra-pc/llm-landskab

# Deploy filer (CLAUDE.md, LOOP_PLAN.md, LOOP_STATE.md) først

for i in $(seq 1 10); do
  echo "=== Iteration $i === $(date)"
  if grep -q "BLOCKED\|FAILED" LOOP_STATE.md 2>/dev/null; then
    echo "=== HALTED ==="
    cat LOOP_STATE.md | head -10
    break
  fi
  timeout 600 /root/.local/bin/claude --print \
    "Du er iteration $i af 10. Følg CLAUDE.md boot-sekvens."
  if ! grep -q "Iteration $i" LOOP_STATE.md 2>/dev/null; then
    echo "=== WARNING: iteration $i opdaterede ikke state ==="
  fi
  echo "=== Iteration $i done === $(date)"
  sleep 10
done
```

---

## Review fra telefon

```bash
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/llm-landskab/LOOP_STATE.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/llm-landskab/RECOMMENDATION.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/llm-landskab/COMPARISON.md"
ssh root@72.62.61.51 "find /root/Yggdra/yggdra-pc/llm-landskab/ -type f | wc -l"
```
