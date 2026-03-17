# Handlingsplan — Yggdra, marts 2026

---

## Top 6 handlinger for PC-Yggdra

### 0. Implementér destruktiv-kommando-guard (S — 30 min, GØR DETTE FØRST)
PreToolUse:Bash hook der blokerer `rm -rf /`, `docker system prune`, `git push --force`, og `ssh root@... "rm"`. Patterns klar i Nate Jones-dokumentet. Eneste handling der forhindrer datatab. PC har SSH-adgang til VPS med root — ét forkert kald kan slette alt.

### 1. Skift memory.py til dense-only default (S — denne session)
VPS-benchmark viser dense 83% vs hybrid 61%. Ændr default i `scripts/memory.py`. Kør eval-suite (`yggdra-pc/overlevering-fra-pc/EVAL_SUITE.json`) mod dense-only. Ret de queries der fejler.

### 2. Absorber PROMPT_KATALOG til brug (S — denne uge)
Kopiér de 8 skabeloner fra `data/vps-sync-20260316/prompt_mining/PROMPT_KATALOG.md` til `projects/REF.prompt-skabeloner/`. Gør dem tilgængelige — ikke som research, men som copy-paste redskaber. Overvej at lave 2-3 af dem til skills.

### 3. Luk 5 backlog-items (S — denne uge)
- `brief.memory-architecture.md` → arkivér (v1 er live)
- `DLR.session-blindhed/` → arkivér (symptom, ikke projekt — løses af hukommelse)
- `vps-sandbox-v2.md`, `vps-prompt-final.md`, `vps-prompt-final-draft.md`, `vps-prompt-v5-implementering.md` → arkivér (historik, ikke handlinger)
- Opdatér TRIAGE.md

### 4. Roter API-nøgler (M — denne uge, kræver Yttre)
Anthropic, OpenAI, Groq, ElevenLabs — alle eksponeret via nginx dot-fil. Fix er lavet, men nøglerne er ikke roteret. Kræver login på hvert dashboard.

### 5. Installér PC load_checkpoint equivalent (M — næste uge)
VPS har `load_checkpoint.sh` der injicerer kontekst ved session-start. PC har ingenting. Design en SessionStart-hook der læser CONTEXT.md + seneste 5 episoder og injicerer dem. Brug VPS-versionen som reference.

---

## Top 3 handlinger for VPS

### 1. Fix process_session_log timeout (S)
Circuit breaker tripped 3/3 gange ved 600s. Øg til 900s eller diagnosticér OOM. Uden dette mister VPS episoder.

### 2. Forny Groq API-nøgle (S)
Returnerer 403. Prompt miner og save_checkpoint kører blind. Alt der bruger Groq er påvirket.

### 3. Fix episode projekt-tildeling (M)
35% episoder (216/614) har `project: unknown`. Groq kaldes kun ved Stop, ikke Notification. Enten kald Groq ved begge events, eller kør batch-retildeling.

---

## Backlog-opdateringer

| Brief | Handling |
|---|---|
| `brief.memory-architecture.md` | **Luk** — v1 er live |
| `RDY.context-engineering.md` | **Opdatér** — VPS prompt mining dækker halvdelen. Skærp scope til det der mangler: feedback-loop fra brug til forbedring |
| `RDY.research-architecture.md` | **Opdatér** — VPS har INDEX.md-struktur. PC's research er stadig uorganiseret |
| `RDY.automation-index.md` | **Opdatér** — VPS har 17 cron jobs. Brief bør fokusere på PC-automatisering specifikt |
| `brief.voice-integration.md` (raw) | **Opgradér til brief** — voice pipeline virker, men er manuelt. Termux vm-kommando er klar |
| VPS prompt-historik (4 filer) | **Arkivér** — historik, ikke handlinger |
| Ny: `brief.session-onboarding.md` | **Opret** — PC mangler SessionStart-hook, load_checkpoint equivalent |

---

## CONTEXT.md diff (foreslået)

Tilføj under "Seneste session":

```
### Session 25 (2026-03-17)
VPS-sync: 135 filer hentet (prompt mining, intelligence, scripts, overlevering, episoder).
Helhedsvurdering: ~35% af systemet bruges dagligt. Skift fra builder mode til operator mode.

**Nyt fra VPS:**
- Qdrant: 6.626 knowledge points (op fra 984), dense-only > hybrid (83% vs 61%)
- Prompt mining: 1.270 prompts analyseret, 8 skabeloner i PROMPT_KATALOG.md
- Mini-Claw fase 1: token-tracking + kill-switch + budget-cap
- 17+ cron jobs kører. Heartbeat, prompt miner, intelligence, episode rotation.
- API-nøgler eksponeret — nginx fixet, rotation mangler

**Beslutninger:**
- memory.py default: hybrid → dense-only
- brief.memory-architecture: lukket (v1 er live)
- VPS reformation: parkeret (brug systemet først, reformér derefter)
- Prompt-skabeloner absorberet fra VPS

**Åbne tråde (opdateret):**
- API-nøgle-rotation (Anthropic, OpenAI, Groq, ElevenLabs)
- VPS process_session_log timeout (600s → 900s)
- VPS Groq API 403
- PC SessionStart-hook mangler
- 35% VPS-episoder har project: unknown
```

Fjern fra "Åbne tråde":
- "Qdrant legacy cleanup" → delvist done (VPS slettede sessions+docs)
- "memory.py eval-suite" → gør det, stop med at liste det

---

## Tidslinje

**Denne session (nu):** Del B prompt-arkitektur + CONTEXT.md opdatering.

**Denne uge:**
- Dense-only default i memory.py
- Eval-suite kørt
- 5 backlog-items lukket
- PROMPT_KATALOG absorberet
- API-nøgler roteret (kræver Yttre)

**Næste uge:**
- PC SessionStart-hook
- VPS fixes (process_session_log, Groq nøgle, episode-tildeling)
- Voice integration brief opgraderet

**Parkeret:**
- VPS reformation blueprint (lev med systemet en uge først)
- Obsidian (hukommelse skal bruges først)
- Nye backlog-briefs (5 skal lukkes først)
