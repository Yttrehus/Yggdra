# Automation Deep Audit — 15. marts 2026

**Tidspunkt:** kl. 14:02-14:30 CET
**Auditor:** Yggdra automation-audit agent

---

## Status per pipeline

| Pipeline | Schedule | Seneste kørsel | Status | Noter |
|---|---|---|---|---|
| **morning_brief** | 07:00 daglig | 15/3 07:00 | OK | cron_guard, 300s timeout |
| **ai_intelligence** | 06:30 daglig | 15/3 06:30 | OK | 23 items hentet, $0.01 |
| **ai_intelligence weekly** | 06:15 sondag | 15/3 06:15 | OK | Ugentlig digest gemt |
| **youtube_monitor** | 07:00 daglig | 15/3 07:00 | CRASHET | cred_text fejl — FIX IMPLEMENTERET |
| **source_discovery** | 08:00 sondag | 15/3 08:00 | DELVIST OK | JSON parse fejl i LLM-svar, 0 nye kilder. Recoverer selv. |
| **heartbeat** | */30 08-21 | 15/3 13:00 | OK | DeprecationWarning fikset, forkert token fikset |
| **process_session_log** | */6 timer | 15/3 12:00 | FEJL | 06:00: Qdrant vector name error. 12:00: Timeout 600s |
| **backup** | 04:00 daglig | 15/3 04:00 | OK | 494MB, Qdrant snapshot + tar |
| **auto_dagbog** | 23:55 daglig | - | OK (antaget) | Ingen fejl i logs |
| **embed_advisor_brain** | 05:00 sondag | 15/3 05:00 | OK | |
| **embed_docs** | 05:00 sondag | 15/3 05:00 | OK | 1466 points |
| **weekly_audit** | 06:00 sondag | 15/3 06:00 | OK | Fitness functions PASSED |
| **daily_sweep** | 08:00 daglig | 15/3 08:00 | OK | |
| **hotmail_autosort** | 08:45,13:45,18:45 | 15/3 10:45 | OK | 1-2 mails/dag |
| **cruft_detector** | 06:30 sondag | 15/3 06:30 | OK | 7 fund rapporteret |
| **score_knowledge** | DISABLED | - | - | Deaktiveret (session3) |
| **sync_inbox** | DISABLED | - | - | Trello droppet 14/3 |
| **voice_memo_pipeline** | DISABLED | - | - | Voice memos ikke aktive |
| **tmux pipe-pane** | DISABLED | - | - | Logs nobody reads |

## Docker containers

Alle 5 containers korer og er stabile (uptime: 2 uger):
- webapp, traefik, qdrant, api-logger, tor-proxy

## Qdrant collections

| Collection | Points | Status |
|---|---|---|
| sessions | 42.507 | green |
| routes | 40.053 | green |
| docs | 1.466 | green |
| advisor_brain | 453 | green |
| knowledge | 246 | green |
| miessler_bible | 102 | green |
| conversations | 81 | green |

---

## Fundne problemer

### KRITISK

**K1: youtube_monitor.py crasher HVER dag (8 gange i trak)**
- Import-linje (`from credentials import OPENAI_KEY`) stod for shebang
- `cred_text` variabel aldrig defineret (manglede `with open()` blok i committed version)
- Koren UDEN cron_guard (ingen timeout-beskyttelse)
- **Konsekvens:** YouTube-intelligence pipeline har ikke produceret data i uger

**K2: process_session_log fejler med Qdrant "Not existing vector name" error**
- Qdrant sessions collection bruger named vectors (`dense`) + sparse vectors
- `ensure_collection()` ville oprette med unnamed vectors ved recreation
- Upsert fejlede 15/3 06:00, derefter timeout 15/3 12:00 (retry af samme batch)
- Error counter: 2/3 (naste fejl tripper circuit breaker)

### HOJ

**H1: heartbeat.py brugte FORKERT Telegram bot token**
- Token i heartbeat.py matchede IKKE CREDENTIALS.md
- Alle Telegram-notifikationer fra heartbeat gik til forkert bot/nowhere
- **Konsekvens:** Heartbeat-alarmer har aldrig nAet Kris

**H2: 7 scripts med import for shebang**
- `ai_intelligence.py`, `atlas_pdf.py`, `auto_dagbog.py`, `daily_sweep.py`, `embed_advisor_brain.py`, `embed_docs.py`, `youtube_monitor.py`
- Virker fordi cron kalder dem med explicit python3, men er forkert og forvirrende

**H3: 6.7GB GPU-pakker i venv pa GPU-los VPS**
- nvidia (4.3GB), torch (1.8GB), triton (641MB) installeret
- Kun brugt af sentence-transformers (get_context.py fallback)
- Disk: 73% brugt, 27GB fri — ikke akut men unodvendigt

### MIDDEL

**M1: source_discovery JSON parse fejl**
- LLM (gpt-4.1-nano) returnerer af og til truncated JSON
- Script recoverer selv (returnerer tom liste)
- Resultat: "0 nye kilder forslAet" i stedet for faktiske forslag

**M2: heartbeat.log fyldt med 336 "can't open" fejlbeskeder**
- Gamle entries fra for cron_guard blev tilfojet
- Skjuler reelle heartbeat-data

**M3: Zombie Trello-referencer i 5 scripts**
- `cruft_detector.py`, `dashboard_api.py`, `heartbeat.py`, `merge_clusters.py`, `morning_brief.py`
- Trello er droppet (4/3-2026) — disse kode-stier er dode

### LAV

**L1: heartbeat.py brugte deprecated `datetime.utcnow()`**
- Python 3.12 DeprecationWarning ved hver korsel (hvert 30 min)

**L2: youtube_monitor og source_discovery uden cron_guard**
- Ingen timeout-beskyttelse, ingen circuit breaker

---

## Implementerede forbedringer

### Fix 1: youtube_monitor.py — shebang + cred_text (KRITISK)
- Rettede import-raekkefolge (shebang forst)
- cred_text blok var allerede tilfojet i working tree (lines 35-37)
- Verificeret: kompilerer OK
- **Backup:** youtube_monitor.py.bak.20260315

### Fix 2: youtube_monitor + source_discovery — cron_guard (HOJ)
- Wrappet begge i cron_guard med 300s timeout
- Giver timeout-beskyttelse + circuit breaker + logging
- **Backup:** crontab_backup_20260315.txt

### Fix 3: process_session_log.py — error handling + collection schema (KRITISK)
- Tilfojet `except Exception` handler ved Qdrant upsert (linje 404)
- Ved Qdrant-fejl: logger fejlen, nulstiller offset (retry naste run)
- Rettede `ensure_collection()` til named vectors (`{"dense": VectorParams(...)}`)
- Verificeret: kompilerer OK
- **Backup:** process_session_log.py.bak.20260315

### Fix 4: heartbeat.py — Telegram token + deprecation (HOJ)
- Rettet Telegram bot token til matche CREDENTIALS.md
- Erstattet `datetime.utcnow()` med `datetime.now(tz=timezone.utc)`
- Verificeret: kompilerer OK
- **Backup:** heartbeat.py.bak.20260315

### Fix 5: Shebang-raekkefolge i 6 scripts (HOJ)
- Rettede import-for-shebang i: ai_intelligence, atlas_pdf, auto_dagbog, daily_sweep, embed_advisor_brain, embed_docs
- Alle verificeret: korrekt raekkefolge
- **Backups:** *.bak.20260315 for alle

### Fix 6: heartbeat.log oprydning (MIDDEL)
- Fjernet 336 "can't open file" fejlbeskeder fra gammel konfiguration
- Log reduceret fra 340 til 4 linjer
- **Backup:** heartbeat.log.bak.20260315

---

## Anbefalinger til naeste session

### Beslutning kraevet

1. **GPU-pakker fjernelse (6.7GB)** — `pip uninstall torch nvidia-* triton` ville frigore 6.7GB. Kraever at `get_context.py` skifter fra lokal sentence-transformers til OpenAI embeddings (som bruges overalt ellers). Lav risiko, stor gevinst.

2. **Trello-oprydning** — Fjern dead Trello-kode fra heartbeat.py, morning_brief.py, cruft_detector.py, dashboard_api.py, merge_clusters.py. Trello er droppet siden 4/3-2026.

3. **process_session_log Qdrant-fejl** — Fejlen "Not existing vector name" kan vaere transient (test upsert virker nu). Naeste korsel (kl. 18:00) vil vise om fix virker. Hvis det fejler igen: undersog om collection schema blev aendret.

### Automatisk opfolging

4. **youtube_monitor** — Naeste korsel: i morgen kl. 07:00. Verificer at den producerer data igen.

5. **Hotmail autosort** — Logger viser korsler hver time (00:45-23:45) men crontab siger kun 8,13,18. De gamle log-entries er fra for crontab-aendringen. Ingen handling nodvendig.

### Teknisk gaeld

6. **Telegram tokens hardcoded** — Bor centraliseres i credentials.py ligesom API keys. 4 scripts har hardcodede tokens.

7. **Log rotation** — 268 gamle tmux-logs (49MB). Ikke akut men bor ryddes op.

8. **source_discovery LLM JSON** — Overvej at bruge structured output / JSON mode i stedet for at parse fri-tekst JSON fra LLM.
