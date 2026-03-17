# Research Deep Study — 15. marts 2026

**Formål:** Konsolidering af eksisterende research + nye kilder. Kortlægning af hvad vi ved, hvad der er tyndt, hvad der mangler, og hvad der overlapper.
**Metode:** 18 interne filer læst (40 linjer hver) + 9 web-søgninger + kildekritik.

---

## Del 1: Hvad vi ved / mangler / overlapper

### 1.1 Hvad vi VED (solid, veldokumenteret)

**Context Engineering (agents_context_engineering.md)**
- Stærk rapport (8/3-2026). Dækker Karpathy/Lutke-definitionen, Manus 100:1 ratio, context rot, 4 strategier (Offload/Reduce/Isolate/Disclose). PLAN.md/STATE.md-pattern fra Zechner/GSD. MCP som standard. Velkildet med 35+ kilder.
- **Vurdering:** Solid fundament. Stadig aktuelt.

**Agent Frameworks (agents_framework_comparison.md)**
- CrewAI, LangGraph, AutoGen, etc. sammenlignet med kodeeksempler og arkitekturoverblik. Verificeret mod aktuelle API'er.
- **Vurdering:** Godt reference-dokument. Frameworks udvikler sig hurtigt — kan være delvist forældet om 3-6 måneder.

**AI Memory Systemer (ai_memory_research.md + memory_autonomy_research.md)**
- Dækker Mem0, LightRAG, Graphiti/Zep, MemGPT/Letta, A-MEM, CrewAI memory. Taxonomi fra arXiv 2512.13564. OpenClaw-principper destilleret. Konkret bygge-rækkefølge defineret.
- **Vurdering:** Stærkeste research-klynge. To rapporter der supplerer hinanden (16/2 + 23/2). Beslutninger taget (Mem0 fravalgt, OpenClaw-principper adopteret, hybrid search prioriteret).

**Kognitionsvidenskab (human_memory_research.md)**
- Episodisk/semantisk/procedural hukommelse, encoding, retrieval, glemsel som feature, spaced repetition, chunking. Direkte paralleller til AI-arkitektur.
- **Vurdering:** Akademisk solid. Sjælden rapport — de fleste AI-projekter ignorerer kognitionsvidenskab.

**Claude Code Økosystem (claude_code_ecosystem_2026.md)**
- 25+ repos kortlagt, Technology Radar (adopt/trial/assess/hold), gap-analyse mod Yggdra, PC-setup guide. 1.500+ skills gennemgået.
- **Vurdering:** Omfattende. Allerede brugt som beslutningsgrundlag for PC-setup.

**Continuous Memory Architecture (ARCHITECTURE_CONTINUOUS_MEMORY.md)**
- Universal pattern destilleret fra OpenClaw, Gastown, Nemori, MemGPT, Miessler PAI. Hot/warm/cold memory layers. Session lifecycle.
- **Vurdering:** Arkitektur-blueprint. Klar til implementering — delvist implementeret (episodes.jsonl, checkpoint hooks).

**Research Workflows (RESEARCH_WORKFLOWS.md)**
- Hallucination-resistent multi-agent research. Orchestrator-worker, shared scratchpad, researcher+fact-checker+critic. Anthropic's 90.2% forbedring med multi-agent.
- **Vurdering:** Praktisk og velkildet. Bruges aktivt i VPS sandbox loops.

**Brainmap & Visualization (brainmap_v2 + viz_survey_pass2)**
- Kognitionsvidenskab bag visualisering, GRINDE framework, argument mapping, Wardley maps, C4-model. 40+ emner.
- **Vurdering:** Grundig teori. Mangler implementering — ingen brainmap er bygget endnu.

**Zero-Token Pipeline (zero_token_pipeline_architecture.md)**
- Unix pipe-filosofi, ETL patterns, regelbaseret NLP, gate-keeper mønster. 70-90% af pipeline-arbejde kan ske uden LLM.
- **Vurdering:** Ny rapport (15/3). Direkte actionable for cost-reduktion.

**Personal Data Pipelines (personal_data_pipeline_best_practices.md)**
- Willison (Dogsheep+SQLite+hybrid search), Karlicoss HPI, Linus Lee Monocle, Steph Ango file-over-app.
- **Vurdering:** Ny rapport (15/3). Praktiker-perspektiv. Gode principper for Yggdra.

---

### 1.2 Hvad der er TYNDT (påstande uden kilder, overfladisk)

**LightRAG-vurderingen**
- memory_autonomy_research.md hævder "entity hallucination, svagt paper (trukket fra ICLR)". Kilden til ICLR-tilbagetrækning er uklar. LightRAG-paperet (arXiv 2410.05779) er accepteret til EMNLP 2025, ikke ICLR. Påstanden om entity hallucination mangler specifik kilde.
- **Anbefaling:** Verificér eller ret denne påstand.

**Mem0's "26% bedre accuracy"**
- Citeret i memory_autonomy_research.md. Tallet stammer fra Mem0's eget paper (arXiv 2504.19413) og blog. Ingen uafhængig replikation fundet. Self-reported benchmarks fra framework-udviklere er upålidelige.
- **Anbefaling:** Betragt som marketing-tal, ikke videnskab.

**"METR: 19% langsommere"**
- Citeret i GAPS.md. METR-studiet (randomiseret kontrolleret forsøg med 16 erfarne udviklere) viste at AI coding tools ikke øgede produktiviteten. Korrekt kilde, men tallet er "19% langsommere end uden AI" — ikke "19% langsommere" som isoleret påstand. Konteksten mangler (det var for erfarne devs på kendte codebases).
- **Anbefaling:** Tilføj nuance: resultatet gælder erfarne devs, ikke nødvendigvis solo-devs med AI som primært værktøj.

**Heartbeat-daemon design**
- ARCHITECTURE_CONTINUOUS_MEMORY.md nævner heartbeat som kritisk komponent (fra OpenClaw). Men ingen konkret design er dokumenteret: hvad tjekker den? Hvad reagerer den på? Hvad koster den? V6 backlog-burn implementerede heartbeat — men designdokumentationen er tynd.
- **Anbefaling:** Dokumentér heartbeat-arkitekturen separat.

**Temporal decay**
- Nævnes i GAPS.md, DECAY_MODEL.md, WHAT_IF.md som vigtig. Men den konkrete decay-funktion er uklar. Eksponentiel? Lineær? Hvad er half-life? DECAY_MODEL.md har sandsynligvis mere, men de første 40 linjer dækker det ikke.
- **Anbefaling:** Konsolidér decay-model til én autoritativ beskrivelse.

---

### 1.3 Hvad der MANGLER (huller ingen fil dækker)

**1. Evaluering af retrieval-kvalitet**
- GAPS.md identificerer det som P2. WHAT_IF.md foreslår 10 test queries. HOLISTIC_EVALUATION.md bekræfter: "Ingen loop byggede dem." Stadig et åbent hul. Ingen eval pipeline, ingen baseline, ingen A/B test.
- **Prioritet:** Kritisk. Uden eval ved vi ikke om forbedringer forbedrer.

**2. VPS-PC synkronisering**
- HOLISTIC_EVALUATION.md: "Alle loops kører på VPS, PC har ingen automatisk måde at hente det." Ingen fil beskriver sync-arkitekturen (git pull? rsync? SSH-baseret sync?).
- **Prioritet:** Høj. Blokerer for sømløs PC-VPS workflow.

**3. Multi-hop reasoning / komplekse queries**
- Vores research dækker single-hop RAG (query → retrieve → generate). Men A-RAG (arXiv 2602.03442) og HiPRAG (arXiv 2510.07794) viser at multi-hop queries kræver fundamentalt anderledes arkitektur: hierarkisk retrieval, iterativ søgning, interleaved tool use. Ingen af vores filer dækker dette.
- **Prioritet:** Medium. Relevant når vidensbasen vokser.

**4. Security og data-poisoning i RAG**
- Web-søgningen afslørede BadRAG og TrojanRAG som kendte angrebsvektorer. Ingen af vores filer nævner RAG-sikkerhed. For et personligt system er risikoen lav, men princippet bør dokumenteres.
- **Prioritet:** Lav (personligt system), men bør kendes.

**5. Cost-tracking og budget-analyse**
- HOLISTIC_EVALUATION.md: "Ingen loop estimerede den samlede månedlige kost." cost_daily.json eksisterer men analyseres ikke systematisk. Med 3 providers (Anthropic+OpenAI+Gemini) er cost-overvågning vigtigere.
- **Prioritet:** Medium.

**6. Memori (relational memory)**
- Ny tilgang: memory som relationel database (Postgres) med skema, constraints, temporal tracking. Fundamentalt anderledes end vektor-baseret. Ingen af vores filer dækker dette.
- **Prioritet:** Lav-medium. Interessant alternativ til Qdrant for visse memory-typer.

**7. Obsidian + AI workflow**
- Eric Ma's blog (marts 2026) beskriver Obsidian med plain-text notes + AI agent skills der reducerer PKM-overhead fra 30-40% til <10%. Relevant for Yggdra-PC men ikke dokumenteret.
- **Prioritet:** Medium (PC-relevant).

---

### 1.4 Hvad der OVERLAPPER (kan merges)

**Overlap 1: Memory-rapporter (3 filer)**
- `ai_memory_research.md` (16/2) + `memory_autonomy_research.md` (23/2) + `ARCHITECTURE_CONTINUOUS_MEMORY.md` (23/2)
- Alle tre dækker agent memory, men fra forskellige vinkler: survey, praktisk evaluering, arkitektur-blueprint. Overlappet er primært i Mem0/LightRAG/Graphiti-vurderinger.
- **Anbefaling:** Behold alle tre, men tilføj krydsreferencer. Overvej en top-level INDEX.md der peger på den rette fil per spørgsmål.

**Overlap 2: Gaps og handlingsplaner (3 filer)**
- `GAPS.md` + `WHAT_IF.md` + `HOLISTIC_EVALUATION.md`
- GAPS identificerer problemer, WHAT_IF foreslår løsninger, HOLISTIC_EVALUATION evaluerer begge. De er designet som pipeline (gap → forslag → evaluering).
- **Anbefaling:** Behold som pipeline. Tilføj status-tracking: hvilke gaps er lukket?

**Overlap 3: Provider/LLM-vurdering**
- `claude_code_ecosystem_2026.md` (Technology Radar) + llm-landskab (7 profiler + RECOMMENDATION.md)
- Førstnævnte fokuserer på Claude Code tooling, sidstnævnte på LLM providers generelt.
- **Anbefaling:** Acceptabel overlap. Forskellige fokus.

**Overlap 4: Pipeline-design (2 filer)**
- `zero_token_pipeline_architecture.md` + `PIPELINE_DESIGN.md`
- Førstnævnte er principiel (Unix-filosofi, gate-keeper), sidstnævnte er konkret (udvidelser til ai_intelligence.py).
- **Anbefaling:** Komplementære. Krydsreferencér.

---

### 1.5 Session-blindhed (DLR.session-blindhed)

Særskilt notering: Dette projekt er unikt i landskabet. Det er empirisk forskning i Claude's egne reasoning-fejl, baseret på data fra faktiske sessions. Ingen ekstern research dækker dette specifikt for Claude Code i et personligt system. Taxonomien (8 kategorier fra 1 episode) er embryonisk men lovende. Fase 2 (retrospektiv mining) vil give langt mere data.

---

## Del 2: Nye kilder fundet

### 2.1 Context Engineering

**Anthropic: "Effective Context Engineering for AI Agents" (2025)**
- Forfatter: Anthropic Engineering Blog
- Nøgleindsigt: Forener history, memory, og scratchpad i én kontinuerlig lifecycle. Scratchpads som /context/pad/taskID. Summarisation → Memory → Retrieval loop. "Don't force the model to remember everything."
- Direkte relevant for Yggdra's arkitektur — bekræfter ARCHITECTURE_CONTINUOUS_MEMORY.md.
- URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**LangChain: "Context Engineering for Agents" (2025)**
- Forfatter: Lance Martin (LangChain)
- 4 kernestrategier: Persistence/Scratchpads, Context Trimming, Context Compression, Isolation. "En fokuseret 300-token kontekst slår ofte en ufokuseret 113.000-token kontekst."
- URL: https://blog.langchain.com/context-engineering-for-agents/

**arXiv 2512.05470: "Everything is Context: Agentic File System Abstraction for Context Engineering" (2025)**
- File system som uniforms kontekstlag. History, memory, scratchpad mappes til filsystem-abstraktioner med metadata og adgangskontrol.
- URL: https://arxiv.org/pdf/2512.05470

**Nate's Newsletter (Substack): "Beyond the Perfect Prompt: The Definitive Guide to Context Engineering"**
- Praktiker-guide. Skelner mellem deterministisk kontekst (prompts, docs) og probabilistisk kontekst (agent-autonomi). God oversigt for ikke-tekniske.
- URL: https://natesnewsletter.substack.com/p/beyond-the-perfect-prompt-the-definitive

**Kubiya: "Context Engineering Best Practices for Reliable AI in 2025"**
- Position i kontekstvinduet matters: primacy og recency bias. Context rot vs. mode collapse. Praktiske tips.
- URL: https://www.kubiya.ai/blog/context-engineering-best-practices

### 2.2 Agent Memory

**arXiv 2512.13564: "Memory in the Age of AI Agents" (Survey, jan 2026)**
- Allerede citeret i ai_memory_research.md. Tredimensionel taxonomi: form × funktion × dynamik. Mest omfattende survey til dato.
- URL: https://arxiv.org/abs/2512.13564

**Letta: "Benchmarking AI Agent Memory: Is a Filesystem All You Need?" (2026)**
- Letta's eget benchmark. Sammenligner OS-inspireret tiered memory (core/recall/archival) med simpelt filsystem. Konklusion: filsystem er overraskende stærkt for simple use cases, men tiered memory vinder på komplekse multi-session scenarier.
- Direkte relevant for Yggdra: vi bruger allerede filsystem-baseret memory. Spørgsmålet er hvornår det ikke rækker.
- URL: https://www.letta.com/blog/benchmarking-ai-agent-memory

**Memori (nyt framework, 2026)**
- Relational DB (Postgres) som memory-backend. Skema-baseret: facts, entities, events, preferences. Temporal tracking (ikke destruktiv overwrite). Vector embeddings som sekundær index. Stærkest for enterprise/compliance.
- Interessant kontrast til vores vektor-primære tilgang.
- URL: https://medium.com/@bumurzaqov2/top-10-ai-memory-products-2026-09d7900b5ab1

**MachineLearningMastery: "Beyond Short-term Memory: The 3 Types of Long-term Memory AI Agents Need" (2026)**
- Episodisk (hvad skete), semantisk (generelle principper), procedural (workflows). Praktisk guide til implementering.
- URL: https://machinelearningmastery.com/beyond-short-term-memory-the-3-types-of-long-term-memory-ai-agents-need/

### 2.3 RAG Fejl og Agentic RAG

**arXiv 2602.03442: "A-RAG: Scaling Agentic Retrieval-Augmented Generation via Hierarchical Retrieval Interfaces" (feb 2026)**
- 3 retrieval-tools: keyword search, semantic search, chunk read. Agenten vælger selv strategi. ReAct-loop (action-observation-reasoning). Outperformer eksisterende tilgange med færre tokens.
- Direkte relevant: vores ctx-kommando er single-shot dense search. A-RAG viser at agentic retrieval er næste niveau.
- URL: https://arxiv.org/abs/2602.03442
- Kode: https://github.com/Ayanami0730/arag

**arXiv 2510.07794: "HiPRAG: Hierarchical Process Rewards for Efficient Agentic RAG" (okt 2025)**
- Process rewards for multi-hop retrieval. Belønner korrekte mellemtrin, ikke kun endeligt svar.
- URL: https://arxiv.org/abs/2510.07794

**arXiv 2512.08892: "Toward Faithful RAG with Sparse Autoencoders" (dec 2025)**
- Bruger sparse autoencoders til at identificere features der triggerer RAG-hallucinationer. Ny tilgang til faithfulness.
- URL: https://arxiv.org/abs/2512.08892

**arXiv 2401.05856: "Seven Failure Points When Engineering a RAG System" (jan 2024, stadig relevant)**
- 7 konkrete fejlpunkter: missing content, missed top-k, not in context, not extracted, wrong format, incorrect specificity, incomplete. Systematisk taxonomi.
- URL: https://arxiv.org/html/2401.05856v1

**Elumenotion: "Retrieval Augmented Generation is an Anti-pattern" (2025)**
- Provokerende titel. Argument: RAG tilføjer kompleksitet der ofte er unødvendig. For mange teams bruger RAG som hammer for alle problemer. Alternativ: fine-tuning, prompt caching, structured outputs.
- URL: https://www.elumenotion.com/Journal/RagIsAnAntipattern.html

### 2.4 Personal Knowledge Management

**Eric Ma: "Mastering Personal Knowledge Management with Obsidian and AI" (marts 2026)**
- Plain-text noter + AI agent skills. Reducerede PKM-overhead fra 30-40% til <10%. Strukturerede note-typer + encoded workflows.
- URL: https://ericmjl.github.io/blog/2026/3/6/mastering-personal-knowledge-management-with-obsidian-and-ai/

**Elephas: "The Solo Consultant AI Stack Guide (2026)"**
- 5 lag: Knowledge, Writing, Client Tracking, Scheduling, Workflow. Alt for under $50/måned. Knowledge Layer = queryable AI brain per klient/projekt.
- URL: https://elephas.app/resources/solo-consultant-ai-stack-guide

### 2.5 Zero-Token / Preprocessing

**Latitude: "Ultimate Guide to Preprocessing Pipelines for LLMs" (2025)**
- Statiske metoder (stopword lists, regex, rule-based lemmatizers) er context-free. LLM-preprocessing kun nødvendigt for semantisk disambiguation. Hovedregel: brug LLM kun hvor lightweight rules ikke rækker.
- Bekræfter vores zero_token_pipeline_architecture.md.
- URL: https://latitude.so/blog/ultimate-guide-to-preprocessing-pipelines-for-llms

**arXiv: Token Cleaning (OpenReview, 2025)**
- Token-level filtering fra noisy-label perspektiv. Generic pipeline der fjerner uninformative tokens fra SFT data.
- URL: https://openreview.net/forum?id=tXkOUS3vLS

### 2.6 Substack-kilder (agent arkitektur)

**Cobus Greyling: "Agentic Context Engineering" (Substack)**
- 2026 = året hvor organisationer spørger om orchestration mellem agenter og hvordan kontekst defineres. Hybrider (orchestration + specialisering) dominerer.
- URL: https://cobusgreyling.substack.com/p/agentic-context-engineering

**FutureAGI: "Top 5 Agentic AI Frameworks to Watch in 2026" (Substack)**
- Framework-landskab med fokus på hvad der overlever 2026-konsolideringen.
- URL: https://futureagi.substack.com/p/top-5-agentic-ai-frameworks-to-watch

**Hugo Bowne-Anderson: "The State of AI in 2025" (Substack)**
- Retrospektiv: hvad der mattered mest i 2025, implikationer for 2026.
- URL: https://hugobowne.substack.com/p/the-state-of-ai-in-2025-what-mattered

**Florian Delval: "The AI Terms That Defined 2025" (Foreign Key, Substack)**
- Context engineering, orchestration, MCP som de definerende termer for 2025.
- URL: https://foreignkey.substack.com/p/ai-terms-that-defined-2025-context-engineering-orchestration-mcp

---

## Del 3: Spørgsmål til næste loop

### Implementerings-spørgsmål (byg-relaterede)

1. **Hybrid search evaluering:** Hvis vi implementerer hybrid search (dense 70% + BM25 30%), hvordan måler vi forbedringen? Vi mangler en eval pipeline. Bør vi bygge 10 test queries med kendte gode svar FØR vi re-ingester?

2. **Reranking cost/benefit:** Cohere Rerank koster ~$1/1000 queries. Med ~20 queries/dag = $0.60/måned. Er latencen (200-500ms) acceptabel for interaktiv brug via ctx?

3. **A-RAG vs. simpel retrieval:** A-RAG giver agenten 3 retrieval-tools (keyword, semantic, chunk read). Kan vi implementere noget lignende med Qdrant + en simpel wrapper, uden at adoptere hele A-RAG frameworket?

4. **Memori-tilgangen:** Er der memory-typer i Yggdra hvor en relationel model (facts, entities, events med timestamps) ville være bedre end vektorer? F.eks. route history, session metadata, decisions?

### Research-spørgsmål (forstå-relaterede)

5. **Context rot kvantificering:** Anthropic og Zechner siger "ting falder fra hinanden ved ~100K tokens." Men vores sessions er typisk 20-50K. Er context rot reelt et problem for os, eller er det premature optimization?

6. **Filesystem vs. tiered memory:** Letta's benchmark viser filsystem er "overraskende stærkt." Yggdra bruger allerede filsystem (NOW.md, episodes.jsonl, MEMORY.md). Hvornår præcist rammer vi grænsen?

7. **Session-blindhed og memory:** DLR.session-blindhed dokumenterer reasoning-fejl. Er der en forbindelse mellem memory-arkitektur og reasoning-fejl? Giver bedre kontekst-loading færre blindhed-episoder?

8. **Sparse autoencoder for faithfulness:** arXiv 2512.08892 bruger SAE til at identificere hallucination-features. Er dette anvendeligt for vores setup, eller kræver det model-intern adgang vi ikke har?

### Meta-spørgsmål (process-relaterede)

9. **Research-vedligeholdelse:** Vi har nu 60+ research-filer. Hvornår begynder mængden at være et problem? HOLISTIC_EVALUATION.md antyder ~30% duplikater. Bør vi konsolidere FØR vi researcher mere?

10. **Adoption gap:** Vi har solid research om hybrid search, reranking, temporal decay, heartbeat. Alt dette er designet men kun delvist implementeret. Bør næste loop fokusere på at BYGGE i stedet for at RESEARCHE?

---

## Kildeliste (nye kilder fundet i denne session)

1. Anthropic Engineering Blog — "Effective Context Engineering for AI Agents" (2025). https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
2. LangChain Blog — "Context Engineering for Agents" (2025). https://blog.langchain.com/context-engineering-for-agents/
3. arXiv 2512.05470 — "Everything is Context: Agentic File System Abstraction" (2025). https://arxiv.org/pdf/2512.05470
4. arXiv 2602.03442 — "A-RAG: Scaling Agentic RAG via Hierarchical Retrieval Interfaces" (2026). https://arxiv.org/abs/2602.03442
5. arXiv 2510.07794 — "HiPRAG: Hierarchical Process Rewards for Agentic RAG" (2025). https://arxiv.org/abs/2510.07794
6. arXiv 2512.08892 — "Toward Faithful RAG with Sparse Autoencoders" (2025). https://arxiv.org/abs/2512.08892
7. arXiv 2401.05856 — "Seven Failure Points When Engineering a RAG System" (2024). https://arxiv.org/html/2401.05856v1
8. Letta Blog — "Benchmarking AI Agent Memory: Is a Filesystem All You Need?" (2026). https://www.letta.com/blog/benchmarking-ai-agent-memory
9. Eric Ma — "Mastering PKM with Obsidian and AI" (marts 2026). https://ericmjl.github.io/blog/2026/3/6/mastering-personal-knowledge-management-with-obsidian-and-ai/
10. Latitude — "Ultimate Guide to Preprocessing Pipelines for LLMs" (2025). https://latitude.so/blog/ultimate-guide-to-preprocessing-pipelines-for-llms
11. Elumenotion — "RAG is an Anti-pattern" (2025). https://www.elumenotion.com/Journal/RagIsAnAntipattern.html
12. Kubiya — "Context Engineering Best Practices" (2025). https://www.kubiya.ai/blog/context-engineering-best-practices
13. Nate's Newsletter — "Beyond the Perfect Prompt" (Substack). https://natesnewsletter.substack.com/p/beyond-the-perfect-prompt-the-definitive
14. Cobus Greyling — "Agentic Context Engineering" (Substack). https://cobusgreyling.substack.com/p/agentic-context-engineering
15. Hugo Bowne-Anderson — "The State of AI in 2025" (Substack). https://hugobowne.substack.com/p/the-state-of-ai-in-2025-what-mattered
16. Elephas — "Solo Consultant AI Stack Guide 2026". https://elephas.app/resources/solo-consultant-ai-stack-guide
17. Florian Delval — "AI Terms That Defined 2025" (Substack). https://foreignkey.substack.com/p/ai-terms-that-defined-2025-context-engineering-orchestration-mcp
18. FutureAGI — "Top 5 Agentic AI Frameworks 2026" (Substack). https://futureagi.substack.com/p/top-5-agentic-ai-frameworks-to-watch
19. MachineLearningMastery — "3 Types of Long-term Memory AI Agents Need" (2026). https://machinelearningmastery.com/beyond-short-term-memory-the-3-types-of-long-term-memory-ai-agents-need/
20. NStarX — "The Next Frontier of RAG 2026-2030". https://nstarxinc.com/blog/the-next-frontier-of-rag-how-enterprise-knowledge-systems-will-evolve-2026-2030/
