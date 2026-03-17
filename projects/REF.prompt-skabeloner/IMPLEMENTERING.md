# Implementeringsplan — Prompt-arkitektur i Yggdra

Red team-justeret. Minimum viable, ikke maximum impressive.

---

## Handlinger (prioriteret)

### 0. Implementér destruktiv-kommando-guard (S — denne session, 30 min, GØR DETTE FØRST)
PreToolUse:Bash hook der blokerer `rm -rf /`, `docker system prune`, `git push --force`, og SSH-destruktive kommandoer. Patterns fra Nate Jones-dokumentet. Eneste handling der forhindrer datatab.

### 1. Opret SKABELONER.md — start tom, voks organisk (S — 5 min)
Nate Jones: *"You don't write a perfect rules file. You start with almost nothing. Then every time your agent does something wrong, you add a line."*

Opret SKABELONER.md med kun 1 mønster (struktureret opgave — den med højest dokumenteret first-shot success rate). Tilføj næste skabelon først når Yttre spontant bruger et genkendt mønster og tænker "det her har jeg skrevet før." Organisk vækst, ikke top-down design.

### 2. Flyt historiske filer til arkiv/ (S — 5 min)
- `VPS_HANDOFF.md` → `arkiv/`
- `BESKED_FRA_ANDEN_SESSION.md` → `arkiv/`

### 3. Overvej 1-2 skabeloner som skills (M — 30 min)
Konvertér "struktureret opgave" og "continuation" til `.claude/skills/` hvis det giver mening. Fordel: tilgængelige via `/skill-navn`. Ulempe: endnu 2 skills i en mappe med 13.

**Betingelse:** Gør det KUN hvis Yttre har brugt SKABELONER.md mindst 2 gange manuelt først. Byg ikke infrastruktur til noget der ikke bruges.

### 4. Ugentlig review-vane (S — 0 min at implementere, svær at opretholde)
Én gang om ugen (fx søndag): åbn INSIGHTS.md, læs nye fund. Opdatér SKABELONER.md hvis nødvendigt. Ingen automatik — bare en vane.

**Realistisk:** Dette sker sandsynligvis ikke. Men det er den eneste måde feedback-cirklen lukkes. Alternativ: lad det ske organisk når der er en ny VPS-sync.

### 5. Ryd duplikater (S — 10 min)
`projects/2_research/sources/` indeholder kopier af `data/vps-sync-20260316/sources/`. Beslut én kanonisk lokation. Anbefaling: behold `projects/2_research/sources/` og slet fra sync-mappen (sync-mappen er ephemeral).

### 6. Skær SYNTESE.md til 5 principper (S — 15 min, efter red team feedback)
Red team anbefaler max 5. De 5 der ændrer adfærd:
1. Context engineering > prompt engineering
2. Struktureret opgave = first-shot success
3. Én feature per session
4. State på disk
5. Feedback-loop (brudt — luk den)

De andre 4 er sande men ikke adfærdsændrende for Yttre specifikt.

### 7. Luk projektet midlertidigt (M — session efter handling 1-5)
Når handling 1-5 er gjort:
- Opdatér CONTEXT.md med "v1 leveret, i brug-test"
- Sæt kill condition (se nedenfor)
- Ingen flere ændringer i 2 uger

---

## Kill condition

**Luk projektet permanent hvis:** SKABELONER.md ikke er åbnet/brugt i 5 sessioner efter oprettelse.

**Mål det:** Næste gang du syncer chatlogs (chatlog-engine), grep for "SKABELONER" eller de 4 mønster-navne i Yttres prompts. Hvis 0 hits over 5 sessioner: arkivér hele REF.prompt-skabeloner/.

---

## Succeskriterium

1. **Minimum:** SKABELONER.md eksisterer med 4 mønstre. Historiske filer i arkiv. Duplikater ryddet.
2. **Godt:** Yttre har brugt mindst 1 skabelon spontant i 3/5 næste sessioner.
3. **Ideelt:** Feedback-cirklen er lukket — en INSIGHTS.md-opdatering har ført til en SKABELONER.md-ændring mindst 1 gang.

---

## Slutspørgsmål

**Gaven fra denne teknologi er:** evnen til at destillere 1.270 prompts, 16 research-kilder og 148 episoder til 4 genanvendelige mønstre og 5 principper på én eftermiddag.

**For at bruge den skal vi:** faktisk åbne SKABELONER.md næste gang vi sidder i Claude Code og tænker "hvordan formulerer jeg det her?"

**Det koster:** 20 minutter at oprette, 0 minutter at vedligeholde (medmindre feedback-vanen holder), og den mentale disciplin at bruge en skabelon i stedet for at taste det første der falder en ind.

**Er det det værd?** Ja — hvis det bliver brugt. Nej — hvis det bliver endnu en fil i et projekt der beskriver sig selv. Red team har været ærlig: mønsteret hidtil er research→rapport→hylde. Denne gang er testen simpel: 5 sessioner, 1 skabelon-brug per session. Hvis ikke, luk det.
