# Google DeepMind

## Identitet

Google DeepMind (fusioneret 2023 fra DeepMind + Google Brain). Verdens største AI-infrastruktur — alle tre rivaler (Anthropic, OpenAI, xAI) træner på Google TPU'er. Google profiterer uanset hvem der "vinder" model-kapløbet. Gemini er integreret i hele Google-økosystemet: Search, Workspace, Android, Chrome.

## Modeller

| Model | Context | Input $/MTok | Output $/MTok | Styrke |
|-------|---------|-------------|--------------|--------|
| **Gemini 3 Pro** | 2M | — | — | #2 Arena Elo (1486). Bedste multimodal. Men "inconsistent" |
| **Gemini 3 Flash** | 1M | — | — | #4 Arena Elo (1470). Remarkabel speed/quality |
| **Gemini Flash-Lite** | — | $0.075 | $0.30 | 67x billigere end Sonnet input. Produktions-workhorse |
| **Deep Think** | — | — | — | Fører Humanity's Last Exam (41%) |

## Styrker (steelman)

1. **Kontekstvindue-king.** 2M native tokens — ingen anden kommer tæt på. Flash har 1M.
2. **Pris-champion.** Flash-Lite ved $0.075/$0.30 er "essentially free." 67x billigere end Sonnet på input.
3. **Multimodal førende.** Bedste visuelle reasoning. Video-forståelse som ingen anden har.
4. **Hastighed.** Flash-modellerne er markant hurtigere end konkurrenterne. Ideal til latency-kritiske pipelines.
5. **Infrastruktur-fordel.** TPU'er, verdensomspændende datacentre, vertikal integration. Ingen kan matche skala.
6. **Deep Think.** Fører Humanity's Last Exam — dybeste reasoning capability på markedet.
7. **Imagen 3.** Stærkeste billedgenerering. Nano Banana Pro (Gemini 3 Pro Image) er Yttres foretrukne visualiseringsværktøj.
8. **$300 Google Cloud credit.** Yttre har aktive credits til Gemini API.
9. **Android-integration.** Gemini er native på Android — relevant for Yttres telefon-first setup.

## Svagheder (red team)

1. **Inkonsistent.** Gemini 3 er "poor at worst compared to 2.5" per udvikler-rapporter. Glemmer kontekst efter 10 prompts trods 2M vindue.
2. **Upålideligt structured output.** Kun 84% schema-valid JSON. Uacceptabelt for datapipelines.
3. **Skjulte thinking-tokens.** Uventede token-costs fra interne ræsonneringstokens der ikke vises.
4. **Ingen stærk CLI-agent.** Intet svar på Claude Code. Google Cloud CLI er ikke det samme.
5. **Privacy-bekymringer.** Google er en reklamevirksomhed. Data bruges til at forbedre produkter.
6. **Workspace-lockin.** Bedste integration kræver Google Workspace. Ikke alle er i det økosystem.
7. **Fragmenteret produktlinje.** Pro, Flash, Flash-Lite, Deep Think, Nano — svært at vide hvad man skal bruge.

## Pricing

| Model | Input $/MTok | Output $/MTok |
|-------|-------------|--------------|
| Flash-Lite | $0.075 | $0.30 |
| Flash | Markant billigere end Sonnet | — |
| Pro | Sammenlignelig med Opus | — |

**Pricing-trend:** Googles priser er de mest aggressive i markedet. Flash-Lite gør high-volume batch-arbejde økonomisk muligt.

## API & Developer Experience

- **Vertex AI:** Enterprise-grade platform. Kompleks men kraftfuld
- **AI Studio:** Lettere developer-interface for prototyping
- **Gemini API:** REST + SDKs (Python, Node.js, Go, Dart)
- **MCP-adoption:** Google har tilsluttet sig MCP-standarden
- **Context caching:** Tilgængelig for lange dokumenter
- **Grounding:** Fact-checking med Google Search integration
- **Code execution:** Sandbox Python miljø

## Relevans for Yttre

| Behov | Google-løsning | Vurdering |
|-------|----------------|-----------|
| **Billedgenerering** | Imagen 3 / Nano Banana Pro | ★★★★★ — Yttres foretrukne. $300 credits |
| **Batch-klassifikation** | Flash-Lite ($0.075/MTok) | ★★★★★ — 67x billigere end Sonnet |
| **Multimodal/vision** | Gemini 3 Pro | ★★★★★ — Bedst i klassen |
| **Coding/agenter** | Gemini Code Assist | ★★☆☆☆ — Langt bag Claude Code |
| **Android-integration** | Gemini native | ★★★★☆ — Relevant for telefon-only setup |
| **Research** | Deep Think | ★★★☆☆ — Stærk reasoning, men inkonsistent |
| **VPS-automation** | Ingen CLI-agent | ★☆☆☆☆ — Intet svar på Claude Code hooks/skills |

**Konklusion:** Google er den vigtigste supplementære provider for Yttre — specifikt til billedgenerering (Imagen/Nano Banana Pro), batch-arbejde (Flash-Lite), og multimodal forståelse. IKKE som primær LLM — inkonsistens og manglende agent-tooling er dealbreakers. Men $300 credits og Android-integration gør det til et naturligt supplement.

## Kilder

- /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (sektioner 4.1-4.3)
- /root/Yggdra/research/AI_CLAUDE_ANTHROPIC_2026.md (sektion 9)
- Arena.ai Leaderboard