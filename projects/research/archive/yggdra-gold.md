# Guldkorn fra Yggdra — destilleret til Basic Setup

Udtrukket 2026-03-10 fra VPS docs/, research/, projects/, DAGBOG.md.
Kilder angivet så næste session kan finde originalen.

---

## 1. Kendte fælder (fra MANUAL.md + DAGBOG 18. feb)

1. **Overplanlægning** — "Der hvor jeg har haft mest fremgang er når jeg bare har implementeret noget" (voice memo 2026-02-18 05:18)
2. **Falsk selvsikkerhed** — Claude *tror* den forstår. Mirror-princippet: genfortæl hvad du forstår FØR du handler
3. **Rigtige idéer skudt ned** — Når Yttre insisterer, er det sandsynligvis Claude der mangler kontekst
4. **Værktøjer glemt** — Claude "glemmer" tools mellem sessioner. Skills og hooks loader dem
5. **"Simpelt" = exact fit** — aldrig oversæt ambition til "gør mindre"

**Kilde:** `/root/Yggdra/docs/MANUAL.md`, `/root/Yggdra/docs/DAGBOG.md`

---

## 2. Arkitektur-principper (valideret i praksis)

- **Bash over MCP** — scripts > integrationer. Composable, verifiable.
- **State på disk** — NOW.md, episodes.jsonl, MEMORY.md. Alt i git.
- **Progressive disclosure** — load kun det relevante. Skills on-demand.
- **Kill conditions** — alt nyt definerer hvornår det fjernes.
- **Adoption over arkitektur** — byg kun det der faktisk bruges.
- **HOT/WARM/COLD memory** — NOW.md (hot), episodes.jsonl (warm), Qdrant (cold)

**Kilde:** `/root/Yggdra/projects/arkitektur/CONTEXT.md`, `/root/Yggdra/docs/ARCHITECTURE_CONTINUOUS_MEMORY.md`

---

## 3. Evaluering/beslutningsstruktur (spredt over 3 filer)

- **PRIORITIES.md** — Tier 0-3 rangering + decision matrix for konflikter
- **TRADEOFFS.md** — dokumenterede kompromiser med acceptable/unacceptable grænser
- **Popper-loop** — Byg → Evaluér → Notér → Parkér (i PLAN.md)
- **Mangler:** Retrospektiv per modul. DAGBOG fanger hvad der skete, men ikke "hvad lærte vi, hvad gør vi anderledes"

**Kilde:** `/root/Yggdra/PRIORITIES.md`, `/root/Yggdra/TRADEOFFS.md`

---

## 4. Session-management (det Yggdra har, PC mangler)

VPS hooks:
- `save_checkpoint.py` — Stop/PreCompact → Groq destillerer → episodes.jsonl + projekt NOW.md
- `load_checkpoint.sh` — SessionStart → injicerer alle projekters NOW.md + seneste 5 episoder
- Daglige checkpoints i `/root/Yggdra/data/checkpoints/` (80KB+ per dag)

PC har INGEN af dette. NOW.md opdateres manuelt. Løses i M7.

**Kilde:** `/root/Yggdra/scripts/save_checkpoint.py`, `/root/Yggdra/.claude/settings.local.json`

---

## 5. Relevant for M4 (projektstruktur)

### PC_SETUP.md foreslog (marts 2026):
```
~/Ydrasil/          # Klonet fra VPS
~/projects/
  ti-app/           # Eget repo
  revisor/          # Eget repo
```

### Yttre besluttede i stedet (denne session):
```
~/dev/
  projects/Basic Setup/   # Main workspace, sub-projekter vokser ud herfra
  archive/                # Afsluttede/gamle ting
  sandbox/                # Eksperimenter, throwaway
  tools/                  # CLI-værktøjer, scripts
  scripts/                # Yggdra PC-tools (ctx, tunnel)
  docs/                   # External reference docs
  BLUEPRINT.md            # Historisk reference
```

### Professionel konvention (fra research):
- Ét root (`~/dev/`), flat sub-organisation, max 2 niveauer
- Polyrepo for uafhængige projekter, monorepo kun ved delt kode
- Hvert projekt: `.gitignore`, `.editorconfig`, `.gitattributes`, `README.md`
- Dotfiles i separat repo (M4 step 4)
- Archive, don't delete

**Kilde:** `references/project-structure.md`, VPS `/root/Yggdra/docs/PC_SETUP.md`

---

## 6. HANDLINGSPLAN konsensusprincpper (fra 11 videoer)

1. Filesystem > RAG for struktureret viden
2. Progressive disclosure er nøglen til skalering
3. To-tier hierarki er optimalt (Planner → Workers → Judge)
4. Context engineering > model intelligence
5. Design for restart, ikke perfektion
6. Separation: Memory / Compute / Interface
7. Start simpelt, tilføj kompleksitet kun når simpelt fejler

**Kilde:** `/root/Yggdra/docs/HANDLINGSPLAN.md`

---

## 7. Ydrasil Atlas kategorier

Alt organiseret i 5 dimensioner med krydsreferencer:
1. **Projekter** — hvad vi bygger
2. **Struktur** — hvordan det er bygget
3. **Viden** — hvad vi ved
4. **Principper** — hvordan vi tænker
5. **Handlinger** — hvad vi skal gøre

**Kilde:** `/root/Yggdra/docs/YDRASIL_ATLAS.md` (27K, mest komplette overbliksfil)

---

## 8. Research-metodologi (allerede dokumenteret)

Fuld guide i `dev/archive/research archive/RESEARCH_METHODOLOGY_META.md`:
- Amateur vs professionel research (6 differentiators)
- Frameworks: Scoping Review, TCCM, ADO, CREDIBLE
- AI-assisted workflow: define → scan → verify → synthesize
- 30-sekunders kildetest: Hvem, Hvilken evidens, Hvem er uenig?
- Zettelkasten: fleeting → literature → permanent notes

**Kilde:** `c:\Users\Krist\dev\archive\research archive\RESEARCH_METHODOLOGY_META.md`
