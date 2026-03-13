# Auto-chatlog

## 0. Metadata
- **Status:** v3 fungerer — gap-baseret sektioner, subagent-abstracts, danske datoer. Mangler automatisering.
- **Oprettet:** 2026-03-11
- **Sidst opdateret:** 2026-03-13 (session 14, sen eftermiddag)
- **Ejer:** Yttre + Claude

## 1. Origin Story
Auto-chatlog opstod 11/3-2026 under session 9. Yttre observerede at Claude Codes .jsonl sessionsfiler vokser kontinuerligt men aldrig omdannes til læsbar chatlog automatisk. De manuelle chatlog-dumps (dump-chatlog.js + chatlogs/-mappen) krævede at Claude blev bedt om det eksplicit — og outputtet var en flad sekvens uden tidsopdeling eller navigation. Den første prototype blev bygget direkte i session 9, men Claude gik i bygge-mode for tidligt. Yttre kalibrerede: "spørg før du bygger." Tre design-iterationer fulgte: navigationslinks, referater, retskrivning — alt parkeret som fremtidige forbedringer. Format først, automatisering bagefter.

## 2. Current State
chatlog-engine.js v3 parser ~2500 beskeder fra 30 sessions. Producerer `chatlog.md` i repo-roden. Kører manuelt i to trin: engine → subagent.

**v3 implementeret (session 14):**
- ✅ Én fil: chatlog.md i roden
- ✅ Gap-baseret sektionering (90 min pause = nyt afsnit, på tværs af sessions)
- ✅ Subagent-genererede abstracts (1-4 sætninger per dag, 1-2 per sektion)
- ✅ Danske datoer i hovedindeks ("fredag d. 13/3-2026")
- ✅ Sessions fra 5 Claude-projektmapper samlet i én
- Kun beskeder — mangler tænkeblokke, tool calls, reasoning
- Navigation: hovedindeks → dato-kapitler → sektioner med prev/next

**Filer:**
- `chatlog-engine.js` — parser JSONL → chatlog.md + sections-digest.json
- `sections-digest.json` — komprimeret input til subagent (genereres af engine)
- `abstracts.json` — subagent-genererede abstracts (læses af engine)
- `redact-patterns.json` — dynamiske secret-patterns (tilføjes af subagent)

**Workflow:** `node chatlog-engine.js --digest` → spawn subagent → `node chatlog-engine.js`

**Checkpoint-integration** (trigger: `/checkpoint` eller ved milestone/pause):
1. Opdatér state-filer: rod-CONTEXT.md, PROGRESS.md, relevante projekt-CONTEXT.md
2. Kør `node chatlog-engine.js --digest`
3. Spawn subagent (haiku) til abstracts + token-review:
   - Læs `sections-digest.json`
   - Skriv dato-abstracts (1-4 sætninger) + sektions-abstracts (1-2 sætninger) til `abstracts.json`
   - Hvis `suspiciousTokens` i digest: vurdér og tilføj bekræftede til `redact-patterns.json`
4. Kør `node chatlog-engine.js` (full build med nye abstracts)
5. Git commit + push
6. Bekræft kort: hvad blev gemt, hvad er næste step

**Regler:**
- Opdatér KUN filer med reelle ændringer — ingen no-op commits
- CONTEXT.md: kort og præcis. En ny session skal kunne starte ved at læse den.
- PROGRESS.md: narrativt. Hvad *skete* og *hvorfor*.
- Afkryds hvert step med det samme — ikke i batches.

**Chatlog-search** (trigger: "hvad sagde vi om X?", "hvornår blev Y besluttet?"):
1. Læs `abstracts.json` — scan dato- og sektions-abstracts for relevante emner
2. Identificér den/de relevante sektioner (sektions-id fra abstracts)
3. Brug Grep-tool (ikke bash grep) til at søge i `chatlog.md` — afgræns til relevant sektion
4. Præsentér: dato, tidspunkt, hvem (YTTRE/CLAUDE), relevant passage
5. Hvis ikke fundet i chatlog: søg i PROGRESS.md → CONTEXT.md → `projects/*/CONTEXT.md` → `git log`
- Vis kun det relevante — aldrig hele filer
- Hvis søgningen tager mere end 3 forsøg, overvej om søgeordene er for generiske

## 3. Problem Statement
- **Hvad:** Claude Code sessionsfiler (.jsonl) er maskinlæsbare men ikke menneskelæsbare. Der er ingen automatisk omdannelse til chatlog. Manuelle dumps glemmes, og outputtet mangler tidsopdeling og navigation.
- **Hvorfor:** Yttre bruger chatlog som kontekst-kilde mellem sessioner og til retrospektiv ("hvad diskuterede vi?"). Uden læsbar chatlog er man afhængig af hukommelse eller at grave i rå JSONL.

## 4. Target State
Én chatlog.md med komplet sessionsdata (inkl. tænkeblokke og tool calls). Session-baseret inddeling med navigationslinks. Opdateres automatisk. Nøgleord via LLM. Semantisk søgbar via vector DB. Yttre kan finde en specifik diskussion på under 30 sekunder.

## 5. Architecture & Trade-offs
- **Node.js engine + Claude subagent:** Engine parser JSONL og laver struktur (billigt, deterministisk). Subagent skriver abstracts (dyrt, intelligent). Adskillelsen betyder at engine kan køre ofte, subagent kun ved behov.
- **Gap-baseret sektionering:** 90 min pause mellem beskeder = nyt afsnit. Virker på tværs af sessions (kl 23→01 = ét afsnit, 6 timer senere = nyt). Erstatter faste 2-timers blokke.
- **Brute-force rebuild:** Hele chatloggen rebuildes fra scratch ved hver kørsel. Simpelt, korrekt, men skalerer ikke til hundredvis af sessions.
- **Dansk tid:** UTC konverteres til Europe/Copenhagen. Vigtigt for korrekt datoskift.
- **Truncation:** Beskeder over 5000 tegn afkortes. Balancerer læsbarhed mod fuldstændighed.
- **System-noise filtrering:** `<system-reminder>`, `<ide_*>`, `<local-command>`, `<command-name>` tags springes over.

## 6. Evaluation
- Kan Yttre finde en specifik diskussion i chatlog.md under 30 sekunder?
- Kører chatlog-engine.js uden fejl efter 10+ sessions akkumuleret?
- Erstatter det reelt de manuelle chatlog-dumps?

## 7. Exit Criteria
- **Done:** Kører automatisk (hook eller file-watcher). Nøgleord-extraction er meningsfuld. Brugt friktionsfrit i 5+ sessioner. Gammel chatlogs/-mappe ikke savnet.
- **Demotion:** Fundamental arkitekturfejl (f.eks. JSONL-format ændres og parser bryder).
- **Sunset:** Hvis chatloggen aldrig konsulteres i 10 sessioner, er den cruft.

## 8. Implementation

### Fase 1: Parser-prototype ✅
- [x] chatlog-engine.js — parser .jsonl → chatlog.md
- [x] Dansk tid (UTC+1)
- [x] System-noise filtrering
- [x] Truncation af lange beskeder

### Fase 2: v3 — gap-baseret + subagent ✅
- [x] Gap-baseret sektionering (90 min threshold, cross-session)
- [x] Subagent-abstracts (dato-niveau + sektions-niveau)
- [x] Danske datoer med ugedage i indeks
- [x] Sessions samlet fra 5 projektmapper
- [x] --digest flag for subagent-workflow

### Fase 3: Automatisering
- [ ] File-watcher mode eller PostToolUse hook
- [ ] Automatisk subagent-kørsel ved nye sessions

### Fase 4: Intelligens
- [ ] Tænkeblokke, tool calls, reasoning i output
- [ ] Retskrivning af bruger-input
- [ ] Session-ID markering ved parallelle sessions

## 9. Changelog
- 2026-03-11 (session 9, ~09:30): Prototype bygget. 494 beskeder parset. UTC→dansk tid fikset. Kronologisk rækkefølge fikset. 2-timers tidsblokke tilføjet.
- 2026-03-11 (session 9, ~10:00): Nøgleord-extraction testet — frekvensbaseret, utilstrækkelig. LLM-baseret løsning parkeret.
- 2026-03-11 (session 11): Flytning til egen projektmappe. Gammel chatlogs/ pensioneret til archive/.
- 2026-03-12 (session 12): 1098 beskeder fra 6 sessions. Datoskift håndteret korrekt.
- 2026-03-13 (session 13): Strukturændring: projects/auto-chatlog/. ADR → CONTEXT.md. V2 krav defineret. V2 implementeret: live.md+archive.md → chatlog.md i roden. Hovedindeks + dato-kapitler + prev/next navigation.
- 2026-03-13 (session 14, tidlig): Sessions fra 5 Claude-projektmapper samlet i c--Users-Krist-dev-projects-Yggdra/. Input-sti opdateret. 2476 beskeder fra 30 sessions.
- 2026-03-13 (session 14, sen): v3 implementeret: gap-baseret sektionering (90 min), subagent-abstracts (dato + sektion), danske datoer. Frekvens-nøgleord erstattet. 2-timers blokke erstattet.

## 10. Backlog
- Automatisering (file-watcher eller hook)
- Tænkeblokke, tool calls, reasoning i output
- Inkrementel opdatering (ikke brute-force rebuild)
- Session-ID markering ved parallelle sessions
- Retskrivning af bruger-input
- Semantisk søgning via vector DB

## 11. Original Design
Denne CONTEXT.md er skrevet retroaktivt i session 12 som del af reformation fase 4. Ingen original dokumentation eksisterede — auto-chatlog startede som en ad-hoc prototype i session 9.
