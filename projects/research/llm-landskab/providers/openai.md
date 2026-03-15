# OpenAI

## Identitet

Grundlagt 2015 af Sam Altman, Elon Musk m.fl. som non-profit. Konverteret til capped-profit i 2019. Dominerede AI-markedet 2022-2024 med ChatGPT (86.7% markedsandel). Nu faldet til 64.5% — stadig størst, men ikke længere uantastet. Partnerskab med Microsoft ($13+ mia. investering). Mest udbredt developer-økosystem.

## Modeller

| Model | Context | Input $/MTok | Output $/MTok | Styrke |
|-------|---------|-------------|--------------|--------|
| **GPT-5.2** | 128K | — | — | Nyeste. Men "uneven, jumpy, noticeably worse in places" |
| **GPT-5.1** | 128K | — | — | Arena Elo ~1449-1458. Markant fald fra historisk dominans |
| **GPT-4.1** | 128K | $2 | $8 | Solid legacy. "Good enough" til mange opgaver |
| **o3 (reasoning)** | 128K | — | — | Separat reasoning-model. Stærk matematik |

Bemærk: GPT-5.2 var en "premature release" ifølge practitioner-reports. Auto-switching mellem Instant/Thinking er upålidelig.

## Styrker (steelman)

1. **Bredeste økosystem.** Plugins, browsing, code execution, billedgenerering (DALL-E), whisper (STT), TTS. Ingen anden provider matcher integrationsdybden.
2. **text-embedding-3-small.** Industristandard embedding-model. $0.02/MTok. Brugt af Qdrant-systemer worldwide, inkl. Yttres.
3. **Whisper.** Open-source STT. Brugt i Yttres voice pipeline via Groq.
4. **Professional knowledge work.** Slår professionelle i 70.9% af tilfælde på tværs af 44 erhverv.
5. **Developer adoption.** Størst community, mest dokumentation, flest tutorials. Nemmest at finde hjælp.
6. **GPT-4.1 pris/ydelse.** $2/$8 er konkurrencedygtigt og "good enough" til mange produktionsopgaver.
7. **Structured output.** JSON mode og function calling er modne og veldokumenterede.
8. **ChatGPT distribution.** 200+ mio. ugentlige brugere. Ingen matcher consumer-reach.

## Svagheder (red team)

1. **Kvalitetsfald.** GPT-5.2 er "uneven" — en prematur release. GPT-5.1 ligger #6-9 på Arena. Fra absolut dominans til "also-ran" på 12 måneder.
2. **Over-sanitized personality.** Svar føles korporative og kedelige sammenlignet med Claude.
3. **Fabricerer API'er.** Opfinder ikke-eksisterende API-endpoints i kode. Dokumenteret og reproducerbart.
4. **Auto-switching upålideligt.** Skift mellem Instant/Thinking modes sker uden brugerkontrol og giver inkonsistente resultater.
5. **Reklamer i ChatGPT.** Annonceret januar 2026. Signal om at brugerdata er produktet.
6. **Dyrere end Flash-Lite.** GPT-4.1 koster 27x mere end Gemini Flash-Lite per input-token.
7. **Kontekstvindue bagud.** 128K vs. Gemini 2M og Claude 1M (beta).
8. **SWE-bench bagud.** GPT-5.2 scorer 80.0% vs. Opus 4.5's 80.9% — tæt, men #2.
9. **Trust-erosion.** Hyppige model-ændringer bryder eksisterende prompts. "Prompts degrade within weeks."

## Pricing

| Model | Input $/MTok | Output $/MTok |
|-------|-------------|--------------|
| GPT-4.1 | $2 | $8 |
| text-embedding-3-small | $0.02 | — |
| Whisper | $0.006/min | — |
| TTS | $15/$30 per MTok | — |
| DALL-E 3 | $0.04-$0.12/billede | — |

**Pricing-trend:** OpenAI-priser er faldet dramatisk. GPT-4-ækvivalent performance koster nu $0.40/MTok, ned fra $20 i slutningen af 2022.

## API & Developer Experience

- **API:** Mest modne og veldokumenterede i industrien. Function calling, structured output, JSON mode
- **SDK:** Python og Node.js. Officielle libraries til alt
- **Plugins/integrations:** Browsing, code interpreter, DALL-E, Whisper, TTS — alt i ét
- **OpenAI Playground:** Interaktiv test-interface
- **Batch API:** Tilgængelig med rabat
- **Rate limits:** Generøse for betalende kunder
- **Assistants API:** Stateful conversations med tool use — men kompleksitet over simpel chat
- **MCP-adoption:** OpenAI har tilsluttet sig MCP (Anthropics protokol)

## Relevans for Yttre

| Behov | OpenAI-løsning | Vurdering |
|-------|----------------|-----------|
| **Embeddings (Qdrant)** | text-embedding-3-small | ★★★★★ — Allerede i brug. 84K vektorer. Billigt ($0.02/MTok) |
| **Voice pipeline** | Whisper (via Groq) | ★★★★★ — Allerede i brug. Open-source, pålidelig |
| **Coding/agenter** | GPT-5.x | ★★☆☆☆ — Bagud Claude. Upålidelig auto-switching |
| **Billedgenerering** | DALL-E 3 | ★★★☆☆ — Funktionel men bagud Gemini Imagen |
| **Daglig chat** | ChatGPT | ★★☆☆☆ — Yttre bruger Claude. Ingen grund til at skifte |
| **Research/analyse** | GPT-5.x | ★★★☆☆ — OK, men Claude reasoning er stærkere |
| **Automation/scripts** | API | ★★★☆☆ — Velfungerende, men Claude Code er bedre til VPS-drift |

**Konklusion:** OpenAI er essentiel som supplementær provider til Yttre — specifikt for embeddings (text-embedding-3-small) og STT (Whisper). Men som primær LLM er OpenAI bagud Anthropic på de dimensioner Yttre prioriterer (coding, agents, reasoning). Behold embeddings + Whisper, brug ikke GPT som primær model.

## Kilder

- /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (sektioner 4.1-4.3, 4.10)
- /root/Yggdra/research/CH3_CLAUDE_CODE.md (sektion 3.1)
- Arena.ai Leaderboard, SWE-bench Verified