# Kapitelstruktur: Konkret forslag

**Dato:** 2026-03-16
**Kilde:** Voice memo session 24 + eksisterende PC/VPS struktur

---

## 1. Kapitler (topic-baseret)

| Nr | Kapitel | Dækker |
|----|---------|--------|
| 01 | SYSTEM | Arkitektur, infrastruktur, hooks, VPS-drift, hukommelse |
| 02 | TRANSPORT | TransportIntra webapp, rute 256, API, chauffør-docs |
| 03 | RESEARCH | AI frontier, LLM-landskab, videns-vedligeholdelse, bøger |
| 04 | VAERKTOEJER | MCP/skills, prompt-skabeloner, manuals, terminal, chatlog |
| 05 | FORRETNING | Bogføring, rejsebureau, udlæg, økonomi, Notion |
| 99 | ARKIV | Afsluttede/parkerede briefs og projekter |

**6 kapitler.** Automation absorberes i 01 (det ER system). Assistent absorberes i 05.

---

## 2. Filnavngivning

### Backlog-briefs (flade filer i roden)
```
{kapitel}.{projektnavn}.{status}.md
```

Status-suffikser:
- `.raw.md` — idé, ubehandlet
- `.brief.md` — beskrevet, venter på prioritering
- `.r2g.md` — ready-to-go, kan startes

Eksempler: `01.hybrid-search.brief.md`, `03.llm-benchmarks.r2g.md`, `05.e-conomic.brief.md`

### Graduerede projekter (mapper i roden): `{kapitel}.{projektnavn}/`

Indhold: `CONTEXT.md` (identitet+state), `progress.md` (sessionshistorik), arbejdsfiler.

---

## 3. Migrationsplan

### Fra PC (projects/)

| Nu | Nyt |
|----|-----|
| `0_backlog/*.md` | Briefs flyttes til rod med kapitelnummer-præfiks |
| `9_archive/` | `99.ARKIV/` |
| `BMS.auto-chatlog/` | `01.auto-chatlog/` |
| `DLR.session-blindhed/` | `03.session-blindhed.brief.md` (nedgradér til brief) |
| `KNB.manuals/` | `04.manuals/` |
| `LIB.research/` | `03.research/` |
| `LIB.ydrasil/` | `99.ARKIV/ydrasil-aera/` |
| `REF.mcp-skills-kompendium/` | `04.mcp-skills/` |
| `REF.prompt-skabeloner/` | `04.prompt-skabeloner/` |
| `REF.transportintra/` | `02.transportintra/` |
| `REF.vps-sandbox/` | `99.ARKIV/vps-sandbox/` |

### Fra VPS (projects/)

| Nu | Nyt |
|----|-----|
| `transport/` | `02.transportintra/` (merge med PC) |
| `assistent/` | `05.assistent.brief.md` (nedgradér — lille scope) |
| `rejse/` | `05.rejsebureau/` |
| `bogfoering/` | `05.bogfoering/` |
| `forskning/` | `03.research/` (merge med PC) |
| `arkitektur/` | `01.system/` |
| `automation/` | `01.automation.brief.md` (absorbér i system) |
| `notion/` | `05.notion.brief.md` (nedgradér — parkeret) |
| `research-architecture/` | `99.ARKIV/research-architecture/` |

---

## 4. Brief-skabelon

```markdown
# {kapitel}.{navn}

**Kapitel:** {nr} {KAPITELNAVN}
**Status:** raw | brief | r2g
**Oprindelse:** {dato}, {kilde}

## Hvad
1-3 sætninger. Hvad er problemet eller idéen.

## Hvorfor nu
Hvorfor er dette relevant lige nu. Hvis tomt → det er ikke.

## Succeskriterium
Én målbar ting der afgør om det er done.

## Næste handling
Præcis ét konkret step.
```

Max 20 linjer. Hvis en brief kræver mere, er den klar til graduering.

---

## 5. Gradueringskriterier

En brief bliver til en projektmappe når **mindst 2** af disse er sande:

1. Den har mere end én arbejdsfil (kode, data, research-output)
2. Den strækker sig over mere end 2 sessioner
3. Den har afhængigheder til andre briefs/projekter
4. Den kræver sin egen CONTEXT.md for at holde styr på state

Graduering: opret `{kapitel}.{navn}/`, flyt brief ind som CONTEXT.md, tilføj progress.md.

---

## 6. `ls`-output i ny struktur

```
$ ls ~/dev/Yggdra/

01.SYSTEM                      ← kapitel-header (tom fil, ren separator)
01.auto-chatlog/
01.hybrid-search.brief.md
01.system/

02.TRANSPORT                   ← kapitel-header
02.sortering-v2.raw.md
02.transportintra/

03.RESEARCH                    ← kapitel-header
03.llm-benchmarks.r2g.md
03.research/
03.session-blindhed.brief.md

04.VAERKTOEJER                 ← kapitel-header
04.context-engineering.brief.md
04.manuals/
04.mcp-skills/
04.prompt-skabeloner/

05.FORRETNING                  ← kapitel-header
05.bogfoering/
05.e-conomic.brief.md
05.notion.brief.md
05.rejsebureau/

99.ARKIV                       ← kapitel-header
99.ARKIV/

CLAUDE.md
CONTEXT.md
PROGRESS.md
chatlog.md
data/
scripts/
```

Kapitel-headere (`01.SYSTEM` etc.) er tomme filer — kun visuel separator i `ls`.

---

## 7. NOW.md og hooks

VPS-projekternes NOW.md → CONTEXT.md i den nye mappe. Indhold bevares.

Hooks (`save_checkpoint.py`, `load_checkpoint.sh`) tilpasses:
- Glob-pattern: `[0-9][0-9].*/CONTEXT.md` i stedet for `projects/*/NOW.md`
- ~5 linjer ændring per script

---

## 8. OpenClaw-agent vedligeholdelse

Shell-funktioner (ikke daemon) der kan:
1. Flytte brief ved statusskift: `mv 01.x.raw.md 01.x.brief.md`
2. Graduere brief → projekt: opret mappe, brief → CONTEXT.md
3. Arkivere til `99.ARKIV/` med dato-præfiks
4. Validere navngivning mod `{nn}.{navn}.{status}.md`

---

## Designbeslutninger

- **Numre = topic, IKKE prioritet.** Topics ændres sjældent, prioritet ugentligt.
- **Maks 8 kapitler.** Passer det ikke → 99.ARKIV.
- **Flat i rod, ingen projects/.** Voice memo krav: max 2-3 klik.
- **VPS og PC samme struktur**, gradvis migration.

*If it looks stupid but works, it ain't stupid.*
