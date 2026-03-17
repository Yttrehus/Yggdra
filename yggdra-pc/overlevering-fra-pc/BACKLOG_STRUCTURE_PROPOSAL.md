# Backlog-struktur: projects/ vs. flat kapitel-nummerering

**Dato:** 2026-03-16
**Kontekst:** Voice memo (session 24) foreslår at opløse projects/ og bruge kapitel-nummerering. PC-Claude var delvist uenig.

---

## Forslaget fra voice memo

Erstat `projects/` med flad kapitel-nummerering:
```
1_transport/
2_research/
3_automation/
...
```
Argument: enklere navigation, eksplicit prioritering via nummer.

## PC-Claudes modargument

projects/ med præfiks-system (BMS., REF., LIB., etc.) giver kategorisering uden at hardcode rækkefølge. Nummerering tvinger en prioritering der ændrer sig ugentligt.

---

## Analyse

### Fordele ved kapitel-nummerering
| Fordel | Vægt |
|--------|------|
| Simpel mental model — "projekt 2 = research" | Høj |
| `ls` sorterer automatisk efter nummer | Medium |
| Ingen præfiks-system at huske (BMS, REF, LIB...) | Høj |
| Visuelt tydeligt i terminal og filmanager | Medium |

### Ulemper ved kapitel-nummerering
| Ulempe | Vægt |
|--------|------|
| Numre hardcoder prioritet — ændres den, skal mapper omdøbes | Høj |
| Omdøbning bryder git history, scripts, imports, symlinks | Høj |
| Hvad gør man med nye projekter? Indsættes som 3b? Renummereres alt? | Medium |
| Numre siger intet om projektets *type* (reference vs. aktiv vs. arkiv) | Medium |

### Fordele ved projects/ med præfiks
| Fordel | Vægt |
|--------|------|
| Kategori synlig i navnet (REF = reference, LIB = library, DLR = deliverable) | Høj |
| Nye projekter tilføjes uden omdøbning af eksisterende | Høj |
| Git history stabil — stier ændres ikke | Høj |
| TRIAGE.md styrer prioritering separat fra filstruktur | Medium |

### Ulemper ved projects/ med præfiks
| Ulempe | Vægt |
|--------|------|
| Præfiks-systemet er en konvention der skal læres/huskes | Medium |
| 7+ præfiks-typer (BMS, REF, LIB, KNB, DLR, SIP, PoC) er mange | Høj |
| `ls` sorterer alfabetisk — BMS før DLR før KNB, ikke efter relevans | Lav |

---

## Anbefaling: Behold projects/, simplificér præfikser

**Kapitel-nummerering løser et reelt problem** (overskuelighed) men skaber et værre problem (rigiditet). Præfiks-systemet er den rigtige idé, men 7 præfikser er for mange.

### Forslag: 3 præfikser i stedet for 7

| Præfiks | Betydning | Eksempler |
|---------|-----------|-----------|
| `active.` | Aktivt arbejde med deadlines/leverancer | transport, automation |
| `ref.` | Opslagsværk, vedligeholdes løbende | mcp-skills, transportintra, research |
| `_archive/` | Afsluttet eller parkeret | gamle projekter |

```
projects/
├── 0_backlog/              ← uændret
├── _archive/               ← samlet arkiv
├── active.transport/
├── active.automation/
├── ref.research/
├── ref.mcp-skills/
├── ref.transportintra/
└── ref.prompt-skabeloner/
```

### Hvorfor dette er bedre end begge alternativer
1. **3 præfikser vs. 7** — nemt at huske, ingen lookup
2. **Stabil** — nye projekter tilføjes som `active.X` uden omdøbning
3. **`ls` sorterer fornuftigt** — `_archive`, `active.*`, `ref.*` (underscore sorterer først)
4. **Overskueligt** — visuelt klart hvad der er aktivt vs. reference
5. **Git-venligt** — én omdøbning nu, derefter stabilt

### Migration fra nuværende system
```
BMS.auto-chatlog → ref.auto-chatlog (det er tooling, ikke deliverable)
DLR.session-blindhed → active.session-blindhed (aktiv research)
KNB.manuals → ref.manuals
LIB.research → ref.research
LIB.ydrasil → ref.ydrasil
REF.mcp-skills-kompendium → ref.mcp-skills
REF.prompt-skabeloner → ref.prompt-skabeloner
REF.transportintra → ref.transportintra
REF.vps-sandbox → _archive/vps-sandbox
```

---

## Alternativ: Gør ingenting

PC-systemet virker. 24 sessioner er gennemført med det nuværende præfiks-system. Kris navigerer via TRIAGE.md og backlog-briefs, ikke via `ls projects/`. Refaktorering nu er overhead der ikke løser et akut problem.

**Anbefaling:** Parkér dette til næste gang strukturen faktisk generer. Hvis den ikke generer, er svaret allerede givet.
