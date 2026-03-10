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
