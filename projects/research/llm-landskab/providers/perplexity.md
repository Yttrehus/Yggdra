# Perplexity AI

## Identitet

Grundlagt 2022. Search-first AI — bygget som "answer engine" der erstatter traditionel websøgning. Ikke en model-provider i traditionel forstand, men en applikation der bruger flere underliggende modeller (bl.a. egne finetuned modeller + Claude, GPT). Fokus: verificerbare svar med kilder.

## Modeller / Produkter

| Produkt | Beskrivelse |
|---------|-------------|
| **Perplexity Pro** | Premium search med adgang til frontier-modeller (Claude, GPT, Gemini) |
| **Perplexity Default** | Gratis search med egne modeller |
| **Sonar API** | Developer-adgang til Perplexity's search + LLM pipeline |
| **pplx-online** | API-model med realtids web-access |

## Styrker (steelman)

1. **Verificerbare svar.** Citerer kilder med links. Transparens om hvor information kommer fra.
2. **Realtids web-access.** Altid aktuel information — ingen knowledge cutoff-problem.
3. **Multi-model routing.** Bruger den bedste model til opgaven. Claude til reasoning, GPT til bredde.
4. **Academic search.** Stærk til forsknings-spørgsmål med akademiske kilder.
5. **Enkelt interface.** Ingen prompt engineering nødvendigt. Spørg → få svar med kilder.
6. **API (Sonar).** Programmatisk adgang til search+LLM. Nyttig til research-pipelines.

## Svagheder (red team)

1. **Ikke en model-provider.** Ingen egen frontier-model. Afhængig af Anthropic, OpenAI, Google.
2. **Begrænset agent-kapabilitet.** Kan søge og svare, men ikke udføre handlinger, redigere filer, eller køre kode.
3. **Pricing for Pro.** $20/md for hvad der fundamentalt er en search-wrapper over andres modeller.
4. **Hallucination trods kilder.** Citerer kilder, men syntetiserer sommetider forkert fra korrekte kilder.
5. **Ingen developer-tooling.** Ingen CLI, ingen agent, ingen MCP.
6. **Rate limits på gratis tier.** Begrænset antal queries/dag.
7. **Overlap med WebSearch.** Claude Codes WebSearch-tool giver lignende funktionalitet direkte.

## Pricing

| Plan | Pris |
|------|------|
| Free | Begrænset, egne modeller |
| Pro | $20/md, frontier-modeller, ubegrænset |
| Sonar API | Pay-per-query, varierer |

## API & Developer Experience

- **Sonar API:** REST API med search+LLM. Simpel at bruge
- **SDKs:** Python, Node.js (community)
- **Output:** Svar + kilder + follow-up forslag
- **Ingen tool use, function calling, eller agent-loops**

## Relevans for Yttre

| Behov | Perplexity-løsning | Vurdering |
|-------|---------------------|-----------|
| **Research med kilder** | Perplexity Pro | ★★★★☆ — God til hurtig research med verifikation |
| **Realtids-information** | pplx-online | ★★★☆☆ — Alternativ til WebSearch |
| **Academic search** | Pro + Academic focus | ★★★☆☆ — Men scripts/research.py + arXiv er gratis |
| **Coding/agenter** | Ingen | ☆☆☆☆☆ — Slet ikke relevant |
| **VPS-automation** | Sonar API | ★★☆☆☆ — Mulig i research-pipelines |

**Konklusion:** Perplexity er et nicheprodukt for Yttre. Nyttigt til hurtig research med kilde-verifikation, men overlapper med Claude Codes WebSearch og scripts/research.py. Sonar API kunne integreres i ai_intelligence.py for kildeverificeret research, men er ikke en prioritet. Ikke en erstatning for nogen eksisterende provider.

## Kilder

- Perplexity.ai officielle docs
- /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (generel kontekst)