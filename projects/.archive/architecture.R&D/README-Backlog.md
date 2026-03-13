# 0_backlog — Briefs

## Hvad er dette?
Idépuljen. Her lever tanker, drømme og koncepter der endnu ikke er klar til aktiv investering. Ingen tidspres, ingen krav om handling. En brief kan ligge her i måneder og langsomt vokse — eller aldrig forlade mappen. Begge dele er fine.

## Behandling
- Én fil per idé — ingen undermapper nødvendige
- Ingen fast struktur påkrævet, men brief-formatet anbefales (se nedenfor)
- Det er tilladt at sidde i Backlog og drømme — tilføj noter, research-links, voice memo transkriptioner
- Briefs gennemgås ved triage-sessioner: hvad er klar til PoC? Hvad mangler?
- Filnavne: `kebab-case.md` (ASCII, ingen specialtegn)

## Brief-format (anbefalet)
```markdown
# [Navn]

**Dato:** YYYY-MM-DD
**Klar til:** Backlog | PoC-klar (mangler: [hvad])

## Opsummering
- [Punkt 1: hvad er idéen]
- [Punkt 2: hvad ville det løse]
- [Punkt 3: hvad kræver det]

## Origin Story
[Hvad udløste tanken, i hvilken kontekst, hvorfor det føles vigtigt.]

## Rå input
[Alt det originale — voice memo, brain dump, samtale-uddrag. Uændret.]
```

## Krav
- Minimum: en fil med et navn og mindst én sætning der beskriver idéen
- Anbefalet: brief-formatet ovenfor

## Promotion til PoC
En brief flyttes til PoC når:
- Der er et klart **Problem Statement** (hvad løser det?)
- Der er et estimeret **ROI** (er det værd at investere tid?)
- Nogen aktivt vælger at arbejde på det (ikke bare "det ville være fedt")

## Eksempler

### God brief
```markdown
# Lokal LLM til opsummering

**Dato:** 2026-03-11
**Klar til:** Backlog (mangler: test af Ollama på denne maskine)

## Opsummering
- Brug Ollama + Mistral lokalt til at generere referater og nøgleord for chatlog
- Erstatter frekvensbaseret keyword extraction der er utilstrækkelig
- Kræver: Ollama installeret, ~4GB RAM, prompt-design

## Origin Story
Opstod under auto-chatlog designet da nøgleord-extraction viste sig
for simpel. Yttre ville have "intelligente" referater men ikke betale
for API-kald til en cloud-LLM for noget så simpelt.

## Rå input
(fra session 9, 2026-03-11)
"...en lama eller mist eller hvad de nu hedder, den skal jo ikke
lave noget komplekst. hvad der var en llm vi selv har designet,
der boede på pc'en og som KUN har til opgave at holde øje med
date og tidspunkt..."
```

### Dårlig brief
```
fil: ideer.md
indhold: "masse ting vi burde lave"
```
Unavngivet, uspecifik, umulig at triage. Split i individuelle briefs.
