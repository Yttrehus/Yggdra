# Arkitektur-forslag — Prompt-viden i Yggdra

---

## Problemet

Prompt- og context engineering viden er spredt over 3+ lokationer, 20+ filer, to maskiner. Ingen vet hvor man finder "den gode skabelon" eller "det princip fra Anthropic". Forskellen mellem research og brug er en mappe-sti man ikke husker.

## Foreslået struktur

Arbejd inden for det der eksisterer. Ingen ny mappe-migration.

```
projects/REF.prompt-skabeloner/
├── CONTEXT.md              ← projekt-state (eksisterer)
├── INVENTAR.md             ← hvad vi har (ny, denne session)
├── SYNTESE.md              ← destillerede principper (ny, denne session)
├── ARKITEKTUR.md           ← denne fil
├── SKABELONER.md           ← 8 copy-paste skabeloner (absorberet fra PROMPT_KATALOG)
├── ANTI_PATTERNS.md        ← hvad der IKKE virker (fra INSIGHTS + CH7)
├── MINING_RESULTS.md       ← chatlog-mining (eksisterer)
└── arkiv/
    ├── VPS_HANDOFF.md      ← historisk
    └── BESKED_FRA_ANDEN_SESSION.md  ← historisk
```

Research-kildefiler **bliver hvor de er** (`data/vps-sync-20260316/sources/`, `projects/2_research/sources/`). De er reference, ikke daglig brug. SYNTESE.md er indgangen — den refererer til kilderne.

## Hvor bor hvad?

| Type | Lokation | Formål |
|---|---|---|
| **Skabeloner** (copy-paste) | `REF.prompt-skabeloner/SKABELONER.md` | Daglig brug. 8 mønstre med eksempler |
| **Principper** (destilleret) | `REF.prompt-skabeloner/SYNTESE.md` | Reference. De 9 principper med kilder |
| **Anti-patterns** | `REF.prompt-skabeloner/ANTI_PATTERNS.md` | Hvad man IKKE skal gøre |
| **Research-kilder** | `data/vps-sync-20260316/sources/` + `projects/2_research/sources/` | Dyb reference. Læses ved behov |
| **Mining-output** | `data/vps-sync-20260316/prompt_mining/` | Rå data. Prompt miner kører dagligt på VPS |
| **Destillater** | `yggdra-pc/overlevering-fra-vps/DESTILLAT_*.md` | VPS-producerede sammenfatninger |
| **Skills** | `.claude/skills/` | Operationelle skills der bruges af Claude Code |

## Videns-flow

```
Research-kilder (papers, blogs, docs)
    ↓ VPS prompt_miner + manuelt
Mining-output (INSIGHTS.md, analysis.jsonl)
    ↓ destillering
SYNTESE.md (9 principper) + SKABELONER.md (8 mønstre) + ANTI_PATTERNS.md
    ↓ daglig brug
Yttres prompts i Claude Code
    ↓ prompt_miner analyserer
Mining-output (feedback-loop)
```

**Cirklen er i dag brudt** mellem "daglig brug" og "mining-output." Prompt miner analyserer, men resultatet bliver ikke til ændrede skabeloner eller opdaterede principper. Det kræver en periodisk review — ikke automation, bare en vane: "en gang om ugen, læs INSIGHTS.md, opdatér SKABELONER.md hvis nødvendigt."

## Hvad ændrer sig på VPS?

Ingenting. VPS kører prompt_miner dagligt og producerer INSIGHTS.md + PROMPT_KATALOG.md. PC henter dem ved sync. Ingen duplikering af pipeline.

## Hvad ændrer sig på PC?

1. `PROMPT_KATALOG.md` absorberes som `SKABELONER.md` i REF.prompt-skabeloner/
2. Anti-patterns samles fra INSIGHTS + CH7 i `ANTI_PATTERNS.md`
3. Historiske filer flyttes til `arkiv/`
4. CONTEXT.md for projektet opdateres

Det er det. Ingen ny infrastruktur, ingen nye mapper, ingen migration.
