# Progress — Yggdra

Fortællende dagbog. Formålet er at en ny Claude-session kan læse dette og forstå *hvorfor* vi er hvor vi er, ikke bare *hvad* der er gjort. CONTEXT.md er state, dette er kontekst.

---

## Session 22 (2026-03-15)

Backlog burn planlagt. VPS V6 deployet. Taxonomy-migration staged fra session 21 verificeret.

**Backlog burn brief skrevet.** Hele backloggen gennemlæst og organiseret i én RDY-brief (`RDY.backlog-burn.md`). Planen har to dele: VPS Ralph loop (7 iterationer, autonom) og PC-opgaver (7 blokke). Samlet forventet lukning: 8 briefs + 6 V4 handlinger.

**VPS V6 deployet.** CLAUDE.md, LOOP_PLAN.md, LOOP_STATE.md uploadet til `/root/Yggdra/yggdra-pc/v6-backlog-burn/`. 7 iterationer:
1. Fix RSS bug + genaktivér heartbeat
2. Temporal decay i get_context.py
3. Cohere reranking (kan BLOCKE hvis API key mangler)
4. Pipeline health check i daily_sweep.py
5. Blog RSS feeds + rens sources
6. Automation inventory (VPS-side)
7. Review alle ændringer

**Taxonomy rename:** Session 21 havde staged `2_research → LIB.research` renames. Ikke committet endnu — venter på session 22 PC-blok P1.

**Beslutninger:**
- Context-engineering fase 1: Gap-analyse viser at 3/4 hooks allerede eksisterer fra VPS-æraen. Reelt gap er kun PostToolUse chatlog-trigger
- Webscraping-audit: Lukkes direkte — Firecrawl skill er allerede installeret og dækker behovet
- Cohere reranking: Sandsynligvis BLOCKED (ingen API key), men prompten håndterer det gracefully

---

## Session 21 (2026-03-15)

VPS sandbox v2 og v3 afsluttet. Output evalueret, guld hentet til PC, resten sorteret fra.

**V3 resultater modtaget.** VPS leverede besked med filregister og evaluering. 6 iterationer, alle done-kriterier opfyldt: Research INDEX.md fik 54 Key Insights (3/3 spot-checks ACCURATE), 4 TI subproject stubs uddybet fra 16→30-40 linjer, chatlog renset (0 artefakter), dialectic-pipeline skill bygget (120L), N8N archive med kausal kæde (93L). Reviewers: 4×IMPROVED, 3×PASS, 0×FAIL.

**Evaluering med subagents.** Tre parallelle subagents hentede og vurderede output via SSH. Research INDEX.md insights verificeret mod kilder — alle 3 spot-checks accurate (CH2 context window 40%, METR 19% langsommere, Armin Ronacher 4 tools). TI subprojects: voice-dekomponering (4 kontekster) var standout, diesel korrekt markeret THIN. OpenClaw-framing i INDEX.md var eneste PARTIAL (komprimerede nuance for aggressivt — tool fravalgt, principper adopteret).

**Fuld VPS-inventar.** 147 filer scannet. 20 med ægte værdi identificeret, ~100 duplikater af PC-filer, resten rådata/proces-artifakter. Fandt uventet guld: BLUEPRINT.md (5-lags systemarkitektur), vps-pc-convergence.md (anbefaler Model B: separate domæner), session-resume og sitrep skills (ikke set i v3-rapporten).

**Hentet til PC (20 filer):**
- 3 skills: dialectic-pipeline, session-resume, sitrep → `.claude/skills/`
- TransportIntra projekt: INDEX.md (194L, crown jewels + hurtigreference), PROGRESS.md (103L, 4 kausale kæder), CONTEXT.md, api-reference.md (519L, 8 endpoints), getrute-schema.md (316L, 132 felter), N8N_SUMMARY.md (93L), 8 subproject CONTEXT.md → `projects/transportintra/`
- Research INDEX.md v3 (54 Key Insights) → `projects/research/`
- BLUEPRINT.md → roden
- vps-pc-convergence.md → `projects/research/`
- MINING_RESULTS.md → `projects/prompt-skabeloner/`
- V3_EVALUATION.md → `projects/vps-sandbox/`

**TRIAGE.md bygget fra PC's briefs.** 12 briefs triageret i 4 kategorier: Klar (context-engineering, automation-index, research-architecture), Næste op (notion-spejling, pdf-skill, abonnement-overblik, cross-session-peer-review), Kræver skærpning (integrationer, visualisering, voice-integration), Lav prioritet (project-taxonomy, work-intake). Session-forslag: context-engineering fase 3-5 først.

**VPS-sandbox som projekt.** `projects/vps-sandbox/CONTEXT.md` oprettet med v1/v2/v3 historik. Dokumenterer infrastrukturen (Ralph loop, LOOP_STATE rolling window, prompt-design) og hvad der er hentet til PC.

**Broken pointer fikset.** N8N_SUMMARY.md refererede til TI_KOMPLET_KILDEINDEX.md uden sti — rettet til VPS-path.

**Beslutninger:**
- VPS yggdra-pc/ indhold triageret: 20 filer hentet, resten ignoreret
- TRIAGE.md bygges fra PC's faktiske briefs, ikke VPS'ens (mismatched count: 16 vs 12)
- BLUEPRINT.md placeret i roden (systemarkitektur, ikke projekt-specifikt)
- VPS-sandbox er ét projekt selvom det berører flere — kan opløses senere

---

## Session 19 (2026-03-14)

VPS sandbox v2 designet, evalueret og deployed. Tre projekter kører nu autonomt i Ralph loop.

**VPS v1 kvalitetsaudit.** Tre subagents undersøgte VPS'ens `yggdra-pc/` sandbox-output fra en tidligere autonom kørsel (6 iterationer). Fandt: direction-analysis var stærk (8/10, ærlig selvkritik), context-engineering god reference (7.5/10), men research-architecture-rapporten overdesignet (6/10 — Zettelkasten + PARA + 6-step pipeline for én person). Mindst én halluceret kilde (Stanford NLP 40% claim). Procesproblemet: 6 iterationer for at aktivere én JSON-fil fordi "done" aldrig blev verificeret.

**Samlet VPS-prompt.** Tre projekter i én Ralph loop: (A) Research Architecture — audit 81 filer, byg INDEX.md. (B) TransportIntra Arkiv — komplet projektmappe fra alle kilder, med TI_KOMPLET_KILDEINDEX.md (519 linjer, fundet på VPS) som scanner-input. INDEX.md er vigtigste deliverable. (C) Prompt-skabeloner — mine chatlog for instruksmønstre, byg 1-2 skills.

**Prompt evalueret med 3 subagents.** Token-efficiency fandt: LOOP_STATE vokser uendeligt (fix: rolling window), iteration 4 risikerer at scanne 942 filer (fix: cap top 30), iteration 9 for komprimeret. Deliverable-quality forudså: TI INDEX.md bliver god, PROGRESS.md risikerer event-liste i stedet for narrativ, subproject CONTEXT.md'er bliver delvist scaffolding. Failure-modes fandt: cascading failure uden input-validering (fix: check forrige iterations output), bash loop uden error handling (fix: grep for BLOCKED). Alt justeret i final prompt.

**Handoff absorberet.** Session github-workflow havde uploadet chatlog.md + prompt.md + reference-skill til VPS for prompt-skabeloner projektet. Cross-session peer review bagt ind som iteration. Prompt-skabeloner CONTEXT.md, CLAUDE.md og VPS_HANDOFF.md committet.

**Brief opdateret.** brief.research-architecture.md nu inkluderer VPS audit-resultater med scores, hvad der holder/ikke holder, og procesproblemer.

**Deployed.** CLAUDE.md (100 linjer), LOOP_PLAN.md (118 linjer), LOOP_STATE.md (initial) uploadet til VPS. Start-kommando: for-loop med timeout 600, blocker-check, state-validering.

---

## Session 18 (2026-03-14)

Tre spor i dag: Ydrasil-projekt, MCP/Skills kompendium, og infrastruktur-oprydning.

**Ydrasil-projekt startet.** VPS research og docs (downloadet i session 16) blev indekseret. INDEX.md oprettet som overblik over alt indhold fra Ydrasil-æraen. Projektet bor i `projects/ydrasil/` med sessions/, docs/ og research/.

**MCP/Skills kompendium research gennemført.** Den adversarial research-proces designet i session 17 blev eksekveret: context scout, parallel research (MCP-landskab, skills-landskab, Yggdra-behov), steelman, red team, neutral evaluator. Resulterede i `kompendium-mcp.md`, `kompendium-skills.md`, `needs-mapping.md` og `anbefaling.md`.

**Skills tilføjet.** Syv nye skills installeret i `.claude/skills/`: context-search, debugging-wizard, mcp-builder, spec-miner, strategic-compact, the-fool, verification-loop.

**Nye backlog briefs.** project-taxonomy og session-blindhed tilføjet. Tre briefs slettet/merged (mcp-skills-kompendium blev projekt, session-drift-pipeline merged med context-engineering, webscraping-audit + terminal-automatisering → raw/).

**Infrastruktur.** `data/` og `scripts/` mapper oprettet i roden. Projektmapper havde midlertidigt fået underscore-prefix (`_auto-chatlog` osv.) — fjernet igen ved checkpoint. Checkpoint-skill rettet: chatlog-engine kører nu som trin 1 (før state-filer opdateres), så sessionsdata fanges inden kontekst-opdatering.

**Beslutninger:**
- Chatlog-engine kører først i checkpoint-flow (fanger sessionsdata før state-opdatering)
- Ingen underscore-prefix på projektmapper (unødvendig konvention)
- data/ og scripts/ i roden (ikke under projects/)

---

## Session 17 (2026-03-14)

Kort session fokuseret på MCP/Skills kompendium-projektet.

Skills-synlighed i VS Code blev afklaret: globale skills i `~/.claude/skills/` vs projekt-specifikke i `.claude/skills/`. Alle relevante skills var allerede synkroniseret i projekt-mappen.

MCP/Skills kompendium opgraderet fra backlog-brief til aktivt projekt i `projects/mcp-skills-kompendium/`. Adversarial research-proces designet: context scout opsamler landskabet → parallel research i tre spor (MCP-servere, skills, Yggdra-behov) → steelman → red team → steelman red team → neutral evaluator. Formålet er at undgå confirmation bias i teknologi-valg.

---

## Session 16 (2026-03-15)

Backlog-audit og VPS research download.

**Backlog-audit:** 14 briefs reduceret til 11. context-engineering og session-drift-pipeline merged. webscraping-audit og terminal-automatisering flyttet til raw/ (ikke modne nok). 6 briefs opdateret og skærpet (visualisering, mcp, integrationer, notion, peer-review, voice).

**VPS Ydrasil-æra download:** Al research og docs fra VPS downloaded til `projects/research/ydrasil/` (89+73 filer, ~9MB). GDrive-duplikat slettet. Research-kvalitet vurderet: høj substans men iterativt klutter (~30% duplikater fra ChatGPT-kapitler).

**Prioriterings-diskussion:** research-arkitektur → agent teams → hukommelse. Vision-briefs parkeret (transport-app, politik, LLM-uafhængighed) — vigtige men ikke næste step.

---

## Session 15 (2026-03-14)

M5 system-opsætning og chatlog-engine forbedringer.

**M5 steps:** Downloads ryddet (225→2 filer), .wslconfig oprettet (8GB/4CPU), JetBrains Mono installeret med ligaturer, quick reference skrevet. M6/M7/M8 flyttet fra PLAN.md til backlog-briefs — de er selvstændige nok til at leve som projekter.

**Chatlog-engine:** Token-scanning tilføjet (heuristisk scanner + subagent-verifikation via redact-patterns.json). Parallel tasks output absorberet i relevante backlog-briefs.

**Oprydning:** "Basic Setup" referencer fjernet overalt. architecture.R&D fik CONTEXT.md. Archive ryddet. Lektie lært: `rm` i bash bypasser Windows papirkurven — slettet er slettet.

---

## Session 14 (2026-03-13)

Session 14 startede med et praktisk problem: Claude-sessions var spredt over 5 projektmapper fordi workspace-stien havde ændret sig over tid. Alle 30 .jsonl-filer blev samlet i én mappe (c--Users-Krist-dev-projects-Yggdra), og chatlog-engine'ens input-sti blev rettet.

Derefter blev chatlog-engine opgraderet til v3. Tre store ændringer: (1) faste 2-timers tidsblokke erstattet af gap-baseret sektionering — 90 minutters pause mellem beskeder = nyt afsnit, virker på tværs af sessions. (2) Frekvens-baserede nøgleord (der var ubrugelige) erstattet af subagent-genererede abstracts — en haiku-subagent læser en komprimeret digest og skriver 1-4 sætnings dato-abstracts + 1-2 sætnings sektions-abstracts. (3) Danske datoer med ugedage i hovedindeks ("fredag d. 13/3-2026").

GitHub push protection blokerede push pga Notion API tokens i chatlog.md. Secret-redaction tilføjet: built-in patterns (Notion, OpenAI, GitHub, Slack, AWS) + dynamisk via redact-patterns.json + heuristisk token-scanner der flagger suspekte strenge til subagent-review.

Checkpoint og chatlog-search skills blev konsolideret ind i auto-chatlog-projektet. Skills-filerne i .claude/skills/ reduceret til korte pointere — fuld dokumentation i projects/auto-chatlog/CONTEXT.md. Mønstret: skill = pointer, projekt = sandhed.

Archive ryddet: implementation-journals, manuelle chatlogs, dump-chatlog.js slettet (alt i git). git-concepts.md → manuals/. google-ai-samtale → architecture.R&D/ (med ny CONTEXT.md der forklarer hvad det var og hvorfor det blev arkiveret).

Template opdateret: NOW.md + PLAN.md slettet, CONTEXT.md template oprettet. CLAUDE.md template og new-project skill opdateret til nyt format.

Reformation fase 6 (oprydning) og fase 7 (omdøbning) afsluttet. "Basic Setup" → "Yggdra" i alle interne referencer. Project Reformation er done.

**Beslutninger:**
- Gap-baseret sektionering (90 min) fremfor faste tidsblokke
- Subagent-abstracts fremfor lokal LLM (Ollama parkeret)
- Skills som pointere, projekter som sandhed
- CONTEXT.md som eneste state-fil-konvention (NOW+PLAN droppet overalt)
- Secret-redaction i chatlog-engine (ikke .gitignore)

---

## Session 13 — 2026-03-13

### Kontekst

Fortsættelse af reformation. Session 12 havde implementeret manifest v1-v3 med pipeline/-struktur. Denne session simplificerede radikalt.

### Hvad skete der

**Fil-audit diskussion:** Startede med at gennemgå manifest fra session 12. Yttre stillede spørgsmål til .firecrawl/ (git-tracked?), references/-mappen, og automation.md. Hver diskussion afslørede at den eksisterende struktur var for kompleks.

**Tre iterationer af mappestruktur:**
1. `pipeline/` med numeriske præfikser (0_backlog → 4_ARC) — fra session 12
2. `Development/` med stage-mapper — Yttre ville have pipeline ud af BMS-roden
3. `projects/` flad — Yttre indså at ADR er bare en mini-CONTEXT.md, og pipeline-stages i mappenavne er overengineering

**ADR → CONTEXT.md:** Yttre sagde "ADR er i bund og grund blot en mini-context.md" — det udløste den største simplificering. Ét format overalt. Stage-navne (PoC/DLR/SIP/BMS) erstattet af plain dansk status ("I gang — parser fungerer, mangler automatisering").

**Manifest v4 implementeret:** Alle filer flyttet til `projects/`. Gamle mapper slettet. CLAUDE.md og NOW.md opdateret. Tre CONTEXT.md-filer opdateret med nye stier og terminologi.

**CONTEXT.md template:** Diskuterede opbygning. Landede på 6 sektioner: Metadata, Hvad er det, Hvor er vi, Hvad mangler, Beslutninger, Changelog. Skalerer fra brief (kun Metadata + Hvad er det) til komplekst projekt (alle sektioner + ekstra efter behov).

**Rod-CONTEXT.md udkast:** Destillerede NOW.md + PLAN.md + PROGRESS.md til ét dokument med graduated summary. ~100 linjer vs 380+ i de tre separate filer.

### Beslutninger

- `projects/` i roden — flad, ét projekt = én mappe
- ADR-terminologi droppet — CONTEXT.md overalt
- Pipeline-stage navne droppet — status i plain dansk
- Manuals og research ind under projects/ (de er projekter)
- CONTEXT.md template: 6 sektioner, skalerbar
- Governance READMEs unødvendige — stage er metadata

### Evaluering

Sessionen viste et mønster: Yttre starter med en kompleks idé (ISO-standarder, pipeline-stages, governance-manualer) og simplificerer progressivt til det essentielle. "Simpelt = exact fit" i praksis. Tre iterationer var nødvendige, men resultatet er markant simplere end udgangspunktet.

---

## Session 12 — 2026-03-12

### Kontekst

Implementeringssession for Project Reformation fase 1-4. Første session der lavede konkrete filflytninger.

### Hvad skete der

**Fase 1-2 (mappestruktur):** Pipeline-mapper oprettet under `pipeline/` med numeriske præfikser (0_backlog → 4_ARC). template/ absorberet i .claude/template/. Alle filer flyttet: references/ opløst, chatlogs/ pensioneret, implementation journals arkiveret. Rod reduceret fra 10 synlige mapper til 3.

**Fase 3 (backlog-briefs):** 13 briefs oprettet fra idé-parkering + parallel-tasks outputs. Alle 7 parallel-tasks outputs (~/parallel-tasks/) mappet til specifikke briefs. PLAN.md idé-parkering erstattet med pointer.

**Fase 4 (ADR'er):** 2 retroaktive ADR'er skrevet: auto-chatlog (SIP) og projekt-omdøbning (PoC). Begge følger 12-sektions template.

**Afkrydsningsfejl:** Step 4.4 (commit) blev udført men ikke afkrydset i ADR'en. Yttre påpegede det. Memory-regel gemt: "afkryds steps med det samme."

### Beslutninger

- Pipeline under `pipeline/` overmappe, ikke i roden
- Numeriske præfikser for kronologisk sortering
- Research er et projekt (research-architecture), ikke bare en mappe
- automation.md → backlog-brief

---

## Session 11 — 2026-03-12

### Kontekst

Fil-audit session (reformation fase 0.5). Formålet var at producere et komplet fil-manifest: hver fil og mappe i repoet → destination + begrundelse. Ingen kode, kun analyse og beslutninger.

### Hvad skete der

**Systematisk audit af 7 områder:** Roden, references/, chatlogs/, .claude/, template/, auto-chatlog/, ~/parallel-tasks/. Hvert område gennemgået fil for fil med destination og begrundelse.

**references/ opløses:** Den vigtigste beslutning i sessionen. Yttre identificerede tre distinkte ting musset sammen i én mappe:
1. **Manualer** (git.md, vscode.md, terminal.md) — levende håndbøger der kan vokse. Startede som cheatsheets men er reelt begyndelsen på en Yggdra-manual. → `manuals/`
2. **Research** — en praksis/kapabilitet, ikke bare en mappe. Betjener hele pipelinen. Kilder: AI-giganter (Anthropic, OpenAI, Perplexity), forskningsinstitutter, eksperter, communities. Al eksisterende research er pre-reformation og mangler kvalitetssikring. → `research/_ARC/`
3. **Historisk/absorberet materiale** (PLAN.v1, git-concepts, google-ai-samtale) → `_ARC/`

**Research-arkitektur som fremtidigt projekt:** Yttre beskrev en vision om research som fundamentalt infrastrukturprojekt — lige så vigtigt som Yggdras kernearkitektur. Alle praksisser, strategier og beslutninger bygger på research, men hvor godt er fundamentet? VPS har masser af research der er forældet eller amatøragtigt udført. Alt skal gennemgås, researches på ny, opdateres. Men først skal research-praksis selv være formidabel. → backlog-brief, høj prioritet post-reformation.

**automation.md → backlog:** Filen dokumenterer hooks/workflows men er forældet og fejlplaceret. Erstattes af et kommende system: levende index over alle automatiske processer, for overblik og cruft-forebyggelse. → backlog-brief.

**chatlogs/ pensioneres:** Flyttes til `_ARC/chatlogs/`. Auto-chatlog i SIP overtager funktionen.

**.firecrawl/ ignoreres:** Ikke git-tracked, tilføjes til .gitignore. Tool-cache, ikke projekt-output.

**Git-tracked forklaret:** Yttre spurgte hvad "git-tracked" betyder. Forklaret: tracked = git kender filen og versionerer den. Ikke tracked = kun lokalt. .gitignore = "ignorer altid."

### Beslutninger

- references/ opløses → manuals/ + research/_ARC/ + _ARC/
- Al eksisterende research er pre-reformation → research/_ARC/
- research/ starter tom — fyldes når research-arkitektur er på plads
- automation.md → backlog (kommende automation-index system)
- brief.research-architecture.md → _backlog/ (høj prioritet post-reformation)
- brief.automation-index.md → _backlog/
- .firecrawl/ → .gitignore

### Fil-manifest produceret

Komplet manifest med destination per fil. Godkendt af Yttre. Klar til implementering (fase 1-2).

---

## Session 3 — 2026-03-10

### Hvad skete der

Yttre åbnede VS Code efter at have lukket den ned for at flytte mapper i File Explorer. Han skrev "done" — fordi den forrige session (session 2) havde bedt ham flytte mapper manuelt og skrive når det var gjort. Men den nye Claude-session (denne) havde ingen kontekst, misforstod "done" som "sessionen er slut", og sagde god nat. Det var forkert, og Yttre blev frustreret.

Det afslørede et fundamentalt problem: **PC'en har ingen mekanisme til at bevare session-kontekst.** NOW.md var ikke opdateret fra session 2. Memory-filer var tomme. Chatloggen var væk. En ny session starter blindt.

### Hvad vi undersøgte

Vi dykkede ned i Yggdra (VPS) for at se hvordan det problem er løst der. VPS'en har et hook-system:
- `save_checkpoint.py` kører ved Stop/PreCompact — læser transcript, destillerer via Groq, opdaterer det relevante projekts NOW.md, appender til episodes.jsonl og daglig log
- `load_checkpoint.sh` kører ved SessionStart — injicerer alle projekters NOW.md + seneste 5 episoder som kontekst

Det system virker. Der er daglige checkpoint-filer på 80KB+, episoder med projekt-routing, og NOW.md'er der faktisk afspejler hvad der skete. Men det er også custom-bygget til Yggdra, afhængigt af Groq API, og læser transcript-filer direkte (implementation detail der kan ændre sig). Vi besluttede at tage det som reference for M7 (context engineering), men ikke kopiere det nu.

### ~/dev/ layout

Session 2 havde påbegyndt M4 step 2 — organisere `~/dev/`. Mapper var allerede oprettet (projects/, archive/, sandbox/, tools/) men ikke alle ting var flyttet endnu. I denne session flyttede vi:
- `~/BLUEPRINT.md` → `~/dev/BLUEPRINT.md` (historisk reference-dokument fra før VS Code-perioden)
- `~/scripts/` → `~/dev/scripts/` (ctx, tunnel, setup — Yggdra PC-tools)
- `~/docs/` → `~/dev/docs/` (external LLM docs for Notion/Qdrant)

`~/CLAUDE.md` bliver i `~/` — den skal ligge der for at virke som global Claude-instruks.

### Deep dive i Yggdra-repoet

Yttre bad mig researche grundigt i VPS-dokumenterne før vi bygger videre, fordi "blandt rodet er der grundlæggende guldkorn" som vi har brugt massive mængder tid og tokens på at grave frem. Han har ret — det er spild at starte forfra uden at lære af det.

Jeg læste alt relevant:
- **DAGBOG.md** — 117 genstarter, vendepunkter, mønstre. Vigtigste indsigt: 18. feb voice memo hvor Yttre siger "der hvor jeg har haft mest fremgang er når jeg bare har implementeret noget"
- **YDRASIL_ATLAS.md** (27K) — det mest komplette overbliksdokument. 5 kategorier (Projekter, Struktur, Viden, Principper, Handlinger) med krydsreferencer via tags
- **HANDLINGSPLAN.md** — 7 konsensusprinciper udtrukket fra 11 videoer (Miessler, Nate Jones, Cole Medin, AI Automators). Valideret mod Yggdras faktiske arkitektur
- **PC_SETUP.md** — en guide fra 3. marts til at sætte PC op med Claude Code + VPS-adgang. Foreslog `~/projects/` med separate repos per projekt
- **ARCHITECTURE_CONTINUOUS_MEMORY.md** — 6 principper for hukommelse, byggeplan, kilder fra MemGPT, OpenClaw, Gastown, GitHub Copilot, Miessler
- **PAI_BLUEPRINT.md** — Miesslers 5-lag model tilpasset Yggdra
- **MANUAL.md** — 4 kendte fælder + mirror-princippet
- **MISSION.md, PRIORITIES.md, TRADEOFFS.md** — system-level beslutningsdokumenter

Alt dette er destilleret til `references/yggdra-gold.md` med kildehenvisninger.

### Research: professionelle mappestruktur-konventioner

Gennemførte M4 step 1 research via web (dev.to, Hacker News, MIT Missing Semester, VS Code docs, mcpmarket.com). Resultat i `references/project-structure.md`:
- Tre reelle organisationsmønstre (by status, by platform, by client)
- Polyrepo er normen for personlige workspaces
- Per-projekt essentials: .gitignore, .editorconfig, .gitattributes, README.md
- Dotfiles-repo: bare git, GNU Stow, eller chezmoi
- VS Code workspace-filer: .code-workspace + .vscode/ per projekt

### Gennemgang af Basic Setup projektet

Læste alle 22 filer i projektet. Identificerede:
- **Outdated:** vscode.md nævner JetBrains Mono og Mermaid Preview som om de er installeret (de er ikke)
- **Mangler:** .editorconfig, .gitattributes, .vscode/extensions.json
- **Tom:** habits/ mappe — intention ukendt
- **Stale:** dump-session.js med hardcoded session ID, session-history.md (446KB fra session 1)

### Beslutninger

1. **Basic Setup er main workspace.** Sub-projekter (fx context engineering) vokser ud til egne workspaces når de kræver det.
2. **Rækkefølgen M4→M5→M6→M7 holdes.** Context engineering (M7) er vigtigt men ikke urgent.
3. **BLUEPRINT.md er historisk.** Det var det strategiske dokument fra *før* VS Code-perioden. Det opdateres ikke løbende.
4. **PC'en kopierer principper fra VPS, ikke struktur.** VPS har cruft (broken services, zombie cron, 27GB ubrugte Docker images). Principperne er solide (state på disk, progressive disclosure, kill conditions).
5. **Chatlog gemmes manuelt** indtil M7 løser det automatisk. dump-chatlog.js konverterer JSONL → markdown.

### Hvad der mangler for M4 completion

- **Step 2 (90% done):** Fastlæg konventionen for ~/dev/ — hvad hører i projects/, sandbox/, tools/, archive/. Evt. README i ~/dev/.
- **Step 3:** Per-projekt skabelon — .editorconfig, .gitattributes, .gitignore, CLAUDE.md, PLAN.md, NOW.md
- **Step 4:** Dotfiles-repo — versionér .zshrc, .gitconfig, starship.toml
- **Step 5:** VS Code workspace-fil skabelon

### Evaluering (Popper-loop)

**Hvad overraskede:** Hvor meget guld der ligger begravet i Yggdra-repoet som aldrig bliver brugt. 60+ research-filer, 10-kapitel bog, detaljerede analyser af 190 AI-samtaler. Problemet er ikke mangel på viden — det er mangel på *retrieval*. Det er præcis det M7 skal løse.

**Hvad gik galt:** Session 2's kontekst gik tabt. NOW.md var ikke opdateret. Ingen chatlog. Ingen hook. Det kostede ~30 minutter af denne session at rekonstruere hvad der var sket.

**Hvad vi gør anderledes:** Denne session gemmer chatlog, opdaterer NOW.md grundigt, og skriver denne progress-rapport. Indtil M7 automatiserer det, er det manuelt.

---

## Session 5 — 2026-03-10 (fortsættelse af session 3)

### Kontekst

Session 3's videreførelse efter compact. Startede med at verificere at alt var gemt, derefter M4 step 2 completion.

### Hvad skete der

**Chatlog-vedligeholdelse:** Opdagede at compact sletter fra JSONL — beskeder efter dump kan gå tabt. Dumpede chatlog igen (122→134→152 beskeder over sessionen).

**~/dev/ layout afsluttet (M4 step 2 DONE):**
- Auditerede alle mapper i ~/dev/
- `tools/` slettet (tom, overlap med scripts/)
- Konvention fastlagt: projects/ (aktive, git repo), archive/ (done/paused), sandbox/ (throwaway), scripts/ (→dotfiles/bin/ ved step 4), docs/ (external)

**Taksonomi-diskussion:** Yttre stillede spørgsmålstegn ved forskellen på scripts/tools/skills/MCP. Første svar var forsimplet — Yttre fangede det ("jeg troede det var AI der brugte tools?"). Rettede til præcis taksonomi: skills inform, hooks enforce, MCP integrates. Research bekræftede at vokabularet stabiliserer men ikke er standardiseret.

**Research (3 parallelle agenter):**
- Claude Code community: skills/hooks/MCP organisation, emerging conventions
- Dev workspace: ~/bin/ vs scripts/ vs tools/ — konsensus er bin/ på PATH for personlige scripts
- AI-augmented workflows: AGENTS.md som vendor-neutral standard (Claude læser det ikke endnu)

**Nomenklatur-rettelse:** "Popper-loop" var opfundet af Claude i session 2. Erstattet med PDCA-cyklus (Plan-Do-Check-Act, Deming — 70+ år, akademisk etableret). Yttre påpegede vigtigheden af professionel nomenklatur.

**Solnedgangsklausul raffineret:** Kill er sidste udvej. Default-respons: justér → omtænk → kill. De fleste ting der "ikke virker" virker bare anderledes end forventet.

**Plan for step 3-5 + PDCA:** Hver step har nu sine egne solnedgangsklausuler. Step 3 evaluerer hver skabelon-fil individuelt (.editorconfig kill-tegn: kun VS Code bruges).

### Beslutninger

- PDCA-cyklus erstatter Popper-loop
- ~/dev/tools/ slettet
- scripts/ → dotfiles/bin/ planlagt til M4 step 4
- Plan v3 initieres efter M4 PDCA-evaluering

### Nye reference-filer

- `references/claude-code-organization.md` — Claude Code skills/hooks/MCP konventioner
- `references/scripts-and-tools-layout.md` — dev workspace layout konventioner

### Idé-parkering gennemgået + parallel tasks forberedt

Alle 12 parkerede idéer auditeret med effort/paralleliserbarhed. 7 task briefs oprettet i ~/parallel-tasks/ til Cowork eller parallelle sessioner. Hver brief er selvstændig med baggrund, metode, forventet output, og eksplicitte bias-warnings. Integrationer (Gmail, Google, mobil-adgang) tilføjet som ny parkering. "Chatlog-arkitektur" omdøbt til "Session-drift pipeline" — dækker hele den daglige drift-loop, ikke kun chatlog. #5 (Adobe Acrobat) anbefalet fjernet (installer ved behov, ikke en parkeret idé).

---

## Session 9 — 2026-03-11

### Kontekst

Sessionen startede med M5 step 10 (bloatware-fjernelse) men eskalerede hurtigt til et fundamentalt arkitektur-redesign af hele projektstyringen.

### Hvad skete der

**M5 step 10:** 11 bloatware-apps fjernet via PowerShell. Derefter opdagede Yttre at PLAN.md ikke var opdateret — step 2-10 var udført men ikke afkrydset. Det afslørede et strukturelt hul i checkpoint-skillen.

**Auto-chatlog:** Yttre spurgte om chatloggen kunne opdatere sig selv automatisk. Det startede en kaskade: vi byggede chatlog-engine.js (parser: .jsonl → live.md + archive.md), itererede tre gange på formatet (dansk tid, under-index med 2-timers blokke, nøgleord). Yttre kalibrerede: "spørg før du bygger" — Claude gik i bygge-mode for tidligt.

**Google AI Mode session:** Parallelt kørte Yttre en samtale med Google AI Mode om R&D-mappestruktur og ADR-templates. Samtalen validerede og forfinede idéen om en livscyklus-pipeline. Pipeline-navne gennemgik flere iterationer: TRL/DLR/SIP/BMS → RAW/DEV/STG/CORE → PoC/DLR/SIP/BMS.

**Project Reformation:** Kulminationen af sessionen. Det blev klart at Basic Setup ikke bare er "opsætning af udviklermiljø" — det er ved at blive et framework for hvordan Yttre arbejder med AI. Reformation designede:

- **Pipeline:** Backlog → PoC → DLR → SIP → BMS (roden er BMS)
- **To dimensioner:** Stage (hvor i pipeline) og Status (Active/Deprecated/Archived)
- **ADR-template** med 11 sektioner: Origin Story øverst (kontekst først), Original ADR nederst (frosset snapshot)
- **Governance-manualer** for alle 5 stages + Backlog med do/don't-eksempler og promotion/demotion criteria
- **Brief-format** for backlog-idéer (opsummering → origin story → rå input)
- **Changelog i dagbogsstil** — nok kontekst til at forstå hvad der skete og hvorfor, ikke bare "promoted til DLR"

**Test-session (9343d480):** Yttre testede en ny session for at se om kontekst overlevede. Det tog 5+ beskeder at genfinde konteksten — live.md var forældet, NOW.md var ufuldstændig. Dette bekræftede behovet for reformationen.

**Checkpoint-analyse:** Yttre opdagede at checkpoint ikke kørte alle 5 trin (NOW.md, PROGRESS.md, PLAN.md, chatlog-dump, git commit+push). Kun NOW.md blev opdateret. Årsag: skillen er en instruktion uden verifikation — ingen gate der sikrer komplet gennemførsel. Det er et generelt skill-arkitektur-problem, ikke specifikt for checkpoint.

### Beslutninger

- PoC/DLR/SIP/BMS som pipeline-navne (1-3 stavelser, professionelle)
- Stage og Status som to separate dimensioner
- ADR bor med det den beskriver (ikke central mappe)
- "brief" som term for backlog-idéer
- Origin Story i toppen af ADR, Original ADR i bunden
- Alle mapper har README.md med governance
- Checkpoint-hul noteret — skill-arkitektur brief planlagt til _backlog/

### Filer oprettet

- `project-reformation/ADR.md` — levende ADR for reformationen
- `project-reformation/ADR-template.md` — skabelon
- `project-reformation/README-Backlog.md`, `README-PoC.md`, `README-DLR.md`, `README-SIP.md`, `README-BMS.md`
- `auto-chatlog/chatlog-engine.js`, `live.md`, `archive.md`
- `references/google-ai-samtale-rd-framework.md`

---

## Session 8 — 2026-03-10

### M4 afsluttet

Step 5 (workspace-fil): Opdaterede basic-setup.code-workspace med extensions-anbefalinger (7 stk), workspace-settings (format on save, LF, trim whitespace) og files.exclude oprydning. Oprettede generisk template/project.code-workspace til nye projekter.

Step 6 (evaluering): /checkpoint evalueret efter 4 brug — virker fra brug #3, tidlige fejl var setup-problemer. /new-project skabelon komplet og skill aktiveret (flyttet til .claude/skills/), men utestet. chatlog-search for tidligt at evaluere.

M4 PDCA: Done-kriterie opfyldt. M4 markeret ✅. Næste modul: M5 (PC-setup).

---

## Session 7 — 2026-03-10

### M4 step 4: dotfiles-repo

Oprettede `~/dev/projects/dotfiles/` med GNU Stow til WSL-dotfiles. Diskuterede tre tilgange (bare git repo, GNU Stow, simpel kopi) — valgte Stow for .zshrc (symlink, ændringer virker straks) og manuel kopi for Windows .gitconfig (ændres sjældent).

Konkret: .zshrc stow-symlinket fra dotfiles/zsh/ → /home/yttre/, .gitconfig kopieret ind i dotfiles/git/, alle 6 scripts fra ~/dev/scripts/ flyttet til dotfiles/bin/ og sat på PATH via .zshrc. ~/dev/scripts/ slettet. README.md med opsætningsinstruktion.

gh CLI installeret (winget) og autentificeret som Yttrehus. Dotfiles-repo pushed til GitHub som privat repo.

### Installeret software

- GNU Stow (WSL, apt)
- GitHub CLI (Windows, winget) — autentificeret med browser-flow

### Workspace-oprydning

Slettet cruft: read-session.js, dump-session.js, session-history.md, chatlog-session4.tmp, habits/ (tom). dump-chatlog.js omskrevet til at gruppere per dato og flette sessions kronologisk — én chatlog-YYYY-MM-DD.md per dag. Oprettet chatlogs/ mappe. Flyttet PLAN.v1.md og git-concepts.md til references/. Oprettet references/README.md med indeks. Opdateret root README.md til aktuel struktur. Root er nu rent: kun state-filer, konventionsfiler, og mapper.

### Skills-arkitektur revideret

Tre ændringer: (1) BS-specifikke skills (checkpoint, session-state) flyttet fra global ~/.claude/skills/ til projekt-niveau .claude/skills/. Princip: skills starter lokalt, promoveres til global når bevist. (2) Feedback-log separeret fra skill-definition — .claude/implementationlogs/ oprettet med checkpoint.md og chatlog-search.md. (3) chatlog-search skill oprettet: søger i chatlogs/ efter specifik kontekst (beslutninger, diskussioner) med tvungen rapportering i implementationlogs.

.gitattributes + .editorconfig tilføjet til BS root fra template/ — fjerner CRLF-warnings der har plaget alle commits.

Diskussion om Claude Code skills-arkitektur: .claude/skills/ filer er reelt instruktionsfiler (kontekst der loades), ikke executable skills. Skill-toolet er for marketplace-plugins. Praktisk ingen forskel for brugeren — "checkpoint" virker ved at Claude læser instruktionen og følger den.

---

## Session 6 — 2026-03-10 (fortsættelse)

### M4 step 3: per-projekt skabelon

Oprettede `template/` med 6 filer: .editorconfig, .gitattributes, .gitignore, CLAUDE.md, PLAN.md, NOW.md. Testet ved at kopiere til sandbox, oprette et Python-projekt, og verificere at alle config-filer virker (indent, line endings, gitignore). Krydscheck mod Basic Setup afslørede at BS selv mangler .editorconfig og .gitattributes — venter med at tilføje til BS er færdig evalueret.

Feedback-loop indbygget: PLAN.md template har en "skabelon-feedback" sektion der besvares ved PDCA-evaluering. Mønstret: 1 projekt ændrer noget → notér. 2+ projekter ændrer det samme → opdatér skabelonen. En fil aldrig åbnet i 3+ projekter → overvej fjernelse.

### Skills oprettet

**`/new-project` (udkast, parkeret til step 5):** Bootstrapper et nyt projekt fra template/ med udfyldte placeholders. Feedback-loopet er indbygget — hvert projekt evaluerer skabelonen.

**`/checkpoint` (installeret, aktiv):** Samler den daglige drift-loop i ét kald: opdatér NOW.md + PROGRESS.md + PLAN.md, dump chatlog, commit + push. Selvvurdering: Claude skriver feedback efter hver brug, obligatorisk evaluering efter 5 brug. Erstatter det manuelle "commit, push, dump chatlog, opdater now.md, progress.md" som Yttre har bedt om ved hver session-pause.

### Beslutninger

- /checkpoint skill installeret nu — bruges resten af M4 for at samle erfaring
- /new-project parkeret til step 5 — kræver workspace-fil integration
- Step 6 tilføjet til PLAN.md: evaluering af begge skills efter step 5

---

## Session 4 — 2026-03-10 (morgen, parallel session)

### Kontekst-test bestod

Yttre åbnede en ny session (1f70d0bd) for at teste om konteksten fra session 3 overlevede. Den nye session fik "hvor er vi?" og svarede korrekt — M4 step 2, 90% done, præcise næste steps. Den læste NOW.md, PLAN.md og MEMORY.md. Chatlog var unødvendig for at komme op til speed. PROGRESS.md + NOW.md + MEMORY.md er tilstrækkeligt til session-kontinuitet.

### Projektet vokser ud af sit navn

Yttre formulerede en vigtig indsigt: "Basic Setup" er ikke basic — det er hovedprojektet. Det er hans personlige udvikler-fundament, og det vokser organisk mod noget større. Han foreslog:

1. **Omdøb projektet** ved M4's Popper-evaluering til noget der afspejler hvad det faktisk er
2. **"Basic Setup" bliver et *output*** — en reproducerbar pakke man kan køre for at genopbygge miljøet. Den pakke indeholder:
   - Installationsguide med step-by-step instrukser til brugeren
   - AI-instruktioner så Claude kan assistere i opsætningen
   - Et **manifest** der forklarer *hvorfor* hver beslutning er taget, ikke bare *hvad*
   - Indexerede chatlogs så man kan spørge "hvorfor valgte vi X?" og få det faktiske svar

### Chatlog-arkitektur (M7-stof, parkeret)

Session 4 og session 3 (denne sessions forgænger) kørte parallelt og reviewede hinandens output. Det udviklede sig til en produktiv diskussion om chatlog-infrastruktur:

**Chatlog-ID'er:** Hver besked får sekvensnummer (T001, T002...) + timestamp. Plan-filer kan referere til specifikke ranges (fx "se chatlog session 4, T042-T058") i stedet for at destillere alt ned til én bullet. Analog løsning der virker uden database.

**Event log:** I stedet for Excel-kolonner (Yttres intuition var visuel: tid × session), er en central JSONL event log bedre — `timestamp | session_id | project | type | content`. Flat, appendable, filtrérbar. Samme princip som Yggdras episodes.jsonl men med cross-session view.

**Tre-lags tilgang (konsensus mellem begge sessioner):**
1. Nu: forbedret dump-script med metadata (implementeret)
2. M7: taksonomi (beslutning/handling/diskussion) + auto-referencer i plan-filer
3. Senere: embedding i Qdrant (kun hvis behov bevist)

### Cross-session peer review

En uventet opdagelse: at køre to parallelle sessioner og lade dem reviewere hinandens output virker som evalueringsværktøj. Yttre medierede — copy-pastede mellem sessionerne og sikrede at han forstod alt. Det er ikke bare to AI'er der snakker; Yttre er aktivt i loopet og godkender hver beslutning. Han nævnte eksplicit at han hader at ikke forstå det der bruges tid på — "du ved ikke om det er bureaukrati eller det bedste siden sliced bread, og det gør det ikke nemmere når LLM'er har tendens til sagligt at begrunde overkomplicerede beslutninger."

Denne praksis bør overvejes igen ved fremtidige planlægnings- og beslutningsfaser.

### Dump-scriptet forbedret

`dump-chatlog.js` opgraderet:
- Auto-detect nyeste session (ingen hardcoded ID)
- Accepterer session-ID som argument for specifik session
- Sekvensnumre: T001, T002... (referencerbare)
- Timestamps per besked
- Session-ID i output
- Filnavne med dato + session-ID: `chatlog-2026-03-10-1f70d0bd.md`

---

## Session 2 — 2026-03-09 (rekonstrueret fra git-historik)

### Hvad vi ved skete (fra commits og PLAN.md)

- M3 blev afsluttet: Zsh + Oh My Zsh + Starship + plugins + aliases konfigureret i WSL
- PLAN.md v2 designet og implementeret med Popper-loop, done-kriterier, idé-parkering, scope-grænse
- PLAN.v1.md arkiveret (omdøbt)
- references/automation.md, terminal.md, vscode.md oprettet
- M4 research påbegyndt: scannede mcpmarket.com top 100 MCPs, parkerede idéer (PDF toolkit, webscraping, MCP kompendium, abonnement-overblik)
- ~/dev/ oprettet med projects/, archive/, sandbox/, tools/
- Mapper skulle flyttes manuelt (Basic Setup → dev/projects/, Old stuff → dev/archive/)
- Poppler installeret for PDF-support
- Research om GSD, RPI, PRD-first, Yttres AI-biografi

### Hvad der gik tabt

Selve mappestruktur-researchen fra session 2 blev aldrig gemt som reference-fil. Commit `1aa8eba` viser at idéer blev tilføjet til PLAN.md's idé-parkering, men det egentlige research-indhold (hvad professionelle gør) var kun i chatten. NOW.md blev ikke opdateret med session-state. Det er præcis det problem session 3 brugte tid på at løse.

---

## Session 1 — 2026-03-08 og tidligere (fra session-history.md + git)

### Den lange rejse

Basic Setup startede som et projekt for at dokumentere og lære de fundamentale opsætninger professionelle udviklere tager for givet. Yttre har ingen formel uddannelse — han er selvlært via intens egeninteresse, startende med ChatGPT i september 2024, eksploderende med Grok i november 2025, og landende på Claude Code i januar 2026.

Projektet har gennemført:
- **M0:** Grundlæggende PC-setup (implicit)
- **M1:** Git — SSH-nøgler, Windows git, commit+push workflow
- **M2:** VS Code — extensions, keybindings, settings, workspace
- **M3:** Terminal/Shell — WSL, Zsh, Oh My Zsh, Starship, plugins, aliases

Alt er dokumenteret i PLAN.v1.md med detaljerede session-noter.

### Kontekst om Yttre

- Kristoffer, 36, chauffør rute 256 (organisk affald, Aarhus), 40% ejerskab i rejseselskab
- Bygger Yggdra — et personligt AI-system på VPS (Qdrant, hooks, 17 cron jobs, TransportIntra webapp)
- Tænker visuelt, arbejder med voice memos, perfektionistisk
- "Simpelt" betyder exact fit, aldrig discount
- Systemer over hukommelse — fejl løses ved at bygge systemer, aldrig ved at "huske bedre"
- Vil have det skal føles som én kontinuerlig samtale — som at tale med en person der husker alt

Den ambition er præcis det der gør session-management så vigtigt. Hver ny session der starter uden kontekst bryder illusionen.
