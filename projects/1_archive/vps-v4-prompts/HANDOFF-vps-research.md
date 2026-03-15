# Handoff: VPS Research Loops

**Til:** Session der deployer VPS Ralph loops
**Fra:** Session 20 (2026-03-14)
**Formål:** Deploy 2+ Ralph loops på VPS der forsker i AI-landskabet

## Hvad er gjort

### Substack-integration (DONE)
- `substack-api` installeret på VPS (`pip install --break-system-packages substack-api`)
- Cookies deployed: `/root/Yggdra/data/substack_cookies.json` (udløber ~2026-06-11)
- `ai_intelligence.py` opdateret med `fetch_substack()` funktion — testet og virker
- `intelligence_sources.json` opdateret med 5 Substacks + 2 RSS feeds
- Test: 7 posts hentet (Import AI, latent.space, One Useful Thing, TheSequence)

### Briefs skrevet (4 stk i `projects/0_backlog/`)
1. **brief.llm-landskab.md** — Per-provider AI intelligence (Anthropic, OpenAI, Google, xAI, Meta, Mistral, Perplexity)
2. **brief.ai-frontier.md** — State of the art: agents, memory, automation, "hvad kan implementeres i morgen"
3. **brief.videns-vedligeholdelse.md** — Design system til at holde AI-viden aktuel (decay, pipelines, protokoller)
4. **brief.youtube-pipeline-v2.md** — Frame extraction, nye kanaler, transcript-forbedring

### VPS-prompts skrevet (2 stk, deploy-klare)
1. **vps-prompt-llm-landskab.md** — 10 iterationer, CLAUDE.md + LOOP_PLAN.md + LOOP_STATE.md + start-kommando
2. **vps-prompt-ai-frontier.md** — 10 iterationer, samme format

Begge kan køre parallelt. Samme infrastruktur som sandbox v2 (vps-prompt-final.md).

## Hvad mangler

### VPS-prompts der endnu ikke er skrevet
- videns-vedligeholdelse (5 iterationer) — bør køre EFTER llm-landskab + ai-frontier
- youtube-pipeline-v2 (3 iterationer) — kan køre parallelt med alt

### Deploy
Prompts er skrevet men IKKE deployed. Du skal:
1. Oprette mapper på VPS (`mkdir -p /root/Yggdra/yggdra-pc/llm-landskab/providers` etc.)
2. Deploye CLAUDE.md, LOOP_PLAN.md, LOOP_STATE.md fra prompt-filerne
3. Starte loops (start-kommandoer er i bunden af hver prompt-fil)

### YouTube: Nye kanaler
Kanalerne er dokumenteret i brief.youtube-pipeline-v2.md men IKKE tilføjet i intelligence_sources.json endnu:
- Andrej Karpathy (UC-rVQ55xcf3DwSUQM-BOdFg)
- Cognitive Revolution (UCjNRVMBVI30Sak_p6HRWhIA)
- latent.space podcast (UCWjBpFQ19_IfjMJ3mCd0rSg)

## VPS-infrastruktur (eksisterende)

### Ralph loop mønster (afprøvet i sandbox v2)
```bash
for i in $(seq 1 N); do
  timeout 600 claude --dangerously-skip-permissions --print \
    "Du er iteration $i af N. Følg CLAUDE.md boot-sekvens."
  sleep 10
done
```

### Relevante VPS-stier
- `/root/Yggdra/yggdra-pc/` — sandbox-rod (V1, V3 eksisterer fra tidligere)
- `/root/Yggdra/research/` — 60+ research-filer (vigtig input for ai-frontier)
- `/root/Yggdra/data/miessler_bible/` — Miessler PAI indhold
- `/root/Yggdra/data/intelligence_sources.json` — kilde-konfiguration
- `/root/Yggdra/scripts/ai_intelligence.py` — daglig scan pipeline
- `/root/Yggdra/scripts/youtube_monitor.py` — YouTube RSS + transcript pipeline

### Substack-adgang
```python
from substack_api import Newsletter, SubstackAuth
auth = SubstackAuth(cookies_path="/root/Yggdra/data/substack_cookies.json")
newsletter = Newsletter("https://www.latent.space", auth=auth)
posts = newsletter.get_posts(limit=3)
```

## Yttres intentioner

Yttre vil have et greb i et konstant forandrende AI-landskab. Nøglepersoner han følger:
- **Nate B. Jones** — YouTube, transkriberet, principper integreret i Yggdra
- **Daniel Miessler** — PAI blog post (scraped i `.firecrawl/`), YouTube, bog-udkast på VPS
- **Simon Willison** — blog (simonwillison.net), LLM tooling ekspert
- **Ethan Mollick** — "One Useful Thing" Substack, akademisk + praktisk AI

Projekterne er designet til at producere actionable viden — ikke research for researchens skyld. "Hvad kan implementeres i morgen med mit setup" er den vigtigste deliverable.

YouTube transkribering er vigtigt. Frame extraction (grafer, slides) er nice-to-have — luksus hvis det virker, ikke blokker.

## Anbefalet rækkefølge
1. **llm-landskab + ai-frontier** parallelt (begge 10 iterationer)
2. **videns-vedligeholdelse** (5 iterationer, efter 1 er færdig)
3. **youtube-pipeline-v2** (3 iterationer, kan køre når som helst)
