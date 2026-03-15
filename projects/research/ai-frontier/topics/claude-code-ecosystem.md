# Claude Code Open-Source Ecosystem — Research

**Dato:** 2026-03-15
**Formål:** Kortlæg de vigtigste open-source projekter der udvider Claude Code, og identificér patterns Yggdra kan adoptere.

---

## 1. Claude Capsule Kit (CCK)

**Repo:** github.com/arpitnath/claude-capsule-kit — 67 stars
**Sprog:** Node.js + Go (optional binaries)

**Hvad gør det?**
Udvider Claude Code med persistent engineering-capabilities via 6 hooks, SQLite session memory (`capsule.db`), 18 specialist-agenter og "Crew teams" der kører parallelt på git worktrees. Installeres globalt: `npm install -g claude-capsule-kit`.

**Nøgle-patterns:**

- **Dependency Scanner:** Pre-built Go-binary der bygger import-grafer. `query-deps`, `impact-analysis`, `find-circular`, `find-dead-code` — instant resultater i stedet for iterativ filscanning.
- **Progressive Reader:** AST-baseret chunking af store filer (>50KB). Splitter i funktioner/klasser/sektioner. Hævder 75-97% token-besparelse. Understøtter TS, JS, Python, Go.
- **Crew Teams:** git worktrees til parallel multi-branch udvikling. `.crew-config.json` definerer teammates med roller (developer/reviewer/tester/architect). Merge preview, conflict detection, orphaned worktree cleanup.
- **blink-query:** "DNS-inspired knowledge resolution" — namespace-baseret SQLite med typer, tags, relationer. Auto-scoping til aktuelt projekt.
- **PreCompact hook:** Gemmer continuity documents FØR kontekst-komprimering. Præcis samme princip vi har i `save_checkpoint.py`.

**Modenhed:** Early adopter (fungerende, men tung stack)
**Relevans for Yggdra:** Indirekte relevant — dependency scanning og AST-chunking er gode idéer, men Node.js+Go stack er overkill for os.
**Effort:** Dage (cherry-pick patterns) / Uger (fuld adoption)

**Hvad kan vi stjæle?**
1. AST-chunking til store filer — Python-version med `ast` eller `tree-sitter`
2. Dependency graph som pre-computed artifact i stedet for runtime scanning
3. Crew-model: git worktrees til parallel agent-kørsel (vi har allerede worktree-support i Claude Code)

---

## 2. ALBA

**Repo:** github.com/onurpolat05/ALBA — 11 stars
**Sprog:** Pure markdown (ingen runtime dependencies)

**Hvad gør det?**
Transformerer Claude Code til personlig AI-agent med persistent hukommelse. 3-lags markdown-baseret memory: HOT (daglige prioriteter), WARM (learnings, fejl, præferencer), COLD (per-projekt kontekst). 9 built-in skills, 6 hooks.

**Nøgle-patterns:**

- **HOT/WARM/COLD temperatur-model:** HOT opdateres dagligt, WARM auto-opdateres ved fejl og læring, COLD er stabil projektkontekst. Simpel men effektiv mental model.
- **Auto error logging:** Fejl auto-registreres med løsninger — aldrig gentag samme fejl. Hook på bash errors.
- **`/reflect` kommando:** Analyserer cross-session patterns og foreslår adfærdsforbedringer. Meta-cognition.
- **Under 200 linjer agent config:** Bevidst constraint — holder kontekst-overhead lav.

**Modenhed:** Eksperimentel (11 stars, tidlig)
**Relevans for Yggdra:** Direkte brugbar — temperatur-modellen og auto error logging er simpelt at implementere.
**Effort:** Timer (markdown-filer + 1 hook)

**Hvad kan vi stjæle?**
1. **Error-logging hook:** Bash errors → automatisk WARM memory med fejl+løsning
2. **`/reflect` pattern:** Periodisk mønstergenkendelse på tværs af sessioner
3. **Temperatur-metafor:** Vi har allerede HOT (NOW.md) og COLD (CONTEXT.md), men mangler WARM (auto-akkumulerede learnings)

---

## 3. PentAGI

**Repo:** github.com/vxcontrol/pentagi
**Sprog:** Go + PostgreSQL + Neo4j

**Hvad gør det?**
Pentesting-agent med sofistikeret multi-agent arkitektur. Orchestrator delegerer til Researcher → Developer → Executor. 3-lags hukommelse (langtid via pgvector, working memory, episodisk). Neo4j knowledge graph. Chain Summarization for context overflow.

**Nøgle-patterns:**

- **Chain Summarization:** Når kontekst overskrider threshold, grupperes ældre meddelelser i sektioner og komprimeres selektivt. Nyeste kontekst bevares intakt (`SUMMARIZER_PRESERVE_LAST`). Konfigurérbare grænser (50KB last section, 64KB QA pairs).
- **ChainAST:** Struktureret repræsentation af samtaler inkl. tool calls — muliggør intelligent komprimering der bevarer tool-resultater.
- **3-lags hukommelse:** Long-term (vektorer + domain expertise), Working (aktive mål + ressourcer), Episodic (kommando-historik + outcomes + success patterns).
- **Orchestrator-delegation:** Klar rollefordeling. Orchestrator planlægger, Researcher finder info, Developer planlægger udførelse, Executor eksekverer med tool retrieval.

**Modenhed:** Production-ready (Go, Docker, real-world pentesting)
**Relevans for Yggdra:** Indirekte relevant — Chain Summarization og episodisk success-pattern tracking er værdifulde.
**Effort:** Dage (patterns) / Uger (Neo4j graph)

**Hvad kan vi stjæle?**
1. **Chain Summarization logik:** Implementér i `save_checkpoint.py` — selektiv komprimering med preservering af seneste kontekst
2. **Success pattern tracking:** Log hvad der virkede (ikke kun fejl) → informér fremtidige sessioner
3. **Konfigurerbare thresholds** for hvornår komprimering aktiveres

---

## 4. Karpathy autoresearch

**Repo:** github.com/karpathy/autoresearch
**Sprog:** Python

**Hvad gør det?**
Autonom ML-research: agent modificerer `train.py`, kører 5-minutters eksperimenter, evaluerer resultater, itererer. ~12 eksperimenter/time, ~100 overnight. `program.md` som instruktionsfil (svarer til CLAUDE.md).

**Nøgle-patterns:**

- **Fixed budget constraint:** 5 min per eksperiment gør resultater sammenlignelige. Forhindrer agents i at overoptimere infrastruktur.
- **Single modifiable file:** Kun `train.py` kan ændres. `prepare.py` er frozen utility. Reducerer search space drastisk.
- **program.md:** Bruger-skrevet kontekst til agenten — ikke kode, men *retning*. Præcis som CLAUDE.md men specifikt til research.
- **Evaluate → Iterate loop:** Automatisk rollback af mislykkede ændringer. Kun forbedringer bevares.

**Modenhed:** Eksperimentel (proof-of-concept fra Karpathy)
**Relevans for Yggdra:** Indirekte relevant — loop-strukturen er god til automatiserede opgaver.
**Effort:** Timer (principper) / Dage (implementer loop)

**Hvad kan vi stjæle?**
1. **Budget-constrained agent loops:** Sæt wallclock-grænser på agent-tasks (vi har lært dette den hårde måde)
2. **Evaluate-gate:** Automatisk kvalitetstjek før ændringer accepteres
3. **Rollback-by-default:** Ændringer er tentative indtil valideret

---

## 5. Claude-Org

**Repo:** github.com/vincitamore/claude-org-template — 42 stars
**Sprog:** Pure markdown + hooks

**Hvad gør det?**
"Attractor basin" framework — i stedet for at stole på at Claude husker kontekst, gør arkitekturen selv-dokumenterende. Enhver Claude-instans kan orientere sig i strukturen uden onboarding. 50-65 minutters guided setup.

**Nøgle-patterns:**

- **Attractor Basins:** Arkitekturen kommunikerer intent og patterns. Strukturen guider tænkning automatisk — Claude "falder ind i" de rigtige mønstre pga. filorganisering.
- **Sovereignty:** Al data lokalt. Ingen eksterne dependencies.
- **Irreducibility:** Komprimer til essentielle indsigter, ikke samtaler. Destillering > arkivering.
- **Single-Source Truth:** Én kanonisk version med afledte views.
- **Setup som samtale:** Claude interviewer brugeren om tænkemønstre → populerer filer kollaborativt → fjerner scaffolding.

**Modenhed:** Early adopter (42 stars, veldokumenteret)
**Relevans for Yggdra:** Direkte brugbar — vi gør allerede meget af dette, men "attractor basin" konceptet er en god mental model.
**Effort:** Timer (principper er allerede delvist implementeret)

**Hvad kan vi stjæle?**
1. **Bevidst attractor design:** Filnavne og struktur der guider Claude mod korrekt adfærd uden eksplicitte instruktioner
2. **Irreducibility-princippet:** Destillér viden til essens — vi gør det i checkpoints, men ikke konsistent nok

---

## 6. Claude Prime

**Repo:** github.com/avibebuilder/claude-prime — 22 stars
**Sprog:** Python

**Hvad gør det?**
One-command setup af Claude Code med skills, agents og memory. Analyserer projekt automatisk og loader kun relevant kontekst. Én agent ("the-mechanic") + mange skills i stedet for mange agenter.

**Nøgle-patterns:**

- **Skills > Agents:** "Skills carry the knowledge, the agent provides the execution." Én generalist-agent med mange skills slår mange specialist-agenter.
- **On-demand context loading:** Skills og project refs loades per-task, ikke ved session start.
- **Workflow-kæde:** `/research → /discuss → /give-plan → /cook → /test → /review-code` — defineret progression.

**Modenhed:** Eksperimentel (22 stars, nyligt)
**Relevans for Yggdra:** Nice to know — vi har allerede on-demand loading via projects/.
**Effort:** Timer

**Hvad kan vi stjæle?**
1. **Skill-first arkitektur:** Konsolidér viden i skills, ikke i agenter. Reducerer kontekst-overhead.

---

## 7. Gobby

**Repo:** github.com/GobbyAI/gobby
**Sprog:** Python (FastAPI + SQLite + Neo4j)

**Hvad gør det?**
Local-first daemon (port 60887) der unified Claude Code, Gemini CLI, Cursor, Windsurf, Copilot og Codex. Session tracking, MCP proxy med progressive discovery, task system med dependency graphs, Neo4j knowledge graph. 4900+ commits — mest bygget af AI-agenter.

**Nøgle-patterns:**

- **MCP Progressive Discovery:** I stedet for at loade alle tool schemas upfront (tusindvis af tokens), vises tools som lightweight metadata. Fulde schemas hentes on-demand. Stor kontekstbesparelse.
- **Cross-CLI session handoffs:** Kontekst fanges ved session-end (mål, ændringer, git status, tool calls) og restores i næste session — uanset hvilket AI-tool der bruges.
- **Task system med dependencies:** Task graphs, TDD-baseret expansion (red/green/blue subtasks), validation gates. Persisteret i `.gobby/tasks.jsonl`.
- **AST-baseret code indexing:** tree-sitter parsing for symbol-level søgning på tværs af 15+ sprog. Agenter kan finde specifikke funktioner uden at læse hele filer.
- **OpenTelemetry observability:** Distributed tracing, metrics, logging. Trace viewer med span waterfalls.
- **Pipeline orchestration:** Deterministisk automation med approval gates, cron scheduling, provider fallback rotation.

**Modenhed:** Alpha (4900+ commits, men alpha-label)
**Relevans for Yggdra:** Indirekte relevant — MCP progressive discovery og AST indexing er stærke patterns.
**Effort:** Uger (fuld adoption) / Dage (cherry-pick patterns)

**Hvad kan vi stjæle?**
1. **Progressive tool discovery:** Reducér MCP token overhead
2. **AST code indexing:** tree-sitter for symbol-level søgning
3. **Session handoff format:** Standardiseret kontekst-capture ved session-end

---

## 8. cc-rig

**Repo:** github.com/runtimenoteslabs/cc-rig
**Sprog:** Python CLI

**Hvad gør det?**
Projekt-setup generator for Claude Code. Vælg framework + workflow → generér CLAUDE.md, hooks, agent config, commands. Scaffolding-tool, ikke runtime.

**Modenhed:** Eksperimentel
**Relevans for Yggdra:** Nice to know — vi har allerede vores egen setup.
**Effort:** Irrelevant

---

## Syntese: Top 5 Patterns Vi Mangler

| # | Pattern | Kilde | Effort | Prioritet |
|---|---------|-------|--------|-----------|
| 1 | **WARM memory (auto error+learning log)** — Bash errors og learnings auto-akkumuleres i en fil der loades ved session start. Vi har HOT (NOW.md) og COLD (CONTEXT.md) men intet WARM lag. | ALBA | 2-3 timer | Høj |
| 2 | **AST-chunking af store filer** — Progressive reader der splitter >50KB filer i navigerbare chunks via AST. Reducerer token-forbrug markant. Python `ast` modul eller `tree-sitter`. | CCK, Gobby | 1 dag | Medium |
| 3 | **Success pattern tracking** — Log hvad der virkede (ikke kun fejl). "Sidst vi deployede webapp, virkede X" → informér fremtidige sessioner. Supplement til episodes.jsonl. | PentAGI | 3-4 timer | Høj |
| 4 | **Chain Summarization med preservering** — Selektiv komprimering af ældre kontekst mens seneste bevares intakt. Konfigurerbare thresholds. Forbedring af nuværende PreCompact hook. | PentAGI | 1 dag | Medium |
| 5 | **`/reflect` meta-cognition** — Periodisk analyse af sessions/episoder for at identificere gentagende mønstre og foreslå forbedringer. Kan køres som weekly cron. | ALBA | 3-4 timer | Medium |

### Honorable mentions:
- **Dependency graph pre-computation** (CCK) — relevant hvis codebase vokser
- **MCP progressive discovery** (Gobby) — relevant når vi tilføjer flere MCP tools
- **Budget-constrained agent loops** (autoresearch) — allerede lært via MEMORY.md, men ikke formaliseret

---

## Hvad Yggdra Allerede Gør Bedre

1. **Projekt-isolation med progressive disclosure.** `projects/*/CONTEXT.md + NOW.md` er renere end CCK's globale SQLite eller ALBA's flat memory. Vi loader kun relevant projekt — de fleste andre loader alt.

2. **Episodisk log via Groq destillering.** `save_checkpoint.py` bruger Groq til at destillere sessioner til 3-5 linjer. CCK og ALBA gemmer rå session data. Vores approach er billigere og mere fokuseret.

3. **Bash-first princippet.** Ingen Node.js runtime, ingen Go binaries, ingen daemon. Scripts er composable og debuggable. CCK kræver Node.js 18+ og optional Go 1.20+. Gobby er en hel daemon.

4. **Kill conditions.** Ingen andre projekter nævner betingelser for hvornår features fjernes. Vi har det som eksplicit princip — det forhindrer bloat.

5. **Dual-location arkitektur (VPS+PC).** Ingen af projekterne adresserer distribueret setup. Vi har clear domæne-opdeling: VPS=drift, PC=udvikling, SSH=bro.

6. **Qdrant vektor-søgning i produktion.** 84K vektorer, 7 collections, hybrid search planlagt. De fleste af disse projekter har ingen vektor-søgning eller bruger det som afterthought.

7. **Real-world domain integration.** TransportIntra API, Telegram, Google Tasks, Gmail — vi bygger mod konkrete use cases, ikke generisk "agent framework".

---

## Konklusion

Økosystemet er ungt. De fleste projekter er 1-3 måneder gamle og eksperimentelle. Ingen enkelt projekt er worth at adoptere wholesale — men der er konkrete patterns at cherry-picke:

**Umiddelbare wins (i dag):**
- WARM memory lag (ALBA-pattern) — tilføj `data/LEARNINGS.md` med auto-append fra hooks
- Success pattern tracking — udvid `episodes.jsonl` med outcome-felt

**Næste sprint:**
- AST-chunking skill til store filer
- `/reflect` kommando som analyserer episoder

**Senere/måske:**
- Chain Summarization i PreCompact
- MCP progressive discovery (når vi har flere tools)

Det vigtigste takeaway: Yggdra er allerede mere moden end de fleste af disse projekter i praksis — men vi mangler det WARM hukommelseslag der fanger fejl og læring automatisk. Det er den største gap.
