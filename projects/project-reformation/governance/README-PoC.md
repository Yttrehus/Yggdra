# 1_PoC — Proof of Concept

## Hvad er dette?
Inkubatoren. Her lever rå idéer, ufiltrerede tanker og hurtige eksperimenter. Formålet er at besvare ét spørgsmål: *kan dette overhovedet lade sig gøre?* Her er støj velkomment — det er bedre at fange en idé uperfekt end at miste den helt.

## Behandling
- Ingen krav til kodekvalitet, dokumentation eller struktur
- Brain-dumps, voice memo-noter, skitser, og "hvad nu hvis..."-tekster er alle gyldige
- En ADR er *valgfri* men anbefalet — selv en halvfærdig ADR med kun Origin Story og Problem Statement er bedre end ingenting
- Brug så lidt tid som muligt — pointen er at teste feasibility, ikke at bygge noget færdigt

## Krav
- Minimum: en fil der beskriver idéen (kan være 3 sætninger)
- Idéen skal have et *navn* — selv et arbejdsnavn. Unavngivne idéer forsvinder

## Promotion til DLR
Idéen flyttes til DLR når:
- Der er et klart **Problem Statement** (hvad løser det?)
- Der er et estimeret **ROI** (er det værd at investere tid/tokens/energi?)
- Der er en person/agent der vil eje det videre

## Demotion hertil
Noget falder tilbage til PoC når:
- DLR-research viser at idéen var baseret på forkerte antagelser
- Scope var for uklart til at planlægge meningsfuldt
- Det viser sig at problemet ikke er det vi troede

## Eksempler

### Godt PoC-entry
```
lokal-llm-opsummering/
  idé.md  →  "Brug Ollama + Mistral til at generere referater
              og nøgleord for chatlog-tidsblokke. Erstatter
              frekvensbaseret keyword extraction. Kræver: Ollama
              installeret, ~4GB RAM, en prompt der producerer
              konsistente 2-sætnings referater."
```
Kort, konkret, testbart. Man ved hvad idéen er og hvad der skal til.

### Dårligt PoC-entry
```
smart-chatlog/
  (tom mappe)
```
Eller:
```
noter.md  →  "vi burde gøre chatloggen smartere"
```
Hvad betyder "smartere"? Ingen kan arbejde videre med dette — heller ikke dig selv om 2 uger.
