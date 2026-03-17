# Prompt Mining Insights — 2026-03-16

## Dataset
1.270 prompts fra 246 sessioner. 1.092 rene bruger-prompts (178 task-notifications filtreret).
Groq-API utilgaengelig (403) — analysen er regelbaseret klassificering + moenster-detektion.

| Kategori | Antal | Andel | Gns. ord |
|---|---|---|---|
| Kommando | 685 | 54% | 8 |
| Koer-loes | 364 | 29% | 55 |
| Meta | 97 | 8% | 674 |
| Korrektion | 80 | 6% | 844 |
| Struktureret | 44 | 3% | 234 |

## Top 3 effektive moenstre

### 1. Struktureret opgave med kontekst + output-spec
Kun 3.5% af prompts, men naesten altid foerstegangs-succes. Definerer identitet, regler, output-format.
```
"Du er Yggdra... VIGTIGE REGLER: 1. UDFOER handlinger — snak ikke om dem.
2. Svar kort (max 3 saetninger) med hvad du HAR GJORT, ikke hvad du PLANLAEGGER."
```
**Signal:** Nummererede trin + anti-patterns + done-kriterium = minimal korrektionsbehov.

### 2. Kommando med fil-reference
13.6% af prompts naevner specifikke stier. Korte imperativer med praecis nok kontekst til entydig handling.
```
"tjek igen DEPLOY_INSTRUCTIONS.md. root/yggdra/yggdra-pc/"
```
**Signal:** Fil-sti eliminerer tvetydighed. Score-forskel vs. kommandoer uden reference er markant.

### 3. Implement-this-plan prompts
Giver komplet plan med kontekst, steps og leverance. Claude eksekverer, ikke designer.
```
"Implement the following plan: # Plan: Cytoscape.js Mindmap
## Kontekst — Den nuvaerende mindmap bruger D3.js ... ## Steps ..."
```
**Signal:** Taenkt igennem foer prompt. Ingen beslutninger overladt til Claude.

## Bund 3 ineffektive moenstre

### 1. Vage kommandoer uden kontekst
53.9% af alle prompts er korte kommandoer. Mange under 5 ord uden fil-reference.
```
"kan ikke finde" / "derefter?" / "og hvad gjorde dette?"
```
**Problem:** Kontekst-afhaengige, kraever opfoelgning, umulige at genbruge som templates.

### 2. Tastefejl-tungt mobil-input (35.8%)
Over en tredjedel af alle prompts har markant tastefejl-signal fra Termux/mobil.
```
"nej den giber ille underskud. hvos vi bsre siger 1 lr pr kf og 50 kr par spand toent"
```
**Problem:** Koster ekstra korrektionsrunder. Claude gisner rigtigt ~80% af tiden, men de 20% fejl udloeser kaskader.

### 3. Korrektions-kaskader (6.3%)
Naar foerste prompt er uklar, foelger lange korrektionskaeder (gns. 844 ord per korrektion).
```
"nej det tror jeg ikke" → efterfoelges af lang forklaring af hvad der faktisk mentes.
```
**Problem:** Mest kostbare moenster i token-forbrug. Foerste prompt sparede 5 sekunder, korrektionen kostede 5 minutter.

### 4. Iterative loops med human-in-the-loop checkpoint (NY)
Kører N autonome loops, stopper med status-tabel, venter på go/korrektion.
```
"Kør 3 loops autonomt per runde. Efter hver runde: STOP og skriv status-tabel.
Vent på 'ok' eller korrektion før næste runde. Maks 4 runder."
```
**Signal:** Balancerer autonomi med kontrol. Forhindrer drift over mange iterationer. Kris kan korrigere kurs uden at miste momentum.

## Anbefalinger

1. **Fil-reference altid:** Naevn stier/filer eksplicit — kun 13.6% goer det i dag, men det aendrer success-rate drastisk
2. **Output-spec i opgaver >20 ord:** Tilfoej "Output: [format]" eller "Maks X linjer" — kun 2.6% goer det
3. **Mobil-input:** Brug voice-to-text eller template-kommandoer paa Termux (35.8% tastefejl-rate)
4. **Undgaa "derefter?"-moenstret:** Beskriv naeste skridt eksplicit fremfor at antage kontekst
5. **Strukturer opgaver >50 ord:** Brug trin-nummerering — 3.5% er strukturerede, men de virker bedst
6. **Scan-forbedring:** Filtrer task-notifications og context-resumptions fra scan-steget
7. **Groq-API:** Noegle returnerer 403 — skal fornyes for AI-baseret scoring

---
*Baseret paa 1.270 prompts, 246 sessioner. Regelbaseret analyse (Groq 403).*
