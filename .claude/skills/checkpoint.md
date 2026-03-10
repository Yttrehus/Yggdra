# Skill: checkpoint

Session-checkpoint: gem alt state til disk i ét kald.

## Trigger

`/checkpoint` eller når Claude vurderer det er tid (efter milestone, før pause, ved vigtig beslutning).

## Hvad den gør

Kør alle 5 trin i rækkefølge:

### 1. Opdatér state-filer
- **NOW.md** — opdatér status, næste step, beslutninger, åbne tråde
- **PROGRESS.md** — append hvad der skete siden sidst (kort, narrativt)
- **PLAN.md** — markér steps done, tilføj nye idéer til parkering hvis relevant

### 2. Dump chatlog
```bash
node "C:/Users/Krist/dev/projects/Basic Setup/chatlogs/dump-chatlog.js"
```

### 3. Git commit + push
```bash
git add -A && git commit -m "checkpoint: [kort beskrivelse]" && git push
```
Commit-besked skal beskrive *hvad der blev opnået*, ikke "update files".

### 4. Bekræft
Vis kort: hvad blev gemt, hvad er næste step.

### 5. Skill-feedback (intern)
Efter hver brug, notér kort i `.claude/implementationlogs/checkpoint.md`:
- Tog det for lang tid? Blev noget glemt? Var rækkefølgen forkert?
- Virkede det friktionsfrit eller krævede det manuel korrektion?

## Regler

- Opdatér KUN filer der har reelle ændringer — ingen no-op commits
- NOW.md: kort og præcis. En ny session skal kunne starte ved at læse den.
- PROGRESS.md: narrativt, ikke bullet-points af commits. Hvad *skete* og *hvorfor*.
- PLAN.md: rør den kun hvis steps faktisk er afsluttet eller planen er ændret
- Chatlog-dump: brug altid seneste session (ingen args til dump-chatlog.js)

## Hvornår

- Yttre siger `/checkpoint`
- Efter afsluttet step/milestone (Claude foreslår det)
- Før session slutter
- Før compact

## Evaluering

**Obligatorisk evaluering efter 5 brug.** Ved evaluering, besvar:

- Hvor mange gange blev /checkpoint brugt?
- Hvor mange gange krævede det manuel korrektion bagefter?
- Var der state der gik tabt trods checkpoint? Hvad?
- Blev PROGRESS.md for lang/ulæselig?
- Blev chatlog-dump faktisk brugt som reference? Af hvem?
- Skal rækkefølgen ændres?
- Skal noget tilføjes/fjernes?

Resultatet af evalueringen skrives i PLAN.md under PDCA-evaluering og bruges til at justere denne skill.

Feedback-log: `.claude/implementationlogs/checkpoint.md`
