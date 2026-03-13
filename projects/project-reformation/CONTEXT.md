# Project Reformation

## 0. Metadata
- **Status:** I gang — struktur implementeret, CONTEXT.md og oprydning mangler
- **Oprettet:** 2026-03-11
- **Sidst opdateret:** 2026-03-13 (session 13)
- **Ejer:** Yttre + Claude

## 1. Origin Story
Project Reformation opstod d. 11/3-2026 under session 9. Det startede ikke som ét projekt men som en kaskade af frustrationer: auto-chatlog var halvfærdig, checkpoint opdaterede NOW.md men glemte PLAN.md, implementation journals eksisterede men var tynde og kontekstløse, og nye idéer druknede i et system der ikke havde infrastruktur til at håndtere dem. Yttre gik fra forstanden over at kontekst forsvandt mellem sessioner — ikke fordi ideerne var dårlige, men fordi der ikke var et stillads der fangede dem. Samtalen eskalerede fra "kan chatloggen opdatere sig selv?" til "hele projektstyringen mangler en livscyklus." En parallel samtale med Google AI Mode validerede idéen om en pipeline med levende projektdokumenter. Det blev klart at Basic Setup ikke bare var "opsætning af et udviklermiljø" — det var ved at blive et framework for hvordan Yttre arbejder med AI.

## 2. Current State
Fase 0-4 komplet ✅. Session 13 simplificerede strukturen radikalt: pipeline-stages og ADR-terminologi erstattet af flad `projects/`-mappe med CONTEXT.md per projekt. Manifestet er implementeret. Næste: fase 5 (rod-CONTEXT.md — bør have sin egen session).

Framework-evolution: session 9-12 byggede pipeline (Backlog→PoC→DLR→SIP→BMS) med ADR-template og governance. Session 13 simplificerede: ét format (CONTEXT.md) overalt, stage som metadata, ingen mappestruktur-encoded pipeline. Briefs i `projects/backlog/` er embryoniske CONTEXT.md'er. Arkiv i `projects/archive/`.

## 3. Problem Statement
- **Hvad:** Implementationer i Basic Setup har ingen formel livscyklus. De opstår i samtaler, halvimplementeres, og mister kontekst mellem sessioner. PLAN.md afspejler ikke virkeligheden. Implementation journals er tynde.
- **Hvorfor:** Det fører til tabt arbejde, gentagne diskussioner, og frustration. Yttre har gentagende gange mistet overblik over hvad der er gjort, hvad der er halvfærdigt, og hvad der bare er en idé.

## 4. Target State
Ethvert projekt har en CONTEXT.md der følger det fra fødsel til arkiv. Samme format som rod-CONTEXT.md — rekursivt design. `projects/` giver øjeblikkeligt overblik. Changelog i dagbogsstil bevarer fuld kontekst — om 5 år kan man samle en arkiveret CONTEXT.md op og forstå alt uden at grave i chatloggen. Intet kræver hukommelse. Stilladset fanger det.

## 5. Architecture & Trade-offs
- **Beslutning:** Flad `projects/`-mappe med CONTEXT.md per projekt. Backlog som `projects/backlog/` (briefs). Arkiv som `projects/archive/`. Ingen pipeline-stages i mappenavne — stage er metadata i CONTEXT.md.
- **Evolution:** Startede som 4-stage pipeline med ADR-template (session 9-12). Simplificeret til rekursivt CONTEXT.md-format (session 13). Governance READMEs og stage-mapper viste sig at være overengineering.
- **Konsekvenser:** Simpelt og fladt. Risiko: manglende synlighed af projekt-modenhed i mappestrukturen. Afbødes ved at CONTEXT.md altid har status/metadata i toppen.

## 6. Evaluation
- Kan vi åbne en CONTEXT.md om 6 måneder og forstå fuld kontekst uden chatloggen?
- Reducerer det "hvad lavede vi sidst?"-spørgsmål ved session-start?
- Føles det som sikkerhedsnet eller bureaukrati?
- Opdateres CONTEXT.md-filer faktisk løbende, eller glemmes de?

## 7. Exit Criteria
- **Done:** CONTEXT.md brugt friktionsfrit i 5+ sessioner. Checkpoint-skill scanner CONTEXT.md automatisk.
- **Demotion:** Hvis CONTEXT.md-filer konsekvent ikke opdateres → systemet er for tungt → simplificér.
- **Sunset:** Hvis vi efter 10 sessioner stadig glemmer at opdatere → forkert design → skrot og find anden tilgang.

## 8. Implementation

**Princip:** Alt i rækkefølge. Hvert step verificeres. Intet slettes — ting flyttes eller arkiveres.

### Fase 0: Forberedelse ✅
- [x] Projektdokument oprettet (session 9)
- [x] Template designet
- [x] Triage af idé-parkering (18 idéer)
- [x] CLAUDE.md context rot rettet
- [x] @import + compaction-instruktion tilføjet
- [x] CONTEXT.md design besluttet (NOW+PLAN+PROGRESS → ét dokument, graduated summary)
- [x] Repo-omdøbning besluttet (→ Yggdra)

### Fase 0.5: Fil-audit ✅
Komplet audit af alle filer i repoet med destination per fil.

**Resultat (session 11-13):** references/ opløst → manuals/ + research/archive/. Al research pre-reformation. Nye briefs: research-architecture, automation-index. Manifest v4: flad `projects/`-struktur.

### Fase 1-2: Mappestruktur + fil-flytning ✅
Udført i session 11-13, itereret tre gange.

**Session 11:** Initiel mappestruktur, stage-mapper i rod.
**Session 12:** Pipeline-stages samlet under `pipeline/` med numeriske præfikser.
**Session 13:** Simplificeret til `projects/` — flad, ét projekt = én mappe. ADR → CONTEXT.md. Manuals og research ind under projects/.

### Fase 3: Backlog-briefs ✅
- [x] 13 brief-filer oprettet i `projects/backlog/`
- [x] 7 ~/parallel-tasks/ outputs mappet til specifikke briefs (kræver revision)
- [x] PLAN.md idé-parkering erstattet med pointer til backlog

### Fase 4: CONTEXT.md for eksisterende projekter ✅
- [x] `projects/auto-chatlog/CONTEXT.md`
- [x] `projects/projekt-omdobning/CONTEXT.md`
- [x] Commit + push

### Fase 5: Rod-CONTEXT.md
Den store konsolidering. Bør have sin egen session.

1. [ ] Skriv CONTEXT.md: NOW + PLAN v3 + PROGRESS (graduated summary)
2. [ ] Arkivér PLAN.md → `projects/archive/PLAN.v2.md` med overgangsnotat
3. [ ] Arkivér PROGRESS.md → `projects/archive/PROGRESS-pre-v3.md`
4. [ ] Slet NOW.md og PROGRESS.md
5. [ ] Opdatér CLAUDE.md: `@NOW.md` → `@CONTEXT.md`
6. [ ] Opdatér global CLAUDE.md: peg til CONTEXT.md
7. [ ] Opdatér MEMORY.md
8. [ ] Verificér: ny session starter med kun CLAUDE.md + CONTEXT.md
9. [ ] Commit: "reformation fase 5: CONTEXT.md live"

### Fase 6: Oprydning
1. [ ] Opdatér checkpoint-skill med CONTEXT-check
2. [ ] Fjern eventuelle forældreløse filer/mapper
3. [ ] Verificér: rod er ren
4. [ ] Commit: "reformation fase 6: oprydning"

### Fase 7: Omdøbning
1. [ ] Omdøb repo: Basic Setup → Yggdra (GitHub + lokal)
2. [ ] Opdatér alle interne referencer
3. [ ] Commit: "reformation fase 7: Basic Setup → Yggdra"

### Post-reformation
- [ ] Kør fuld session med ny struktur — evaluér friktion
- [ ] Opdatér denne CONTEXT.md, vurdér om reformation er done
- [ ] M5 step 11-17
- [ ] MEMORY.md audit

### Afhængigheder
- Fase 5 bør have sin egen session
- Fase 6-7 er oprydning

---

## 9. Changelog
- 2026-03-11 (session 9, ~09:30): Det hele startede med et spørgsmål om automatisk chatlog-opdatering. Prototype bygget, design-diskussioner, "spørg før du bygger" kalibreret.

- 2026-03-11 (~10:00): Eskalation til implementation journals, ADR-format, staging-mapper. Tre design-iterationer af chatlog.

- 2026-03-11 (~11:00): Google AI Mode session validerede pipeline-idéen. Navne-iterationer: TRL/DLR/SIP/BMS → RAW/DEV/STG/CORE → PoC/DLR/SIP/BMS.

- 2026-03-11 (~13:00): PLAN.md step 2-10 gjort men ikke afkrydset. Understregede behovet for reformation.

- 2026-03-12 (session 10): Separat review-session. Tre beslutninger: (1) Repo → Yggdra. (2) M7 context engineering trukket ud som selvstændigt projekt. (3) PLAN.md v3 pipeline-baseret. Context rot i CLAUDE.md rettet. Graduated summary komprimeringsregler besluttet.

- 2026-03-12 (session 12, fase 1-2): Pipeline-stages under `pipeline/` med numeriske præfikser. template/ → .claude/template/. Rod reduceret til 3 mapper.

- 2026-03-12 (session 12, fase 3): 13 backlog-briefs oprettet. 7 parallel-tasks outputs mappet til briefs.

- 2026-03-12 (session 12, fase 4): 2 projekt-CONTEXT.md'er skrevet retroaktivt: auto-chatlog og projekt-omdøbning.

- 2026-03-13 (session 13): Strukturændring v3 → v4. Pipeline-stages og ADR-terminologi droppet. `pipeline/` → `projects/` (flad). ADR → CONTEXT.md. Manuals og research ind under projects/. Governance READMEs arkiveret. Rod reduceret til 2 mapper (projects, .claude).

## 10. Backlog
- Opdatér checkpoint-skill til at scanne CONTEXT.md
- Context engineering som selvstændigt projekt — research i projects/research/archive/context-engineering-research.md
- Push-system (automatisk checkpoint ved Stop/PreCompact) — session-drift-pipeline projekt
- Graduated summary komprimeringsregler (besluttet session 10):
  - **Seneste session:** Alt. Fuld detalje.
  - **Session 2-3:** Alt væsentligt. Kun gentagelser og tangenter skæres.
  - **Session 4-6:** Beslutninger + resultater + refs. Ingen narrativ.
  - **Session 7-10:** 1 afsnit: hvad skete, hvad blev besluttet. Ref til archive/.
  - **Session 11+:** 1-3 sætninger + dato + ref.
  - **Undtagelse:** Ældre sessioner der stadig er direkte aktive forbliver på deres niveau.
  - **Fuld detalje altid i archive/.** Evaluér i praksis før yderligere justering.

## 11. Original Design
Startede som ADR (Architecture Decision Record) med 4-stage pipeline (PoC → DLR → SIP → BMS), governance READMEs per stage, og ADR-INDEX.md. Simplificeret i session 13 til rekursivt CONTEXT.md-format med flad projects/-struktur. Originalt design arkiveret i projects/archive/.
