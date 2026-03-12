# BMS — Baseline Module System

## Hvad er dette?
Fundamentet. Her lever de etablerede, stabile moduler der er systemets rygrad. Alt i BMS er testet, dokumenteret, og bevist i praksis. Det er sandheden — det andre moduler bygger ovenpå. BMS er ikke et gravsted for færdige ting — det er et levende fundament der vedligeholdes og forbedres, men med respekt for stabilitet.

## Behandling
- **Stabilitet er prioritet #1** — ændringer her kræver omtanke
- ADR forbliver **levende**: Changelog og Current State opdateres ved enhver ændring
- Enhver ændring logges med begrundelse i Changelog (hvorfor, ikke bare hvad)
- Større ændringer kræver en ny ADR eller en "Superseded"-note i den eksisterende
- Scaffolding er fjernet — modulet kører på egen kraft
- Andre moduler (i pipeline/1_PoC, 2_DLR, 3_SIP) kan referere til og bygge ovenpå BMS-moduler

## Krav
- ADR er komplet med alle 12 sektioner inklusiv Origin Story og Original ADR (sektion 11)
- Current State afspejler virkeligheden (ikke bare hvad vi håbede)
- Evaluering bestået med dokumenterede resultater
- Ingen kendte kritiske fejl

## Promotion
BMS er det sidste stadie. Der er ingen promotion herfra — kun vedligeholdelse, eller:
- **DEPRECATED** → modulet erstattes af noget nyt (som starter i PoC/DLR)
- **ARCHIVED** → modulet er helt pensioneret, ADR flyttes til arkiv med fuld historik intakt

## Demotion til SIP
Falder tilbage til SIP når:
- En kritisk fejl opdages der kræver fundamental rettelse
- Krav til modulet ændrer sig drastisk (nyt use case, ny kontekst)
- Et andet modul i SIP skal erstatte dette — begge kører parallelt i SIP indtil det nye er valideret

## Eksempler

### Godt BMS-entry
```
checkpoint/
  ADR.md    →  Komplet ADR. Origin Story beskriver hvordan det startede
                som en manuel process i session 3. Current State beskriver
                at det nu er en skill der kører friktionsfrit. Changelog
                har 8 entries der dokumenterer fejl, rettelser og
                evalueringer. Evaluation viser: brugt 10+ gange,
                NOW.md opdateres konsekvent. Backlog nævner: "bør også
                opdatere PLAN.md checkboxes" (fremtidig forbedring).
```
Fuld dokumentation. Levende. Man kan åbne den om 2 år og forstå alt.

### Dårligt BMS-entry
```
checkpoint/
  checkpoint.md  →  "Skill der opdaterer NOW.md. Virker fint."
  (ingen ADR)
  (ingen historik over beslutninger)
  (ingen evaluering)
```
Om 6 måneder: "Hvad gør denne? Hvorfor er den lavet sådan? Kan jeg ændre den?" Ingen svar. Man starter forfra — den dybe tallerken opfindes igen.
