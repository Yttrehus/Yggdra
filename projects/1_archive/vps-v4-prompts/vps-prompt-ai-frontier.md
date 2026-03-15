# VPS Ralph Loop — AI Frontier

Deploy til `/root/Yggdra/yggdra-pc/ai-frontier/`.
10 iterationer. Kan køre parallelt med llm-landskab.

---

## CLAUDE.md

```markdown
# AI Frontier — Sandbox

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

State of the art i AI agents, automation, hukommelse, workflows.
Fokus: hvad virker, hvad er hype, hvad kan Yttre implementere i morgen.
Output i `topics/` og rod-filer.

## Regler

### Token-bevidsthed
- Læs ALDRIG filer >500 linjer i helhed. Brug head, tail, grep
- Max 3 parallelle subagents
- Skriv kompakt

### Eksisterende research (BRUG DEN)
Der er 60+ research-filer i /root/Yggdra/research/. Start altid med at læse eksisterende materiale FØR du researcher nyt. Din opgave er syntese, ikke gentagelse.

Nøglefiler:
- CH6_AGENTS_AUTOMATION.md, CH6_AGENTS_PRACTICE.md, CH6_AGENTS_PRODUCTION.md
- HOW_TO_BUILD_AGENTS.md
- AI_MEMORY_SYSTEMS_SURVEY.md
- memory_autonomy_research_2026-02-23.md
- AI_WORKFLOW_RESEARCH_2026.md
- /root/Yggdra/data/miessler_bible/ (PAI arkitektur)
- /root/Yggdra/yggdra-pc/research/reports/ (3 rapporter fra sandbox v1)

### Vurdering per emne
For hvert topic, bedøm eksplicit:
- **Modenhed:** Production-ready / Early adopter / Eksperimentel / Hype
- **Relevans for Yttre:** Direkte brugbar / Indirekte relevant / Nice to know
- **Implementation effort:** Timer / Dage / Uger

### Build > Research
- Hver iteration SKAL producere filer på disk

### Done = Verified
- Test med kommandoer, spot-check

### Miljø
- Du er PÅ VPS'en
- SØG IKKE på nettet
- Qdrant: curl localhost:6333/...
```

---

## LOOP_PLAN.md

```markdown
# Loop Plan — AI Frontier (10 iterationer)

## Iteration 1 — Audit eksisterende research
**Opgave:** Kategorisér /root/Yggdra/research/ (alle .md filer)
**Metode:** 2 subagents:
- Sub A: `find /root/Yggdra/research/ -name '*.md' -exec wc -l {} + | sort -rn` + head -5 af de 15 største
- Sub B: Kategorisér efter emne (agents, memory, tools, workflow, prompting, infrastructure, other)
- Merger til _audit.md
**Done:** _audit.md med tabel [fil, emne, linjer, kvalitet (1-5), dækning], >50 entries

## Iteration 2 — Agent Architectures
**Opgave:** Byg topics/agent-architectures.md
**Input:** _audit.md + CH6_AGENTS_*.md + HOW_TO_BUILD_AGENTS.md
**Dæk:**
- Single agent patterns (ReAct, tool-use loops, planning)
- Multi-agent patterns (orchestrator, pipeline, debate, swarm)
- Claude-specifikt: subagents, Agent SDK, --print loops
- Anti-patterns (agent sprawl, context loss, infinite loops)
**Format:** Per pattern: beskrivelse, modenhed, relevans for Yttre, eksempel
**Done:** >100 linjer, >6 patterns beskrevet

## Iteration 3 — Agent Teams
**Opgave:** Byg topics/agent-teams.md
**Input:** _audit.md + eksisterende research + Miessler PAI agent system
**Dæk:**
- Frameworks: CrewAI, AutoGen, LangGraph, Claude subagents, custom (Ralph loops)
- Erfaringer: hvad virker i praksis vs. demo-kvalitet
- Yttres erfaringer: sandbox v2 loops, subagent-delegering
- Hvornår teams vs. single agent
**Done:** >100 linjer, >4 frameworks vurderet

## Iteration 4 — Memory Systems del 1
**Opgave:** Byg topics/memory-systems.md (første halvdel: RAG + vector DB)
**Input:** AI_MEMORY_SYSTEMS_SURVEY.md + memory_autonomy_research.md + CH5_*.md
**Dæk:**
- RAG patterns (naive, advanced, hybrid search, reranking)
- Vector DB valg (Qdrant vs. alternativer)
- Chunking strategier
- Yttres Qdrant setup (84K vektorer, dense-only → hybrid?)
**Done:** >80 linjer, med konkrete anbefalinger for Yttres Qdrant

## Iteration 5 — Memory Systems del 2
**Opgave:** Udvid topics/memory-systems.md (knowledge graphs + session persistence + episodic)
**Input:** Miessler PAI memory (3 tiers) + human_memory_research.md
**Dæk:**
- Knowledge graphs (hvornår, frameworks, cost/benefit)
- Session persistence (compaction, checkpoints, hooks)
- Episodic memory (Miessler SIGNALS, ratings, failure captures)
- Claude Memory (auto-memory system) vs. custom
**Done:** memory-systems.md total >150 linjer

## Iteration 6 — Automation Patterns
**Opgave:** Byg topics/automation-patterns.md
**Input:** Audit af /root/Yggdra/scripts/ + crontab -l + hooks
**Dæk:**
- Hvad kører allerede (cron jobs, hooks, scripts) — komplet inventar
- Event-driven patterns (hooks, webhooks, file watchers)
- Proaktiv AI (scheduled research, auto-digest, auto-maintenance)
- Ralph loops som pattern (erfaringer fra sandbox v1+v2)
**Done:** >80 linjer + inventar af alle kørende automations

## Iteration 7 — Automation Patterns del 2 + Miessler PAI
**Opgave:** Udvid med Miessler PAI hooks/orchestration + Nate principper
**Input:** /root/Yggdra/data/miessler_bible/ + Nate transcripts
**Dæk:**
- Miessler: 17 hooks, 7 lifecycle events, FormatReminder, Algorithm
- Nate: intent-first, memory as foundation, progressive automation
- Hvad kan Yttre adoptere direkte?
**Done:** automation-patterns.md total >120 linjer

## Iteration 8 — WHAT_IF.md
**Opgave:** "Hvad kan Yttre implementere i morgen?"
**Input:** Alle topic-filer
**Format per forslag:**
```
### [Forslag]
**Effort:** Timer/Dage/Uger
**Impact:** Høj/Medium/Lav
**Kræver:** [dependencies]
**Risiko:** [hvad kan gå galt]
**How-to:** [3-5 konkrete steps]
```
**Inkludér også:** "Hvad hvis Yttre skifter codebase?" (Cursor, Windsurf, Aider). "Hvad hvis multi-provider?"
**Done:** >80 linjer, >5 forslag, prioriteret

## Iteration 9 — GAPS.md
**Opgave:** Hvad mangler i Yttres setup vs. state of the art?
**Input:** Alle topic-filer + WHAT_IF.md
**Format:** Gap → hvad state of the art gør → hvad Yttre har i dag → effort at lukke
**Done:** >60 linjer, >5 gaps identificeret

## Iteration 10 — Review
**Opgave:** 3 Reviewer-subagents
- Reviewer A: Er topics-filerne baseret på eksisterende research (ikke halluceret)?
- Reviewer B: Er modenhed/relevans-vurderingerne konsistente?
- Reviewer C: Er WHAT_IF.md actionable? Ville Yttre vide hvad han skal gøre mandag?
**Done:** EVALUATION.md
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
Audit eksisterende research
```

---

## Start-kommando

```bash
mkdir -p /root/Yggdra/yggdra-pc/ai-frontier/topics
cd /root/Yggdra/yggdra-pc/ai-frontier

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
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/ai-frontier/LOOP_STATE.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/ai-frontier/WHAT_IF.md"
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/ai-frontier/GAPS.md"
ssh root@72.62.61.51 "ls /root/Yggdra/yggdra-pc/ai-frontier/topics/"
```
