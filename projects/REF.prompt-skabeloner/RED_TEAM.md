# Red Team — Angreb på SYNTESE.md og ARKITEKTUR.md

---

## Angreb på SYNTESE.md

### Er syntesen cherry-picked?

**Ja, delvist.** De 9 principper er alle "god praksis" — ingen af dem er kontroversielle. Det der mangler:

1. **Principper der modsiger hinanden.** "Minimal prompt = nok" (princip 2) modsiger "struktureret opgave = first-shot success" (princip 3). En struktureret opgave med kontekst + output-spec + anti-patterns er per definition ikke minimal. Syntesen glatter denne spænding i stedet for at adressere den.

2. **Principper der fejler i praksis.** "Bevar fejl i konteksten" (princip 4) lyder godt, men Manus selv rapporterer at det fylder konteksten med noise efter 10+ iterations. Der er en grænse. Syntesen nævner den ikke.

3. **Kost-benefit mangler.** Princip 9 (feedback-loop) kræver at prompt_miner kører dagligt, at INSIGHTS.md læses, at skabeloner opdateres. Hvad koster det i tid? 30 min/uge? Er det det værd for en skraldemand der prompter 2-3 timer om dagen?

4. **METR-studiet ignoreres.** DESTILLAT_agents_automation nævner at AI-tools gør erfarne devs 19% langsommere. Men syntesen konklusion er "brug det mere." Hvad hvis svaret er "brug det mindre, men bedre?"

### Hvad ignorerer syntesen?

- **Emotionel tilstand påvirker prompts.** 35,8% Termux-tastefejl er ikke et prompt-problem, det er et interface-problem. Ingen prompt-skabelon fikser at man taster på en telefon i en lastbil.
- **Claude-versioner ændrer sig.** Halvdelen af principperne er version-specifikke (prefilling deprecated, XML tags, structured output). Om 3 måneder er halvdelen af syntesen forældet.
- **Solo-dev ≠ team.** Alle kilder (Anthropic, Manus, LangChain) er skrevet til teams. Yttres kontekst er fundamentalt anderledes: én person, intet code review, ingen kolleger der læser prompts.

---

## Angreb på ARKITEKTUR.md

### Er arkitekturen for ambitiøs?

Nej — den er faktisk minimalistisk nok. Ingen nye mapper, ingen migration, ingen ny infrastruktur. Det er dens styrke.

**Men:** Den tilføjer 3 nye filer (SKABELONER.md, ANTI_PATTERNS.md, arkiv/) til et projekt der allerede har 5 filer. 8 filer i et "reference-projekt" er på grænsen. Og hvem opdaterer dem?

### Vil det faktisk blive brugt?

**Det ærlige svar: sandsynligvis ikke.**

Bevisførelse:
- PROMPT_KATALOG.md har eksisteret på VPS i mindst en uge. Yttre har ikke åbnet den.
- MINING_RESULTS.md har eksisteret siden session 19 (14/3). Yttre har ikke refereret til den i en prompt.
- INSIGHTS.md ligger i en sync-mappe. Ingen har læst den manuelt.
- REF.prompt-skabeloner/ er oprettet session 18 (14/3) — 3 dage siden. Ingen af filerne er brugt til at ændre en eneste prompt.

**Mønsteret:** Research produceres → destilleres → arkiveres → glemmes. Arkitekturen ændrer ikke dette mønster — den organiserer det bare pænere.

### Hvornår har Kristoffer sidst åbnet en research-fil for at forbedre en prompt?

Baseret på tilgængelig data: **aldrig.** Research-filer produceres af Claude (på VPS eller PC). De læses af Claude (ved session-start eller sync). Yttre læser CONTEXT.md og PROGRESS.md. Det er det.

### Hvad er den simpleste version der giver 80% af værdien?

**Én fil. SKABELONER.md. Intet andet.**

- Kopiér de 3 mest brugte skabeloner direkte ind i CLAUDE.md under en ny sektion "Prompt-mønstre"
- Slet resten af projektet
- Prompt mining-data bliver på VPS og refereres ved behov

**Alternativt:** Gør de 3 bedste skabeloner til skills i `.claude/skills/`. Så er de tilgængelige via `/skabelon-navn` uden at åbne en fil.

---

## Reviderede anbefalinger

1. **Drop ANTI_PATTERNS.md.** Anti-patterns er allerede i INSIGHTS.md og CH7. Endnu en fil = endnu en fil der ikke læses.

2. **SKABELONER.md: ja, men max 4 skabeloner.** 8 er for mange. Vælg de 4 der matcher Yttres faktiske brug: (1) struktureret opgave, (2) implement-this-plan, (3) kør-løs med scope, (4) continuation. De andre er nice-to-have.

3. **SYNTESE.md: behold, men skær til 5 principper.** 9 er for mange at huske. De 5 der faktisk ændrer adfærd: context engineering > prompting, struktureret opgave, én feature per session, state på disk, feedback-loop.

4. **Arkiv: ja.** Flyt VPS_HANDOFF og BESKED til arkiv. Det er ren oprydning.

5. **INVENTAR.md: behold som reference.** Den er nyttig for fremtidige sessioner der skal finde materiale.

6. **Test det.** I de næste 5 sessioner, brug SKABELONER.md mindst 1 gang per session. Hvis det ikke sker spontant, er projektet shelf-ware og bør lukkes.
