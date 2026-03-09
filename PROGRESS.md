# Progress — Basic Setup

Fortællende dagbog. Formålet er at en ny Claude-session kan læse dette og forstå *hvorfor* vi er hvor vi er, ikke bare *hvad* der er gjort. NOW.md er state, dette er kontekst.

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
