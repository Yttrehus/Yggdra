# ADR-001: Project Reformation

## 0. Metadata
- **Stage:** DLR
- **Status:** Active
- **Oprettet:** 2026-03-11
- **Sidst opdateret:** 2026-03-12
- **Ejer:** Yttre + Claude

## 1. Origin Story
Project Reformation opstod d. 11/3-2026 under session 9. Det startede ikke som ét projekt men som en kaskade af frustrationer: auto-chatlog var halvfærdig, checkpoint opdaterede NOW.md men glemte PLAN.md, implementation journals eksisterede men var tynde og kontekstløse, og nye idéer druknede i et system der ikke havde infrastruktur til at håndtere dem. Yttre gik fra forstanden over at kontekst forsvandt mellem sessioner — ikke fordi ideerne var dårlige, men fordi der ikke var et stillads der fangede dem. Samtalen eskalerede fra "kan chatloggen opdatere sig selv?" til "hele projektstyringen mangler en livscyklus." En parallel samtale med Google AI Mode validerede idéen om en 4-stage pipeline (PoC → DLR → SIP → BMS) med levende ADR-dokumenter. Det blev klart at Basic Setup ikke bare var "opsætning af et udviklermiljø" — det var ved at blive et framework for hvordan Yttre arbejder med AI.

## 2. Current State
DLR-fase. Framework er fuldt designet: pipeline (Backlog→PoC→DLR→SIP→BMS), ADR-template (11 sektioner), governance-README'er (5 stk), brief-format for backlog, triage af 18 idéer udført. Fil-flytning planlagt i detaljer (T112/T153 i chatlog). Intet er rørt i det eksisterende filsystem endnu.

Session 10 (2026-03-12) tilføjede: context engineering research (8 kilder, Anthropic officiel + community), repo-omdøbning besluttet (Basic Setup → Yggdra), PLAN.md v3 struktur diskuteret (pipeline-baseret i stedet for modulbaseret), M7 (context engineering) omtænkt som selvstændigt projekt i pipelinen i stedet for modulstep. CLAUDE.md-filer opdateret: context rot fjernet, @import NOW.md tilføjet, compaction-instruktion tilføjet.

## 3. Problem Statement
- **Hvad:** Implementationer i Basic Setup har ingen formel livscyklus. De opstår i samtaler, halvimplementeres, og mister kontekst mellem sessioner. PLAN.md afspejler ikke virkeligheden. Implementation journals er tynde.
- **Hvorfor:** Det fører til tabt arbejde, gentagne diskussioner, og frustration. Yttre har gentagende gange mistet overblik over hvad der er gjort, hvad der er halvfærdigt, og hvad der bare er en idé.

## 4. Target State
Ethvert modul/projekt har en ADR der følger det fra fødsel til arkiv. Fire stadier (PoC → DLR → SIP → BMS) giver øjeblikkeligt overblik. Changelog i dagbogsstil bevarer fuld kontekst — om 5 år kan man samle en arkiveret ADR op og forstå alt uden at grave i chatloggen. Intet kræver hukommelse. Stilladset fanger det.

## 5. Architecture & Trade-offs
- **Beslutning:** 4-stage pipeline (PoC → DLR → SIP → BMS) med levende ADR-dokumenter. ADR bor med det den beskriver, ikke i en central mappe. ADR-INDEX.md i roden linker til alle. Fraktal: hvert projekt kan have sin egen pipeline-instans.
- **Konsekvenser:** Mere dokumentation per modul. Risiko for bureaukrati. Afbødes ved stram template + dagbogsstil changelog (nok kontekst, ikke en roman). Mappestrukturen kræver en omstrukturering af Basic Setup.

## 6. Evaluation
- Kan vi åbne en ADR om 6 måneder og forstå fuld kontekst uden chatloggen?
- Reducerer det "hvad lavede vi sidst?"-spørgsmål ved session-start?
- Føles det som sikkerhedsnet eller bureaukrati?
- Opdateres ADR'er faktisk løbende, eller glemmes de?

## 7. Exit Criteria
- **Promotion til SIP:** ADR-template testet på mindst 2 moduler. README'er for alle 4 stages skrevet. Eksisterende filer mappet til ny struktur.
- **Promotion til BMS:** Brugt friktionsfrit i 5+ sessioner. Checkpoint-skill scanner ADR'er automatisk.
- **Demotion:** Hvis ADR'er konsekvent ikke opdateres → systemet er for tungt → simplificér template.
- **Sunset:** Hvis vi efter 10 sessioner stadig glemmer at opdatere → forkert design → skrot og find anden tilgang.

## 8. Implementation

**Princip:** Alt i rækkefølge. Hvert step verificeres. Intet slettes — ting flyttes eller arkiveres.
**Forudsætning:** Komplet fil-audit (fase 0.5) før noget flyttes.

### Fase 0: Forberedelse ✅
- [x] ADR oprettet (session 9)
- [x] ADR-template designet (12 sektioner inkl Implementation)
- [x] Governance-README'er (5 stk)
- [x] Triage af idé-parkering (18 idéer)
- [x] CLAUDE.md context rot rettet
- [x] @import + compaction-instruktion tilføjet
- [x] CONTEXT.md design besluttet (NOW+PLAN+PROGRESS → ét dokument, graduated summary)
- [x] PLAN.md v3 struktur besluttet (pipeline-baseret, lagdelt evolution)
- [x] Repo-omdøbning besluttet (→ Yggdra)
- [x] ADR-filnavn konvention: `emne.adr.md`
- [x] Implementation merged ind i ADR (dette dokument)

### Fase 0.5: Fil-audit
Komplet audit af alle filer i repoet med destination per fil. Gøres FØR fase 1.

1. [ ] Audit: roden (alle filer, hvad er BMS, hvad flyttes)
2. [ ] Audit: references/ (opslagsværk vs research vs arkiv, freshness)
3. [ ] Audit: chatlogs/ (relation til SIP/auto-chatlog, pensioneringsplan)
4. [ ] Audit: .claude/ (skills, hooks, implementation journals → _ARC/)
5. [ ] Audit: template/ (skal ADR-template og CONTEXT-template ind her?)
6. [ ] Audit: auto-chatlog/ (hvad eksisterer, hvad mangler)
7. [ ] Audit: ~/parallel-tasks/ (7 outputs → mapping til specifikke briefs)
8. [ ] Skriv komplet fil-manifest: hvad → hvor, med begrundelse per fil

### Fase 1: Mappestruktur
Opret mapper med governance-README'er. Intet flyttes endnu.

1. [ ] Opret `_backlog/` + governance README
2. [ ] Opret `PoC/` + governance README
3. [ ] Opret `DLR/` + governance README
4. [ ] Opret `SIP/` + governance README
5. [ ] Opret `_ARC/` + skriv README
6. [ ] Verificér: alle 5 mapper eksisterer med README.md
7. [ ] Commit: "reformation fase 1: mappestruktur oprettet"

### Fase 2: Fil-flytning
Flyt filer ifølge fil-manifestet fra fase 0.5. Roden ER BMS.

1. [ ] `project-reformation/` → `DLR/project-reformation/`
2. [ ] `auto-chatlog/` → `SIP/auto-chatlog/`
3. [ ] `.claude/implementation journals/` → `_ARC/implementation-journals/`
4. [ ] `references/PLAN.v1.md` → `_ARC/PLAN.v1.md`
5. [ ] `references/git-concepts.md` → `_ARC/` (historisk læremateriale)
6. [ ] `references/google-ai-samtale-rd-framework.md` → `_ARC/` (kontekst nu i ADR)
7. [ ] Opdatér `references/README.md` med indeks + freshness-tabel
8. [ ] Verificér: alle filer fra manifestet er på rette plads
9. [ ] Commit: "reformation fase 2: filer flyttet til pipeline-struktur"

### Fase 3: Backlog-briefs
Opret briefs i `_backlog/` fra idé-parkering + ~/parallel-tasks/ output.

1. [ ] Opret 13 brief-filer med opsummering → origin story → rå input
2. [ ] Map alle 7 ~/parallel-tasks/ outputs til specifikke briefs
3. [ ] Fjern idé-parkering fra PLAN.md, erstat med pointer til `_backlog/`
4. [ ] Commit: "reformation fase 3: briefs oprettet"

### Fase 4: ADR'er for eksisterende moduler
Navnekonvention: `emne.adr.md`

1. [ ] `SIP/auto-chatlog/auto-chatlog.adr.md`
2. [ ] `PoC/projekt-omdobning/projekt-omdobning.adr.md`
3. [ ] Verificér: ADR-template følges (12 sektioner)
4. [ ] Commit: "reformation fase 4: ADR'er oprettet"

### Fase 5: CONTEXT.md
Den store konsolidering. Bør have sin egen session.

1. [ ] Skriv CONTEXT.md: NOW + PLAN v3 + PROGRESS (graduated summary)
2. [ ] Arkivér PLAN.md → `_ARC/PLAN.v2.md` med overgangsnotat
3. [ ] Arkivér PROGRESS.md → `_ARC/PROGRESS-pre-v3.md`
4. [ ] Slet NOW.md og PROGRESS.md
5. [ ] Opdatér projekt-CLAUDE.md: `@NOW.md` → `@CONTEXT.md`
6. [ ] Opdatér global CLAUDE.md: peg til CONTEXT.md
7. [ ] Opdatér MEMORY.md
8. [ ] Opdatér `basic-setup.code-workspace` → `yggdra.code-workspace`
9. [ ] Verificér: ny session starter med kun CLAUDE.md + CONTEXT.md
10. [ ] Commit: "reformation fase 5: CONTEXT.md live"

### Fase 6: ADR-INDEX + oprydning
1. [ ] Skriv `ADR-INDEX.md` i roden
2. [ ] Opdatér checkpoint-skill med ADR-check
3. [ ] Fjern eventuelle forældreløse filer/mapper
4. [ ] Verificér: rod er ren
5. [ ] Commit: "reformation fase 6: ADR-INDEX, oprydning"

### Fase 7: Omdøbning
1. [ ] Omdøb repo: Basic Setup → Yggdra (GitHub + lokal)
2. [ ] Opdatér alle interne referencer
3. [ ] Commit: "reformation fase 7: Basic Setup → Yggdra"

### Post-reformation
- [ ] Kør fuld session med ny struktur — evaluér friktion
- [ ] Opdatér denne ADR's Current State, vurdér promotion til SIP
- [ ] M5 step 11-17
- [ ] MEMORY.md audit

### Afhængigheder
- Fase 0.5 (audit) SKAL ske før fase 1-2
- Fase 1-4 kan gøres i én session
- Fase 5 bør have sin egen session
- Fase 6-7 er oprydning

---

## 9. Changelog
- 2026-03-11 (session 9, ~09:30): Det hele startede med et spørgsmål om automatisk chatlog-opdatering. Yttre observerede at Claude Codes .jsonl sessionsfiler vokser kontinuerligt men aldrig omdannes til læsbar chatlog automatisk. En parser-prototype (chatlog-engine.js) blev bygget i chatlog-test/ — den virkede, men designet var ikke færdigt da Claude gik i bygge-mode for tidligt. Yttre kalibrerede: "spørg før du bygger."

- 2026-03-11 (~10:00): Diskussionen eskalerede til implementation journals, ADR-format, og staging-mappe for prototyper. Yttre foreslog at ADR'er bor med det de beskriver (ikke central mappe). Plan+NOW+Progress sammensmeltning blev diskuteret og parkeret som idé. Tre iterationer af chatlog-design: navigationslinks, referater, retskrivning — alt parkeret som fremtidige forbedringer.

- 2026-03-11 (~11:00): Google AI Mode session validerede og forfinede idéen. Pipeline-navne gennemgik flere iterationer: TRL/DLR/SIP/BMS → RAW/DEV/STG/CORE → endelig landing på PoC/DLR/SIP/BMS. Fraktal struktur bekræftet: hvert projekt har sin egen pipeline-instans. ADR-template fusioneret fra Google-session + vores iterationer.

- 2026-03-11 (~13:00): PLAN.md afslørede et strukturelt problem: step 2-10 i M5 var gjort men ikke afkrydset. Checkpoint opdaterer NOW.md men rører ikke PLAN.md. Dette understregede behovet for Project Reformation. ADR-template færdigdesignet: Origin Story i toppen (kontekst først), Current State med narrativ, dagbogsstil changelog, Original ADR som frosset snapshot til sidst. Template og ADR skrevet til disk i project-reformation/.

- 2026-03-12 (session 10): Separat review-session med fokus på state-filer og kontekst-kvalitet. Læste alle chatlog-filer fra session 9 (T001-T158) for fuldt overblik. Tre beslutninger: (1) Repo omdøbes fra "Basic Setup" til "Yggdra" — det ER allerede Yggdra, ét system/ét navn. (2) M7 (context engineering) trækkes ud af PLAN.md's modulstruktur og bliver et selvstændigt projekt i pipelinen (DLR eller PoC). Research udført med 8 kilder (Anthropic officiel, community patterns) — gemt i references/context-engineering-research.md. Kerneresultat: @import syntax, .claude/rules/, compaction-instruktioner, ~80% kontinuitet er realistisk. (3) PLAN.md v3 diskuteret: pipeline-baseret i stedet for modulbaseret. Aktive moduler (M5 rest, M6) beholdes, men resten erstattes af pipeline-overblik. Context rot i begge CLAUDE.md-filer rettet: forældet state fjernet, slettet scripts/-reference, @import NOW.md tilføjet, compaction-instruktion tilføjet. PROGRESS arkiveringspolitik besluttet: "destillér først, arkivér dernæst" — principper trækkes til CLAUDE.md/MEMORY.md før rå materiale flyttes til _ARC/.

## 10. Backlog
- README'er/governance-manualer for PoC, DLR, SIP, BMS (punkt 3 i planen)
- Map eksisterende filer til ny struktur (punkt 4)
- ADR-INDEX.md i roden
- Test ADR-template på auto-chatlog og checkpoint som første moduler
- Navigationslinks i chatlog-engine.js
- Plan-konsolidering (plan+now+progress → ét dok) — parkeret som eksperiment
- Lokal LLM (Ollama) til opsummering/nøgleord — parkeret som fremtidigt projekt
- Opdatér checkpoint-skill til at scanne ADR'er og PLAN.md checkboxes
- Overvej om project-reformation/ selv skal leve i en PoC/DLR/SIP/BMS-struktur (meta!)
- Context engineering som selvstændigt projekt i DLR (udtrukket fra M7) — research allerede i references/context-engineering-research.md
- Repo-omdøbning Basic Setup → Yggdra (besluttet session 10, implementeres ved reformation)
- PLAN.md v3 design: pipeline-baseret struktur, NOW-sektion integreret, afsluttede moduler → _ARC/PLAN.v2.md
- PROGRESS arkiveringspolitik: destillér principper til CLAUDE.md/MEMORY.md, derefter flyt rå sessioner til _ARC/

## 11. Original ADR

### Problem Statement
- Hvad: Implementationer (auto-chatlog, checkpoint, skills, hooks) har ingen formel livscyklus. De opstår i samtaler, halvimplementeres, og mister kontekst mellem sessioner.
- Hvorfor: Det fører til tabt arbejde, gentagne diskussioner, og PLAN.md der ikke afspejler virkeligheden.

### Target State
Ethvert modul/projekt har en ADR der følger det fra idé til arkiv. Livscyklus-stadier (PoC → DLR → SIP → BMS) giver øjeblikkeligt overblik over modenhed. Intet kræver hukommelse — stilladset fanger alt.

### Architecture & Trade-offs
- Beslutning: 4-stage pipeline med levende ADR-dokumenter. ADR bor med det den beskriver. Fraktal: hvert projekt kan have sin egen instans af pipelinen.
- Konsekvenser: Mere dokumentation per modul. Risiko for bureaukrati. Afbødes ved at holde ADR-templaten stram og changelog i dagbogsstil.

### Evaluation
- Kan vi åbne en ADR om 6 måneder og forstå fuld kontekst uden chatloggen? (Ja = virker)
- Reducerer det antallet af "hvad lavede vi sidst?"-spørgsmål ved session-start? (Ja = virker)
- Føles det som bureaukrati eller som et sikkerhedsnet? (Bureaukrati = juster)

### Exit Criteria
- Promotion til SIP: ADR-template testet på mindst 2 eksisterende moduler (auto-chatlog + checkpoint). README'er for PoC/DLR/SIP/BMS skrevet.
- Promotion til BMS: Brugt friktionsfrit i 5+ sessioner. Checkpoint-skill opdateret til at scanne ADR'er.
- Demotion: Hvis ADR'er konsekvent ikke opdateres → for tungt → simplificér.
- Sunset: Hvis vi efter 10 sessioner stadig glemmer at opdatere ADR'er, er systemet forkert designet.
