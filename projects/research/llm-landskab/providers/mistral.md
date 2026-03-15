# Mistral AI

## Identitet

Fransk AI-startup grundlagt 2023 af ex-DeepMind og ex-Meta forskere. EU's svar på US-dominans i AI. Fokus: data-suverænitet, GDPR-compliance, europæisk infrastruktur. Tilbyder både open-weight og proprietære modeller. Stærkeste europæiske AI-provider.

## Modeller

| Model | Styrke |
|-------|--------|
| **Mistral Large** | Stærkeste proprietære. Konkurrerer med GPT-4.1 |
| **Mistral Medium** | Balance pris/kvalitet |
| **Mistral Small** | Hurtig, billig |
| **Mixtral 8x22B** | Open-weight MoE. Stærk til pris |
| **Mistral OCR** | Specialiseret dokumentforståelse |

## Styrker (steelman)

1. **EU data-suverænitet.** Europæisk hosting, GDPR-compliant by design. Eneste seriøse europæiske alternativ til US-providers.
2. **OCR-kapabilitet.** Mistral OCR er specialiseret til dokumentscanning og -forståelse. Niche men stærk.
3. **Open-weight modeller.** Mixtral er tilgængelig til self-hosting. MoE-arkitektur giver god pris/ydelse.
4. **Le Chat.** Consumer-produkt der konkurrerer med ChatGPT i Europa.
5. **Competitive pricing.** Billigere end OpenAI og Anthropic for sammenlignelig kvalitet.
6. **Multilingual styrke.** Stærk på europæiske sprog inkl. fransk, tysk, spansk.

## Svagheder (red team)

1. **Ikke frontier-kvalitet.** Ingen Mistral-model er i Arena top-10. Bagud på coding og reasoning.
2. **Lille developer-community.** Langt færre tutorials, eksempler og community-support end OpenAI/Anthropic.
3. **Ingen agent-tooling.** Ingen CLI-agent, ingen pendant til Claude Code.
4. **Fragmenteret modelportefølje.** Mange modeller, uklart hvornår man bruger hvad.
5. **Begrænset vision/multimodal.** Bag Gemini og Claude på multimodal.
6. **Enterprise-fokus.** Bedste features kræver enterprise-aftaler.

## Pricing

Generelt 20-40% billigere end OpenAI for sammenlignelig kvalitet. Mixtral open-weight er gratis at self-hoste.

## API & Developer Experience

- **La Plateforme:** Mistral's API-platform. Solid men mindre moden end Anthropic/OpenAI
- **SDK:** Python, TypeScript
- **Function calling:** Tilgængelig
- **MCP:** Ikke officielt adopteret endnu
- **Hosting:** Europæiske datacentre

## Relevans for Yttre

| Behov | Mistral-løsning | Vurdering |
|-------|-----------------|-----------|
| **GDPR/data-suverænitet** | EU-hosting | ★★★★☆ — Relevant hvis compliance bliver kritisk |
| **OCR** | Mistral OCR | ★★★☆☆ — Niche-relevant for dokumentscanning |
| **Coding/agenter** | Ingen tooling | ★☆☆☆☆ — Langt bag Claude Code |
| **Daglig brug** | Le Chat | ★★☆☆☆ — Fungerer, men ingen fordel over Claude |

**Konklusion:** Mistral er kun relevant for Yttre i to scenarier: (1) GDPR-compliance bliver et hårdt krav, eller (2) OCR af specifikke dokumenttyper. Ellers ingen fordel over eksisterende setup.

## Kilder

- /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (sektion 4.2)