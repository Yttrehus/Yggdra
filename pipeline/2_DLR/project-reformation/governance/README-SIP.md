# 3_SIP — Staged Implementation Plan

## Hvad er dette?
Sandboxen. Her bliver planer til virkelighed — men i et kontrolleret miljø. Koden kører, data flyder, men med ekstra overvågning og scaffolding. Formålet er at validere om det faktisk virker i praksis, ikke bare i teorien. Fejl her er billige og forventede.

## Behandling
- Implementation er aktiv — kode skrives, testes, og itereres
- Alt kører med **scaffolding**: ekstra logging, feature flags, parallelle systemer (gammel + ny)
- Data indsamles aktivt for at udfylde Evaluation-sektionen i ADR
- Changelog opdateres hyppigt — hver vigtig observation, ikke kun beslutninger
- Eksisterende systemer må **ikke** brydes — SIP kører parallelt eller i isolation
- Regelmæssig evaluering: matcher virkeligheden vores Exit Criteria?

## Krav
- ADR fuldt udfyldt (alle 12 sektioner, 0-11)
- Fungerende implementation der kan testes
- Evalueringsdata indsamles (ikke bare "det føles som om det virker")
- Mindst én runde feedback fra faktisk brug

## Promotion til BMS
Flyttes til BMS når:
- **Stabilitet bevist**: kører uden fejl i defineret testperiode
- **Scaffolding kan fjernes**: implementation fungerer uden ekstra overvågning
- **Evaluering bestået**: målbare parametre fra sektion 6 er opfyldt
- **ADR er komplet**: Origin Story, Current State, og Changelog dokumenterer hele rejsen
- **Gammel system kan pensioneres** (hvis SIP erstatter noget eksisterende)

## Demotion til DLR
Falder tilbage til DLR når:
- Fundamental arkitektur-fejl opdages under test
- Antagelser fra DLR-fasen viser sig forkerte i praksis
- Implementation kræver en helt anden tilgang end planlagt

## Eksempler

### Godt SIP-entry
```
auto-chatlog/
  ADR.md              →  Alle sektioner udfyldt. Changelog dokumenterer
                          3 iterationer af formattet baseret på feedback.
                          Evaluation viser: parser håndterer 500+ beskeder,
                          dansk tid virker, under-index med 2-timers blokke.
  chatlog-engine.js   →  Fungerende parser, kører manuelt.
  live.md             →  Output fra dagens session.
  archive.md          →  Output fra tidligere datoer.
  (gammel chatlogs/ mappe kører stadig parallelt som fallback)
```
Virker, testes, data indsamles, gammel system kører stadig som sikkerhedsnet.

### Dårligt SIP-entry
```
auto-chatlog/
  chatlog-engine.js   →  "Virker vist nok. Smed den i produktion."
  (gammel chatlogs/ mappe slettet)
  (ingen ADR)
```
Ingen evaluering. Ingen fallback. Ingen dokumentation af hvad der virker og hvad der ikke gør. Hvis det går galt, er der ingen vej tilbage og ingen der ved hvorfor.
