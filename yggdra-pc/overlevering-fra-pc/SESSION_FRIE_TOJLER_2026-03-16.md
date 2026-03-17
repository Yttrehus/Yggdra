# Session: Frie Tøjler — 16. marts 2026, kl. 13:23–13:33

**Model:** Opus 4.6 (VPS)
**Metode:** 6 loops, sekventiel udførelse
**Varighed:** ~10 minutter

---

## Hvad blev gjort

### Loop 1: Knowledge ingest — 83 research-filer + 30 docs-filer
- **research/** (83 .md filer) → 3171 chunks ingestet til knowledge
- **docs/** (30+ .md filer) → 1037 chunks ingestet til knowledge
- Knowledge collection: 2450 → **6626 points** (+4176)
- Inkluderer: CH1-CH10 bog-kapitler, DESTILLAT-filer, psykologi, pipeline-arkitektur, audit-rapporter, transportintra-profil, alle docs

### Loop 2: Sessions cleanup
- `sessions` collection (198 points) inspiceret: tmux-logfiler fra 3. marts med ANSI-støj
- **Slettet.** Ingen værdi.
- Collections: 6 → **5** (routes, knowledge, advisor_brain, miessler_bible, episodes)

### Loop 3: Episodes rotation
- **scripts/rotate_episodes.py** oprettet — 90 dages retention, arkivér til `data/episodes_archive/`
- Testet: alle 633 episoder er fra seneste 3 uger, intet at rotere endnu
- Systemet vokser ~30/dag — rotation nødvendig om ~2 måneder
- Klar til at tilføjes som cron-job

### Loop 4: Hybrid search eval — OVERRASKENDE RESULTAT
- Kørte EVAL_SUITE.json (20 queries) mod både hybrid (RRF) og dense-only
- **Hit@5 resultater:**
  - Dense-only: **15/18 = 83%** (op fra 61% baseline med 2450 points)
  - Hybrid RRF: **11/18 = 61%** (uændret fra baseline!)
- **Konklusion:** Mere data hjalp (61%→83%), men hybrid RRF **skader** rankeringen. RRF diluter gode dense-resultater med mediokre sparse-matches.
- **Anbefaling:** Brug dense-only som primær. Sparse/BM25 kun som fallback for exact-match.
- Rapport: `EVAL_RESULTS_HYBRID.md`

### Loop 5: Advisor_brain analyse
- 453 points fra 3 unikke kilder: Miessler (175), Nate Jones (146), Practitioner's Bible (132)
- Originalindhold fra betroede rådgivere — IKKE research-resuméer
- **Anbefaling: BEHOLD separat.** Advisor-indhold bør ikke drukne i 6626 generelle knowledge-chunks.

### Loop 6: ctx / memory.py konsolidering
- **Analyse:** ctx (913 linjer) = search-specialist, memory.py (519 linjer) = CRUD/ingest-specialist
- **Overlap:** Kun search-funktionalitet. ctx er bedre (reranking, routing, alle collections)
- **Anbefaling:** Behold begge, separate roller. Prematur at merge.
- **FIX:** ctx opdateret — fjernet references til slettede `conversations` og `docs` collections
- **FIX:** Default-adfærd ændret: `ctx "query"` søger nu routes + knowledge (ikke de slettede)
- Verificeret: ctx finder korrekt i knowledge (Ebbinghaus, Nate Jones osv.)

---

## Qdrant efter session

| Collection | Points | Ændring |
|------------|--------|---------|
| routes | 40.053 | — |
| knowledge | 6.626 | +4.176 (research + docs ingestet) |
| advisor_brain | 453 | — (behold separat) |
| miessler_bible | 102 | — |
| episodes | 91 | +32 (nye sessioner) |
| ~~sessions~~ | ~~198~~ | **SLETTET** |
| **Total** | **47.325** | -198 + 4.176 = **+3.978 net** |

---

## Filer oprettet/ændret

| Handling | Fil | Beskrivelse |
|----------|-----|-------------|
| OPRETTET | `scripts/rotate_episodes.py` | 90-dages episoderotation |
| OPRETTET | `scripts/eval_hybrid_search.py` | Eval-suite runner (hybrid vs dense) |
| OPRETTET | `yggdra-pc/overlevering-fra-pc/EVAL_RESULTS_HYBRID.md` | Eval-resultater med konklusion |
| ÆNDRET | `scripts/get_context.py` | Fjernet slettede collections, default → routes+knowledge |
| OPRETTET | Denne fil | Session-opsummering |

---

## Hvad virkede

1. **Knowledge ingest i bulk** — memory.py håndterede 113 filer uden fejl
2. **Dense-only search forbedring** — 61% → 83% bare ved at tilføje mere data. Simpelt er bedst.
3. **ctx oprydning** — fjernede forældede collection-references forhindrer runtime-fejl

## Hvad næste session bør fokusere på

1. **Dense-only som default i memory.py** — eval viser at RRF skader. Overvej at ændre memory.py's search til dense-only (eller gør det konfigurerbart).
2. **Reranker i ctx** — torch mangler, reranking failer til fallback. Installér `sentence-transformers` (men OBS disk: venv er allerede 7.6 GB) eller find lightweight alternativ.
3. **rotate_episodes.py som cron** — tilføj til crontab (fx ugentlig søndag kl. 05:30)
4. **embed_docs cron DEAKTIVÉR** — docs er nu i knowledge via memory.py. embed_docs duplicerer.
5. **Episodes-enrichment** — 216/633 episoder har `project: unknown`. Backfill med Groq-klassificering.

---

*Genereret kl. 13:33, mandag 16. marts 2026. VPS Opus 4.6, autonom session.*
