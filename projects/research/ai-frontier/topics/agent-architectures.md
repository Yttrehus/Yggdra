# Agent Architectures — State of the Art (marts 2026)

**Kilder:** HOW_TO_BUILD_AGENTS.md, CH6_AGENTS_*.md, agents_framework_comparison.md, armin_ronacher_agent_philosophy_2026.md, zechner_minimal_agent.md, anthropic_building_effective_agents.md, sources/manus_context_engineering.md

---

## 1. Fundamentet: Workflows vs. Agents

Anthropic trækker den eneste grænse der betyder noget:
- **Workflows:** Predefineret kontrolflow. Developeren bestemmer.
- **Agents:** LLM bestemmer kontrolflow dynamisk.

**Praksitest:** Kan du tegne hele flowet på en whiteboard FØR systemet kører? Ja → workflow. Nej → agent.
De fleste "agents" i markedet er reelt workflows — og det er fint. Workflows er billigere, mere reliable og nemmere at debugge.

**Modenhed:** Production-ready (workflows), Early adopter (agents)
**Relevans for Yttre:** Direkte brugbar — Yttres cron+hooks er L1-L2, scripts med LLM-kald er L4

---

## 2. Automationsspektret (L0-L5)

| Level | Hvad | Reliability | Cost | Yttre bruger? |
|-------|------|-------------|------|---------------|
| L0 | Manual | 100% | Tid | Ja (mest) |
| L1 | Cron + scripts | 99%+ | $0 | Ja (17 cron jobs) |
| L2 | Webhooks/events | 99%+ | $0 | Delvist (hooks) |
| L3 | Workflow engine | 99%+ | $0-50/mo | Nej (droppede n8n) |
| L4 | LLM-in-the-loop | 90-95% | $5-50/mo | Ja (morning_brief, save_checkpoint) |
| L5 | Autonom agent | 60-90% | $50-5K/mo | Eksperimentelt (Ralph loops) |

**Kerneindsigt:** De fleste problemer er L1-L3. Industrien hyper L5. "A cron job has never been cancelled for unclear business value."

---

## 3. De 6 Composable Patterns (Anthropic)

### Pattern 1: Augmented LLM
Model + retrieval + tools. Ikke en agent. Byggeklods.
- **Modenhed:** Production-ready
- **Relevans:** Direkte brugbar — Yttres ctx-kommando + Qdrant

### Pattern 2: Prompt Chaining
Sekventielle LLM-kald med validerings-gates.
- **Modenhed:** Production-ready
- **Relevans:** Direkte brugbar — save_checkpoint.py (destillering → NOW.md)

### Pattern 3: Routing
LLM klassificerer input → dispatcher til specialiseret handler.
- **Modenhed:** Production-ready
- **Relevans:** Direkte brugbar — task_router.py, Telegram dispatch

### Pattern 4: Parallelization
Fan-out til flere LLMs, fan-in resultater. Sectioning eller voting.
- **Modenhed:** Early adopter
- **Relevans:** Indirekte — research-agenter (3 parallelle) bruger dette

### Pattern 5: Orchestrator-Workers
Central LLM dekomponerer, delegerer til workers.
- **Modenhed:** Early adopter
- **Relevans:** Indirekte — Ralph loop er en simpel version

### Pattern 6: Evaluator-Optimizer
Generér → evaluér → iterér. Kræver ekstern ground truth.
- **Modenhed:** Eksperimentel (uden ground truth = self-deception)
- **Relevans:** Nice to know — Yttre har ingen eval pipeline

---

## 4. ReAct (Reason + Act)

Det mest udbredte agent-pattern. Think → Act → Observe → loop.

**Velegnet:** Dynamisk tool-selection, 3-7 steps, step-by-step reasoning.
**Uegnet:** Long-horizon planning, >10 steps (compounding error), faste procedurer.

**Failure modes:**
- Myopisk reasoning (lokalt optimalt, globalt forkert)
- Error propagation fra tidlige dårlige handlinger
- Infinite loops uden circuit breakers

**Modenhed:** Production-ready (med guardrails)
**Relevans for Yttre:** Direkte brugbar — Claude Code bruger ReAct internt
**Effort:** Timer (allerede aktivt brugt)

---

## 5. Plan-and-Execute

Separér planlægning fra eksekvering. Plan → Execute → Re-plan.

**Velegnet:** 10+ step tasks, behov for human approval af plan, audit trail.
**Uegnet:** Simple nok til ReAct, dynamiske miljøer hvor planer hurtigt forældes.

**Failure modes:** Plan rigidity, over-dekomposition (15 subtasks når 3 ville gøre det), plan hallucination (steps der refererer tools der ikke eksisterer).

Claude Code bruger denne arkitektur: planlæg multi-fil edits → vis plan → eksekver.

**Modenhed:** Early adopter
**Relevans:** Direkte brugbar — Ralph loops bruger implicit plan-execute
**Effort:** Timer

---

## 6. Minimalisten: Zechner/Ronacher-filosofien

Mario Zechner (pi) og Armin Ronacher repræsenterer den modsatte pol af framework-tilgangen:

**4 tools er nok:** Read, Write, Edit, Bash. Alt andet er støj.
**Intet MCP:** MCP-servere (Playwright: 13.7K tokens, Chrome DevTools: 18K) spiser 7-9% af context. CLI tools med README er billigere.
**Ingen sub-agents:** Fuld visibility. Spawner pi via bash hvis nødvendigt.
**Ingen plan mode:** Filbaserede planning docs i stedet for opaque sub-agent planning.
**YOLO by default:** Ingen permission prompts. Antagelsen: brugeren er kompetent.

**Selvmodifikation:** "If you want the agent to do something it doesn't do yet, you ask the agent to extend itself." Hot-reload, test i loop.

**Benchmark:** Terminal-Bench 2.0: pi + Claude Opus 4.5 konkurrerer med Codex, Cursor, Windsurf.

**Modenhed:** Early adopter (produktivt men niche)
**Relevans for Yttre:** Direkte brugbar — Yttre kører allerede minimal (4 tools + bash)
**Effort:** Timer (filosofi-alignment, ikke implementering)

---

## 7. MOM-patternet (Zechner/Ronacher)

Slack-bot bygget på pi. Per kanal:
- `log.jsonl` — komplet beskedhistorik (ground truth)
- `context.jsonl` — hvad LLM'en ser (synkroniseret fra log)
- `MEMORY.md` — kanalspecifik kontekst der bevares på tværs

**Selvforvaltende:** Installerer egne deps, skriver CLI-wrappers, opretter SKILL.md.

**Modenhed:** Eksperimentel
**Relevans for Yttre:** Direkte brugbar — MOM ≈ Yttres Telegram bot + memory pattern
**Effort:** Dage (men principperne er allerede implementeret)

---

## 8. Anti-patterns

### Agent sprawl
For mange agents der "samarbejder." Koordinationsoverhead > gevinst. 40% multi-agent piloter fejler inden 6 måneder.

### Context loss
Lang-kørende agents akkumulerer historie → context overflow → glemmer egen plan. Yttres PreCompact hook addresserer dette.

### Infinite loops
$47K API bill over 11 dage. To agents i recursive loop uden termination condition. **Altid circuit breakers.**

### Grading own homework
Evaluator-Optimizer uden ekstern ground truth. Agenten bekræfter sine egne fejl.

### Premature agentification
Bygger L5 agent til et L1 problem. "Most automation problems are Level 1-3."

---

## 9. Compounding Reliability Problem

Den vigtigste matematik i agent-design:

**Success = per_step_reliability ^ antal_steps**

| Steps | 95% per step | 99% per step |
|-------|-------------|-------------|
| 3 | 86% | 97% |
| 5 | 77% | 95% |
| 10 | 60% | 90% |
| 20 | 36% | 82% |

**Fixes:** Færre steps, human checkpoints, bedre per-step reliability (tool design > model capability).

---

## 10. State of the Field (marts 2026)

### Hvad virker
- Coding agents med human oversight (SWE-bench: 80.9%, Claude Opus 4.5)
- Customer support tier-1 deflection (50-65% automation)
- Research/analyse med klare parametre og review

### Hvad virker ikke (endnu)
- Fuldt autonome forretningsprocesser (11% i produktion)
- Multi-agent systems at scale (40% pilot failure)
- Computer use agents (GUI for ustabil)

### METR-bomben
RCT med 16 devs, 246 issues: **AI tools gjorde dem 19% langsommere.** De TROEDE de var 20-30% hurtigere. Self-reported productivity ≠ faktisk produktivitet.

---

## 11. Yttres Position

Yttre sidder i et sweet spot:
- **L1-L2 er solid** (cron, hooks, scripts)
- **L4 bruges aktivt** (LLM-in-the-loop: morning_brief, checkpoint, research)
- **L5 er eksperimentelt** (Ralph loops — fungerer men kræver supervision)
- **Minimal-filosofien** (4 tools, bash-first) aligner med Zechner/Ronacher
- **Context engineering** (CLAUDE.md, NOW.md, skills/) er Yttres stærkeste differentiator

### Næste skridt
1. Circuit breakers på Ralph loops (effort: timer)
2. Hybrid search i Qdrant for bedre retrieval (effort: dage)
3. Evaluerings-pipeline for at måle om agents faktisk hjælper (effort: dage)
