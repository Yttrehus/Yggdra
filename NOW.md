# NOW — Hvor vi er

**Sidst opdateret:** 2026-03-11 23:10 (session 9, afslutning)
**Status:** M5 step 1-10 DONE. Project Reformation i DLR-fase — framework designet, triage udført, klar til fil-flytning.

## Næste step (start her)

**Næste session:** Implementér mappestrukturen (den store flytning).
1. Opret `_backlog/`, `PoC/`, `DLR/`, `SIP/`, `_ARC/` med README.md i hver
2. Flyt project-reformation/ → DLR/project-reformation/
3. Flyt auto-chatlog/ → SIP/auto-chatlog/
4. Opret backlog-briefs (13 stk) med cowork-output som rå input
5. Opret ADR.md for auto-chatlog, session-drift-pipeline, file-watcher, projekt-omdøbning, skill-arkitektur
6. Flyt implementation journals → _ARC/, PLAN.v1.md → _ARC/
7. ADR-INDEX.md i roden
8. Derefter: M5 step 11-17

## Hvad sessionen producerede

### M5 bloatware-fjernelse (step 10)
- 11 bloatware-apps fjernet via PowerShell
- PLAN.md step 2-10 markeret done (var glemt af checkpoint — strukturelt problem identificeret)

### Project Reformation (hovedfokus)

**Pipeline besluttet:** Backlog → PoC → DLR → SIP → BMS (roden)
- Stage = hvor i pipelinen (Backlog/PoC/DLR/SIP/BMS)
- Status = er det levende (Active/Deprecated/Archived)

**Filer oprettet i `project-reformation/`:**
- `ADR.md` — levende ADR for selve reformationen (DLR, Active)
- `ADR-template.md` — skabelon med 11 sektioner (Origin Story → Original ADR)
- `README-Backlog.md` — governance + brief-format for idéer
- `README-PoC.md` — governance for rå eksperimenter
- `README-DLR.md` — governance for aktiv research
- `README-SIP.md` — governance for sandbox/test
- `README-BMS.md` — governance for etableret fundament

**Design-beslutninger:**
- Roden ER BMS — etablerede ting flyttes ikke
- ADR bor med det den beskriver
- Stage og Status er to separate dimensioner
- Backlog-idéer bruger brief-format (opsummering → origin story → rå input)
- "brief" som term for idé-dokumenter
- Alle README'er har do/don't eksempler
- Origin Story øverst i ADR, Original ADR (frosset snapshot) nederst
- Current State med narrativ der forklarer hvad der er sket siden oprettelsen
- Changelog i dagbogsstil (nok kontekst, ikke telegram)

### Auto-chatlog (SIP)
- `auto-chatlog/chatlog-engine.js` — parser virker (503 beskeder, dansk tid, 2-timers blokke)
- Mangler: navigationslinks, file-watcher
- Kører parallelt med gammel `chatlogs/`

### Google AI Mode session
- Validerede pipeline-konceptet
- Gemt i `references/google-ai-samtale-rd-framework.md`

## Fil-status

```
project-reformation/     ← DLR: framework-design (7 filer)
auto-chatlog/            ← SIP: chatlog-prototype (3 filer)
chatlogs/                ← BMS: gammel chatlog (kører stadig)
references/              ← BMS (12 filer)
template/                ← BMS (8 filer)
.claude/skills/          ← BMS (6 skills)
.claude/implementation journals/  ← DEPRECATED: erstattes af ADR
```

## Planlagt rækkefølge

1. ~~Pipeline-navne~~ → DONE (Backlog/PoC/DLR/SIP/BMS)
2. ~~ADR-template~~ → DONE
3. ~~README'er per stage~~ → DONE
4. Triage PLAN.md idé-parkering → briefs i _backlog/ ← NÆSTE
5. Map eksisterende filer til ny mappestruktur
6. ADR-INDEX.md i roden
7. Navigationslinks i chatlog-engine.js
8. M5 step 11-17

## Vigtig kontekst

- Claude Code Bash-tool kører i Windows, ikke WSL
- Windows git konfigureret med SSH — Claude kan commit+push
- gh CLI autentificeret som Yttrehus (HTTPS)
- **INGEN session-save hook på PC** — NOW.md skal opdateres manuelt
- **Regel:** Spørg før du bygger. Diskussion færdig → bekræftelse → kode.

## Åbne tråde

- M5 step 11-17 (filsystem, X1, fonts, Dev Drive, wslconfig, quick reference)
- JetBrains Mono + Mermaid Preview extension
- Notion-struktur venter
- Poppler PATH-verifikation efter restart
- /new-project skill aldrig testet
- Prettier mangler .prettierrc
- 7 parallel task briefs i ~/parallel-tasks/
- Integrationer parkeret: Gmail, Hotmail, Google, mobil-adgang
- implementation journals/ → migreres til ADR ved fil-mapping
