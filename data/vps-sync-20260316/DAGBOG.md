# Arbejdsdagbog

Løbende noter om hvad vi bygger, beslutninger, og mønstre i arbejdet.

---

## 2026-01-25: Projekt opstart

### Hvad vi lavede
- Reverse-engineered TransportIntra webapp → lokal klon i `/app/`
- Dark mode CSS
- API debug logging
- Analyseret 577 rutefiler, 40.053 stops
- Dokumenteret getRute API schema (`/data/GETRUTE_SCHEMA.md`)
- Bygget RuteMap med SVG markers, farvekoder, navigation

### Beslutninger
- Køre webapp lokalt men tale med rigtig TI-server (proxy-approach)
- Bruge Google Maps API til kortvisning (allerede i TI-koden)
- Pass-through logging i n8n (lad AI gøre analysen)

### Tekniske observationer
- TI API bruger negativ rute_id i responses (-232 vs 232)
- 100% GPS dækning i rutedata
- 48% har forskellig kunde/work adresse
- Status 50 = normal fuldført (93.8% af stops)

---

## 2026-01-26: Extra Route feature + Kort-forbedringer

### Hvad vi lavede
- **Extra Route overlay** - Kan tilføje ruter fra andre dage oven på aktuel rute
  - Kompakt popup med dansk kalender (Ma-Sø)
  - Farvekodede pins per ekstra rute
  - Fuldt interaktive stops (Kør, Pluk, sorter) med korrekt API-kald til rigtig rute_id
- **Kort-forbedringer**
  - Dark mode default ON med checkbox toggle
  - Vis alle / Følg / Mørk / Centrér knapper i bunden af kortet
  - Centrér-knap: zoom til 10km radius omkring min position
  - Fix: kun én rød prik (min position), ikke spor af gamle positioner
  - Fix: pins forsvinder når stops afsluttes (både hoved- og ekstra ruter)
- Webapp kører som systemd service (port 3000, auto-start ved reboot)

### Tekniske udfordringer løst
- `updateMyPos` overskrev debug-panel → fjernet
- Ekstra rute pins forsvandt ikke ved fjernelse → tilføjet `ruteMap.initMap()` kald
- Afsluttede ekstra-rute stops beholdt pins → server kan returnere gammel status, nu force-opdateres lokalt
- Flere røde prikker → async `addMyPos` callback ryddede ikke gamle markers, nu fjernes de først

### Mønstre i arbejdet
- Kris tester live på telefon mens vi udvikler
- Iterativt: lav ændring → genstart service → test → feedback → fix
- UI-feedback er primært visuel ("jeg ser X men forventede Y")
- Kris tænker i brugsscenarier: "når jeg er på tirsdagsruten og vil se mandagens stops"

---

## Kris' arbejdsprofil
- **Rolle:** Chauffør, Rute 256, organisk affald, Aarhus-området
- **Enhed:** Telefon (horisontal = kort, vertikal = liste)
- **Arbejdsmønster:** Kører ruter dagligt, vil optimere med data fra andre dage
- **Teknisk niveau:** Forstår API-koncepter, kan læse kode, tænker i features
- **Kommunikation:** Dansk, kortfattet, visuel feedback

---

## 2026-01-27: PAI Framework + Waypoints

### Hvad vi lavede
- **PAI Blueprint** - Komplet dokumentation af Miessler's PAI v2 arkitektur
- **TELOS framework** - Skabelon til kerneværdier, mission, mål, strategier
- **Waypoints system** helt nyt:
  - Stop-waypoints (per adresse): "Her er indkørslen", "Container bag bygning"
  - Globale pins (altid synlige): Tank, hjem, depot, genbrugsstation
  - Emoji-picker (15 ikoner)
  - Map-pick: Klik på kort for at vælge koordinater
  - Grupper med toggle-knapper i toolbar
- **Coordinate fixes** - Lokal GPS-korrektion for stops med forkerte koordinater
- **UI_ELEMENTS.md** - Komplet dokumentation af alle UI-elementer og JS-objekter

### Beslutninger
- Waypoints gemmes i localStorage (simpelt, virker offline)
- Gruppering af globale pins (tank, hjem, etc.) for nem toggle
- Stop-waypoints kobles til adresse+postnr (ikke disp_id, da det ændrer sig)

### Tekniske observationer
- Map-pick kræver reference til Google Maps instance (waypointUI._mapRef)
- Emoji som ikon fungerer godt i SVG markers

---

## 2026-01-28: Distance Service + Arrival Predictor + GPS Recording

### Hvad vi lavede
- **Distance Service** (`distanceService.js`):
  - Henter køretid/afstand via Google Maps DistanceMatrix API
  - Batching: Max 25 destinationer per request
  - Cache: Genberegner kun når GPS har flyttet sig >300m
  - Viser "3,2 km · 8 min" på kort-pins
- **Arrival Predictor** (smart feature!):
  - Lærer Kris' personlige køremønster over tid
  - Tracker: Hvornår blev stop aktivt → hvornår ankom GPS inden for 100m
  - Beregner ratio (faktisk tid / Google's estimat)
  - Vægtet gennemsnit: Nyere observationer tæller mere (3% decay)
  - Eksempel: Hvis Kris konsekvent bruger 18% længere tid → faktor 1.18
  - Alle fremtidige Google-estimater ganges med faktoren
- **GPS Recording** (GPSTracker.js):
  - Start/pause/stop optagelse af kørselsrute
  - Punkt hvert 3. sekund med lat/lng/accuracy/speed/heading
  - Km-tracking undervejs
  - Gem til localStorage med export som JSON
  - Live visning af optaget rute på kortet (orange linje)
- **RuteMap opdateringer**:
  - Waypoint-markers (stop + globale)
  - Distance labels på pins
  - updateDistanceLabels() til refresh uden fuld initMap()
- **Ruter.js opdateringer**:
  - Extra route header i rutelisten
  - Kort opdateres når stop afsluttes

### Tekniske observationer
- DistanceMatrix har limit på 25 destinations per request → batching nødvendig
- Arrival predictor clamps faktor til 0.5-3.0 for at undgå outliers
- GPS recording bruger enableHighAccuracy + maximumAge: 0 for præcision

### Mønstre i arbejdet
- Fokus på "læring over tid" features (arrival predictor)
- Data gemmes lokalt først, cloud sync kan komme senere
- Bygger på eksisterende Google Maps integration

---

## 2026-01-28 (fortsat): Qdrant Integration + Task Router

### Hvad vi lavede
- **Qdrant Vector Database** op og kører:
  - 40.053 rute-punkter embedded (routes collection)
  - 31 samtale-punkter embedded (conversations collection)
  - OpenAI text-embedding-3-small (1536 dimensioner)
- **Scripts oprettet:**
  - `embed_routes.py` - Embed rutedata til Qdrant
  - `embed_conversations.py` - Embed CHATLOG til Qdrant
  - `search.py` - Søg i collections
  - `get_context.py` - Hent formateret kontekst (kombineret søgning)
  - `token_tracker.py` - Log og analysér token-forbrug
  - `task_router.py` - Klassificér opgaver og anbefal model
- **Task Router kategorier:**
  - LOOKUP → Haiku (data-opslag, facts)
  - FORMAT → Haiku (formatering, konvertering)
  - EDIT_SIMPLE → Sonnet (små kodeændringer)
  - EDIT_COMPLEX → Opus (refactoring, nye features)
  - ANALYSIS → Opus (research, planlægning)
  - CHAT → Sonnet (generel samtale)

### Tekniske beslutninger
- Qdrant over ChromaDB/Pinecone (self-hosted, REST API, gratis)
- OpenAI embeddings over lokal model (~10x hurtigere, $0.04 total for 40K punkter)
- Regex-baseret task classification (simpelt, hurtigt, nok til v1)

### Mønstre i arbejdet
- Fokus på token-effektivitet (ikke Opus til alt)
- Bygge infrastruktur for RAG før AI-integration
- Skridt-for-skridt: DB → søgning → kontekst → routing

### Session 2 (aften)

**Webapp ændringer:**
- Body padding så vægtbar ikke blokerer indhold
- Debug labels toggle (🏷️) - viser element-navne på UI
- DataLogger - gemmer alle API requests/responses i localStorage

**Viden tilføjet:**
- rute_id struktur: 231-234 = rute 256 (ma-fr), ikke separate ruter
- Gastown reference dokumenteret i AI_ARKITEKTUR.md
- Kris ønsker selvstændig handling, ikke spørgsmål om ting jeg burde vide

**Idéer noteret (ikke implementeret):**
- Web scraper workflow med progressiv filtrering
- YouTube transcript pipeline med multimodal "se" funktion

---

## 2026-01-31: Skills + Glossary — Modulær kontekst

### Hvad vi lavede
- **Skills-system oprettet** i `.claude/skills/` med 6 modulære skills:
  - `route-lookup` — Qdrant søgning, getRute API, rute ID mapping
  - `sync-sorting` — n8n workflow references, data flow, sync kommandoer
  - `webapp-dev` — Webapp filstruktur, dark mode, custom JS-moduler
  - `youtube-pipeline` — Second Brain API, pipeline-moduler
  - `infrastructure` — Docker, systemd, Qdrant, services, credentials, tmux
  - `data-analysis` — Data-lokationer, analyse-tilgange, historiske indsigter
- **Glossary oprettet:**
  - `/data/glossary.json` — maskinlæsbar (rutekoder, status-koder, container-typer, forkortelser)
  - `/data/glossary.md` — menneskelæsbar tabel-format
- **CLAUDE.md slanket** fra 552 linjer til 176 linjer
  - Detaljeret viden flyttet til skills (getRute reference, webapp-sektion, Docker-kommandoer, Qdrant-detaljer)
  - Beholdt: project overview, automatisk kontekst, dokumentationskrav, session log, infra-oversigt
  - Tilføjet: skills-reference tabel, glossary-reference
- **Duplikat-mappe fjernet:** `/c/docs/` (var kopi af `/docs/`)

### Beslutninger
- Skills placeres i `.claude/skills/` (projekt-niveau, ikke globalt) — følger Claude Code konventioner
- Hver skill har frontmatter med `description` og `use when` for automatisk triggering
- CLAUDE.md forbliver primær fil men som "index" — detaljeret viden i skills
- Glossary i både JSON (til scripts) og MD (til direkte læsning)
- Session log forbliver i CLAUDE.md (altid loaded, kronologisk overblik)

### Tekniske observationer
- 552 → 176 linjer = 68% reduktion i CLAUDE.md
- Skills-format med frontmatter (`---` blokke) er standard for Claude Code skill-filer
- Infrastructure-skill er den største (~120 linjer) da den samler Docker, systemd, Qdrant, services, token tracking
- Route-lookup skill inkluderer system architecture diagram (relevant for at forstå data-flow)

### Mønstre i arbejdet
- "Progressive disclosure" — kun load kontekst når det er relevant
- Modularitet reducerer token-forbrug per session
- Glossary som single source of truth for domæne-termer (kan bruges af scripts + Claude)

---

## 2026-02-01: V2 webapp + logging-fix + auto-dagbog

### Hvad vi lavede (natlig session kl. ~22:00–03:00 + eftermiddagssession)

**Natlig session (anden Claude-instans):**
- **V2 webapp** bygget i `/c/v2/` — helt ny version med Alpine.js, modulær struktur (app.js, api.js, store.js, routes.js, map.js, route-detail.js), dark mode, dansk
- **PWA support** tilføjet til både v1 og v2 — manifest.json, service worker, ikoner (192/512px)
- **Chat API** (`scripts/chat_api.py`) — ny API på port 3003 der sender webapp-beskeder til tmux Claude session
- **V1 webapp opdateret** — app.js, Ruter.js, RuteMap.js, distanceService.js, featurePanel.js, ydrasilChat.js, CSS
- **Deep research** gemt i `/data/research/`:
  - `01_lifecycle_tracker.md` — PDCA, OODA, ADR, Popper, projekt-lifecycle tracking
  - `02_android_chat_app.md` — Android chat/knowledge app
  - `03_voice_whisper.md` — Voice assistant med wake word + Whisper STT
- **Scripts opdateret:** process_session_log.py (batch-fix), cost_guardian.py, webapp_server.py

**Eftermiddagssession (denne session, fra kl. 15:01):**
- **Diagnosticeret** at tmux pipe-pane ikke kørte (ingen log for i dag)
- **Diagnosticeret** at process_session_log.py havde fejlet 16 timer i træk (57MB tmux-log sprængte OpenAI's 300K token grænse)
- **Implementeret 3-lags logging-fix:**
  1. `.tmux.conf` med hooks — pipe-pane aktiveres automatisk ved ny session/vindue
  2. Hourly cron genstarter pipe-pane med time-baseret filnavn (`tmux-YYYY-MM-DD-HH.log`)
  3. `auto_dagbog.py` — cron kl. 23:55, henter Qdrant-opsummeringer → appender til DAGBOG.md + Session Log
- **process_session_log.py forbedret** — sorterer mindste filer først, så nye time-filer processeres før gamle kæmpefiler
- **Fjernet** `@reboot` cron for pipe-pane (erstattet af hourly + .tmux.conf)
- **Opdateret** CLAUDE.md dokumentationssektion + Session Log

### Automatiske systemer der kørte i dag
- Navigator briefing kl. 06:00 — status: Fase 1 ~done
- Intelligence briefing kl. 08:00 — fangede Claude Code v2.1.29, Qdrant v1.16.3
- Source discovery + YouTube monitoring
- process_session_log.py kl. 14:00 og 15:00 — 328 opsummeringer embedded (efter batch-fix)

### Beslutninger
- Time-rotation på tmux logs i stedet for dagsfiler — forhindrer kæmpefiler
- Auto-dagbog som sikkerhedsnet — selv hvis Claude glemmer at dokumentere, fanger cron det
- Pipe-pane via `.tmux.conf` hooks + hourly cron — dobbelt sikkerhed
- Princip: "Gør det umuligt at glemme" fremfor "husk at gøre det"

### Observationer
- Den natlige session lavede meget arbejde men opdaterede IKKE CLAUDE.md/DAGBOG — præcis det problem vi har set før
- tmux-log fra 31. jan er 57 MB (10.042 chunks) pga. intensiv videoanalyse — tog processing-systemet ud i 16 timer
- Auto-dagbog virker men kvaliteten afhænger af at Qdrant har data — pipe-pane SKAL køre
- Haiku deprecation warning i cron.log — skal migreres inden 19. feb 2026

### Cleanup: Haiku deprecation
- Advarslen i cron.log var fra den GAMLE version af process_session_log.py (31. jan) der brugte Anthropic Haiku
- Nuværende version bruger allerede `gpt-4.1-nano` — ingen aktive Haiku-kald
- Opdateret cost_guardian.py pris-tabel: `claude-3-5-haiku-20241022` → `claude-haiku-4-5-20251001`

### Problemer at følge op på
- ~9.500 uprocesserede chunks fra gårsdagens 57MB log (processeres gradvist, 200/time)
- V2 webapp er bygget men ikke testet/verificeret af Kris endnu
- Research-filer i `/data/research/` er rå session-transcripts (JSON), ikke redigerede rapporter
- ~~**Session-kontinuitet** — ny Claude-session ved ikke hvad forrige session lavede~~ **LØST** med hooks (se nedenfor)

### Session-kontinuitet: Hooks-baseret checkpoint-system
- **Problem:** Ny Claude-session ved ikke hvad forrige session lavede. Kris: "det skulle aldrig være et problem"
- **Løsning:** Claude Code hooks i `.claude/hooks.json`:
  - `SessionEnd` + `PreCompact` → `save_checkpoint.py` → gemmer til `/data/NOW.md`
  - `SessionStart` → `load_checkpoint.sh` → injicerer NOW.md som kontekst
- **NOW.md indeholder:** tidsstempel, CWD, aktive tasks, seneste samtale (tekst-only, ingen tool-noise)
- **Checkpoint gemmes automatisk** — ingen Claude-session behøver "huske" at gøre det
- Checkpoint udløber efter 48 timer (irrelevant efter lang inaktivitet)

---

## 2026-02-02: Voice pipeline + MCP + Qdrant-integration

Første lange arbejdsdag efter opstart-ugen. Kristoffer ville have systemet til at lytte, forstå og huske — ikke bare svare.

Byggede voice-pipeline: lydoptagelse → Whisper-transkription → klassifikation → Qdrant-embedding. Fik MCP-server fra Qdrant op at køre så Claude Code kan søge direkte i vektordatabasen. Stødte på Python-installationsproblemer (qdrant_client manglede, typing-extensions konflikter). Testede Fabric framework til automatisk databehandling men parkerede det — for komplekst til hvad vi har brug for nu.

**Beslutninger:** MCP til Qdrant som primær søgning. OpenAI embeddings (ikke lokal model). YouTube-download droppet pga. JavaScript-begrænsninger — bruger transcript-API i stedet.

---

## 2026-02-03–05: Stille dage

Ingen aktive sessioner. Cron-jobs kørte automatisk (embedding, monitoring, backup). Systemet var stabilt.

---

## 2026-02-06: Voice memos fra bilen

Kristoffer optog to voice memos under kørsel. Første gang han brugte systemet i praksis — talte om sine oplevelser med appen, irritationspunkter, og idéer til forbedringer. Memoerne blev transkriberet og embedded i Qdrant. Vigtig milepæl: data fra den virkelige arbejdsdag begyndte at flyde ind.

---

## 2026-02-08: Playbook-struktur diskuteret

Kristoffer ville samle al viden i ét dokument — en "playbook" der kortlægger alle tanker, beslutninger og planer. Vi diskuterede struktur og format. Konklusionen: det skal være et levende dokument, ikke en statisk rapport. Platformen tillader ikke filoverførsel i denne kontekst, så vi arbejder med tekst.

---

## 2026-02-09: Kapitel 6 — Automation, Simplicity Wins

Skrev kapitel 6 til AI Practitioner's Bible. Analyserede vores egne 8 cron-jobs (0 fejl på 6 uger) mod komplekse workflow-engines som n8n. Dokumenterede at LLM-in-the-loop virker bedst som funktionskald i deterministiske workflows — ikke som autonome agenter.

Kerne-indsigt: Computer Use og Browser Agents er demo-grade. MCP har 3 CVE'er fra januar 2026. Simple løsninger vinder i produktion.

---

## 2026-02-10: Sikkerhedsaudit — 3 kritiske fund

Gennemførte komplet audit af 22 infrastruktur-punkter. Fandt: (1) Tor-proxy eksponeret på internettet, (2) API-nøgler ikke gitignored, (3) dokumentation 18x forældet på Qdrant-tal. Fixede Tor-binding til 127.0.0.1 akut. Udvidede weekly_audit.py til at fange alle 22 punkter automatisk. SESSION_LOG markeret deprecated — DAGBOG er nu primær.

---

## 2026-02-11: Telegram som interface

Byggede Python-bot der forbinder Telegram med Claude Code via tmux. Konfigurerede SSH-adgang fra Termux. Beslutning: Telegram bliver primær kommunikationskanal i stedet for separat PWA. Voice-pipeline prioriteret som MVP.

---

## 2026-02-12: Voice-appen lanceret

"Shadow & Gold"-tema med Cormorant Garamond og breathing glow-animation. Skiftede LLM fra Claude Sonnet til Groq Kimi K2 — fra $5/md til $0. Single-tap optagelse virker. Men kritisk problem: Telegram-bridge mister voice-noter efter transkribering. Data går tabt. Voice-app uden Qdrant-kontekst er bare en chatbot, ikke en rådgiver.

---

## 2026-02-13: Audit session + voice fra bilen

58 audit-fund, 38 fixet (66%). Voice diary fra bilen transkriberet i tre dele — del 2 gik tabt ved session-crash. Smertefuld påmindelse om at gemme FØR processing. Groq-løsningen bekræftet som holdbar.

---

## 2026-02-14: RAG optimeret + Google Drive integreret

Stor evalueringsdag. Dense-only søgning (75% hit rate) slår hybrid search (65%). LightRAG forkastet — RAM-begrænsninger. Reranking afvist — problemet er chunk-kvalitet, ikke ranking. Mindmap deployed på webapp. Google Drive downloadet komplet (819 MB, 1.518 filer) via rclone.

Overraskelse: danske queries scorer bedre end engelske (88% vs 75%). Systemet matcher Kristoffers naturlige sprog.

Kristoffer frustreret over PC-forslag. Han har KUN Android/Termux. Dokumenteret i MEMORY.md — aldrig igen.

---

## 2026-02-15: Chat-analyser + friktions-audit

**Den store selvransagelse.** Analyserede alle AI-samtaler fra tre platforme:
- ChatGPT: 44 samtaler over 16 måneder. December 2025 var vendepunktet — 28 samtaler på én måned, hvor Kristoffer opdagede AI til rutesorttering.
- Grok: 118 samtaler, 19.562 beskeder. November 2025 = "AI-vækkelsesmåneden" (86% af al brug). Kristoffer brugte Grok som både builder-assistent og samtalepartner.
- Claude: allerede kendt fra daglig brug.

Friktions-audit afslørede to kerneproblemer: (1) Claude ignorerede gentagne gange Nano Banana Pro — Kristoffers foretrukne værktøj. (2) Claude foreslog simplere løsninger end det Kristoffer bad om. Ny regel: "Gå 100% efter hvad Kristoffer siger FØRST. Tilbyd alternativer som supplement, ikke erstatning."

Ugentlig audit: disk 96.7% fuld. Secondbrain-api inaktiv. 81.675 Qdrant-punkter.

---

## 2026-02-16: Mindmap-dagen — 4 voice memos, vild ambition

Kristoffer vågnede kl. 06:29 og optog 40 minutters brainstorm om ALLE projekter. Han ville have mindmaps over alt: TransportIntra (sortering, GPS, diesel, kundekartotek, nøgler, chat, tidsreg, ferie, lørdagsvagter, stop-beskrivelser med video), personlig AI-assistent (mail, kalender, Trello, indkøb), research-agent, arkitektur, rejseagent, bogføring.

Visionen: et interaktivt GraphRAG-view. Cirkler med forbindelser. Klik på en boble → den bliver hovedboblen. Hver boble skal have log, noter, vedhæftninger, PRD, to-do. "Nærmest en 4-dimensionel BrainMap."

Byggede mindmap v1, v2, og Cytoscape-version. Kristoffer gav detaljeret feedback i memo 2 (07:51): "Det ser rigtig fint ud." Memo 3 (08:33): bad om kronologisk samling af ALLE samtaler. Memo 4 (10:11): udvidet boble skal erstatte sidepanel, flere visningsmodi, cross-referencing.

Research: AI memory (MemGPT, Letta), menneskehukommelse (chunking, spaced repetition), knowledge visualization.

---

## 2026-02-17: Pause fra mindmaps — markdown i stedet

Kristoffer bremser op i voice memo (10:41): "Stop med mindmaps midlertidigt." Vil have markdown-dokumenter med overblik i stedet. Tre overkategorier: Projekter, Strukturer/Arkitektur, Viden. Hvert emne med tags der viser relationer. Beder om forsøg med Nano Banana Pro til visualisering.

Byggede mindmap v3 med varianter (elixir, simple). Fortsatte knowledge visualization research.

---

## 2026-02-18: "Jeg overplanlægger"

**Vendepunkt.** Kristoffer optog 28 minutters voice memo kl. 05:18 — ærlig selvrefleksion: "Min erfaring er, at der hvor jeg har haft mest fremgang, det er når jeg bare har implementeret noget." Han bad om tre konkrete ting:
1. Sort/hvid overblik over AI-funktioner (hvad sker automatisk, hvad sker på kommando)
2. TransportIntra-kompendium: side-for-side gennemgang med screenshots
3. Nano Banana Pro-guide så han selv kan designe UI

Leverede kompendium v1. Kristoffer gav live-feedback i memo 2 (12:59): "Et skridt i den rigtige retning. Det er det jeg mener når det skal være professionelt." Feedback: adskil originalt fra tilføjet indhold, dæk alle ruter, screenshots i multiple formater.

**Beslutning:** Professionelt udseende — sort på hvid, serif font, korrekt linjeafstand, som en universitetsopgave.

---

## 2026-02-19: Feedback-appen + kompendium-frustrationer

Tre voice memos. Det vigtigste: feedback-app til personalemødet 27. februar.

Konceptet (memo 2, 12:45): Anonym feedback-app til chauffører. Pseudonymiseret login, voice memo-optagelse, automatisk transskription og anonymisering, iterativ proces. Formål: kortlægge friktionspunkter. Budget: 500 kr til Whisper for potentielt 100 timers samtale fra 100 chauffører. "Jeg kan godt lide sådan noget her — planlægning og evaluering og kortlægning."

Kompendium v2 og v3 leveret men memo 3 (20:54) var frustreret: "Det er simpelthen blevet forrodet." Originalt, tilføjet og ideelt indhold blandet sammen. Navne (Kris, Ydrasil) skal IKKE bruges — professionelt sprog. Positiv om diagrammerne.

**Vigtig korrektion:** "Jeg gider faktisk ikke blive kaldt Kris. I dokumenter: Kristoffer. I chatten: Yttre."

Screenshots taget via headless browser: 16 stk i desktop, mobil og tablet-formater.

---

## 2026-02-20: Kompendium v4 samlet

Stille arbejdsdag. Kompendium v4 leveret som samlet PDF (1.8 MB) med tre klare dele: (1) original TransportIntra-manual, (2) tilpasninger, (3) fremtidsvision. Inkluderer mobile screenshots.

---

## 2026-02-21: Trello som operativsystem

**Stor strukturerings-dag.** Kristoffer ville have Trello til at fungere som primært projekt- og kommunikationsværktøj.

**Bygget:**
- 4 Trello boards: TI-Project, Rejsebureau, Revisor, Personligt — med labels, custom fields (Prioritet, Estimat, Fokus nu), checklister, covers, beskrivelser
- Dashboard-board med Udbakke (upload voice memos/filer), Daglig Log (auto time-for-time), Voice Memos (14 uploadet), I dag-liste
- `trello_audit.py` — ROI-scoring, fokus/sekundær, stale detection, kommentar-scanning
- `sync_inbox.py` — action-chains (afkryds task → auto-generér næste)
- `trello_logbog.py` — daglig log med cron, voice memo upload, dokument-upload
- `trello_comment_watch.py` — scanner ALLE boards hvert minut for kommentarer, vedhæftninger, nye kort, flytninger, checklisteændringer, labels, deadlines

**Reorganisering:**
- Google Drive parallel med Trello-struktur
- Alle udlægs-filer omdøbt med HU-reference
- Excel-overblik over udlæg (estimeret 33.697 DKK)
- Alle kort fik unikke referencer: T-1..9, R-1..5, E-1..2, P-1..6, D-1..16
- To Do-lister fjernet — member assignment er nok (widget "Mine kort")
- Hotmail token refreshed — virker uden re-auth

**Voice memos (uploadet via Trello Udbakke — første gang!):**
- Memo 1 (16:39): To Do-kort er overflødige. Member assignment er nok. Ét overordnet fokus-sted.
- Memo 2 (16:45): Dagbogen skal være mere uddybende. Gå helt tilbage og skriv referat for hver dag.

**Kristoffers kommentarer på Trello-kort (scannet automatisk):**
- R-4: "Er bilag i drive ikke ordnet? Lav excel-overblik. Task om bank-CSV."
- R-1: "Der har lige været flere udlæg, venter til de bliver trukket."
- T-2: "Pseudonymt pga. GDPR. Alt anonymiseres."
- T-3: "Hvor er linket [til prototypen]?"
- T-8: "Giver du besked når du har bygget den? Jeg finder layout, du programmerer."

Kommentarer fungerer som separation of concerns — samtalen gemmes automatisk på det rigtige kort.

---

## Mønster i perioden 15.–21. februar

Kristoffer oscillerer mellem stor ambition (GraphRAG brainmap, alle projekter som mindmap) og pragmatisk selvransagelse (18. feb: "Jeg overplanlægger"). Retningen peger mod:
1. **Kompendium** som professionelt reference-dokument
2. **Feedback-app** som konkret værdi for firmaet (deadline 27/2)
3. **Trello som operativsystem** — kommunikation, tracking, dagbog, alt ét sted
4. **Dagbog** som arkiv over hele rejsen

---

## 2026-02-23: Dagbogsafsnit

### Hvad vi lavede
- Arbejdede med at forbedre grafframeworks som Graphiti, GraphRAG, Letta og MAGMA.
- Foretog kritisk analyse af LightRAG og Graphiti.
- Lavet forbedringer i scripts til håndtering af store logfiler.

### Beslutninger
- Beslutning om at optimere processering af store filer og undgå svære RAM-udfald.

### Observationer
- Identificeret problemer med store logfiler, hvilket førte til opdateringer i scripts for mere effektiv behandling.

---

## 2026-03-15: Ydrasil-projektets fremgang

### Hvad vi lavede
- Kørte en iteration med CLAUDE, men processerne blev afbrudt.
- Analyserede Nate B Jones' videoer om AI-output, kritisk vurdering og proaktivitet.

### Beslutninger
- Ingen beslutninger blev taget under sessionen.

### Observationer
- Videoerne understregede vigtigheden af kritisk vurdering af AI-output og proaktivitet i AI-systemer.
- Ydrasil-projektet skal fokusere på at forbedre data- og outputsikkerhed samt præcision i systemer.
