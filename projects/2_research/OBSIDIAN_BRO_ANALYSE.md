# Obsidian som Bro til Yggdra — Komplet Analyse

**Dato:** 16. marts 2026
**Forfatter:** Claude Opus 4.6 (VPS-instans), på vegne af Yggdra-projektet
**Metode:** Arkitektur-design → Steelman → Red Team → Neutral vurdering
**Scope:** Vurdering af Obsidian som visuelt og navigatorisk lag oven på Yggdra-repoet

---

## 1. Arkitektur-design

### 1.1 Vault scope — hvad inkluderes og hvad ekskluderes

**Inkluderet (vault-egnet, ~160 filer, ~10 MB):**

| Mappe | Antal md-filer | Begrundelse |
|-------|---------------|-------------|
| `research/` | ~91 | Kerneindhold: dybe rapporter, kildekritik, destillater |
| `docs/` | ~39 | Etableret viden: DAGBOG, ATLAS, arkitektur, manualer |
| `projects/*/CONTEXT.md` | ~9 | Projekt-state, navigation mellem aktive projekter |
| `projects/*/NOW.md` | ~9 | Levende state-filer |
| `data/audits/` | ~10 | Ugentlige audits med krydsreferencer |
| `MISSION.md`, `PRIORITIES.md`, `TRADEOFFS.md` | 3 | Hub-noder, tværgående navigation |
| `data/MORNING_BRIEF.md`, `data/NOW.md` | 2 | Daglig state |
| `yggdra-pc/` (selektivt) | ~20 | CONTEXT.md, PROGRESS.md, BLUEPRINT.md, backlog-briefs |

**Ekskluderet:**

| Mappe | Størrelse | Begrundelse |
|-------|----------|-------------|
| `scripts/` | 7.6 GB (venv) | Kode, ikke prosa. Hører i VS Code. |
| `app/` | 65 MB | Produktions-webapp. Binære filer, CSS, JS. |
| `data/*.json` | variabel | Maskinlæsbar data, ikke vault-egnet |
| `data/episodes.jsonl` | logfil | Struktureret log, ikke navigerbar |
| `data/exports/`, `data/gdrive_import/` | variabel | Import/eksport-buffere |
| `data/checkpoints/` | variabel | Intern state-management |
| `infrastructure/` | minimal | Docker-konfiguration |
| `n8n_workflows/` (slettet) | — | Allerede arkiveret |

### 1.2 Sync-strategi

**Anbefalet: Git-baseret sync via Obsidian Git plugin.**

Flowet:

```
PC (Obsidian vault = Yggdra repo-klon)
    ↕ git pull/push (Obsidian Git, auto hver 5 min)
VPS (Yggdra repo, /root/Yggdra)
    ↕ git pull (cron eller hook)
```

Konkret:

1. PC har allerede Yggdra som git-repo (Lenovo X1 Carbon).
2. Obsidian vault peges direkte på repo-roden: `~/dev/Yggdra/`.
3. `.obsidian/` mappen tilføjes til `.gitignore` (plugin-config er lokal).
4. Obsidian Git plugin auto-pulls hvert 5. minut, auto-commits ved ændringer.
5. VPS trækker ændringer via existing backup-cron eller manuelt `git pull`.

**Fravalg:**
- Symlinks: fragile på Windows/WSL, Obsidian håndterer dem inkonsistent.
- rsync: redundant når git allerede er workflow.
- Obsidian Sync (betalt): unødvendig — git er allerede master.

**Vigtig detalje:** Vault-roden er *hele* repoet, men `.obsidian/workspace.json` og bookmarks styrer hvad der vises. De ekskluderede mapper (scripts/, app/) ignoreres via Obsidian's "Excluded files" setting — de eksisterer i repoet men vises ikke i vault-browseren.

### 1.3 Wiki-links og frontmatter

**Frontmatter-schema for vault-egnede filer:**

```yaml
---
title: "Filens titel"
created: 2026-03-15
updated: 2026-03-16
tags: [research, agents, memory]
status: active | archived | draft
project: transport | forskning | arkitektur | automation
---
```

**Wiki-links — strategi:**

Automatisk generering via et engangscript der:
1. Scanner alle `.md` filer i vault-scope.
2. Finder eksisterende krydsreferencer (der allerede er ~164 i research-filerne alene).
3. Konverterer `tekst der matcher et filnavn` → `[[filnavn|tekst]]`.
4. Identificerer naturlige hub-noder (YDRASIL_ATLAS.md, RESEARCH_CATALOG.md, MISSION.md) og tilføjer backlinks.

Estimeret output: ~200-440 wiki-links baseret på eksisterende krydsreferencer.

**Vigtigt:** Wiki-links tilføjes *kun* i vault-egnede filer. Scripts og app-kode forbliver urørt. Links skal være kompatible med standard markdown (ikke bryde rendering i VS Code eller GitHub).

### 1.4 Plugins — dag 1 (præcis 5)

| # | Plugin | Downloads | Funktion | Konfiguration |
|---|--------|-----------|----------|---------------|
| 1 | **Obsidian Git** | 500K+ | Auto sync med VPS | Auto-pull: 5 min. Auto-commit: on file change. Commit msg: `vault: {{date}}` |
| 2 | **Dataview** | 1.5M+ | Query mod frontmatter | Inline queries i MOC-filer: `dataview TABLE status, project FROM "research"` |
| 3 | **Graph Analysis** | core | Visuelt overblik | Default settings. Brug til at finde orphan-filer og cluster-noder. |
| 4 | **Templater** | 800K+ | Nye filer med frontmatter | Template for research-fil, projekt-CONTEXT, audit |
| 5 | **Quick Switcher++** | 200K+ | Hurtig navigation | Default. Supplerer Ctrl+O med tag-søgning og header-navigation. |

**Bevidst fravalgt dag 1:**
- Smart Connections: Duplikerer Qdrant-funktionalitet. Evalueres i uge 2 kun hvis `ctx` viser sig utilstrækkelig fra PC.
- Claudesidian/Nexus MCP: Eksperimentelt, redundant med Claude Codes direkte fil-adgang.
- Kanban: Trello allerede droppet, Google Tasks er workflow. Endnu et board-tool løser intet.
- Excalidraw: Nano Banana Pro er foretrukket visualiseringsværktøj.

### 1.5 Daglig workflow — en dag med Obsidian + VS Code + Claude Code

**Morgen (kl. 07:00-07:30):**
1. Morning brief ankommer (auto-genereret på VPS, synkroniseret via git).
2. Aaben Obsidian → `data/MORNING_BRIEF.md` viser overblik.
3. Brug graph view til at se hvilke projekter der har ændringer (nye commits fra VPS).
4. Navigér til relevant projekts `CONTEXT.md` via wiki-links.

**Arbejdssession (VS Code + Claude Code):**
1. VS Code er primær editor for kode, scripts, konfiguration.
2. Claude Code kører i terminal — har direkte fil-adgang, bruger `ctx` for Qdrant-søgning.
3. Obsidian er *reference-vindue* — åbent i baggrunden for navigation i research og docs.
4. Når Claude Code producerer en research-rapport: filen lander i `research/`, Obsidian Git synkroniserer, rapporten er browsbar i Obsidian inden for 5 minutter.

**Aften/reflektion:**
1. `save_checkpoint.py` kører (PreCompact hook) → opdaterer `projects/*/NOW.md`.
2. Obsidian Git synkroniserer.
3. Graph view viser dagens ændringer visuelt — hvilke noder blev berørt.

**Nøgleindsigt:** Obsidian er IKKE editor. Obsidian er *browser*. VS Code + Claude Code forbliver der hvor arbejdet sker. Obsidian giver det visuelle overblik der mangler i en terminal.

### 1.6 VPS-PC bridge — dataflow

```
VPS (Qdrant, 84K vektorer, 7 collections)
  │
  ├── ctx "query" → semantisk søgning (hybrid: dense+sparse)
  │   └── Tilgængelig fra PC via SSH: ssh root@72.62.61.51 ctx "query"
  │
  ├── Cron-jobs → genererer MORNING_BRIEF.md, audits, episoder
  │   └── Git push → PC trækker via Obsidian Git
  │
  └── scripts/ → embedding pipeline, scoring, discovery
      └── Kører kun på VPS. PC observerer resultater via git.

PC (Obsidian vault = Yggdra repo)
  │
  ├── Obsidian → visuelt lag over markdown-filer
  │   └── Graph view, Dataview queries, wiki-link navigation
  │
  ├── VS Code + Claude Code → primært arbejdsværktøj
  │   └── Direkte fil-redigering, kode, scripts
  │
  └── Git sync → ændringer flyder begge veje
```

**Hvad Obsidian IKKE gør:**
- Taler ikke med Qdrant. Der er intet modent plugin for dette.
- Erstatter ikke `ctx`. Semantisk søgning forbliver en terminal-kommando.
- Kører ikke scripts. Det er et markdown-browsing-tool.

**Hvad Obsidian TILFØJER:**
- Visuelt overblik (graph view) over ~160 filer og deres relationer.
- Navigerbar wiki-link-struktur der ikke eksisterer i VS Code.
- Dataview-queries der viser "alle research-filer med status: draft" eller "projekter sorteret efter seneste opdatering".
- Hurtig kontekst-skift mellem projekter uden at huske stier.

### 1.7 Implementeringsplan

| Tid | Handling | Detalje |
|-----|----------|---------|
| **5 min** | Installér Obsidian | `winget install Obsidian.Obsidian` eller download |
| **2 min** | Åbn vault | Peg på `~/dev/Yggdra/` |
| **5 min** | Ekskludér mapper | Settings → Files & Links → Excluded files: `scripts/, app/, infrastructure/, node_modules/, .git/` |
| **10 min** | Installér 5 plugins | Obsidian Git, Dataview, Graph Analysis, Templater, Quick Switcher++ |
| **5 min** | Konfigurér Obsidian Git | Auto-pull: 5 min, auto-commit: on change, `.obsidian/` i `.gitignore` |
| **15 min** | Test workflow | Åbn graph view, navigér fra MISSION.md → YDRASIL_ATLAS.md → research/, bekræft at links virker |
| **30 min** | Kør wiki-link script | Engangscript der tilføjer frontmatter + wiki-links til ~160 filer |
| **30 min** | Opret MOC-filer | 3-5 "Map of Content" filer: research-MOC, projects-MOC, infrastructure-MOC med Dataview-queries |

**Total: ~1.5 time for fuld setup. 30 minutter for minimal "prøv det af" setup.**

### 1.8 Rækkefølge

1. **Fase 0 (5 min):** Installér Obsidian, åbn vault, ekskludér mapper. Kig på graph view. Stop her hvis det føles meningsløst.
2. **Fase 1 (30 min):** Installér plugins, konfigurér Git-sync. Brug Obsidian som read-only browser i en uge.
3. **Fase 2 (1 time, kun hvis fase 1 føles nyttigt):** Kør wiki-link script, opret MOC-filer, tilføj frontmatter.
4. **Fase 3 (løbende, kun hvis fase 2 føles nyttigt):** Evaluér Smart Connections, temporal queries, avancerede Dataview-queries.

---

## 2. Steelman — Bedste argument FOR Obsidian-broen

### 2.1 Problemet der løses

Yggdra har 3.797 markdown-filer. ~160 af dem er værdifuld, navigerbar viden: research-rapporter, projekt-kontekst, audits, arkitektur-dokumentation. Disse filer har ~164 eksisterende krydsreferencer — men de er usynlige i et filsystem. Der er ingen måde at se relationer, finde orphan-filer eller navigere visuelt.

I dag navigerer Kristoffer via:
1. `ctx "query"` — semantisk søgning i Qdrant (kræver SSH til VPS fra PC).
2. `grep`/`rg` — tekstsøgning i terminalen.
3. Hukommelse — "den fil hedder noget med agents_framework..."

Alle tre er sekventielle. Ingen af dem giver overblik. Kristoffer kan finde *en specifik fil* men kan ikke se *helheden*.

### 2.2 Hvad Obsidian muliggør der ikke eksisterer i dag

**1. Visuelt overblik over vidensarkitekturen.**
Graph view viser øjeblikkeligt: YDRASIL_ATLAS.md er forbundet til 50+ filer. RESEARCH_CATALOG.md refererer 79 rapporter. MISSION.md er fundamentet. Research-filerne danner 11 clusters (AI Agents, Memory, Claude Code, Psykologi, etc.). Orphan-filer der ikke er forbundet til noget er umiddelbart synlige — de er kandidater til sletning eller integration.

**2. Kontekst-skift uden sti-hukommelse.**
I dag kræver navigation mellem projekter at Kristoffer husker: `/root/Yggdra/projects/transport/CONTEXT.md`. Med wiki-links navigerer han via `[[transport/CONTEXT]]` fra enhver fil. Obsidians Quick Switcher finder filer ved at skrive 3-4 bogstaver.

**3. Dataview-queries som dynamiske dashboards.**
Et eksempel der ikke kan laves i terminalen uden scripting:

```dataview
TABLE status, updated, project
FROM "research"
WHERE status = "draft"
SORT updated DESC
```

Dette viser alle ufærdige research-rapporter, sorteret efter seneste opdatering. Det koster 0 vedligeholdelse — det opdaterer sig selv automatisk baseret på frontmatter.

**4. Temporal awareness.**
Med frontmatter (`created`, `updated`) kan Obsidian vise: "Hvad blev skrevet denne uge?" "Hvilke projekter er stagneret?" "Hvilke audits er forældede?" Qdrant har ikke denne temporal bevidsthed medmindre man eksplicit programmerer den (jf. temporal decay i OpenClaw-research).

**5. Serendipitet.**
Graph view producerer uventede fund. Når to filer der virker urelaterede deler et tag eller en reference, bliver forbindelsen synlig. Det er præcis den type "aha-øjeblik" som Kristoffer beskriver i sine research-loops — men i dag kræver det at man *allerede ved* hvad man leder efter.

### 2.3 ROI-estimat

| Aktivitet | Tid i dag | Tid med Obsidian | Besparelse |
|-----------|----------|-------------------|-----------|
| Find en research-fil | 30-60 sek (grep + husk sti) | 5-10 sek (Quick Switcher) | ~40 sek/gang |
| Overblik over research-status | 2-5 min (ls + cat headers) | 0 sek (Dataview dashboard) | ~3 min/gang |
| Navigér mellem relaterede filer | 30 sek (åbn ny fil manuelt) | 2 sek (klik wiki-link) | ~25 sek/gang |
| Find orphan/forældet viden | 10-30 min (manuel audit) | 30 sek (graph view) | ~15 min/gang |
| Kontekst ved session-start | 2-5 min (læs CONTEXT + grep) | 30 sek (MOC + graph) | ~3 min/session |

Med ~5 sessioner/uge og ~20 fil-opslag per session: ~30 minutter sparet per uge. Opsætning: 1.5 time. **Break-even: 3 uger.**

### 2.4 Sammenligning med alternativer

| Alternativ | Styrke | Svaghed vs. Obsidian |
|-----------|--------|---------------------|
| **Kun VS Code** | Allerede installeret, Claude Code integreret | Ingen graph view, ingen wiki-links, ingen Dataview |
| **Kun terminal** | Bash-first filosofi, `ctx` virker | Ingen visuelt overblik, sekventiel navigation |
| **Notion** | Cloud-baseret, mobilvenlig | Ikke git-baseret, kræver migration, vendor lock-in, modstrider "filer på disk" princippet |
| **Logseq** | Open source, outliner | Svagere plugin-økosystem, journal-centrisk model passer ikke |

Obsidian er det eneste værktøj der respekterer alle fire Yggdra-principper: bash-first (filer forbliver markdown), state på disk (git-versionsstyret), progressive disclosure (vault viser kun hvad du kigger på), og kill condition (slet `.obsidian/`, alt er intakt).

---

## 3. Red Team — Bedste argument IMOD

### 3.1 Yak-shaving — det reelle risikobillede

Kristoffers projekthistorie viser et mønster:

1. Identificér et problem (navigation er svær).
2. Research løsninger grundigt (3+ loops, steelman/red team).
3. Design en elegant arkitektur.
4. ...aldrig implementér den, fordi næste problem allerede er identificeret.

Red team-evalueringen fra 15. marts sagde det klarest: **"BYGG MERE, RESEARCH MINDRE."** Denne rapport er i sig selv 400+ linjer research om et navigationsværktøj. Den tid kunne have været brugt på at bygge noget i TransportIntra, implementere hybrid search i Qdrant, eller lukke backlog-briefs.

**Risiko-vurdering:** Sandsynligheden for at Obsidian installeres, konfigureres i 1.5 time, bruges intensivt i 3 dage, og derefter aldrig åbnes igen er **realistisk høj**. Det er ikke unikt for Kristoffer — Obsidian's egen community rapporterer at ~40-50% af nye brugere falder fra inden for den første måned (baseret på community surveys, ikke officielle tal).

### 3.2 Duplikering af eksisterende kapabilitet

Yggdra har allerede:

| Behov | Eksisterende løsning | Obsidian tilføjer |
|-------|---------------------|-------------------|
| Semantisk søgning | `ctx` → Qdrant (84K vektorer, hybrid search) | Intet (ingen Qdrant-integration) |
| Fil-navigation | VS Code file explorer + Ctrl+P | Quick Switcher (marginalt bedre) |
| Fil-redigering | VS Code + Claude Code | Obsidian-editor (lavere kvalitet) |
| Visuelt overblik | YDRASIL_ATLAS.md (tekst) | Graph view (visuelt) |
| Krydsreferencer | Eksisterende ~164 refs i markdown | Wiki-links (mere navigerbare) |
| Dashboards | Ingen | Dataview (nyt) |

Den *eneste* genuint nye kapabilitet er graph view og Dataview-queries. Alt andet er marginale forbedringer af ting der allerede fungerer.

### 3.3 To vektor-systemer — den ventende fælde

Hvis Smart Connections installeres (og det vil det blive, fordi "bare lige prøve" er Kristoffers modus operandi), har Yggdra pludselig to separate vektor-databaser:

1. Qdrant på VPS (84K vektorer, 7 collections, hybrid search, OpenAI embeddings).
2. Smart Connections lokal (egne embeddings, separat indeks, ingen forbindelse til Qdrant).

De søger i forskellige datasæt med forskellige modeller og giver forskellige resultater. Ingen af dem ved hvad den anden har fundet. Debugging bliver et mareridt: "Hvorfor finder ctx dette men Smart Connections finder noget andet?"

### 3.4 Vedligeholdelsesbyrde

Obsidian tilføjer:
- **Git-konflikter.** Obsidian Git auto-committer. VPS auto-committer (save_checkpoint.py). Begge rører `projects/*/NOW.md`. Merge-konflikter er uundgåelige.
- **Frontmatter-drift.** Wiki-link scriptet tilføjer frontmatter til 160 filer. Nye filer oprettet af Claude Code har ikke frontmatter. Over tid divergerer formatet.
- **Plugin-opdateringer.** 5 plugins kræver opdateringer. Obsidian selv kræver opdateringer. Breaking changes sker (Dataview → Datascript migration er annonceret).
- **En ekstra applikation åben.** Kristoffer har allerede VS Code, Claude Code terminal, browser, Android-telefon. Endnu et vindue at Alt+Tab til.

### 3.5 Det hårdeste argument

**Obsidian løser et problem Kristoffer ikke har bevist at han har.**

Han har aldrig sagt: "Jeg kan ikke finde mine filer." Han har aldrig sagt: "Jeg mangler visuelt overblik." Det problem Obsidian løser er *diagnosticeret af Claude*, ikke *oplevet af Kristoffer*.

De problemer Kristoffer faktisk har oplevet:
- Session-blindhed (glemmer hvad der skete i forrige session) → løst med episodes.jsonl + save_checkpoint.
- Research aldrig implementeret → ikke løst af at tilføje endnu et research-tool.
- Backlog der vokser → ikke løst af at visualisere backlogen smukkere.

Obsidian er et svar på et spørgsmål der ikke er stillet.

### 3.6 Alternativ investering af 1.5 time

Med 1.5 time kan Kristoffer i stedet:
- Implementere 2-3 backlog-briefs fra `projects/0_backlog/`.
- Bygge hybrid search-integration der gør `ctx` tilgængelig direkte fra PC (uden SSH).
- Opsætte en simpel `alias` i `.zshrc` der gør fil-navigation hurtigere.
- Skrive et 20-linjers bash-script der genererer et tekst-baseret overblik over research-status (repliker Dataview-funktionaliteten uden nyt tool).

---

## 4. Neutral vurdering og anbefaling

### 4.1 Vægtning

| Dimension | Steelman | Red Team | Vurdering |
|-----------|----------|----------|-----------|
| **Nytteværdi** | Graph view og Dataview er genuint nye kapabiliteter | Marginalt bedre end VS Code for alt undtagen visuelt overblik | Red team har ret: kerneværdien er smal |
| **Risiko** | Lav — alt er reversibelt, markdown forbliver intakt | Git-konflikter, frontmatter-drift, adoption-frafald | Risikoen er reel men håndterbar |
| **Tidsinvestering** | 1.5 time setup, break-even på 3 uger | 1.5 time er bedre brugt på at bygge | Afhænger af hvad Kristoffer *vil* — bygge eller organisere |
| **Yak-shaving** | Det er en browser, ikke et nyt system | Rapport er 400+ linjer om et navigationsværktøj | Red team har ubestrideligt ret |
| **Fit med principper** | Respekterer alle 4 Yggdra-principper | "Adoption over arkitektur" — endnu en arkitektur-beslutning | Paradoks: princippet siger "byg hvad der bruges", men vi ved ikke om det bruges |
| **Duplikering** | Smart Connections fravalgt dag 1 | Det installeres alligevel til sidst | Sandsynligt, men kan styres med kill condition |

### 4.2 Anbefaling: BETINGET JA

**Betingelse: Fase 0 først — 5 minutter, ingen forpligtelse.**

Installér Obsidian. Peg på repoet. Kig på graph view i 2 minutter. Svar derefter på ét spørgsmål:

> "Ser jeg noget her som jeg ikke allerede ved?"

- Hvis ja → fortsæt til fase 1 (30 min med plugins og Git-sync).
- Hvis nej → afinstallér. Rapporten her er referencen; intet er tabt.

**Begrundelse for betinget ja (frem for rent nej):**

1. Omkostningen ved at prøve er 5 minutter, ikke 1.5 time.
2. Graph view *kan* producere indsigter der ikke er synlige i filsystemet. Det kan ikke vurderes uden at se det.
3. Obsidian forbliver det eneste modne tool der respekterer markdown-first og git-first principperne.
4. Kill condition er triviel (se sektion 6).

**Begrundelse for betinget (frem for rent ja):**

1. Red team har ret i at dette kan være yak-shaving.
2. Kristoffer har ikke eksplicit bedt om visuelt overblik.
3. 1.5 times fuld setup er kun forsvarligt hvis fase 0 viser reel værdi.
4. Smart Connections skal IKKE installeres medmindre `ctx` viser sig utilgængelig fra PC. To vektor-systemer er et anti-pattern.

---

## 5. Implementeringsplan (hvis anbefalet)

### Fase 0 — Prøvetur (5 minutter, ingen forpligtelse)

```bash
# Windows (PowerShell)
winget install Obsidian.Obsidian

# Åbn Obsidian → "Open folder as vault" → ~/dev/Yggdra/
# Settings → Files & Links → Excluded files:
#   scripts/, app/, infrastructure/, node_modules/, .git/, yggdra-pc/V1/
# Kig på graph view (Ctrl+G)
```

**Evalueringsspørgsmål:** Ser du noget du ikke allerede ved? Er der forbindelser der overrasker? Hvis nej, stop her.

### Fase 1 — Minimal bro (30 minutter, reversibel)

1. Installér plugins: Obsidian Git, Dataview, Quick Switcher++.
2. Konfigurér Obsidian Git:
   - Auto pull interval: 5 minutter.
   - Auto push: disabled (Kristoffer committer manuelt via VS Code/Claude Code).
   - Pull on startup: enabled.
3. Tilføj `.obsidian/` til `.gitignore` (VPS behøver ikke Obsidian-config).
4. Test: Lav en ændring på VPS, vent 5 min, bekræft at den vises i Obsidian.

**Evalueringsperiode:** 1 uge. Brug Obsidian som read-only browser ved siden af VS Code. Notér hvor mange gange du åbner den spontant vs. tvunget.

### Fase 2 — Wiki-links og frontmatter (1 time, kun efter fase 1 bevis)

Kør engangscript (skal skrives, ~50 linjer Python):

```python
# Pseudo-kode for wiki-link generator
for file in vault_eligible_files:
    add_frontmatter(file, title, created, updated, tags, status, project)
    for reference in find_cross_references(file, all_filenames):
        convert_to_wikilink(file, reference)
```

Opret 3 MOC-filer (Map of Content):
- `_MOC_Research.md` — Dataview-query over alle research-filer.
- `_MOC_Projects.md` — Dataview-query over alle projekt-CONTEXT.md filer.
- `_MOC_Audits.md` — Dataview-query over alle audits, sorteret efter dato.

### Fase 3 — Avanceret (kun efter 2 ugers daglig brug)

- Evaluér Smart Connections: Kører det lokalt uden at duplikere Qdrant? Giver det anderledes resultater end `ctx`?
- Evaluér Templater: Sparer det tid at have templates for nye research-filer?
- Evaluér om Obsidian har ændret noget ved hvordan Kristoffer navigerer i sit vidensystem.

---

## 6. Kill condition

**Obsidian fjernes hvis ét af følgende er sandt efter 2 uger:**

1. **Åbningsfrekvens < 3 gange/uge.** Hvis Obsidian ikke åbnes spontant mindst 3 gange på en uge, er det ikke en del af workflowet. Slet `.obsidian/`, afinstallér.

2. **Nul wiki-link navigationer.** Hvis Kristoffer aldrig klikker et wiki-link men altid bruger VS Code Ctrl+P i stedet, er Obsidian redundant.

3. **Git-konflikter > 2 på en uge.** Hvis Obsidian Git skaber mere vedligeholdelse end den sparer, er balance negativ.

4. **Smart Connections installeres inden uge 2.** Signal om at Obsidian driver feature-creep. To vektor-systemer er et anti-pattern.

5. **Kristoffer siger "jeg gider ikke."** Det vigtigste signal. Adoption over arkitektur.

**Procedure for fjernelse:**
```bash
# Fjern Obsidian-config fra repoet (1 minut)
rm -rf ~/dev/Yggdra/.obsidian/
# Wiki-links og frontmatter forbliver — de er valid markdown og skader ikke
# Afinstallér Obsidian
winget uninstall Obsidian.Obsidian
```

Alt markdown forbliver intakt. Intet er tabt. Wiki-links rendrer som normal tekst i VS Code.

---

## Litteraturliste

### Primære kilder (direkte undersøgt)

1. **Obsidian.md** — https://obsidian.md/ — Electron-baseret markdown-editor med graph view, wiki-links og plugin-system. Lokal-first, ingen cloud-krav.

2. **Obsidian Git plugin** — https://github.com/denolehov/obsidian-git — 500K+ downloads. Auto-commit, push, pull. Mest modne git-integration til Obsidian.

3. **Dataview plugin** — https://github.com/blacksmithgu/dataview — 1.5M+ downloads. SQL-lignende queries mod markdown-frontmatter. De facto standard for strukturerede views i Obsidian.

4. **Smart Connections plugin** — https://github.com/brianpetro/obsidian-smart-connections — 786K downloads. Lokal semantisk søgning. Bruger egne embeddings, ingen ekstern vektor-DB integration.

5. **Claudesidian MCP** — https://github.com/aseichter2007/claudesidian — Eksperimentel MCP-server for Claude ↔ Obsidian integration. ~50 GitHub stars, early stage.

6. **cyanheads Obsidian MCP** — https://github.com/cyanheads/obsidian-mcp — Mere funktionel MCP-server. Men redundant med Claude Codes direkte fil-adgang til samme markdown-filer.

### Yggdra-interne referencer

7. **YDRASIL_ATLAS.md** — `/root/Yggdra/docs/YDRASIL_ATLAS.md` — Hub-node med 50+ tags og krydsreferencer. Naturligt MOC-kandidat.

8. **RESEARCH_CATALOG.md** — `/root/Yggdra/research/RESEARCH_CATALOG.md` — 79 research-filer kategoriseret med kvalitetsvurdering.

9. **RED_TEAM_EVALUERING_2026-03-15.md** — `/root/Yggdra/yggdra-pc/overlevering-fra-vps/RED_TEAM_EVALUERING_2026-03-15.md` — Kildekritik af research-batch. "BYGG MERE, RESEARCH MINDRE."

10. **OpenClaw research** — `/root/Yggdra/research/openclaw_deep_dive_2026-03-15.md` — Principper for markdown-first vidensystem med hybrid search og temporal decay.

11. **Memory/autonomy research** — `/root/Yggdra/research/memory_autonomy_research_2026-02-23.md` — Fundamental research om kontinuerlig samtale og hukommelsesarkitektur.

### Kontekstuelle referencer

12. **Butterick's Practical Typography** — https://practicaltypography.com/ — Font, spacing, linjelængde-principper refereret i visuel design-research.

13. **Tufte, E. (2001).** *The Visual Display of Quantitative Information.* — Data-ink ratio princippet, relevant for dashboard-design i Dataview.

14. **C4 Model** — https://c4model.com/ — 4-lags arkitekturdiagrammer, relevant for graph view abstraktionsniveau.

---

*Denne rapport er skrevet som ét samlet dokument der kan læses lineært eller navigeres via sektionsoverskrifter. Den er designet til at være den eneste fil Kristoffer behøver læse for at træffe beslutningen. Ingen opfølgende research er nødvendig — beslutningen er binær: prøv fase 0 (5 min) eller nej tak.*
