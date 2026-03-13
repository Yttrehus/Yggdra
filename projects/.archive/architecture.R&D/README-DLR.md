# 2_DLR — Discovery-Led Roadmap

## Hvad er dette?
Laboratoriet. Her omdannes rå idéer til strukturerede planer. Fokus skifter fra "kan det lade sig gøre?" til "hvordan gør vi det rigtigt?" Research, arkitektur-design, og feasibility-tests hører hjemme her. Intet kode rammer produktion fra denne stage — det er tænkning og planlægning.

## Behandling
- En ADR er **påkrævet** — minimum sektion 0-7 (Metadata → Exit Criteria)
- Research dokumenteres: hvad undersøgte vi, hvad fandt vi, hvilke alternativer overvejede vi
- Arkitektur-beslutninger beskrives med trade-offs (hvad vinder vi, hvad ofrer vi)
- Prototyper er tilladt men lever i isolation — de må ikke røre eksisterende systemer
- Changelog opdateres løbende i dagbogsstil

## Krav
- ADR med udfyldt Problem Statement, Target State, og Exit Criteria
- Mindst én dokumenteret arkitektur-beslutning med trade-offs
- Klart defineret plan for hvad der skal testes i SIP

## Promotion til SIP
Flyttes til SIP når:
- Der er en **teknisk plan** der er modulær nok til at blive testet uden at vælte BMS
- **Exit Criteria** er defineret (hvad er success, hvad er failure)
- En prototype eller proof-of-concept bekræfter at planen er realistisk
- Der er enighed om at investere tid i faktisk implementation

## Demotion til PoC
Falder tilbage til PoC når:
- Research viser at grundantagelsen var forkert
- Problemet viser sig at være anderledes end beskrevet
- ROI-estimatet holder ikke efter dybere analyse

## Eksempler

### Godt DLR-entry
```
auto-chatlog/
  ADR.md        →  Fuld ADR med Problem Statement ("chatlog opdateres
                    ikke automatisk"), Target State ("live.md opdateres
                    inden for sekunder"), tre overvejede tilgange
                    (file-watcher vs hook vs polling), valgt retning
                    med trade-offs dokumenteret.
  research.md   →  Undersøgelse af Claude Code .jsonl format,
                    fs.watch vs chokidar, performance ved store filer.
  prototype/    →  chatlog-engine.js (parser, testet på 500+ beskeder)
```
Klar plan, dokumenterede valg, testbar prototype.

### Dårligt DLR-entry
```
auto-chatlog/
  ADR.md        →  "Vi skal lave en automatisk chatlog.
                    Claude bygger det nok."
```
Ingen research. Ingen alternativer overvejet. Ingen Exit Criteria. Ingen ved hvornår det er "done" eller hvornår det skal skrottes. → Hører hjemme i PoC, ikke DLR.
