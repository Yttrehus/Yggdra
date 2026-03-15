# Meta AI (Llama)

## Identitet

Meta Platforms (ex-Facebook). Open-weight strategi — Llama-modellerne er gratis at downloade og køre. Metas AI-strategi: giv modellerne væk, profitér af adoption i Meta-produkter og cloud-partnerskaber. Ingen direkte API-service — Llama køres via cloud-udbydere (AWS, Google, Azure) eller self-hosted.

## Modeller

| Model | Context | Pris | Styrke |
|-------|---------|------|--------|
| **Llama 4** | 10M (!) | Gratis (self-hosted) | Længste kontekstvindue. Open-weight |
| **Llama 4 Maverick** | 1M | Gratis | MoE-arkitektur, effektiv |
| **Llama 3.3** | 128K | Gratis | Stabil, velkendt, bred adoption |

## Styrker (steelman)

1. **Open-weight.** Fuld kontrol over modellen. Ingen vendor lock-in. Ingen API-afhængighed.
2. **10M kontekstvindue.** Llama 4's kontekstvindue er 5x Geminis 2M. Unikke muligheder for lange dokumenter.
3. **Data-suverænitet.** Self-hosting = data forlader aldrig dine servere. Kritisk for GDPR, sundhed, finans.
4. **Ingen per-token cost.** Eneste cost er compute (GPU-leje eller ejet hardware). Ved >20M tokens/måned er self-hosting billigere.
5. **Community.** Størst open-source AI community. Tusindvis af finetuned varianter. HuggingFace-integration.
6. **Ingen rate limits.** Self-hosted = ubegrænset throughput (kun begrænset af hardware).
7. **Finetuning-muligheder.** LoRA, QLoRA, fuld finetune. Tilpas til specifikke domæner.

## Svagheder (red team)

1. **Kræver GPU-hardware.** Self-hosting kræver minimum 1x A100 (40GB) for de store modeller. Dyre cloud-instanser.
2. **Ingen managed service.** Meta tilbyder ingen API. Du skal selv håndtere inference, scaling, monitoring.
3. **Kvalitet bag frontier.** Llama 4 er ikke på Arena top-10. Qwen 3 har overtaget som bedste open-weight.
4. **Ingen agent-tooling.** Ingen CLI-agent, ingen skills, ingen hooks. Du bygger alt selv.
5. **Ingen embeddings.** Ingen officiel embedding-model fra Meta.
6. **Inference-kompleksitet.** vLLM, TGI, Ollama — mange serving-frameworks, ingen standard.
7. **Support = community.** Ingen SLA, ingen enterprise-support fra Meta direkte.
8. **"Open" med forbehold.** Licensen har restriktioner for virksomheder >700M MAU. Ikke truly open-source.

## Pricing

| Scenario | Estimat |
|----------|---------|
| Self-hosted (1x A100) | ~$1.50-3.00/time cloud-leje |
| Self-hosted (eget hardware) | Engangsinvestering $10-30K |
| Via cloud-udbyder | Varierer, ofte billigere end OpenAI/Anthropic ved volume |
| Break-even vs. API | ~20M tokens/måned |

## API & Developer Experience

- **Ingen officiel API.** Brug via AWS Bedrock, Google Vertex, Azure, Together.ai, Groq, etc.
- **Serving:** vLLM, TGI (HuggingFace), Ollama (lokalt), llama.cpp (CPU)
- **Finetuning:** LoRA/QLoRA via HuggingFace, Axolotl, unsloth
- **MCP:** Qwen 3 (ikke Llama) er MCP-native
- **Community tools:** LangChain, LlamaIndex, HuggingFace Transformers

## Relevans for Yttre

| Behov | Meta-løsning | Vurdering |
|-------|--------------|-----------|
| **Self-hosting** | Llama 4 via Ollama | ★★★☆☆ — Muligt men VPS har kun 96GB disk, ingen GPU |
| **Data-suverænitet** | Full control | ★★★★☆ — Relevant ved sensitive data |
| **Coding/agenter** | Ingen tooling | ★☆☆☆☆ — Alt skal bygges selv |
| **Daglig brug** | Ikke praktisk | ★☆☆☆☆ — Kræver infrastruktur Yttre ikke har |
| **Batch-volume** | Billigt ved >20M tok/md | ★★☆☆☆ — Yttres volume er for lavt |

**Konklusion:** Llama er irrelevant for Yttres nuværende setup. Ingen GPU, lavt token-volume, og Claude Code giver langt bedre developer experience. Llama bliver relevant hvis: (a) Yttre får GPU-hardware, (b) data-suverænitet bliver kritisk, eller (c) token-volume overstiger 20M/måned. Indtil da: ignorer.

## Kilder

- /root/Yggdra/research/CH4_LLM_LANDSCAPE.md (sektioner 4.2, 4.3)
- HuggingFace Llama Model Cards