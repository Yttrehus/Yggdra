# YouTube Pipeline v2

**Dato:** 2026-03-14
**Klar til:** Backlog — VPS (kan køre parallelt med andre)
**Prioritet:** Medium

## Opsummering
Opgradér youtube_monitor.py: bedre transkribering, frame extraction til grafer/slides, nye kanaler.

## Hvorfor
YouTube er en primær videnskilde (Nate, Miessler, Karpathy). Nuværende pipeline henter transcripts og embedder i Qdrant, men misser visuelt indhold (grafer, slides, diagrammer) som ofte bærer den vigtigste information.

## Scope

**Inden for:**
- Frame extraction: screenshot hvert N sekund, OCR for tekst i slides
- Vision-analyse: brug LLM vision (Claude/Gemini) til at beskrive grafer og diagrammer
- Transcript-forbedring: bedre chunking, tidsstempel-alignment
- Nye kanaler: Karpathy, swyx/latent.space, Cognitive Revolution, Matt Shumer
- Substack-integration: latent.space har både podcast og Substack

**Uden for:**
- Real-time streaming/monitoring
- Egne transcription-modeller (brug eksisterende APIs)
- Video-hosting

## Deliverables

1. Nye kanaler tilføjet i intelligence_sources.json
2. Frame extraction funktion i youtube_monitor.py (ffmpeg → screenshots → OCR/vision)
3. Opdateret transcript processing med timestamps
4. Test-kørsel med 2-3 videoer der har synligt grafisk indhold

## Implementation (3 iterationer eller manuelt)

### Iteration 1: Nye kanaler + audit
Tilføj kanaler. Audit nuværende pipeline: hvad virker, hvad fejler, transcript-kvalitet.
**Done:** Nye kanaler i config, audit-rapport.

### Iteration 2: Frame extraction PoC
ffmpeg extract frames (1 per 30 sek). For frames med tekst/grafer: send til vision API for beskrivelse. Gem som metadata ved siden af transcript.
**Krav:** ffmpeg installeret, vision API tilgængelig (Gemini gratis tier eller Claude vision).
**Done:** PoC der kører på én video og producerer frame-descriptions.

### Iteration 3: Integration + test
Integrer i youtube_monitor.py. Test med Nate-video der har grafer. Verificér Qdrant-embedding inkluderer frame-beskrivelser.
**Done:** Pipeline kører automatisk med frames for nye videoer.

## Eksisterende infrastruktur
- `/root/Yggdra/scripts/youtube_monitor.py` — RSS feeds, transcripts, Qdrant embedding
- `/root/Yggdra/data/intelligence_sources.json` — 7 YouTube kanaler konfigureret
- Qdrant `sessions` collection (~42K punkter)
- OpenAI API (til embeddings) + Groq (til summarization)

## Nye kanaler at tilføje
| Kanal | Channel ID | Prioritet | Topics |
|---|---|---|---|
| Andrej Karpathy | UC-rVQ55xcf3DwSUQM-BOdFg | high | deep technical, neural nets, AI fundamentals |
| Cognitive Revolution | UCjNRVMBVI30Sak_p6HRWhIA | high | interviews, AI industry, PAI |
| latent.space (podcast) | UCWjBpFQ19_IfjMJ3mCd0rSg | high | agent architectures, tooling |

## Kill condition
Hvis frame extraction producerer mere støj end signal (>50% frames er ubrugelige) → drop frames, behold transcript-forbedringer.
