# VPS Reformation Blueprint — "Fortsæt hvor du slap"

**Dato:** 16. marts 2026
**Formål:** Design for at gøre VPS og PC nærmest identiske, så Kris kan skifte mellem dem seamlessly.
**Status:** UDKAST — kræver Kris' beslutning på flere punkter.

---

## 1. Visionen

**Ideal:** Log ind på VPS → se præcis samme state som PC havde → fortsæt arbejdet.

**Praktisk:** VPS og PC deler ét git-repo med identisk CLAUDE.md, hooks og projektstruktur. Qdrant kører kun på VPS (PC bruger SSH-tunnel). State-filer har maskin-ID så de ikke konflikter.

---

## 2. Anbefalet Arkitektur: "Shared Repo, Split State"

```
Git Repo: Yggdra (ét repo, begge maskiner)
├── CLAUDE.md              ← IDENTISK på begge
├── CONTEXT.md             ← Delt state (sidst-skrivende vinder)
├── BLUEPRINT.md           ← Delt
├── PROGRESS.md            ← Delt (append-only, ingen konflikter)
├── projects/              ← Delt, identisk struktur
│   ├── */CONTEXT.md       ← Delt per-projekt state
│   └── */NOW_vps.md       ← Maskin-specifik checkpoint
│       */NOW_pc.md
├── research/              ← Delt
├── data/
│   ├── episodes.jsonl     ← Delt (append-only)
│   ├── MORNING_BRIEF.md   ← VPS genererer, PC læser
│   ├── HEARTBEAT.md       ← VPS config
│   └── checkpoints/       ← Maskin-specifikke (.gitignore)
├── scripts/               ← VPS-specifikke (cron, embedding)
├── app/                   ← VPS-specifik (produktion)
└── .claude/
    ├── settings.local.json ← Maskin-specifik (.gitignore)
    └── skills/             ← Delt
```

### Nøgleprincip: State-filer med maskin-ID

I stedet for at VPS og PC kæmper om NOW.md, skriver hver sin:
- `NOW_vps.md` — VPS checkpoint
- `NOW_pc.md` — PC checkpoint
- `CONTEXT.md` — delt, opdateres af den der sidst arbejdede

SessionStart-hook læser BEGGE:
```bash
# load_checkpoint.sh
echo "## VPS sidst:" && cat projects/*/NOW_vps.md
echo "## PC sidst:" && cat projects/*/NOW_pc.md
echo "## Delt state:" && cat CONTEXT.md
```

### Merge-protokol

1. **Automatisk (ingen konflikter):** episodes.jsonl (append-only), PROGRESS.md (append-only), research/ (nye filer)
2. **Sidst-skrivende vinder:** CONTEXT.md, projects/*/CONTEXT.md
3. **Aldrig auto-merge:** CLAUDE.md (ændringer aftales), scripts/ (VPS-ejer), app/ (VPS-ejer)

---

## 3. Hvad skal konvergeres

### 3.1 CLAUDE.md

PC og VPS har forskellige CLAUDE.md. De skal merges til én:

| Dimension | PC nu | VPS nu | Konvergeret |
|-----------|-------|--------|-------------|
| Identitet | "Personligt udvikler-fundament" | "Personligt vidensystem" | Begge |
| Projekter | Stage-præfiks (BMS., REF.) | Simple navne (transport, assistent) | **BESLUTNING KRÆVES** |
| Workflow | "Spørg før du bygger" | "Bare gør det" | **BESLUTNING KRÆVES** |
| Hooks | 4 hooks | 3 hooks | 4 hooks (tilføj UserPromptSubmit på VPS) |
| Auto-load | CLAUDE.md + @CONTEXT.md | CLAUDE.md + hooks injicerer | Konvergér til @CONTEXT.md |
| Compaction | Explicit compaction-regler | Ingen | Tilføj på begge |

### 3.2 Projekt-navne

**Option A:** Adoptér PC-konventionen (stage-præfiks)
```
transport → REF.transportintra
forskning → LIB.research
automation → BMS.automation
```
- Fordel: Konsistent med PC
- Ulempe: VPS har 614 episoder + hooks der refererer gamle navne

**Option B:** Adoptér VPS-konventionen (simple navne)
```
BMS.auto-chatlog → auto-chatlog
REF.transportintra → transportintra
LIB.research → research
```
- Fordel: Simpelt, ingen præfiks at huske
- Ulempe: PC har 24 sessioners historie med gamle navne

**Option C:** Ny konvention (fra BACKLOG_STRUCTURE_PROPOSAL.md)
```
active.transport
active.automation
ref.research
ref.transportintra
_archive/vps-sandbox
```
- Fordel: 3 præfikser vs. 7, nemt at huske
- Ulempe: Kræver rename på begge

**Anbefaling:** Option C — det er det simpleste der giver mening for begge.

### 3.3 Hooks

VPS mangler `UserPromptSubmit` hook. PC har det som `post_session_check.sh`.

**Plan:**
1. Portér PC's `post_session_check.sh` til VPS
2. Tilpas til VPS-kontekst (tjek CONTEXT.md i stedet for marker-filer)
3. Begge maskiner: SessionStart, PreCompact, UserPromptSubmit, Stop

### 3.4 Research-struktur

PC bruger `INDEX.md` + `_inbox/` + `_archive/` + `reports/`.
VPS bruger flad 97-fil-struktur.

**Plan:**
1. VPS adopterer PC-strukturen
2. VPS /research/ reorganiseres med INDEX.md og undermapper
3. RESEARCH_CATALOG.md erstattes af INDEX.md

---

## 4. Qdrant-strategi

**Princip:** Qdrant kører KUN på VPS. PC bruger SSH-tunnel.

```
VPS Qdrant (master):
├── knowledge  (2450 pts) ← Begge feeder
├── episodes   (59 pts)   ← Begge feeder
├── advisor_brain (453)   ← VPS vedligeholder
├── miessler_bible (102)  ← VPS vedligeholder
├── routes (40K)          ← VPS vedligeholder (TransportIntra)
└── docs (1466)           ← MIGRER til knowledge, derefter slet

PC:
└── ctx "query" via SSH   ← ssh root@72.62.61.51 ctx "query"
    ELLER
    memory.py search      ← Lokal hybrid search med SSH-tunnel til Qdrant
```

**PC's memory.py:**
- Skrives om til at bruge VPS Qdrant via SSH-tunnel i stedet for lokal Qdrant
- Ingest sker via VPS (push ændrede filer → VPS embedder)
- ELLER: PC embedder lokalt og pusher til VPS Qdrant via API

---

## 5. Sync-flow (dagligt)

```
MORGEN (automatisk):
  VPS: morning_brief.py → MORNING_BRIEF.md
  VPS: git commit + push
  PC:  git pull (Obsidian Git eller manuelt)
  PC:  Læs MORNING_BRIEF.md → start dagen

ARBEJDE (løbende):
  PC/VPS: Arbejd → commit + push til main
  Anden maskine: git pull ved næste session
  Hooks: save_checkpoint.py → NOW_{maskin}.md → commit

AFTEN (automatisk):
  VPS: auto_dagbog.py → DAGBOG.md
  VPS: git commit + push
```

**Konflikthåndtering:**
- State-filer (NOW_*.md): maskin-specifik, ingen konflikt
- CONTEXT.md: sidst-skrivende vinder (accept)
- Research: nye filer, ingen konflikt
- Scripts: VPS ejer, PC rører ikke

---

## 6. Migrations-plan

### Fase 0: Forberedelse (VPS, uden PC)
- [x] VPS Sundhedstjek skrevet
- [x] Memory cleanup (221→74 linjer)
- [x] GPU packages slettet (6.7 GB)
- [x] Research-kvalitetsaudit
- [ ] Denne blueprint
- [ ] Git commit af uncommittet arbejde

### Fase 1: Beslutninger (kræver Kris)
- [ ] Vælg projekt-navne konvention (A/B/C)
- [ ] Vælg workflow-mode ("spørg først" vs "bare gør det" — eller kontekstafhængig)
- [ ] Bekræft Qdrant-strategi (VPS-only vs. dual)
- [ ] SSH-nøgle setup for password-auth deaktivering

### Fase 2: Konvergering (PC + VPS)
- [ ] Merge CLAUDE.md til én version
- [ ] Rename projects/ til valgt konvention (begge maskiner)
- [ ] Portér UserPromptSubmit hook til VPS
- [ ] Reorganisér VPS /research/ til INDEX.md struktur
- [ ] Opsæt SSH-tunnel alias på PC (`alias ctx='ssh root@72.62.61.51 ctx'`)

### Fase 3: Verifikation
- [ ] Test: PC commit → VPS git pull → VPS ser ændring
- [ ] Test: VPS checkpoint → PC git pull → PC ser state
- [ ] Test: ctx-søgning fra PC via SSH
- [ ] Test: Begge maskiner kan starte session med fuld kontekst

---

## 7. Åbne spørgsmål til Kris

1. **Projekt-navne:** Option A (PC-stil), B (VPS-stil), eller C (active/ref/_archive)?
2. **Workflow:** "Spørg først" (PC) eller "bare gør det" (VPS) — eller begge afhængig af kontekst?
3. **SSH-nøgler:** Er de sat op? Kan vi deaktivere password-login?
4. **Qdrant:** VPS-only (PC bruger SSH) eller dual (PC har lokal Qdrant)?
5. **Obsidian:** Parkeret, men fits godt med denne arkitektur. Fase 0 test stadig relevant?
6. **N8N:** Fjernet fra docker-compose — er det bevidst?

---

*Blueprint genereret kl. 12:58, mandag 16. marts 2026.*
*Kræver Kris' beslutninger på 6 punkter før implementation kan starte.*
