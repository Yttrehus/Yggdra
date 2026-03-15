# VPS Ralph Loop — YouTube Pipeline v2

Deploy til `/root/Yggdra/yggdra-pc/youtube-pipeline-v2/`.
3 iterationer. Kan kore uafhaengigt af andre loops.

---

## CLAUDE.md

```markdown
# YouTube Pipeline v2 — Sandbox

Du korer autonomt i en Ralph loop. Yttre er ikke tilgaengelig.
Hver iteration er et `claude --print` kald.

## Boot-sekvens

1. Dit iterationsnummer er givet i prompten
2. Laes LOOP_STATE.md — check ## Blokkere
3. Laes den relevante iteration i LOOP_PLAN.md
4. VALIDER INPUT: Check at filer fra forrige iteration eksisterer
5. Udfor opgaven. Skriv output til disk
6. Verificer output med kommandoer (ls, wc -l, head, python3 -c "...")
7. Opdater LOOP_STATE.md
8. Stop

## LOOP_STATE format

```
# Loop State
## Blokkere
(ingen / liste)

## Filregister
(kumulativ liste af producerede filer)

## Iteration [N-1] (seneste)
Opgave: ...
Output: ...
Done: ... -> PASS/FAIL

## Naeste: Iteration N
```

## Projekt

Opgrader youtube_monitor.py: nye kanaler, bedre transkribering, frame extraction til grafer/slides.
Dette er et BUILD-projekt — du skriver kode, ikke rapporter.

## Regler

### Token-bevidsthed
- Laes ALDRIG filer >500 linjer i helhed. Brug head, tail, grep
- Max 3 parallelle subagents
- Skriv kompakt

### Build > Research
- Hver iteration SKAL producere kode eller config paa disk
- Ingen rapporter — kun audit i iteration 1, resten er kode

### Done = Verified
- Test ALTID med `python3 -c "..."` eller `python3 script.py --test`
- Verificer at nye kanaler faktisk returnerer data
- Verificer at frame extraction producerer filer

### Miljo
- Du er PAA VPS'en. ALDRIG ssh til dig selv
- SOG IKKE paa nettet
- Python: /root/Yggdra/scripts/venv/bin/python3
- youtube_monitor.py: /root/Yggdra/scripts/youtube_monitor.py (477 linjer)
- intelligence_sources.json: /root/Yggdra/data/intelligence_sources.json
- ffmpeg: check med `which ffmpeg` — BLOCKER hvis ikke installeret
- Qdrant: curl localhost:6333/collections (for embedding-verifikation)

### Anti-patterns
- Omskriv IKKE hele youtube_monitor.py — udvid den
- Installer IKKE nye pakker uden at teste dem forst
- Koer IKKE frame extraction paa >3 videoer (token/disk budget)
- Brug IKKE vision API uden at tjekke pris forst
```

---

## LOOP_PLAN.md

```markdown
# Loop Plan — YouTube Pipeline v2 (3 iterationer)

## Iteration 1 — Audit + nye kanaler
**Opgave:** Audit nuvaerende pipeline. Tilfoej 3 nye kanaler
**Metode:**
1. Laes `head -80 /root/Yggdra/scripts/youtube_monitor.py` — forstaa arkitekturen
2. Laes `/root/Yggdra/data/intelligence_sources.json` — se eksisterende kanaler
3. Test nuvaerende pipeline: `/root/Yggdra/scripts/venv/bin/python3 /root/Yggdra/scripts/youtube_monitor.py --dry-run` (eller lignende)
4. Tilfoej 3 nye kanaler til intelligence_sources.json:
   - Andrej Karpathy (UC-rVQ55xcf3DwSUQM-BOdFg) — high priority
   - Cognitive Revolution (UCjNRVMBVI30Sak_p6HRWhIA) — high priority
   - latent.space podcast (UCWjBpFQ19_IfjMJ3mCd0rSg) — high priority
5. Verificer: `python3 -c "import json; d=json.load(open('/root/Yggdra/data/intelligence_sources.json')); print(len(d['youtube_channels']), 'channels')"`
**Output:** _audit.md (pipeline-arkitektur, hvad virker, hvad mangler) + opdateret intelligence_sources.json
**Done:** 3 nye kanaler i config, audit >30 linjer

## Iteration 2 — Frame extraction PoC
**Opgave:** Byg frame_extractor.py der udtraekker keyframes fra en YouTube-video
**Forudsaetning:** `which ffmpeg` — hvis ikke installeret: BLOCKER i LOOP_STATE
**Metode:**
1. Check ffmpeg: `which ffmpeg && ffmpeg -version | head -1`
2. Skriv `/root/Yggdra/scripts/frame_extractor.py`:
   - Input: YouTube URL eller lokal video-fil
   - Download video med yt-dlp (allerede installeret? check: `which yt-dlp`)
   - ffmpeg: extract 1 frame per 30 sekunder
   - For hver frame: detect om den indeholder tekst/graf (simpel heuristik: filstorrelse > threshold = mere indhold)
   - Output: mappe med frames + metadata.json (tidspunkt, filnavn, har_tekst)
3. Test paa 1 kort video (<10 min) — Nate Jones eller Karpathy
4. Verificer: `ls output_dir/ | wc -l` + `cat output_dir/metadata.json | python3 -m json.tool | head -20`
**Output:** frame_extractor.py + test-output
**Done:** Script korer uden fejl, producerer >5 frames fra 1 video, metadata.json eksisterer

## Iteration 3 — Integration + test
**Opgave:** Integrer frame extraction i youtube_monitor.py workflow
**Input:** frame_extractor.py + _audit.md (forstaa eksisterende arkitektur)
**Metode:**
1. Tilfoej `extract_frames()` funktion til youtube_monitor.py (eller import fra frame_extractor.py)
2. I processing-pipeline: efter transcript, kor frame extraction paa nye videoer
3. Gem frame-beskrivelser som ekstra metadata i Qdrant embedding
4. Test: kor pipeline paa 1 ny video fra en af de nye kanaler
5. Verificer Qdrant: `curl -s localhost:6333/collections/sessions/points/scroll -X POST -H 'Content-Type: application/json' -d '{"limit":1,"with_payload":true}' | python3 -m json.tool | head -30`
**Output:** Opdateret youtube_monitor.py + test-log
**Done:** Pipeline korer paa 1 video, frames udtrukket, embedding inkluderer frame-data
```

---

## LOOP_STATE.md (initial)

```markdown
# Loop State

## Blokkere
(ingen)

## Filregister
(tomt)

## Naeste: Iteration 1
Audit + nye kanaler
```

---

## Start-kommando

```bash
cd /root/Yggdra/yggdra-pc/youtube-pipeline-v2

for i in $(seq 1 3); do
  echo "=== Iteration $i === $(date)"
  if grep -q "BLOCKED\|FAILED" LOOP_STATE.md 2>/dev/null; then
    echo "=== HALTED ==="
    cat LOOP_STATE.md | head -10
    break
  fi
  timeout 600 /root/.local/bin/claude --print \
    "Du er iteration $i af 3. Folg CLAUDE.md boot-sekvens."
  if ! grep -q "Iteration $i" LOOP_STATE.md 2>/dev/null; then
    echo "=== WARNING: iteration $i opdaterede ikke state ==="
  fi
  echo "=== Iteration $i done === $(date)"
  sleep 10
done
```

---

## Review fra telefon

```bash
ssh root@72.62.61.51 "cat /root/Yggdra/yggdra-pc/youtube-pipeline-v2/LOOP_STATE.md"
ssh root@72.62.61.51 "ls /root/Yggdra/scripts/frame_extractor.py 2>/dev/null && echo 'EXISTS' || echo 'MISSING'"
ssh root@72.62.61.51 "cat /root/Yggdra/data/intelligence_sources.json | python3 -c 'import json,sys;d=json.load(sys.stdin);print(len(d[\"youtube_channels\"]),\"channels\")'"
```
