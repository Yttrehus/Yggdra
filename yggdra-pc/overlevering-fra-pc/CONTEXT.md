# Overlevering fra PC — 16. marts 2026

## Hvad skete i session 24 (PC)

### Hukommelsesarkitektur v1 — bygget og kører
- `scripts/memory.py` på PC — CLI med: setup, ingest, search, status, nuke
- Qdrant genstartet fra scratch. Kun to collections:
  - **knowledge** (984 points) — 62 research-filer fra `projects/2_research/`
  - **episodes** (59 points) — chatlogs, voice memo, progress
- **Hybrid search:** dense (text-embedding-3-small) + sparse (BM25-approksimation) + RRF fusion
- **Temporal decay** i søgning (nyere vejer tungere)
- **Content hashing** (skip uændrede filer ved re-ingest)
- **Kontekstuel chunking** (titel + heading prepended før embedding)
- Legacy collections (sessions 43K, advisor_brain 453, docs 1466, miessler_bible 102, conversations 81) URØRT — venter på cleanup
- `routes` (40K, TransportIntra) URØRT — produktion

### Voice memo transkriberet
- `Voice 260316_053647.m4a` (60 min) → Groq Whisper → 28K tegn
- Renskrevet i 8 kapitler → `voice_memos/voice_260316_053647.md` (på PC)
- Indhold: hukommelsesarkitektur, OpenClaw mini-claws, backlog-reform, APA-referencer, mappestruktur, vedligehold

### VPS overlevering analyseret
- Alle MD-filer fra `overlevering-fra-vps/` hentet til PC `projects/2_research/`
- REFLEKSION.md læst og diskuteret
- Qdrant collections gennemgået — beslutning: start fra scratch

### Obsidian
- `OBSIDIAN_BRO_ANALYSE.md` hentet og læst
- Beslutning: **parkeret**. Hukommelsesarkitekturen skal virke først.

## Beslutninger taget
1. Qdrant kun to collections: knowledge + episodes. Intet advisor_brain, intet miessler_bible.
2. Chatlogs under episodes (source-tag filtrerer), ikke egen collection.
3. Obsidian parkeret til hukommelse er afprøvet i praksis.
4. OpenClaw mini-claw arkitektur er næste planlægningssession.
5. Voice memos gemmes i `voice_memos/` på PC (ny mappe).

## Åbne opgaver PC-side (når PC er online igen)
1. Eval-suite: 20 test-queries med forventede svar til memory.py search
2. Slet legacy collections fra Qdrant
3. Auto-ingest hook (kør memory.py ingest ved filændringer)
4. OpenClaw evaluering + mini-claw arkitektur planlægning
5. Alias: `mem search query` i stedet for lang .venv-sti
6. Ingest resten: CONTEXT.md-filer, BLUEPRINT.md, backlog-briefs

## Session-fil
`a833d545-ac8f-41df-958f-439ff6c22761.jsonl` i `~/.claude/projects/c--Users-Krist-dev-projects-Yggdra/`
