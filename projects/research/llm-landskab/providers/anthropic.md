# Anthropic

## Identitet

Grundlagt 2021 af Dario og Daniela Amodei (ex-OpenAI). Mission: AI safety-first. Vurderet til $350 mia. (januar 2026), ~$10 mia. årlig omsætning. Planlagt børsnotering 2026-2027. Partnerskaber med Allianz, US Department of Energy, Salesforce. $50 mia. planlagt til datacentre i Texas og New York. Donerede MCP (Model Context Protocol) til Linux Foundation — nu industristandard med 10.000+ offentlige servere og 97 mio. månedlige SDK-downloads.

## Modeller

| Model | Context | Input $/MTok | Output $/MTok | Styrke |
|-------|---------|-------------|--------------|--------|
| **Opus 4.6** | 200K (1M beta) | $5 | $25 | #1 Arena Elo (1496). SWE-bench 80.8%. Adaptiv tænkning (low/medium/high/max) |
| **Opus 4.5** | 200K (1M beta) | $5 | $25 | Effort-parameter (unique). 76% færre tokens på medium vs. Sonnet |
| **Sonnet 4.5** | 200K (1M beta) | $3 | $15 | OSWorld #1 (61.4%). 30 timers autonom kørsel. "Verdens bedste coding-model" |
| **Haiku 4.5** | 200K | $1 | $5 | Matcher Sonnet 4 performance. Hurtig, billig |

Udgåede: Opus 4.0 og 4.1 fjernet fra både Claude og Claude Code.

## Styrker (steelman)

1. **Ubestridt #1 til coding og agentopgaver.** Opus 4.6 topper SWE-bench Verified (80.8%) og Arena Elo (1496). Claude Code er "first convincing demonstration of what an LLM agent looks like" (Karpathy).
2. **Adaptiv tænkning.** Opus 4.6 skalerer ræsonnementsdybde automatisk — tænker hårdere på svære problemer. Effort-parameter giver direkte kontrol.
3. **Lang-kontekst kohærens.** 76% på 8-needle MRCR ved 1M tokens. Stærkeste needle-in-haystack performance.
4. **MCP som industristandard.** Anthropic definerede protokollen, donerede den, og profiterer mest af adoption. OpenAI, Google, Microsoft har adopteret den.
5. **Claude Code økosystem.** Skills, hooks, checkpoints, subagents, LSP, VS Code extension. >$500 mio. run-rate revenue. 1.096 commits i v2.1.0.
6. **API-innovation.** Prompt caching (90% cost reduction, 85% latency reduction). Batch API (50% rabat). Structured outputs. Code Execution Tool (sandbox Python). Files API. Tool Search Tool.
7. **Safety-track record.** Mest konservativ af de store providers. Refuser tvivlsomt indhold fremfor at servere det.
8. **Enterprise traction.** Allianz (alle medarbejdere), Salesforce (Agentforce 360), US DOE.

## Svagheder (red team)

1. **Usage limits er brutale.** Pro-plan throttler efter 10-15 minutters brug. Dyreste per-token af de store providers.
2. **Ingen persistent memory.** Hver session starter fra scratch. CLAUDE.md, auto memory og Qdrant er workarounds — ikke løsninger.
3. **Over-cautious refusals.** Safety-first betyder lejlighedsvis uberettigede afvisninger. Irriterende i produktion.
4. **Hallucinerer på niche-emner.** Som alle LLMs, men Anthropics konservative profil skaber en falsk tryghedsfølelse.
5. **Lukket økosystem.** Ingen open-weight modeller. Du er låst til Anthropics API og priser.
6. **Svag multimodal.** Ingen video-forståelse. Vision er funktionel men bag Gemini. Ingen billedgenerering.
7. **Kontekstvindue degraderer i praksis.** 1M tokens annonceret, men reliable reasoning falder efter ~400K. Auto-compaction mister detaljer.
8. **Datacenter IP-restriktioner.** VPS-drift kræver workarounds for YouTube, Google m.fl.
9. **Cowork er Mac-first.** Windows-support på vej, men ikke klar. Android/mobil-bruger har begrænset adgang.

## Pricing

| Plan | Pris |
|------|------|
| Pro | $20/md (throttled) |
| Max | Højere grænser |
| Team | Enterprise-features |
| Enterprise | Custom |
| Code Execution | 50 gratis timer/dag, derefter $0.05/time |

**Pricing-trend:** Token-priser er stabile (Sonnet 4.5 uændret fra Sonnet 4). Prompt caching og batch API giver reelle besparelser. Haiku er den bedste pris/ydelse i Anthropic-lineup.

## API & Developer Experience

- **Platform:** platform.claude.com (rebrandet fra console.anthropic.com)
- **Claude Code CLI:** Mest modne agent-development interface. Skills, hooks, checkpoints, subagents, LSP
- **Agent SDK:** Python + TypeScript. Programmatisk adgang til Claude Code-værktøjer
- **MCP Connector:** Forbind til remote MCP-servere uden klientkode
- **Structured Outputs:** JSON schema compliance med `strict: true`
- **Prompt Caching:** Op til 1 times cache. Cache reads tæller IKKE mod input rate limits
- **Batch API:** 50% rabat, separate rate limits, 24-timers SLA
- **Cowork:** Desktop-agent for ikke-udviklere (Mac, Pro-plan)
- **Excel/Word/PDF:** Agent Skills til office-dokumenter

## Relevans for Yttre

| Behov | Anthropic-løsning | Vurdering |
|-------|-------------------|-----------|
| **Claude Code (dagligt)** | Opus 4.6 + Sonnet 4.5 | ★★★★★ — Kerneværktøj. Skills, hooks, checkpoints |
| **VPS-automation** | Hooks (SessionStart, PreCompact, Stop) | ★★★★★ — Direkte integration med cron, scripts |
| **Qdrant/embedding** | Ingen embedding-model | ★★☆☆☆ — Kræver OpenAI text-embedding-3-small |
| **Voice pipeline** | Ingen STT/TTS | ★☆☆☆☆ — Kræver Whisper (OpenAI/Groq) |
| **TransportIntra webapp** | Claude Code til udvikling | ★★★★★ — Webapp-dev skill, nginx, produktion |
| **Research/analyse** | Opus 4.6 deep reasoning | ★★★★★ — Bedste reasoning-model |
| **Subagents** | Haiku 4.5 exploration | ★★★★☆ — Billig, hurtig, men ingen nesting |
| **Billedgenerering** | Ingen | ☆☆☆☆☆ — Brug Gemini Imagen eller DALL-E |

**Konklusion:** Anthropic er Yttres primære provider og bør forblive det. Svagheder (embeddings, voice, billeder) dækkes af supplementære providers.

## Kilder

- /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (sektioner 4.1-4.3, 4.10)
- /root/Yggdra/research/AI_CLAUDE_ANTHROPIC_2026.md (komplet)
- /root/Yggdra/research/CH3_CLAUDE_CODE.md (sektioner 3.1-3.6)
- Arena.ai Leaderboard, SWE-bench Verified, LMSYS Chatbot Arena