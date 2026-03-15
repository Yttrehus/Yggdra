# xAI (Grok)

## Identitet

Grundlagt 2023 af Elon Musk. Profilerer sig som "anti-woke" AI — færre indholdsrestriktioner end konkurrenterne. Integreret i X (Twitter). Grok var Yttres første AI-værktøj — historisk relevans, men brugen er stoppet. Massiv GPU-infrastruktur (100.000+ H100 cluster i Memphis).

## Modeller

| Model | Context | Input $/MTok | Output $/MTok | Styrke |
|-------|---------|-------------|--------------|--------|
| **Grok 4.1 Thinking** | 128K | — | — | #3 Arena Elo (1475). Stærk matematik/logik |
| **Grok 3** | 128K | — | — | Generel chat, X-integration |
| **Grok 3 Mini** | 128K | — | — | Billigere, hurtigere |

## Styrker (steelman)

1. **Stærk matematik og formel logik.** Grok 4.1 Thinking er #1 på flere math benchmarks. Genuine styrke i formelle ræsonnementer.
2. **Færre refusals.** Færre indholdsrestriktioner end Claude og ChatGPT. Besvarer spørgsmål andre modeller afviser.
3. **X/Twitter-integration.** Realtids-adgang til social media data. Unik datakilde.
4. **GPU-infrastruktur.** 100.000+ H100 cluster giver rå compute-kraft til fremtidige modeller.
5. **Arena Elo #3.** Grok 4.1 Thinking scorer 1475 — over GPT-5.1 og Sonnet 4.5.

## Svagheder (red team)

1. **#1 benchmarks, #66 brugertilfredshed.** Den mest dramatiske disconnect i AI-industrien. Stærk på tests, svag i praksis.
2. **Safety-krise.** Dokumenterede problemer med harmful output. Færre guardrails er et feature-claim, men en reel risiko.
3. **Svagt developer-økosystem.** Ingen CLI-agent. Begrænset API-dokumentation. Ingen pendant til Claude Code, MCP, eller OpenAIs plugin-system.
4. **X-afhængighed.** Primært tilgængelig via X. Enterprise-adoption begrænset.
5. **Inkonsistent kvalitet.** Benchmark-scores afspejler ikke brugeroplevelsen. Brugere rapporterer "impressive sometimes, terrible often."
6. **Politisk polarisering.** Musks offentlige profil skræmmer enterprise-kunder væk. Bias-bekymringer.
7. **Begrænset kontekstvindue.** 128K — halvdelen af Claudes 200K, en brøkdel af Geminis 2M.

## Pricing

Grok er primært tilgængelig via X Premium+ ($16/md) og X Premium ($8/md med begrænsninger). API-priser er ikke offentligt konkurrencedygtige sammenlignet med de andre store providers.

## API & Developer Experience

- **API:** Tilgængelig men underudviklet sammenlignet med Anthropic/OpenAI
- **SDK:** Begrænset officiel support
- **Dokumentation:** Sparsom
- **Tool use:** Basalt, ingen MCP-support
- **Integration:** Primært X/Twitter. Ingen office-integration, ingen IDE-plugins
- **Community:** Lille developer-community sammenlignet med konkurrenterne

## Relevans for Yttre

| Behov | xAI-løsning | Vurdering |
|-------|-------------|-----------|
| **Coding/agenter** | Grok API | ★☆☆☆☆ — Ingen CLI-agent, svagt ecosystem |
| **Matematik/logik** | Grok 4.1 Thinking | ★★★☆☆ — Stærk, men niche-behov |
| **Research** | X-data integration | ★★☆☆☆ — Social media data, ikke akademisk |
| **VPS-automation** | Ingen | ☆☆☆☆☆ — Intet relevant |
| **Daglig chat** | Grok via X | ★★☆☆☆ — Yttre er skiftet til Claude |

**Konklusion:** Grok var Yttres første AI-værktøj, men er nu irrelevant for hans setup. Ingen CLI-agent, svagt developer-økosystem, og #66 brugertilfredshed trods #1 benchmarks. Historisk interessant, praktisk ubrugelig for Yttres use cases. Eneste nicheargument er matematik-reasoning, men det dækkes tilstrækkeligt af Claude Opus.

## Kilder

- /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (sektioner 4.1, 4.2)
- Arena.ai Leaderboard