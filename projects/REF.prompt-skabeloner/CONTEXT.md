# Prompt-skabeloner

## Metadata
- **Status:** REF — v1 leveret. Syntese + arkitektur + red team + implementeringsplan. I brug-test.
- **Sidst opdateret:** 2026-03-17 (session 25: VPS-sync, fuld prompt-arkitektur deep dive)
- **Ejer:** Yttre + Claude

## Hvad er det
Genanvendelige prompt-skabeloner for instrukser Yttre skriver igen og igen. Ikke et katalog over prompts — men **genveje** der sparer ham fra at skrive 200 ord hver gang han vil igangsætte et genkendbart workflow.

Eksempler på hvad der skal fanges:
- "Start et projekt fra en brief" (projekt-kickoff)
- "Kør adversarial proces: plan → red-team → steelman → eval" (dialectic pipeline)
- "Undersøg hvad en anden session laver og koordinér" (session-koordinering)
- "Gør denne idé skarpere" (brief-skærpning)
- "Hvad tænker du om det?" (diskussions-invitation med krav om ærlig vurdering)

Disse mønstre er i Yttres muskelhukommelse men kræver lange beskeder for at kommunikere intentionen præcist. Målet er at gøre dem til invokérbare skills eller standardiserede skabeloner.

## Baggrund — hvad skete i session 315694ad

Yttre bad om "et projekt der ender med at jeg har en masse gode prompts." Sessionen kørte en fuld dialektisk proces (plan → red-team → steelman → kontekst-fri evaluator) der konkluderede:

- **Evaluator gav 3/10** til et "prompt-katalog" projekt — meta-work forklædt som produktivitet
- **Collector's Trap:** At katalogisere prompts man allerede kender er busywork
- **Men:** Det egentlige behov var aldrig et katalog. Det var **genveje** — "jeg skriver de samme lange beskeder igen og igen for at få Claude til at forstå hvad jeg vil. Gør dem til genanvendelige skabeloner."

Parallelt kørte session `5f9753fe` (Skills) et MCP/Skills kompendium-projekt (`projects/mcp-skills-kompendium/`) med research, adversarial-proces, og konkret anbefaling (1 MCP + 2 skills). Den session landede på et **opslagsværk** — nyttigt men løser ikke Yttres problem med gentagne instrukser.

## Hvad der adskiller dette fra mcp-skills-kompendium

| | mcp-skills-kompendium | prompt-skabeloner |
|---|---|---|
| **Formål** | Opslagsværk: hvad findes der af MCP/skills | Genveje: spar tid på gentagne instrukser |
| **Output** | Ranket liste over tools + anbefaling | Invokérbare skills eller paste-bare prompts |
| **Bruger det** | Når Yttre overvejer nye tools | Hver gang Yttre starter et genkendbart workflow |
| **Kilde** | Web-research, mcpmarket.com | Yttres egne chatlog, sessions, arbejdsmønstre |

## Hvor er vi

### Gjort (session 25, 2026-03-17)
- VPS prompt mining absorberet (1.270 prompts, 8 skabeloner, INSIGHTS.md)
- INVENTAR.md: komplet katalog af alt materiale (16+ kilder, vurderet guld/sølv/støj)
- SYNTESE.md: 9 principper destilleret fra alle kilder (red team anbefaler skæring til 5)
- ARKITEKTUR.md: filstruktur og videns-flow designet
- RED_TEAM.md: ærlig kritik — "mønsteret er research→rapport→hylde, vil dette være anderledes?"
- IMPLEMENTERING.md: 7 handlinger, kill condition (5 sessioner), succeskriterium

### Næste
- [ ] Opret SKABELONER.md med 4 mønstre (handling 1)
- [ ] Flyt VPS_HANDOFF + BESKED til arkiv/ (handling 2)
- [ ] Brug-test: 5 sessioner, 1 skabelon per session
- [ ] Kill condition: hvis SKABELONER.md ikke bruges i 5 sessioner → arkivér projektet

### Gjort (i session 315694ad)
- Dialektisk analyse gennemført — "katalog" forkastet, "genveje" identificeret som det reelle behov
- Kendte prompt-mønstre identificeret fra explore-agent:
  - "hvad tænker du?" (20+ gange i chatlog)
  - "gør skarpere" (brief-skærpning)
  - "kør the fool / red team" (adversarial)
  - Projekt-kickoff fra brief
  - Session-koordinering
  - Checkpoint-flow
- Planfil: `.claude/plans/cached-wibbling-mochi.md` (fuld dialektisk proces)

### Ikke gjort
- Ingen chatlog-mining udført (explore-agenten fandt mønstre men greppede ikke systematisk)
- Ingen skills bygget endnu
- Ikke afklaret: hvilke mønstre er komplekse nok til at retfærdiggøre et skill vs. en one-liner

## Hvad mangler
- [ ] Mine chatlog.md + vps-chatlog.md for gentagne instruksmønstre (lange beskeder fra Yttre der starter workflows)
- [ ] Kategorisér: hvilke er simple (one-liner prompt) vs. komplekse (multi-step skill med subagents)
- [ ] For hvert komplekst mønster: byg et skill (SKILL.md + references/)
- [ ] For simple mønstre: afklar om de overhovedet behøver formalisering eller bare er naturlig kommunikation
- [ ] Test: kan en frisk session invokere skabelonerne og producere det forventede output?

## Beslutninger
- **Done-kriterie:** 3-5 invokérbare skills/skabeloner der sparer Yttre tid ved genkendte workflows
- **Tilgang:** Mine → kategorisér → byg de komplekse → test med frisk session
- **Afgrænsning:** Kun Yttres egne mønstre. Ikke eksterne "awesome prompts" lister.
- **Collector's Trap-vakcinering:** Hvis mining producerer >20 "mønstre" er filteret for svagt. Max 10 kandidater, max 5 skills.

## Relaterede sessions og projekter
- **Session `315694ad`** (denne sessions ophav) — dialektisk analyse, planfil `cached-wibbling-mochi.md`
- **Session `5f9753fe`** (Skills) — MCP/Skills kompendium, projekt `projects/mcp-skills-kompendium/`
- **Session `6db590b3`** (Ydrasil) — VPS data-indexering, projekt `projects/ydrasil/`
- **Planfil denne session:** `.claude/plans/cached-wibbling-mochi.md`
- **Planfil skills-session:** `.claude/plans/greedy-whistling-hare.md`
- **Planfil ydrasil-session:** `.claude/plans/misty-wibbling-kahn.md`

## Datakilder til mining
- `chatlog.md` — ~2500 beskeder, 30 sessions (PC)
- `projects/ydrasil/vps-chatlog.md` — 49K linjer (VPS sessions)
- `projects/auto-chatlog/abstracts.json` — session-abstracts for hurtig scanning
- `.claude/skills/` — eksisterende skills som reference for format/struktur

## Åbne tråde
- Dialectic-pipeline skill (plan→redteam→steelman→eval) er den mest oplagte kandidat — mønsteret blev brugt i dag og kostede ~200 ord at instruere
- Session-koordinering ("se hvad andre sessions laver") er et andet mønster der tog mange runder — måske et skill der scanner aktive JSONL-filer
- Projekt fra brief ("tag denne brief og gør den til et aktivt projekt") overlapper med `/new-project` men er mere end bare scaffolding

## Changelog
- 2026-03-17: Session 25 — VPS-sync + fuld deep dive. 5 nye filer: INVENTAR, SYNTESE, ARKITEKTUR, RED_TEAM, IMPLEMENTERING. Kill condition sat (5 sessioner). Næste: SKABELONER.md + arkiv/.
- 2026-03-14: Projekt oprettet. Baseret på session 315694ad's dialektiske analyse. Formålet skærpet fra "prompt-katalog" til "genanvendelige instruksskabeloner."

## Skabelon-feedback
Ved PDCA-evaluering, besvar:
- Hvilke template-filer blev brugt som de var?
- Hvilke blev ændret inden for de første 2 sessioner?
- Hvilke blev aldrig åbnet?
- Forslag til ændringer i template/?
