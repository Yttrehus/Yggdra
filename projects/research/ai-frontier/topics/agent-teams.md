# Agent Teams — Frameworks, Patterns & Erfaringer (marts 2026)

**Kilder:** agents_framework_comparison.md, CH6_AGENTS_AUTOMATION.md, armin_ronacher_agent_philosophy_2026.md, manus_context_engineering.md, HOW_TO_BUILD_AGENTS.md

---

## 1. Hvornår Teams vs. Single Agent

**90% af use cases klares af én agent med gode tools.** Multi-agent er kun berettiget når:
- Opgaven naturligt dekomponerer i uafhængige specialiseringer
- Perspektiv-diversitet forbedrer output (review, debate)
- Kontekstvinduet er for lille til hele opgaven

**Multi-agent pilot failure rate:** 40% inden 6 måneder (Gartner 2025)
**Mest udbredte failure mode:** Agents der taler i cirkler, brænder tokens uden konvergens.

---

## 2. Multi-Agent Patterns

### Orchestrator-Workers
Central agent dekomponerer, delegerer til specialiserede workers.
- Claude Agent SDK: parent→subagent
- CrewAI: hierarchical process med manager
- LangGraph: supervisor node med conditional edges

### Pipeline (Sequential)
Agent A → Agent B → Agent C. Hvert trin processer output fra forrige.
- CrewAI sequential process
- Manus: append-only context, KV-cache optimeret

### Debate/Review
To+ agents diskuterer til konvergens eller approval.
- AutoGen: RoundRobinGroupChat, SelectorGroupChat
- Evaluator-Optimizer pattern (Anthropic)

### Handoff (Routing)
Triage-agent sender samtalen videre til specialist. Kun én agent aktiv ad gangen.
- OpenAI Swarm: transfer-funktioner
- Claude Agent SDK: subagent invocation

### Swarm
Mange peer-agents med decentraliseret koordination.
- AutoGen Swarm pattern
- I praksis: mest hype, mindst produktion

---

## 3. Framework-vurdering

### CrewAI — Role-Based Crews
**Stars:** ~30K | **Modenhed:** Stabil (v0.80+)

**Arkitektur:** Agents med roller, goals, backstories. Crews orkestrerer. Flows wrapper til produktion.
**Memory:** 4 typer built-in (short-term, long-term, entity, contextual).
**Multi-agent:** Sequential eller hierarchical (manager delegerer).

**Styrker:** Intuitiv rollemodel, rig memory, god docs.
**Svagheder:** Abstractions-overhead, role/backstory prompting brænder tokens (~30% ekstra), debugging er ugennemsigtig.

**Cost:** $0.15-0.50 per run (4-agent crew, GPT-4o). Hierarchical ~2x sequential.

**Modenhed:** Early adopter
**Relevans for Yttre:** Indirekte relevant — Yttre foretrækker minimal tilgang
**Effort:** Dage (setup + tilpasning)

---

### AutoGen (Microsoft) — Conversational Multi-Agent
**Stars:** ~40K | **Modenhed:** Pre-1.0 (v0.4)

**Arkitektur:** 4 lag (Core, AgentChat, Extensions, Studio). Agent-samarbejde = gruppesamtale.
**Memory:** Ingen built-in long-term. State serialization for checkpointing.
**Multi-agent:** RoundRobin, Selector, Swarm, GraphFlow.

**Styrker:** Mest modne community, fleksible patterns, code execution built-in, cross-language (Python + .NET).
**Svagheder:** API churn (v0.2→v0.4 breaking), group chat spiral, heavy deps, ingen long-term memory.

**Cost:** $0.10-2.00 per task. Group chats med 3+ agents: $0.50-2.00.

**Modenhed:** Early adopter (enterprise-backed men ustabilt API)
**Relevans for Yttre:** Nice to know — for komplekst til solo setup
**Effort:** Uger

---

### Swarm (OpenAI) — Lightweight Handoffs
**Stars:** ~20K | **Modenhed:** Eksperimentel (erstattet af Agents SDK)

**Arkitektur:** ~500 linjer. Stateless. Agent = navn + instructions + funktioner. Handoff = funktion der returnerer anden agent.
**Memory:** Ingen. Stateless.

**Styrker:** Dødenkelt. Læs hele koden på 20 min. Perfekt til læring.
**Svagheder:** Ikke production-ready, ingen persistence, OpenAI-only, superseded.

**Cost:** $0.02-0.20 per interaction.

**Modenhed:** Eksperimentel (droppet)
**Relevans for Yttre:** Nice to know — handoff-patternet er brugbart som koncept
**Effort:** Timer (men ingen produktionsværdi)

---

### smolagents (Hugging Face) — Code-First
**Stars:** ~15K | **Modenhed:** Stabil (v1.x)

**Arkitektur:** ~1000 linjer. Agents skriver Python i stedet for JSON tool calls. 30% færre LLM-kald.
**Memory:** Ingen persistence.
**Multi-agent:** ManagedAgent (hierarchisk delegation).

**Styrker:** Minimalt, model-agnostisk, gratis med lokale modeller, Hub til tool-deling.
**Svagheder:** Code execution = sikkerhedsrisiko, basalt multi-agent, ingen observability.

**Cost:** Gratis med lokale modeller. $0.02-0.10 med cloud API.

**Modenhed:** Early adopter
**Relevans for Yttre:** Indirekte relevant — code-agent idéen er interessant for Qdrant-scripts
**Effort:** Dage

---

### LangGraph — Graph-Based Orchestration
**Stars:** ~10K | **Modenhed:** Stabil (v0.2+)

**Arkitektur:** StateGraph med nodes (funktioner), conditional edges, typed state.
**Memory:** Built-in checkpointing (pause, resume, fork, replay).
**Multi-agent:** Agents som subgraphs, supervisor patterns.

**Styrker:** Mest kontrol over flow, production-grade persistence, stærkt human-in-the-loop.
**Svagheder:** Stejl læringskurve (grafprogrammering), bundet til LangChain, verbose for simple tasks.

**Modenhed:** Production-ready (for komplekse use cases)
**Relevans for Yttre:** Indirekte relevant — overkill for solo, men persistence-idéerne er gode
**Effort:** Uger

---

### Claude Agent SDK — Anthropic's Framework
**Modenhed:** Ny (2026)

**Arkitektur:** Claude Code som library. Built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch). Hooks for governance.
**Memory:** Sessions (resumable, forkable) + CLAUDE.md + Skills.
**Multi-agent:** Parent-child subagents.

**Styrker:** Zero tool implementation, same capabilities som Claude Code, hooks, sessions.
**Svagheder:** Claude-only (komplet vendor lock-in), dyr (Opus: $0.50-3.00/task), nyere økosystem.

**Modenhed:** Early adopter
**Relevans for Yttre:** Direkte brugbar — Yttre kører allerede Claude Code med hooks og skills
**Effort:** Timer (allerede i brug implicit)

---

## 4. Sammenligningstabel

| Dimension | CrewAI | AutoGen | Swarm | smolagents | LangGraph | Claude SDK |
|-----------|--------|---------|-------|------------|-----------|------------|
| Kompleksitet | Medium | Høj | Lav | Lav | Høj | Lav |
| Multi-agent | Roller | Gruppesamtale | Handoff | Hierarkisk | Graf | Parent-child |
| Memory | 4 typer | Ekstern | Ingen | Ingen | Checkpoints | Sessions |
| Model lock-in | Nej | Nej | OpenAI | Nej | Nej | Anthropic |
| Cost/task | $0.15-0.50 | $0.10-2.00 | $0.02-0.20 | $0.00-0.10 | API pris | $0.10-3.00 |
| Bedst til | Forretning | Enterprise | Læring | Open-source | Komplekse flows | Kode-automation |

---

## 5. Yttres Erfaringer

### Ralph Loops (Sandbox v1-v3)
Yttres multi-agent erfaringer er primært fra Ralph loops:
- `claude --print` i loop med iterationsnummer
- LOOP_STATE.md som shared state (fil-baseret, ikke framework)
- LOOP_PLAN.md som dekomposition (plan-and-execute pattern)
- Circuit breakers: max iterationer, timeout

**Hvad virker:** Simpel, fuld visibility, alt på disk, ingen framework-afhængighed.
**Hvad fejler:** Ingen automatisk recovery ved fejl. Context loss over mange iterationer. Ingen parallel execution.

### Subagent-delegering
Claude Code's Task tool = parent-child delegation. Erfaringer:
- Agenter kan køre i timevis uden feedback (ISS-001, 8/3-2026)
- **Altid sæt timeout/max_turns** (3-5 min per agent)
- Rate-limiting og context overflow = stille fejl

### Manus-inspiration
Manus' context engineering er direkte relevant:
- **KV-cache optimering:** Append-only context, stable prefixes → 10x billigere
- **File system som memory:** Skriv til disk, læs on demand → ingen context overflow
- **Todo.md pattern:** Manipulér attention via recitation → agent glemmer ikke planen

---

## 6. Anbefalinger for Yttre

1. **Bliv på Claude SDK + bash** — ingen framework giver merværdi for solo setup
2. **Implementér circuit breakers** på alle agent-loops (max_turns, timeout, cost cap)
3. **Adopter Manus' append-only context** — stop med at mutere state i prompts
4. **Todo.md pattern** til komplekse opgaver — eksplicit attention management
5. **Undgå multi-agent frameworks** medmindre opgaven kræver parallel specialisering
6. **Mål faktisk produktivitet** — METR viste at perceived ≠ actual
