# Destillat: AI Agents & Automation

**Produceret:** 15. marts 2026
**Metode:** Destillering af 13 research-filer fra Yggdra-systemet. Overlappende materiale elimineret, evidensgrundlag markeret, litteraturliste konsolideret.
**Evidensmarkeringer:** [SOLID] = peer-reviewed/reproducerbart, [ANEKDOTISK] = praktiker-erfaring (n=1-5), [VENDOR] = producent-claims uden uafhængig verifikation.

---

## 1. Agent-arkitekturer

### 1.1 Den afgørende distinktion: Workflows vs. Agents

Anthropic trækker den eneste grænse der tåler kritisk eftersyn:

- **Workflows:** Predefineret kontrolflow. Developeren bestemmer rækkefølgen.
- **Agents:** LLM bestemmer kontrolflow dynamisk.

Praksistest: kan du tegne hele flowet på en whiteboard FØR systemet kører? Ja = workflow. Nej = agent. De fleste systemer markedsført som "agents" er workflows — og det er korrekt design. Workflows er billigere, mere pålidelige og nemmere at debugge. [SOLID — Anthropic, "Building Effective Agents", 2025]

### 1.2 Automationsspektret (L0-L5)

| Level | Beskrivelse | Pålidelighed | Omkostning |
|-------|-------------|-------------|-----------|
| L0 | Manuel | 100% | Tid |
| L1 | Cron + scripts | 99%+ | $0 |
| L2 | Webhooks/events | 99%+ | $0 |
| L3 | Workflow engine (n8n, Temporal) | 99%+ | $0-50/md |
| L4 | LLM-in-the-loop | 90-95% | $5-50/md |
| L5 | Autonom agent | 60-90% | $50-5K/md |

**Kerneindsigt:** De fleste automatiseringsproblemer er L1-L3. Industrien hyper L5. En cron-job er aldrig blevet aflyst for "unclear business value." [ANEKDOTISK — konsensus blandt Ronacher, Zechner, Miessler]

### 1.3 Anthropics 6 composable patterns

1. **Augmented LLM** — Model + retrieval + tools. Ikke en agent. Byggestenen. [SOLID]
2. **Prompt Chaining** — Sekventielle LLM-kald med valideringsgates. [SOLID]
3. **Routing** — LLM klassificerer input, dispatcher til handler. [SOLID]
4. **Parallelization** — Fan-out til flere LLMs, fan-in resultater. [SOLID]
5. **Orchestrator-Workers** — Central LLM dekomponerer, delegerer. [ANEKDOTISK]
6. **Evaluator-Optimizer** — Generér, evaluér, iterér. Kræver ekstern ground truth; uden den er det selvbedrag. [ANEKDOTISK]

### 1.4 ReAct (Reason + Act)

Det mest udbredte agent-pattern. Think, Act, Observe, loop. Velegnet til dynamisk tool-selection i 3-7 steps. Uegnet til long-horizon planning (>10 steps) på grund af compounding error. [SOLID — Yao et al., 2023]

**Failure modes:** Myopisk reasoning, error propagation fra tidlige handlinger, infinite loops uden circuit breakers.

### 1.5 Plan-and-Execute

Separér planlægning fra eksekvering. Plan, Execute, Re-plan. Velegnet til 10+ step tasks med behov for human approval af plan. Uegnet når planer hurtigt forældes i dynamiske miljøer.

**Failure modes:** Plan rigidity, over-dekomposition (15 subtasks når 3 er nok), plan hallucination (steps der refererer tools der ikke eksisterer). [ANEKDOTISK]

### 1.6 Minimalismen: Zechner/Ronacher-filosofien

Mario Zechner (PI-skaber) og Armin Ronacher (Flask-skaber, Sentry CTO) repræsenterer den modsatte pol af framework-tilgangen:

- **4 tools er nok:** Read, Write, Edit, Bash. Alt andet er støj.
- **Intet MCP:** MCP-servere spiser 7-9% af kontekstvinduet, uanset om de bruges. CLI-tools med README er billigere via "progressive disclosure."
- **Ingen sub-agents:** Fuld visibility. Spawner separate pi-instancer via bash hvis nødvendigt.
- **Ingen plan mode:** Filbaserede planning docs (PLAN.md) frem for opaque sub-agent planning.
- **YOLO by default:** Ingen permission prompts. Containere er svaret, ikke falsk tryghed.

**Benchmark-evidens:** Terminal-Bench 2.0 — PI + Claude Opus 4.5 konkurrerer med Codex, Cursor, Windsurf. [ANEKDOTISK — Zechner, 2025]

**MCP vs CLI benchmark** (120 tests, 3 tasks, 4 tools, 10 repetitioner):

| Tool | Gennemsnitspris | Varighed |
|------|----------------|----------|
| tmux | $0.3729 | 1m 28.7s |
| terminalcp CLI | $0.3865 | 1m 37.2s |
| terminalcp MCP | $0.4804 | 1m 22.6s |
| screen | $0.6003 | 1m 46.2s |

Alle tools: 100% success rate. MCP er hurtigere men dyrere. Zechners konklusion: "Inherent knowledge about standard tools beats in-context learning about previously unseen tools." [ANEKDOTISK — Zechner, 2025-08-15]

---

## 2. Frameworks sammenlignet

### 2.1 Sammenligningstabel

| Dimension | CrewAI | AutoGen | Swarm | smolagents | LangGraph | Claude SDK |
|-----------|--------|---------|-------|------------|-----------|------------|
| Stars | ~30K | ~40K | ~20K | ~15K | ~10K | N/A |
| Kompleksitet | Medium | Høj | Lav | Lav | Høj | Lav |
| Multi-agent | Roller | Gruppesamtale | Handoff | Hierarkisk | Graf | Parent-child |
| Memory | 4 typer built-in | Ekstern | Ingen | Ingen | Checkpoints | Sessions |
| Model lock-in | Nej | Nej | OpenAI | Nej | Nej | Anthropic |
| Cost/task | $0.15-0.50 | $0.10-2.00 | $0.02-0.20 | $0.00-0.10 | API-pris | $0.10-3.00 |
| Modenhed | Stabil | Pre-1.0 | Droppet | Stabil | Production | Early adopter |

### 2.2 CrewAI — Role-Based Crews

**Filosofi:** Teams af rollebaserede agenter. Du "ansætter" Research Analyst, Technical Writer osv.
**Styrker:** Intuitiv rollemodel, rig memory (4 typer: short-term, long-term, entity, contextual), god dokumentation.
**Svagheder:** Abstractions-overhead. Role/backstory prompting brænder ~30% ekstra tokens. Debugging er ugennemsigtig. Hierarchical mode fordobler omkostningen.
**Bedst til:** Forretningsprocesautomation hvor tasks mapper til menneskelige roller. [VENDOR — CrewAI docs]

### 2.3 AutoGen (Microsoft) — Conversational Multi-Agent

**Filosofi:** Agent-samarbejde = gruppesamtale. Agenter sender beskeder til hinanden.
**Styrker:** Mest modne community, fleksible patterns (RoundRobin, Selector, Swarm, GraphFlow), code execution built-in, cross-language (Python + .NET).
**Svagheder:** API churn (v0.2 til v0.4 var en breaking rewrite). Group chat kan spiralere (agenter taler i cirkler uden konvergens). Ingen built-in long-term memory. Tungt dependency-tree.
**Status:** Microsoft Agent Framework (merger AutoGen + Semantic Kernel) targeterer 1.0 GA Q1 2026.
[VENDOR — Microsoft docs, community reports]

### 2.4 Swarm (OpenAI) — Lightweight Handoffs

~500 linjer kode. Stateless. Agent = navn + instructions + funktioner. Handoff = funktion der returnerer anden agent. Eksplicit eksperimentel — erstattet af OpenAI Agents SDK. Perfekt til at lære multi-agent patterns. Ingen produktionsværdi. [VENDOR]

### 2.5 smolagents (Hugging Face) — Code-First

~1000 linjer. Agenter skriver Python i stedet for JSON tool calls — 30% færre LLM-kald. Model-agnostisk, gratis med lokale modeller. Minimalt multi-agent (ManagedAgent). Code execution = sikkerhedsrisiko. Ingen observability. [VENDOR]

### 2.6 LangGraph — Graph-Based Orchestration

**Filosofi:** Nodes gør arbejdet, edges bestemmer hvad der sker derefter.
**Styrker:** Mest kontrol over flow. Production-grade persistence (checkpointing, pause, resume, fork, replay). Stærkt human-in-the-loop.
**Svagheder:** Stejl læringskurve (grafprogrammering). Verbose for simple tasks. Bundet til LangChain.
**Bedst til:** Komplekse flows der kræver finkornet kontrol over state transitions. [ANEKDOTISK]

### 2.7 Claude Agent SDK — Anthropics Framework

Claude Code som library. Built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch). Hooks for governance. Sessions (resumable, forkable). CLAUDE.md + Skills.
**Styrker:** Zero tool implementation, same capabilities som Claude Code.
**Svagheder:** Komplet vendor lock-in (Claude-only). Dyr (Opus: $0.50-3.00/task). Yngre økosystem.
[VENDOR — Anthropic, 2026]

### 2.8 Ærlig vurdering

**For solo-udviklere:** Intet framework giver merværdi over Claude SDK + bash. Frameworks tilføjer kompleksitet uden proportional gevinst når der kun er én bruger og ét runtime-miljø.

**For teams:** LangGraph til komplekse stateful flows. CrewAI til rollebaserede pipelines. AutoGen til enterprise/Microsoft-miljøer.

**For alle:** 90% af use cases klares af én agent med gode tools. Multi-agent er kun berettiget ved: (1) naturlig dekomposition i uafhængige specialiseringer, (2) perspektiv-diversitet, (3) kontekstvinduet er for lille. Multi-agent pilot failure rate: 40% inden 6 måneder. [ANEKDOTISK — Gartner, 2025]

---

## 3. Compounding reliability

### 3.1 Matematikken

**Success = per_step_reliability ^ antal_steps**

| Steps | 95% per step | 99% per step |
|-------|-------------|-------------|
| 3 | 86% | 97% |
| 5 | 77% | 95% |
| 10 | 60% | 90% |
| 20 | 36% | 82% |

En 5-step agent med 95% per-step pålidelighed lykkes 77% af tiden. Et forkert tool-valg i step 2 forgifter alle efterfølgende steps. [SOLID — matematisk identitet; observeret i praksis af METR og Superface]

### 3.2 METR-studiet

RCT med 16 erfarne udviklere, 246 issues over 3 uger. Resultat: **AI-tools gjorde dem 19% langsommere.** Udviklerne *troede* de var 20-30% hurtigere. Selvrapporteret produktivitet afveg markant fra målt produktivitet. [SOLID — METR, 2025, pre-registreret RCT]

**Implikation:** Man kan ikke evaluere agents via intuition. Instrumenteret, automatiseret måling er nødvendig.

### 3.3 Bredere failure rates

- 75% af agentic AI-opgaver fejler i produktion på reelle workflows (Superface, 2025). [ANEKDOTISK — survey]
- 95% af enterprise AI-piloter når ikke produktion. [ANEKDOTISK — industri-surveys]
- Kun 11% af organisationer har agentic AI i produktion (Cleanlab, late 2025). [ANEKDOTISK — survey]

### 3.4 Modforanstaltninger

1. **Færre steps.** Redesign opgaven til at kræve færre agent-beslutninger.
2. **Human checkpoints.** Menneske godkender kritiske beslutninger.
3. **Bedre per-step reliability.** Tool-design (80% af værdien) > model capability (20%).
4. **Circuit breakers.** Max iterationer, timeout, cost cap. Aldrig loops uden termination.
5. **Evaluering.** Offline eval på testsæt (52.4% adoption iflg. LangChain survey). Online eval via LLM-judges og anomaly detection.

---

## 4. Context engineering

### 4.1 Definition

Tobi Lutke (Shopify CEO, 2025): Prompten er ~5% af kontekstvinduet. De øvrige 95% er scaffolding — retrievede dokumenter, samtalehistorik, tool-definitioner, memory og state. Andrej Karpathy bekræftede: "The delicate art and science of filling the context window with just the right information for the next step." [ANEKDOTISK — offentlige posts]

### 4.2 Tre kræfter

**Context rot.** Accuracy falder med voksende kontekst. "Lost in the middle"-effekten: information begravet i midten af lang kontekst er effektivt usynlig. "Things start falling apart around 100K tokens. Benchmarks be damned." (Zechner, 2025) [ANEKDOTISK — reproduktivt observeret af flere praktikere]

**Token-eksplosion.** Produktionsagenter (Manus) rapporterer 100:1 input-til-output token ratio. En 50-step agent-session kan nå 200K+ tokens, hvoraf størstedelen er stale tool output. [VENDOR — Manus]

**Cost-skalering.** Tokens i kontekst betales ved *hvert* API-kald. KV-cache misses (fra kontekst-mutationer) multiplicerer dette. [SOLID — API-prisstrukturer]

### 4.3 Fire strategier

**Offload (skriv til disk).** Det mest undervurderede pattern. I stedet for at holde state i samtalen: skriv til disk, læs on demand. Filsystemet er ubegrænset, persistent og direkte opererbart. Zechner: "Prompts are code, .json/.md files are state." GSD formaliserer det med STATE.md (<150 linjer, pointer-fil). [ANEKDOTISK — Zechner 2025-06-02]

**Reduce (komprimér).** Sliding window compaction (summarize old, keep recent verbatim). Tool output compaction (reducer 10K tokens til 500 med metadata bevaret). Manus rapporterer 60-80% token-reduktion over 50+ tool calls. [VENDOR — Manus]

**Isolate (frisk kontekst).** Spawn sub-agenter med rene 200K-token vinduer. GSD: hver task-plan eksekveres af en sub-agent der kun ser plan + config + state pointers — ikke fuld sessionshistorik. Orkestratoren forbliver på 10-15% kontekst-udnyttelse. PI's session branching: forgren sessionen, løs delproblem, bring kun resultatet tilbage. [ANEKDOTISK — GSD, Zechner]

**Disclose progressively (load on demand).** Manus' todo.md recitation-pattern: konstant genskriv todo-listen i slutningen af kontekst. Modvirker goal drift via recency bias. CLI-tools med READMEs giver progressive disclosure — agenten betaler token-prisen kun ved aktiv brug, modsat MCP-servere der dumper 7-9% altid. [VENDOR — Manus, ANEKDOTISK — Zechner]

**Samlet effekt:** Anthropic rapporterer at context engineering-strategier giver **54% bedre agent-performance** versus prompt-optimering alene. [VENDOR — Anthropic engineering blog]

### 4.4 Systempromptstørrelse

PIs systemprompt er ~500 tokens. Konkurrenter bruger 10.000+. Zechners konklusion: frontier-modeller er trænet via RL til at forstå coding agent-mønstre; massive prompts tilføjer støj, ikke signal. [ANEKDOTISK — Zechner]

---

## 5. Praktikere vs. forskere

### 5.1 Armin Ronacher — Minimalisme og kritisk tænkning

**Profil:** Skaber af Flask, Jinja2, Click, Werkzeug. Medgrundlægger/CTO Sentry (forlod 2025). Grundlagde Earendil (2026).

**Kernepositioner:**

- **MCP-fravalg:** "I barely use MCP because Claude Code is very capable of just running regular tools." Bruger kun Playwright MCP. Alt andet via scripts/Makefile. [ANEKDOTISK]
- **Agent Psychosis (jan. 2026):** Ukritisk accept af AI-output. "It takes you a minute of prompting...but actually honestly reviewing a pull request takes many times longer." Review er bottleneck, ikke generation. [ANEKDOTISK]
- **The Final Bottleneck (feb. 2026):** Nu er kodeskrivning hurtigere end kodereview. Den irreduktible bottleneck: human review + accountability. 2500+ PRs i limbo i OpenClaw. Engineers mister overblik. [ANEKDOTISK]
- **SDK-valg:** Gå direkte mod provider-SDK. Aldrig Vercel AI SDK eller andre abstraktionslag. Forskelle mellem modeller er for store.
- **Caching:** Manuelle cache-points (Anthropic) > automatisk. Dynamisk information efter cache-points.
- **Model-præferencer:** Haiku + Sonnet til tool-calling loops (bedre end GPT). Gemini til dokumenter/PDF/billeder. GPT til mobile.
- **Memory:** "Agent memory isn't model learning. It's state ownership + rehydration." Plain Markdown, filer = ground truth.
- **Sikkerhed:** "Lethal trifecta" (Willison): private data + untrusted content + external communication = prompt injection risiko.

### 5.2 Mario Zechner — PI og den minimale agent

**Profil:** Skaber af PI coding agent, libGDX, heisse-preise.io.

**Kernepositioner:**

- **Systempromptstørrelse er invers korreleret med performance.** 500 tokens > 10.000 tokens. [ANEKDOTISK]
- **4-tool-arkitekturen er et valg, ikke en begrænsning.** Read, Write, Edit, Bash. "Models know how to use bash and have been trained on similar schemas."
- **No-MCP som princip.** Progressive disclosure via CLI > 7-9% permanent kontekst-overhead.
- **Session-kontinuitet via filbaseret state.** PLAN.md på disk. Deles, versionsstyres, observerbart.
- **YOLO mode som default.** Permission-checks er falsk tryghed.
- **Selvmodifikation.** "If you want the agent to do something it doesn't do yet, you ask the agent to extend itself." Hot-reload, test i loop.

**Praktisk demonstration:** MiniJinja Go-port. 10 timers session (3 timers supervision + 7 timer uovervåget). ~45 min aktiv human-tid. $60 i API-tokens, 2.2M tokens. Skiftede fra Opus 4.5 til GPT-5.2 Codex for long-tail test-fixing. [ANEKDOTISK — Ronacher, 2026-01-14]

### 5.3 Daniel Miessler — Personal AI Infrastructure

**Profil:** Sikkerhedsekspert, Fabric-skaber, PAI-arkitekt.

**PAI-arkitektur:**
- **TELOS:** 10 identitetsfiler (MISSION, GOALS, PROJECTS, BELIEFS, MODELS, STRATEGIES, NARRATIVES, LEARNED, CHALLENGES, IDEAS) autoloaded som kontekst.
- **6 lag customization:** Identity, Preferences, Workflows, Skills, Hooks, Memory.
- **3-tier memory:** Hot (aktiv session), Warm (nylig), Cold (arkiv).
- **The Last Algorithm:** Loop: observér CURRENT STATE, sammenlign med IDEAL STATE, tag optimal handling, gentag.
- **AIMM (AI Impact Maturity Model):** 5 niveauer. "Move as fast as possible to Level 2. Get your context into it."
- **Multi-provider agents:** Claude + Gemini + Grok parallelt, voice output via ElevenLabs. [VENDOR — Miessler]

### 5.4 Nate Jones — Strateg og enterprise-tænker

**5 kerneindsigter:**
1. **Context Engineering > Domain Memory.** "Domain memory er biblioteket. Context engineering er hvad der ligger på skrivebordet."
2. **Human Throttle.** Reversibilitet afgør om AI kan handle autonomt. 5 primitiver: comfort zones, undo-infrastruktur, human throttle, reversibilitet, bounded operations.
3. **Non-Engineer Builder.** De der bygger AI-native systemer først, får uindhentelig fordel.
4. **Compounding Gap.** Forskellen mellem forberedte og uforberedte vokser eksponentielt.
5. **Attention Drowning.** Selv med 100K+ tokens forringes reasoning. Signal drukner i støj. [ANEKDOTISK — Jones YouTube, 5 videoer]

### 5.5 Syntese: Praktikere vs. Framework-producenter

| Dimension | Praktikere (Ronacher, Zechner) | Framework-producenter (CrewAI, LangGraph) |
|-----------|-------------------------------|------------------------------------------|
| Tooling | 4 tools, bash, scripts | 200+ integrations, MCP |
| Memory | Markdown-filer, plain text | Vector DBs, embedded memory systems |
| Multi-agent | "Brug det ikke" | Kernefeature |
| Filosofi | Kontrol, observerbarhed | Abstraktion, convenience |
| Evidens | Egne codebases, benchmarks | Blog posts, demos |
| Pris | $0.05-0.50/task | $0.15-3.00/task |

---

## 6. Automation spectrum — hvornår bruges hvad

### 6.1 Decision framework

| Signal | Brug dette level |
|--------|-----------------|
| Opgaven er identisk hver gang | L1 (cron) |
| Opgaven trigges af ekstern event | L2 (webhook/hook) |
| Opgaven har forgreninger men er forudsigelig | L3 (workflow) |
| Én beslutning kræver LLM-vurdering | L4 (LLM-in-the-loop) |
| Kontrolflowet er ukendt på forhånd | L5 (agent) |

### 6.2 Patterns i praksis

**Scheduled Batch (L1).** Cron + Python. 100% reliability, $0, ingen dependencies. Svaghed: ingen realtime, ingen kontekst-bevidsthed.

**Event-Driven (L2).** Webhooks, filewatchers, Claude Code hooks (SessionStart, Stop, PreCompact). Reagerer på reelle events.

**Polling (L2).** Periodisk check for ændringer. Simpelt, robust. Latency = polling interval.

**LLM-in-the-Loop (L4).** Deterministisk pipeline med ét LLM-beslutningspunkt. Groq/Haiku = gratis/billigt. Reliability 90-95%. LLM-fejl propagerer, ingen self-correction.

**Ralph Loop (L5).** `claude --print` i loop med LOOP_STATE.md som shared state. Fuld Claude-capability, alt på disk, fuld visibility. Ingen auto-recovery. Context loss over mange iterationer.

**Heartbeat Daemon (L4-L5).** Periodisk check af inboxes, spawn agent ved arbejde. Bruger kun tokens når der er signal. Risiko for runaway. [ANEKDOTISK — OpenClaw, Yggdra]

### 6.3 L3-springet

Solo-setups har sjældent brug for L3 (workflow engines som n8n, Temporal). Bash scripts med LLM-kald (L4) giver samme funktionalitet uden ekstra service. L3 er mest værdifuldt ved team-brug og visual debugging. [ANEKDOTISK — Yggdra-erfaring: n8n droppet]

---

## 7. OpenClaw + PAI — status i Yggdra

### 7.1 OpenClaw: Hvad det er

Open-source autonom AI-agent bygget oven på Claude Code. Tilføjer 3 ting Claude Code mangler: persistent hukommelse, heartbeat-daemon, messaging-integration (Telegram/WhatsApp/Slack). 430K+ linjer TypeScript/Node.js. Peter Steinberger startede det, forlod til OpenAI feb 2026. Nu community-drevet.

**Kerneforskel fra Claude Code:** Claude Code er reaktiv (du starter session). OpenClaw er proaktiv (den vågner selv, checker inboxes, handler). [VENDOR — OpenClaw docs]

### 7.2 OpenClaws 4 byggeklodser

1. **SOUL.md** — Agentens identitet. Loades først. = Yggdras CLAUDE.md.
2. **HEARTBEAT.md** — Tjekliste hvert 30 min. Regel-baserede checks, LLM kun ved signal. = Yggdras heartbeat.py (disabled).
3. **3-lags hukommelse:**
   - Tier 1 (always loaded): MEMORY.md, ~100 linjer. = Yggdras MEMORY.md.
   - Tier 2 (daily context): `memory/YYYY-MM-DD.md`. I dag + i går loades automatisk. = Yggdras episodes.jsonl.
   - Tier 3 (deep knowledge): `memory/people/`, `projects/`, `topics/` via vektor-embeddings. = Yggdras Qdrant (7 collections, ~84K vektorer).
4. **memsearch** (Zilliz): Markdown-filer, splitter i chunks, embedder, hybrid search (dense + BM25 + RRF reranking). Filer er source of truth, ikke vector-indexet.

### 7.3 Yggdras status vs. OpenClaw

| Komponent | OpenClaw | Yggdra | Gap |
|-----------|----------|--------|-----|
| Identitet (SOUL/CLAUDE.md) | SOUL.md | CLAUDE.md + MEMORY.md | Ingen |
| Heartbeat | systemd daemon, hvert 30 min | heartbeat.py (disabled) | Genaktivér med regelfilter |
| Tier 1 memory | MEMORY.md | MEMORY.md | Ingen |
| Tier 2 memory | daily markdown logs | episodes.jsonl + DAGBOG.md | Mangler per-dag filer |
| Tier 3 memory | memsearch + Milvus | Qdrant (84K vectors) | Mangler hybrid search + reranking |
| Messaging | Telegram/WhatsApp/Slack | Telegram (output only) | Mangler input-polling |
| Cron-isolering | Isolerede sessions, billigere model | `claude --print` | Mangler model-override per job |

### 7.4 Hvad Yggdra skal STJÆLE (ikke installere)

| # | Handling | Effort | Impact |
|---|---------|--------|--------|
| 1 | Genaktivér heartbeat.py med regel-baseret filter | 2 timer | Proaktivitet uden LLM-cost |
| 2 | Opret HEARTBEAT.md som config | 15 min | Behavior-as-config |
| 3 | Tilføj daily markdown-logs i save_checkpoint.py | 30 min | Tier 2 memory |
| 4 | Hybrid search i Qdrant (sparse vectors + RRF) | 1 dag | 15-25% bedre retrieval |
| 5 | Reranking i ctx (cross-encoder) | 2 timer | Præcisere top-5 |
| 6 | Temporal decay i ctx-scoring | 30 min | Friskere resultater |

**Total effort:** ~2 dage. **Resultat:** ~90% af OpenClaws værdi, 0% af dens kompleksitet.

### 7.5 Hvad Yggdra IKKE skal gøre

- **Installere OpenClaw** — 430K linjer TypeScript, massiv dependency. Principperne er nok.
- **Installere memsearch** — kræver Milvus. Qdrant kan det samme. Stjæl mønstret.
- **Heartbeat med Opus** — én bruger betalte $18.75 på én nat for "er det dag endnu?" hvert 30. minut.
- **Gateway-daemon** — cron hvert 30 min gør det samme.
- **Multi-agent routing** — OpenClaws multi-agent er for teams.

### 7.6 Miessler PAI vs. Yggdra

| PAI-princip | Yggdra-pendant | Status |
|-------------|---------------|--------|
| TELOS (10 identitetsfiler) | MISSION.md + PRIORITIES.md + TRADEOFFS.md + CLAUDE.md | Implementeret |
| The Last Algorithm | NOW.md (current state) vs. MISSION.md (ideal state) | Manuelt, ikke automatiseret |
| 3-tier memory | MEMORY.md + episodes.jsonl + Qdrant | Implementeret |
| Multi-provider agents | Groq + OpenAI embeddings + Claude | Delvist |
| Skills system | .claude/skills/ | Implementeret |
| Hook system | SessionStart/Stop/PreCompact | Implementeret |

---

## 8. Evaluering og observabilitet

### 8.1 Hvorfor agent-evaluering er anderledes

Tre fundamentale brud med traditionel softwaretest:

1. **Non-determinisme.** Samme prompt kan producere forskellige tool-call sekvenser og outputs.
2. **Multi-step compounding.** Fejl i step 2 forgifter step 3-N. Man skal evaluere trajektoren, ikke kun destinationen.
3. **Partial success.** En agent der finder 4 af 5 relevante dokumenter — pass eller fail? Gradueret scoring, ikke binær.

### 8.2 Tre evalueringsniveauer

**Run-level (single-step).** Unit test for agent reasoning. Isolér ét beslutningspunkt, verificér tool-valg og argumenter. Billigt, hurtigt, mest debugbart.

**Trace-level (trajectory).** Evaluér fuld eksekvering. To sub-tilgange: trajectory matching (eksakt sammenligning) og LLM-as-judge (dommer-model vurderer rimelighed).

**Thread-level (conversation).** Sværeste evalueringstype. Test kontekst-bevarelse, præference-memory, kohærent adfærd over multiple user-turns.

### 8.3 Offline vs. Online

**Offline (pre-deployment):** Agent mod kurateret datasæt med known-good outputs. 52.4% adoption. [VENDOR — LangChain State of Agent Engineering, 2026]

**Online (produktion):** Reference-free evaluators, user feedback, anomaly detection på token usage/latency/error rates.

### 8.4 Observabilitets-primitiver

- **Run:** Atomisk enhed. Én LLM-call med input og output.
- **Trace:** Linker runs til komplet eksekvering. Træstruktur. Agent-traces kan være hundredvis af MB.
- **Thread:** Grupperer traces til konversationel session.

Nesting: Thread, Trace, Run.

### 8.5 Ronacher om evals

"The hardest problem." Traditionelle eksterne eval-systemer virker ikke til agents. Man skal instrumentere de faktiske test-runs. Ingen god løsning endnu. [ANEKDOTISK — Ronacher, 2025-11]

---

## 9. Åbne spørgsmål

### 9.1 Ubesvarede spørgsmål

1. **Hvornår overtager per-step reliability problemet?** Vi ved at 0.95^n er matematisk — men hvad er den faktiske per-step reliability for state-of-the-art modeller i praksis? Ingen systematiske studier udover METR.

2. **Er METR-resultatet reproduktivt?** n=16 er meget lille. Gælder det erfarne AI-brugere eller kun novices? Ingen replikationsstudier endnu.

3. **Hybrid search vs. dense-only.** Qdrant supporterer sparse vectors. memsearch bruger det. Men den faktiske forbedring (de citerede "15-25%") er OpenClaws egne tal. Uafhængig benchmark mangler.

4. **Optimal heartbeat-interval.** OpenClaw bruger 30 min. Ingen evidens for at dette er optimalt vs. 15 min eller 1 time. Afhænger af use case.

5. **Context window sweet spot.** Zechner siger 100K tokens. Anthropic benchmarker 200K. Hvad er den faktiske grænse for *agent*-kvalitet (ikke recall-benchmarks)?

6. **Accountability-problemet.** Ronacher identificerer det (feb. 2026): kodegenerering er hurtigere end kodereview. 2500+ PRs i limbo i OpenClaw. Ingen foreslår løsninger.

7. **Cost-subsidering.** Ronacher: "Current prices are potentially subsidized." Hvad sker med agent-arkitekturer hvis token-priser stiger 3-5x?

8. **Mem0/LightRAG/GraphRAG viability.** Alle har svagt evidensgrundlag (egne papers, små benchmarks). Mem0 er "3 prompts oven på vector DB." LightRAG's paper trukket fra ICLR. GraphRAG for dyrt til personlig brug. Hybrid search i eksisterende Qdrant er sandsynligvis sufficient. [ANEKDOTISK — research 23/2-2026]

### 9.2 Næste research-targets

1. **Replikation af METR med erfarne AI-brugere.** De fleste METR-deltagere var erfarne *developere*, ikke erfarne *AI-brugere*. Forskel kan være signifikant.
2. **Hybrid search benchmark på Yggdra-data.** Mål dense-only vs. dense+BM25+RRF på egne collections. Kost: ~2 timer.
3. **Heartbeat cost-tracking.** Kør heartbeat i 1 uge, mål faktisk token-forbrug og signal-to-noise.
4. **Agent eval harness på egne scripts.** Brug den implementerede eval_harness.py på morning_brief, daily_sweep, ai_intelligence.
5. **Longitudinal self-study.** Mål produktivitet med/uden agent-assistance over 2 uger. Simpelt A/B: ulige dage = agent, lige dage = manuelt.

---

## 10. Samlet litteraturliste

### Akademiske kilder [SOLID]
- Yao, S. et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023.
- METR (2025). Pre-registreret RCT: AI tools og udviklerproduktivitet. n=16, 246 issues.
- Anthropic (2025). "Building Effective Agents." Anthropic engineering blog.
- Anthropic (2025). Context engineering research — "lost in the middle" effekten.

### Praktiker-kilder [ANEKDOTISK]
- Zechner, M. (2025-06-02). "Prompts are code, .json/.md files are state." mariozechner.at.
- Zechner, M. (2025-08-15). "MCP vs CLI: Benchmarking Tools for Coding Agents." mariozechner.at.
- Zechner, M. (2025-11-02). "What if you don't need MCP at all?" mariozechner.at.
- Zechner, M. (2025-11-30). "What I learned building an opinionated and minimal coding agent." mariozechner.at.
- Zechner, M. (2025-12-22). "Year in Review 2025." mariozechner.at.
- Ronacher, A. (2025-11-21). "Agents are Hard." lucumr.pocoo.org.
- Ronacher, A. (2026-01-14). "MiniJinja Go Port." lucumr.pocoo.org.
- Ronacher, A. (2026-01-18). "Agent Psychosis." lucumr.pocoo.org.
- Ronacher, A. (2026-01-31). "PI." lucumr.pocoo.org.
- Ronacher, A. (2026-02-13). "The Final Bottleneck." lucumr.pocoo.org.
- Syntax Podcast #976 (2026-02-04). "Pi — The AI Harness That Powers OpenClaw." Gæster: Ronacher, Zechner.
- Ethers Club #58 (2026-01-19). "Mario Zechner — Pi, AI Agents, and Music."
- Jones, N. (2025-2026). 5 YouTube-videoer om context engineering, human throttle, compounding gap.
- Miessler, D. (2025-2026). Personal AI Infrastructure (PAI), TELOS, AIMM. GitHub + blog.
- Karpathy, A. (2025). Context engineering definition. Offentlig post.
- Lutke, T. (2025). "Context engineering" reframing. Offentlig post.
- incident.io (2025). "Shipping Faster with Claude Code and Git Worktrees." Blog.
- blle.co (2025). "Automated Claude Code Workers." Blog.
- Superface (2025). 75% agent task failure rate. Survey.
- Cleanlab (2025). 11% agentic AI adoption. Survey.
- Gartner (2025). 40% multi-agent pilot failure. Survey.
- Willison, S. (2025). "Lethal trifecta" prompt injection model.

### Vendor-kilder [VENDOR]
- CrewAI documentation + GitHub (~30K stars).
- Microsoft AutoGen documentation + GitHub (~40K stars).
- OpenAI Swarm GitHub (~20K stars). Eksperimentel, erstattet af Agents SDK.
- Hugging Face smolagents GitHub (~15K stars).
- LangGraph documentation + GitHub (~10K stars).
- Anthropic Claude Agent SDK (2026).
- Manus (2025-2026). Context engineering production reports. 100:1 token ratio, todo.md pattern.
- GSD — Get Shit Done (2025). GitHub. STATE.md, subagent orchestration, wave parallelization.
- Claude Code Scheduler (jshchnz). GitHub. NLP scheduling + git worktree isolation.
- Anthropic Autonomous Coding Quickstart. GitHub. Two-agent pattern.
- claude-flow (ruvnet). GitHub. 250K+ LOC multi-agent framework.
- OpenClaw GitHub + docs. 430K+ LOC. Heartbeat, memory, messaging.
- memsearch (Zilliz). GitHub. OpenClaw memory som standalone. Hybrid search + RRF.
- mini-claw (htlin222). GitHub. Minimal Telegram bot.
- LangChain "State of Agent Engineering" survey (2026). 52.4% offline eval adoption.

### Yggdra-interne kilder
- HOW_TO_BUILD_AGENTS.md — 800+ linjers praktikermanual produceret af Yggdra Research System.
- agents_framework_comparison.md — 6-frameworks sammenligning.
- agents_langgraph_deep_dive.md — LangGraph arkitektur og patterns.
- agents_evaluation_observability.md — evaluering og observabilitet.
- agents_context_engineering.md — context engineering patterns.
- agent_implementation_notes.md — 5 runnable reference-implementationer.
- autonomous_ai_setup.md — 7 autonome AI-setups analyseret.
- openclaw_deep_dive_2026-03-15.md — OpenClaw arkitektur og hvad Yggdra stjæler.
- armin_ronacher_agent_philosophy_2026.md — Ronacher filosofi og praktik.
- mario_zechner_pi_research_2026-03-06.md — Zechner research og PI-arkitektur.
- agent-architectures.md (ai-frontier) — arkitekturoverblik.
- agent-teams.md (ai-frontier) — multi-agent frameworks.
- automation-patterns.md (ai-frontier) — automation inventar og patterns.
