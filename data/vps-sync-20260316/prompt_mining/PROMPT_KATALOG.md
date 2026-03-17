# Prompt Katalog — Afprøvede skabeloner

Samling af prompt-typer der har vist sig effektive. Copy-paste klar.
Opdateres løbende baseret på prompt_miner analyse og erfaring.

---

## 1. Struktureret opgave med regler og anti-patterns

**Hvornår:** Store opgaver med klart mål men risiko for drift.

```
KONTEKST: [Hvad er status, hvad er sket]

OPGAVE: [Præcis leverance — antal, format, done-kriterium]

REGLER:
1. UDFØR handlinger — snak ikke om dem
2. Svar kort med hvad du HAR GJORT
3. [Anti-patterns specifik for opgaven]

PRE-FLIGHT:
- [Verificerings-kommandoer]

DONE = [Præcis definition af færdig]
```

**Eksempel:** Trello-agent, overleveringsopdatering, mega-sessions.

---

## 2. Implement-this-plan

**Hvornår:** Plan er allerede tænkt igennem, Claude skal eksekvere.

```
Implement the following plan:

# Plan: [Navn]

## Kontekst
[Baggrund]

## Steps
1. [Step 1]
2. [Step 2]

## Done = [Kriterium]
```

**Eksempel:** Cytoscape mindmap, Groq harness migration.

---

## 3. Iterative loops med human-in-the-loop

**Hvornår:** Mange små opgaver, behov for retningskontrol undervejs.

```
KONTEKST: [Status]

METODE: Iterative loops med human-in-the-loop checkpoint.
- Kør 3 loops autonomt per runde (scan → beslut → eksekvér → verificér)
- Efter hver runde (3 loops): STOP og skriv status-tabel:
  | Loop | Hvad | Resultat | Fil/ændring |
  Vent derefter på "ok" eller korrektion før næste runde.
- Hvis et loop fejler: dokumentér fejlen, spring videre, tag det med i status.
- Maks 4 runder (12 loops total). Hellere 9 solide end 12 halvfærdige.

PRE-FLIGHT:
- [Verificerings-kommandoer]

LOOP-KILDE: Scan disse for opgaver, prioritér efter impact/effort:
1. [Kilde 1]
2. [Kilde 2]

LOOP-REGLER:
- Hvert loop = én afgrænset opgave med kørbar output
- Smoke test obligatorisk per loop
- Ingen rapporter som leverance — kun kørbare ting

ANTI-PATTERNS:
- Rapport → STOP, omformulér til kørbar leverance
- >5 min per loop → TIMEOUT, gå videre
- I tvivl om scope → vælg det mindre

DONE = status-tabel + "Venter på go/korrektion"
```

**Eksempel:** Backlog burn, cron cleanup, VPS sterilisering.

---

## 4. Kør-løs med konkret scope

**Hvornår:** Ambitiøs opgave, klart mål, frie tøjler.

```
[Beskriv opgaven naturligt]
Output = [hvad der skal produceres]
Maks [begrænsning]
```

**Eksempel:** "Alt research i udbakken, arrangeret efter dato."

---

## 5. N leverancer — frie tøjler inden for rammer

**Hvornår:** Sessioner med flere uafhængige opgaver.

```
KONTEKST: [Status]

OPGAVE: 3 leverancer — frie tøjler inden for disse rammer:

1. **[Leverance 1]** → [beskrivelse]. Output = [format].
2. **[Leverance 2]** → [beskrivelse]. Output = [format].
3. **Valgfri leverance** → Find selv den opgave med højest impact/effort.

METODE: Parallelle agenter til uafhængige opgaver. Sekventiel for afhængige.
SCOPE: Ingen nye services uden kill condition. Maks N leverancer.
DONE = status-tabel: leverance | fil | smoke test | tid brugt.
```

**Eksempel:** Mega-prompt session 16/3 (overlevering + prompt miner + heartbeat).

---

## 6. Kommando med fil-reference

**Hvornår:** Korte opgaver hvor kontekst er i en fil.

```
[Imperativ handling] [filsti]
```

**Eksempel:** "tjek DEPLOY_INSTRUCTIONS.md i yggdra-pc/", "opdatér projects/transport/NOW.md med seneste status"

---

## 7. Cross-repo sync + helhedsvurdering

**Hvornår:** Ny session på ét repo skal absorbere alt nyt fra det andet repo, vurdere og handle.

```
FASE 0: Hent data via scp/rsync. Stop. Vent på "værsgo".
FASE 1-N: Autonome faser (absorption → konvergens → red team → handlingsplan).
Brug subagenter til fillæsning. Kontekst-checkpoint mellem faser.
Hvis kontekst løber tør → skriv FORTSAET.md med continuation-prompt.
```

**Eksempel:** PC-Yggdra session 23 mega-prompt (9 faser, VPS-absorption + prompt-arkitektur).

---

## 8. Kontekst-bevarende continuation

**Hvornår:** Opgaven er for stor til ét kontekstvindue.

```
Mellem hver fase: vurdér "Har jeg nok kontekst til resten med kvalitet?"
Hvis nej:
1. Skriv alt produceret til disk
2. Skriv FORTSAET.md med: hvad er gjort, hvad mangler, præcis kontekst
3. Stop og bed bruger starte ny session med FORTSAET.md
```

**Signal:** Partial output > dårlig output. Ærlig stop > forceret afslutning.

---

## Meta

- **Kilde:** prompt_miner.py analyse af 1270 prompts fra 246 sessioner
- **Insights:** Se `INSIGHTS.md` i samme mappe
- **Opdateret:** 2026-03-16
- **Kill condition:** Fjern hvis ikke refereret i 30 dage
