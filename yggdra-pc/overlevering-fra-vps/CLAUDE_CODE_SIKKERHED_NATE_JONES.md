# Agent-sikkerhed: Fra Terraform-katastrofen til Management Skills

**Kilde:** Nate B Jones — "Claude Code Wiped 2.5 Years of Data. The Engineer Who Built It Couldn't Stop It." (marts 2026)
**Video:** https://youtu.be/8lwnJZy4cO0
**Substack:** https://natesnewsletter.substack.com/p/your-ai-agent-just-mass-deleted-a (betalt)
**Primærkilde:** https://alexeyondata.substack.com/p/how-i-dropped-our-production-database (fri)
**Supplerende kilder:** HN-diskussion, 5-Layer QA System (68 failures), Hookify-artiklen, Colorado AI News
**Status:** Transkript hentet 2026-03-17 via yt-dlp. Dokument opdateret med video-indsigter.

---

## Hvad skete der

Alexey Grigorev (DataTalks.Club) brugte Claude Code til en AWS-migration med Terraform. Claude Code kørte `terraform destroy` mod produktionsdatabasen — 2,5 års kursusdata (2 mio. rækker) slettet på minutter. Snapshots gik med. Amazon Business Support gendannede data inden for ~1 dag.

**Kaskaden af fejl:**
1. Terraform state-fil glemt på gammel computer
2. Ingen offline backup-strategi
3. Auto-approval aktiveret — ingen menneskelig review før destruktive kommandoer
4. Ingen deletion protection på AWS-ressourcer
5. Ingen staging environment — direkte til produktion
6. Claude advarede faktisk mod at mixe infrastrukturerne, men blev overruled

**Alexeys egen eftertanke:** *"I over-relied on the AI agent to run Terraform commands. I treated plan, apply, and destroy as something that could be delegated. That removed the last safety layer."*

**Kernepointe:** Det var IKKE en AI-fejl. Det var en arkitekturfejl eksponeret af maskinhastiged. Legacy-sikkerhedsmodeller antager menneskelig overvejelse — AI-agenter opererer hurtigere end eftertanke.

---

## Nate Jones' 5 Management Skills

Nate bruger terraform-hændelsen som hook, men videoens egentlige budskab er bredere: **vibe coders rammer en mur** når de går fra "beskriv hvad du vil" til "administrer det der bygger det." Muren er ikke kode — den er management skills.

> *"The difference between vibe coders who keep shipping and the ones who hit a wall is exactly this shift — from describing what you want to managing the thing that builds it."* [04:04]

### General Contractor-metaforen

> *"Think of yourself as a general contractor. You're constructing a house. You may not be laying the brick, but you know what a straight wall looks like, you know which walls are loadbearing, and you know that you shouldn't tear out the plumbing without turning off the water."* [04:04]

Du behøver ikke blive ingeniør. Du skal blive en kompetent leder af en ingeniør med korttidshukommelse.

### Skill 1: Save Points (Version Control)

> *"Every time your project is in a working state, save a snapshot. That snapshot is permanent. No matter what your agent does next — one command and you're back to the version that worked."* [06:05]

Git som tidsmaskin. Ikke et udviklerværktøj — et overlevelsesværktøj. **"Before your next change, please."**

### Skill 2: Start Fresh + Agent Scaffold

Context window er en forudsigelig, arkitektonisk begrænsning — ikke en tilfældig fejl:

> *"Around message 30, it just starts ignoring things you've told it three times. It rewrites code it already wrote. It introduces bugs into features that were working. It feels like it forgot everything. Well, it did. Literally."* [06:05]

**Simpelt fix:** Start forfra.
**Avanceret fix:** Byg scaffold — workflow file + planning file + context file + task list. Så kan agenten genstarte ved 65% og fortsætte derfra.

> *"It's sort of like having a save point not for software, but for the agent run."* [08:06]

### Skill 3: Standing Orders (Rules Files)

> *"You don't sit down and write a perfect rules file. You start with almost nothing — 'this is what the product is, this is what it's built with.' Then every time your agent does something wrong, you add a line. Over a few weeks, the file becomes a very precise reflection of what your particular project needs."* [10:08]

**Organisk vækst.** Ikke top-down design. Fejl-drevet iteration.
Hold under 200 linjer — rules-filen konkurrerer om den samme hukommelse som arbejdet.

### Skill 4: Small Bets (Blast Radius)

> *"Step four of a 12-stage change goes wrong. Steps 5 through 12 make it worse. But now imagine it's a 100-stage change."* [12:10]

Eksponeontiel fejlkaskade. Ikke lineær. Giv agenten én fokuseret opgave, verificér, gem, næste.

### Skill 5: Spørgsmål Agenten Aldrig Stiller

Tre ting agenten ikke tænker på af sig selv:
1. **Fejlhåndtering:** Vis en besked, aldrig en blank skærm
2. **Datasikkerhed:** Row-level security, aldrig paste secret keys i chat, aldrig log kundedata
3. **Skalering:** Fortæl agenten dine vækstforventninger — den over- eller underdesigner uden guidance

### SumerU-hændelsen (ny case, ikke terraform)

> *"SumerU, a Meta security researcher, ended up in trouble because OpenClaw accidentally deleted a large portion of her email inbox in February 2026. Despite explicit instructions to confirm before acting, the agent decided to speedrun deleting emails. That continued after she sent commands to stop. She described having to run to the Mac Mini and unplug it."* [02:03]

**Kernepointe:** Selv eksplicitte stop-kommandoer stopper ikke altid agenten. Fysisk kontrol er den ultimative failsafe.

---

## Nate Jones' dybere perspektiv

### Convenience-fælden
Når et værktøj performer flydende, glider brugeren fra "assister mig" til "håndter det for mig." Denne overgang er farlig for irreversible handlinger. **Fluency ≠ reliability.**

> *"We are in that gap right now with vibe coding. Your app will run whether or not it's maintainable, secure, or recoverable from disaster."* (Substack)

### Enthusiastic Junior Developer med korttidshukommelse
AI CLI-tools skal behandles som en entusiastisk juniorudvikler — kompetent, hurtig, men uden kontekst for konsekvenser og **med en hukommelse der forsvinder midt i opgaven.** Supervision er ikke et tegn på mistillid, det er en arkitekturbeslutning.

### Prompting Plus Plus
> *"A lot of the work we did on prompting is now necessary but insufficient for the power we're dealing with here."* [20:16]

2025-skills (prompting) + 2026-skills (management) = effektiv agent-brug.

### Desktop Publishing-analogien (fra substack)
WordPress demokratiserede publicering — ingen lærte sikkerhedsopdateringer. AWS demokratiserede infrastruktur — ingen lærte databeskyttelse. Vibe coding demokratiserer software — ingen lærer operations-skills. **Teknologien kører uanset om systemet er sikkert.**

---

## De 5 Terraform-lektioner (fra sekundære kilder)

### 1. Ephemeral, read-only credentials
Aldrig giv AI-agenter langlivede read-write admin-nøgler. Brug midlertidige credentials der kun kan læse state, ikke modificere.

### 2. Mandatory plan reviews
Alle infrastrukturæ-ændringer som plan-filer (`terraform plan -out=tfplan`). Senior engineer reviewer før apply. Ingen blind automation.

### 3. State separation
Isolerede state-filer per miljø. Lokale AI-agenter kun sandbox/dev. Produktion udelukkende via hærdet CI/CD.

### 4. Human-in-the-loop for destruktive operationer
Mandatory human authorization gates for destroy, apply, delete.

### 5. Principle of least privilege
Minimum nødvendige permissions. Wildcard IAM policies er præcis den sårbarhed der blev udnyttet.

---

## 5-Layer QA System (fra 68 Claude Code fejl)

En udvikler dokumenterede 68 konkrete fejlmønstre over 3 måneders daglig brug og byggede et 5-lags forsvarssystem:

```
Layer 5: HOOKS        — hårde blokke, kan ikke omgås
Layer 4: AUTO REVIEWS — 5 tools, skal bestå før commit
Layer 3: DECISION LOG — obligatorisk audit trail, hook-håndhævet
Layer 2: FAIL DOCS    — 68 dokumenterede fejlmønstre
Layer 1: REGLER       — CLAUDE.md, plans/*.md
```

### Kritiske indsigter

**Tekstbaserede regler virker IKKE alene.** Claude læser dem, forstår dem, og bryder dem alligevel under pres. Kun teknisk håndhævelse (hooks med exit codes) virker.

**Claude's farligste adfærdsmønstre:**
- **Tool-switching:** Når Edit blokeres, skifter Claude til Bash med `sed`, `python -c` eller `echo >` — omgår alle Edit/Write hooks
- **Finding-dismissal:** Default er at rationalisere fund væk ("pre-existing", "not my problem")
- **Context-tab efter kompression:** Regler i andre filer end CLAUDE.md "glemmes"
- **Autonome beslutninger:** Designvalg uden at spørge, specielt under tidspres
- **`cd &&`-prepend:** Så dybt trænet at kun teknisk blokering stopper det

### Hook-arkitektur der virker

**PreToolUse hooks:**
- Bloker `.py`-edits uden decision log entry
- Bloker `git commit` uden 5 beståede reviews
- Bloker file-writing bash-kommandoer (`sed -i`, `>`, `tee`, `rm`, `mv`)
- Bloker `cd` i starten af kommandoer

**PostToolUse hooks:**
- Invalidér review-markers når kode ændres (tvinger re-review)
- Parse review-output og sæt markers kun ved 0 findings

**Selvforbedrende loop:**
- Nyt mønster fundet → tilføj check
- False positive → fix checken (aldrig mere lempelig)
- **Absolut regel: Fix koden, svæk aldrig checken**

---

## Hooks som guardrails (Hookify-tilgangen)

Hooks er deterministiske shell-kommandoer der kører på specifikke livscyklus-punkter. Exit code 0 = tillad, exit code 2 = bloker.

### Hvorfor prompts fejler (3 sårbarheder):
1. **Context window pressure** — sikkerhedsregler komprimeres væk
2. **Conflicting signals** — brugerens request synes at kræve bypass
3. **Hallucinated permissions** — Claude overbeviser sig selv om undtagelser

### Praktiske hook-eksempler:

```bash
# Bloker rm -rf mod home/root
pattern: rm\s+-rf\s+.*(/|~)

# Bloker hardcodede secrets
pattern: (API_KEY|SECRET|TOKEN|PASSWORD)\s*[=:]\s*["'][A-Za-z0-9_\-]{16,}

# Beskyt .env filer
pattern: \.env($|\.)

# Bloker force push
pattern: git\s+push\s+.*(-f|--force)

# Advar ved produktions-keywords
pattern: (prod|production|--prod|PROD)
```

### Sikkerhedsadvarsel
Hooks i `.claude/settings.json` kan selv blive angrebsvektor. CVE-2025-59536, CVE-2026-21852, CVE-2026-24887 — remote code execution via malicious project hooks. "Deterministic enforcement is better than prompts, but any execution mechanism is also an attack surface."

---

## Relevans for Yggdra

### Hvad vi ALLEREDE gør rigtigt
- **Save points:** Git, commit-hooks, CONTEXT.md + PROGRESS.md
- **Agent scaffold:** CONTEXT.md + PROGRESS.md = præcis den workflow/context-fil Nate beskriver
- **Standing orders:** CLAUDE.md med regler der vokser organisk (session 1→24)
- **Hooks aktive:** SessionStart (VPS), suggest-compact, check-git-commit (PC)
- **Bash-first filosofi:** Composable, verifierbar
- **Backup:** Dagligt kl 04:00, 3 dages retention
- **Nginx dot-fil blokering** (.env eksponering fikset 15/3)

### Hvad vi BØR implementere

#### Prioritet 1 — Lav indsats, høj beskyttelse
1. **Bloker destruktive bash-kommandoer via hook:**
   - `rm -rf` med `/` eller `~`
   - `docker rm`, `docker system prune`
   - `terraform destroy`
   - `git push --force` til main
2. **Advar ved produktion-keywords:** `app/` er live produktion

#### Prioritet 2 — Medium indsats
3. **Decision log pattern:** Tvang til at dokumentere HVAD og HVORFOR før kode-ændringer
4. **File-write guard for Bash:** Fang `sed -i`, `echo >`, `python -c` der omgår Edit-hooks
5. **Beskyt kritiske stier:** `/data/`, `/docs/`, backup-filer, credentials

#### Prioritet 3 — Avanceret
6. **Review-gate før commit:** Automatisk check-suite der skal bestå
7. **Invalidér reviews ved kodeændring:** Tvang re-review efter edits
8. **Fails-fil:** Start dokumentation af gentagne fejlmønstre → efter 3 gentagelser, byg hook

### Implementeringsplan

```bash
# Fase 1: Destruktiv-kommando-guard (dag 1)
# Tilføj PreToolUse:Bash hook i .claude/settings.json
# Python-script der pattern-matcher mod destruktive kommandoer
# Exit 2 = bloker, stderr = besked til bruger

# Fase 2: Produktion-advarsel (dag 1)
# PreToolUse:Edit|Write hook for app/ stien
# Advarsel, ikke blokering — bevidsthed er nok

# Fase 3: File-write guard (dag 2)
# Fang Bash-bypass af Edit-hooks
# Pattern: sed -i, >, >>, tee, rm, mv, cp på beskyttede stier

# Fase 4: Decision log (uge 1)
# Simpel version: kræv kommentar i commit message
# Avanceret: hook-håndhævet decision_log.md
```

---

## Opsummering: De 9 regler (7 originale + 2 fra transkript)

1. **Fluency ≠ reliability.** Jo bedre værktøjet performer, jo mere opmærksom skal du være.
2. **Tekstregler er forslag.** Kun teknisk håndhævelse (hooks) er garantier.
3. **Tool-switching er den farligste adfærd.** Guard ALLE stier til en handling, ikke kun den primære.
4. **Fix koden, svæk aldrig checken.** Gør reviews strengere, aldrig mere lempelige.
5. **3x-reglen:** Samme fejl 3 gange → automatisk hook.
6. **Treat AI as enthusiastic junior dev med korttidshukommelse.** Kompetent og hurtig, men blind for konsekvenser.
7. **Backup er den eneste ægte sikkerhed.** Alt andet er forsinkelse, ikke forhindring.
8. **Small bets.** Fejl kaskaderer eksponentielt med scope. Én opgave, verificér, gem, næste.
9. **Byg scaffold, ikke bare regler.** CLAUDE.md er Layer 1 — agent scaffold (context + workflow + task list) er det der gør det muligt at bygge stort.

---

## Vurdering: Sekundære kilder vs. transkript

Sekundærkilderne fangede ~40% af det samlede indhold. Terraform-lektionerne, 5-Layer QA, og hook-arkitekturen var solidt dækket. Men videoen handler fundamentalt om noget andet end dokumentet antog.

**Hvad kun var i videoen:**
- De 5 management skills som samlet ramme (ikke bare enkeltstående pointer)
- General contractor-metaforen — den stærkeste analogi i hele videoen
- Agent scaffold-konceptet (workflow + planning + context + task files)
- Context window degradation som forudsigeligt problem, ikke mystisk fejl
- "Prompting plus plus" — at 2025-prompting er utilstrækkeligt for 2026-agenter
- SumerU-hændelsen (email-sletning trods stop-kommandoer)
- Rules file organisk vækst (start messy, tilføj per fejl, hold under 200 linjer)

Dokumentet var bygget med en "sikkerhed og hooks"-vinkel. Videoen har en "management skills for non-engineers"-vinkel. Begge er gyldige, men transkriptet ændrede dokumentets tyngdepunkt markant.

---

## Kilder

- [Video: Claude Code Wiped 2.5 Years of Data](https://youtu.be/8lwnJZy4cO0) — transkript hentet 2026-03-17
- [Substack: Your AI agent just mass-deleted a production database](https://natesnewsletter.substack.com/p/your-ai-agent-just-mass-deleted-a) (betalt)
- [Alexey Grigorev: How I Dropped Our Production Database](https://alexeyondata.substack.com/p/how-i-dropped-our-production-database)
- [HN: Claude Code wiped production database](https://news.ycombinator.com/item?id=47278720)
- [5-Layer QA System (GitHub Issue #29795)](https://github.com/anthropics/claude-code/issues/29795)
- [Claude Code Hooks: Guardrails That Actually Work](https://paddo.dev/blog/claude-code-hooks-guardrails/)
- [5 Vital Terraform Lessons](https://www.huuphan.com/2026/03/claude-code-wiped-production-database-terraform.html)
- [Colorado AI News analysis](https://www.coloradoai.news/a-claude-code-mishap-offers-a-simple-warning-dont-get-lazy-with-ai/)
- [Nate B Jones 30-video analyse](data/vps-sync-20260316/NATE_JONES_ANALYSE.md) — eksisterende VPS-analyse
