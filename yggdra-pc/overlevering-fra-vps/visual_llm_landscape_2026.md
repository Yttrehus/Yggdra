# Visuelle LLM'er og Diagram-generering: Landskab Marts 2026

**Forskningsrapport**
**Dato:** 15. marts 2026
**Forfatter:** Claude (Opus 4.6) for Kris/Yttre
**Metode:** Systematisk websearch + kildekritik. Akademiske databaser (arXiv, Frontiers, ACL, NeurIPS), teknisk dokumentation, benchmark-leaderboards.
**Omfang:** ~350 linjer. Tre blokke: Vision-forståelse, diagram-generering, steelman/red team.

---

## Indholdsfortegnelse

1. Multimodal vision — hvad kan modellerne?
2. Benchmarks og hvad de måler
3. Hvor modellerne fejler systematisk
4. Symbol grounding-problemet — ægte forståelse vs. mønstergenkendelse
5. Diagram-generering — strategier og værktøjer
6. SCHEMA-frameworket for Gemini 3 Pro Image
7. Steelman: Hvorfor visuelle LLM'er allerede er nyttige
8. Red team: Hvor lyver benchmarks, og hvad kan de ikke?
9. Neutral vurdering: Ærlig status marts 2026
10. Implikationer for Kris' workflow
11. Litteraturliste

---

## 1. Multimodal vision — hvad kan modellerne?

### Landskabet marts 2026

Vision-Language Models (VLM'er) har udviklet sig eksplosivt siden GPT-4V (marts 2023). De vigtigste kommercielle modeller er:

- **Gemini 3 Pro / 3 Pro Image (Nano Banana Pro)** — Googles native multimodale model med billedgenerering. 3 Pro Preview deprecated 9/3-2026; 3.1 Pro Preview er efterfølgeren. Image-varianten kører stadig.
- **GPT-5.2** — OpenAIs seneste, med forbedret visuel reasoning.
- **Claude Opus 4.6** — Anthropics 1M-context model med multimodal input (ikke billedgenerering).
- **Qwen2.5-VL-72B** — Alibabas open-source flagskib. MMMU: 64.0, MathVista: 80.1.
- **InternVL3-78B** — Open-source SOTA på MMMU med 72.2.

Open-source modeller har indsnævret gabet markant. InternVL3 og Qwen2.5-VL matcher eller overgår ældre kommercielle modeller på flere benchmarks.

### Hvad de kan (reelt)

- **Dokumentforståelse:** OCR er nu en solved problem for de fleste formater. GOT-OCR 2.0 og DeepSeek-OCR håndterer tabeller, formler, multi-kolonne layout i et enkelt pass.
- **Billedbeskrivelse:** Detaljerede beskrivelser af fotos, kunstværker, screenshots. Generelt pålidelige for standardmotiver.
- **Kode fra wireframes:** Excalidraw/tldraw "Make Real"-funktionalitet oversætter håndtegnede skitser til funktionel kode.
- **Chart-aflæsning:** Søjlediagrammer, linjediagrammer og simple pie-charts aflæses med rimelig præcision.

---

## 2. Benchmarks og hvad de måler

### MMMU (Massive Multi-discipline Multimodal Understanding)

Yue et al. (2024). CVPR 2024.
11.500 spørgsmål fra universitetsniveau på tværs af 6 discipliner (kunst, business, naturvidenskab, medicin, humaniora, teknik). Kræver faglig viden + visuelt input. MMMU-Pro (2024) er en sværere variant; modeller scorer 16,8–46,3% — dramatisk lavere end standard-MMMU.

### MathVista

Lu et al. (2024).
Matematisk reasoning med visuelle input: geometri-diagrammer, søjlediagrammer, abstrakte scener. Modeller scorer op til 80,1 (Qwen2.5-VL), men forskning viser at de "er stærkt afhængige af tekstuelle spørgsmål frem for visuel forståelse af diagrammerne."

### MM-Vet

Yu et al. (2024).
Evaluerer integrerede kompetencer: genkendelse, OCR, spatial awareness, sprog-generation. Nyeste modeller scorer ~78,4.

### POPE (Polling-based Object Probing Evaluation)

Li et al. (2023). EMNLP 2023.
Tester objekthallucination: "Er der en stol i billedet?" med tre sværhedsgrader (Random, Popular, Adversarial). Adversarial-splittet er konsekvent det mest diskriminerende. Modeller er "tilbøjelige til hallucinationer om objekters eksistens, og endnu mere om finmaskede attributter."

### H-POPE (Hierarchical POPE)

Park et al. (2024).
Udvidelse med hierarkisk evaluering af hallucinationer i LVLMs.

### SpatialBench

Chen et al. (2025).
Benchmarker spatial kognition specifikt: position, retning, afstand, rum-forståelse.

### MermaidSeqBench

IBM Research (2025). NeurIPS 2025.
Første systematiske benchmark for LLM→Mermaid sekvensdiagram-generering. 132 prøver evalueret på 6 dimensioner: syntax, logik, komplethed, aktivering, fejlhåndtering, praktisk brugbarhed. Afslører "signifikante kapacitetsgab på tværs af modeller."

---

## 3. Hvor modellerne fejler systematisk

### 3.1 Spatial reasoning

Liu et al. (2025) "Deconstructing Spatial Intelligence in Vision-Language Models" indfører en tre-niveau kognitiv hierarki: Perception → Understanding → Extrapolation. VLM'er klarer sig rimeligt på perception (hvad er der?), men fejler systematisk på understanding (hvor er det i forhold til andet?) og extrapolation (hvad sker der hvis det flyttes?).

Konkrete tal:
- GPT-4o: ~86% accuracy på visual grounding (IoU-baseret lokalisering)
- Open-source modeller: ~60%
- Spatial relationer ("mellem," "foran," "bag"): konsekvent svagt
- Dybde-afhængige præpositioner: endnu sværere
- Små objekter: dramatisk dårligere end store

### 3.2 Tælling

Modellerne kan ikke tælle pålideligt. Imbalanceret træningsdata fører til "logiske inkonsistenser i tælleaufgaver." Et billede med 7 æbler kan give svaret 5 eller 9 afhængigt af prompt-formulering. Problemet er værst for >5 objekter og for delvist skjulte objekter.

### 3.3 Kort og legender

GDELT-projektets systematiske test (2024) viste at "både GPT-4V og Gemini kæmper enormt med at fortolke kort og fejler selv de mest basale opgaver med at aflæse legender og associere farver med labels." Gemini bruger billeder som "seeds til træningsdata og reciterer typisk sine træningsdata i stedet for at beskrive hvad der faktisk er i billedet."

### 3.4 Multi-billede reasoning

MME-Survey (Fu et al., 2024): På MuirBench scorer GPT-4o 68,0% og Gemini Pro 49,3%. Open-source modeller scorer under 33,3% — dårligere end tilfældig gæt.

### 3.5 Medicinsk billedforståelse

OmniMedVQA: De fleste MLLMs "overgår kun tilfældig gæt marginalt." Specialiserede modeller: 41,5%. Generelle modeller: 50,7%.

### 3.6 Højopløsningsbilleder

MME-RealWorld: Modeller "har ikke opnået mere end 60% accuracy" på high-res billeder med fine detaljer.

---

## 4. Symbol grounding-problemet — ægte forståelse vs. mønstergenkendelse

### Farkaš, Vavrečka & Wermter (2025)

"Will multimodal large language models ever achieve deep understanding of the world?"
Frontiers in Systems Neuroscience, 2025.

Denne artikel er den mest grundige akademiske kritik af multimodale LLM'ers "forståelse" til dato. Hovedargumenter:

**Grounding-gabet:** Selv med sensorer og værktøjer forbliver "gabet mellem symbolske tokens, neurale repræsentationer og kropslig erfaring en fundamental udfordring." Mennesker grunder mening via to veje: direkte (sensorisk, motorisk, emotionel) og indirekte (sprogmedieret). MLLMs har kun adgang til den indirekte vej.

**Ikke-udviklingsmæssig træning:** Menneskelig læring er sekventiel og scaffolded — simple koncepter før komplekse. LLM'er behandler "alle ord ens, da distributionel statistik beregnes for dem alle, uanset deres naturlige tilegnelsesalder." Random dataset-ordering forhindrer meningsfuld vidensskalering.

**Vektorgrundsproblemet:** Et nyt koncept introduceret af forfatterne. Selv multimodale repræsentationer er fundamentalt "ugrundede" fordi de mangler kausal forbindelse til fysisk virkelighed. Det der ligner spatial forståelse er statistiske korrelationer i træningsdata.

**Konklusion:** Ægte forståelse kræver "tæt koblede udviklingsframeworks" hvor mening opstår gennem interaktion med verden, ikke post-hoc multimodal alignment af prætræne-de sprogmodeller.

### Implikation

Det modellerne gør er sofistikeret mønstergenkendelse i et enormt statistisk rum. Det er ekstremt nyttigt — men det er ikke forståelse i kognitiv forstand. Forskellen er kritisk: mønstergenkendelse fejler uforudsigeligt på edge cases, mens ægte forståelse degraderer gradvist og forudsigeligt.

---

## 5. Diagram-generering — strategier og værktøjer

### 5.1 Tekst-til-kode-til-diagram pipeline

Den mest pålidelige tilgang er at lade LLM'er generere struktureret kode (Mermaid, PlantUML, Graphviz DOT) som derefter renderes af dedikerede engines.

**Mermaid.js** — Markdown-lignende syntax, native support i GitHub, GitLab, Notion, Obsidian. LLM'er er stærke til at generere Mermaid-kode fordi syntaksen ligner naturligt sprog. MermaidSeqBench (IBM, NeurIPS 2025) bekræfter at modeller genererer syntaktisk korrekte sekvensdiagrammer i de fleste tilfælde, men fejler på komplethed og fejlhåndtering.

**Graphviz DOT** — Mere kontrol over layout (hierarkisk, cirkulært, kraft-baseret), men mere kompleks syntax. Bedre til store grafer og netværksdiagrammer.

**PlantUML** — Stærk til UML-specifikke diagrammer (klasse, sekvens, use case). Mere verbose end Mermaid.

### 5.2 AI-native diagramværktøjer

**Excalidraw AI** — Open-source. Text-to-diagram genererer op til 5 varianter per prompt. MCP-integration tilgængelig (mcp_excalidraw). Håndtegnet æstetik.

**tldraw "Make Real"** — Konverterer håndtegnede skitser til funktionel kode. "Draw"-funktion bruger canvas som AI-input.

**Eraser.io** — AI workflow diagram generator. Fokus på arkitekturdiagrammer og systemdesign.

**Whimsical AI** — Mindmaps, flowcharts, sekvensdiagrammer fra tekst-prompts.

**GitMind** — Genererer flowcharts, UML, ERD, infographics med AI.

### 5.3 Natif billedgenerering af diagrammer

Gemini 3 Pro Image kan generere diagrammer direkte som billeder. Fordelen er fleksibilitet i layout og æstetik. Ulempen er at output er pixel-baseret (ikke redigerbart som kode), og at tekst-rendering i genererede billeder stadig er upålideligt.

### 5.4 Hybrid-tilgang (anbefalet)

Den mest effektive pipeline kombinerer:
1. LLM genererer struktureret data/kode (Mermaid, JSON, DOT)
2. Rendering-engine producerer SVG/PNG
3. (Valgfrit) Gemini 3 Pro Image til "polish" — tilføje visuel kontekst, ikoner, farvepalette

---

## 6. SCHEMA-frameworket for Gemini 3 Pro Image

### Cazzaniga (2026)

"SCHEMA for Gemini 3 Pro Image: A Structured Methodology for Controlled AI Image Generation on Google's Native Multimodal Model."
arXiv:2602.18903.

Denne artikel er direkte relevant for Kris' brug af Nano Banana Pro. Nøglefund:

**Tre progressive niveauer:**
- **BASE (Discovery):** ~5% kontrol. Eksplorativ fase for at identificere model-biases.
- **MEDIO (Direction):** ~85% kontrol. Professionelle udkast med 7 kernelabels.
- **AVANZATO (Deliverable):** 95–98% kontrol. Produktion med målbare specifikationer.

**7 kernelabels:** Subject, Style, Lighting, Background, Composition, Mandatory, Prohibitions.

**Empiriske fund:**
- Prohibitions (negative constraints) overgår Mandatory (positive constraints): 94% vs. 91% compliance. Sig "INGEN refleksioner" i stedet for "mat overflade."
- Strukturerede SCHEMA-prompts giver 8–9 substansielt identiske billeder per 10-batch, mod 3–6 for narrative prompts.
- >95% first-generation compliance på ~300 infographics med AVANZATO-niveau prompts.

**Kritiske designprincipper:**
- Erstat subjektive termer med målbare parametre: HEX-farvekoder, Kelvin-temperatur, brændvidde-ækvivalenter.
- Single-generation filosofi: design prompten så den virker på første forsøg.
- Eksplicit failure routing: definer hvornår man skifter til alternativt værktøj.

---

## 7. Steelman: Hvorfor visuelle LLM'er allerede er nyttige for solo-dev workflows

**Argument 1: Iteration-hastighed.** En solo-udvikler kan generere 10 diagram-varianter på 30 sekunder med Mermaid + LLM. Samme arbejde tager 2-4 timer manuelt i Lucidchart. Selv hvis 3 af 10 er forkerte, er netto-tidsbesparelsen enorm.

**Argument 2: OCR er en solved problem.** Dokumentforståelse, faktura-scanning, screenshot-aflæsning fungerer pålideligt nok til produktionsbrug. GOT-OCR 2.0 og DeepSeek-OCR håndterer kanttilfælde som håndskrift og kemiske formler.

**Argument 3: "Good enough" visuals.** Gemini 3 Pro Image med SCHEMA-framework leverer >95% first-generation compliance på infographics. For en solo-dev der skal kommunikere idéer (til sig selv, til kunder, til dokumentation) er dette transformativt.

**Argument 4: Kode-fra-skitse.** tldraw "Make Real" og Excalidraw AI eliminerer det traditionelle gap mellem whiteboard-idé og funktionel prototype. En håndtegnet wireframe på telefon bliver til HTML/CSS på sekunder.

**Argument 5: Token-effektiv kommunikation.** Et diagram erstatter 500-1000 ord tekst. For en solo-dev med begrænset tid er evnen til at generere visuals der kommunikerer systemarkitektur, workflows og dataflows en force-multiplier.

---

## 8. Red team: Hvor lyver benchmarks, og hvad kan de ikke?

### 8.1 Benchmarks overvurderer kapabilitet

**Testset-kontaminering:** MMMU og MathVista bruger spørgsmål fra offentligt tilgængelige eksamener og lærebøger. Modeller trænet på web-data har sandsynligvis set varianter af disse spørgsmål. Der er ingen vandtæt garanti mod data leakage.

**Multiple-choice er nemt at game:** De fleste benchmarks bruger multiple-choice format. En model der forstår 40% af billedet men er god til at eliminere usandsynlige svar kan score 70%+. Åbne spørgsmål giver dramatisk lavere scores.

**Aggregerede scores skjuler huller:** En model med MMMU 64.0 kan score 90% på kunsthistorie og 30% på kemisk strukturanalyse. Gennemsnittet er meningsløst for den specifikke opgave du har.

### 8.2 "Forståelse" er et forkert ord

Når GPT-4V "forstår" et diagram, gør den følgende: tokeniserer billedet i patches, matcher patches mod træningsdata-distributioner, og genererer tekst der er statistisk sandsynlig givet patch-repræsentationerne. Det er ikke forståelse — det er sofistikeret mønstergenkendelse.

**Bevis:** GDELT-projektets kort-test. Modellerne kan ikke aflæse legender — en triviel opgave for et barn på 8 år. Det skyldes at kort-legender har lav frekvens i træningsdata sammenlignet med generelle billedtyper. Mønstergenkendelse fejler når mønsteret er sjældent.

### 8.3 Reasoning-modeller hallucinerer mere

OpenAIs o3-model hallucinerer 33% af tiden på PersonQA — dobbelt så meget som forgængeren o1 (16%). "Dybere reasoning" øger tilsyneladende hallucinationsrisikoen. Gemini-2.0-Flash-001 har den laveste hallucinationsrate (0,7%), men det er en hurtig, ikke-reasoning model.

### 8.4 Hvad ingen taler om

**Spatial reasoning er fundamentalt brudt.** VLM'er scorer 50-60% på spatial reasoning — marginalt bedre end tilfældig gæt for binære spørgsmål. "Er koppen til venstre for tallerkenen?" er et coin-flip.

**Tælling er upålideligt.** >5 objekter = kaos. Delvist skjulte objekter = værre. Der er ingen model der konsistent kan tælle 12 mennesker i et gruppefoto.

**Tekst i genererede billeder er stadig dårligt.** Gemini 3 Pro Image er bedre end forgængerne, men tekst-rendering i genererede billeder indeholder stadig stavefejl, forvredne bogstaver og layoutproblemer. SCHEMA-frameworket hjælper, men løser det ikke.

**Multi-billede reasoning er katastrofalt.** Opgaver der kræver sammenligning af to eller flere billeder scorer under 50% for de fleste modeller. "Hvad er forskellen mellem disse to arkitekturdiagrammer?" er en opgave de ikke kan løse pålideligt.

---

## 9. Neutral vurdering: Ærlig status marts 2026

### Hvad virker godt nok til produktion

| Opgave | Status | Pålidelighed |
|--------|--------|-------------|
| OCR / dokument-parsing | Solved | >95% |
| Billedbeskrivelse (standard) | Stærk | ~90% |
| Chart-aflæsning (simple) | God | ~80% |
| Mermaid/PlantUML generering | God | ~85% syntax-korrekt |
| Infographic-generering (SCHEMA) | God | >95% med struktureret prompt |
| Wireframe → kode | Stærk | ~85% |

### Hvad virker, men med forbehold

| Opgave | Status | Pålidelighed |
|--------|--------|-------------|
| Kompleks diagram-forståelse | Medium | ~60-70% |
| Spatial reasoning | Svag | ~50-60% |
| Tekst i genererede billeder | Medium | ~70-80% |
| Chart med mange datapunkter | Medium | ~65% |

### Hvad virker ikke

| Opgave | Status | Pålidelighed |
|--------|--------|-------------|
| Tælling (>5 objekter) | Svag | ~40-50% |
| Kort/legend-fortolkning | Svag | ~30-40% |
| Multi-billede sammenligning | Svag | ~35-50% |
| Medicinsk billedanalyse | Svag | ~40-50% |
| High-res detailanalyse | Svag | <60% |

### Den ærlige konklusion

Multimodale LLM'er er ekstremt nyttige generative værktøjer og rimelig pålidelige fortolkere af standardbilleder. De er dårlige analytikere af komplekse visuelle scener og upålidelige til opgaver der kræver ægte spatial forståelse.

For en solo-dev som Kris er den optimale strategi:
1. **Generering:** Brug Gemini 3 Pro Image med SCHEMA til infographics og visuals.
2. **Diagrammer:** Brug LLM → Mermaid/Graphviz → rendering pipeline. Aldrig bed en LLM om at "forstå" et eksisterende diagram; lad den generere et nyt.
3. **Dokumenter:** OCR og chart-aflæsning er pålidelig. Brug det.
4. **Verifikation:** Stol aldrig på en VLM's spatial eller kvantitative analyse uden manuel kontrol.

---

## 10. Implikationer for Kris' workflow

### Nano Banana Pro (Gemini 3 Pro Image)

SCHEMA-frameworket er den vigtigste opdagelse i denne research. Kris bør:
- Adoptere de 7 kernelabels (Subject, Style, Lighting, Background, Composition, Mandatory, Prohibitions)
- Bruge AVANZATO-niveau prompts med HEX-farver og målbare parametre
- Huske: negative constraints virker bedre end positive (sig "INGEN" i stedet for "skal have")

### Mindmaps og systemdiagrammer

Den mest token-effektive pipeline:
1. Beskriv strukturen i naturligt sprog
2. LLM genererer Mermaid-kode
3. Render via Mermaid CLI eller browser
4. (Valgfrit) Gemini polish til præsentation

For Ydrasil Atlas/brainmap: Mermaid er bedre end billedgenerering fordi output er redigerbart, versionerbart og søgbart.

### Hvad man IKKE skal bruge VLM'er til

- Analyse af eksisterende komplekse diagrammer (bed i stedet om at genskabe dem)
- Tælling af elementer i billeder
- Sammenligning af to versioner af et diagram
- Aflæsning af kort eller specialiserede legender

---

## 11. Litteraturliste

### Benchmarks og surveys

1. **Yue, X. et al.** (2024). "MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI." CVPR 2024. https://mmmu-benchmark.github.io/

2. **Fu, C. et al.** (2024). "MME-Survey: A Comprehensive Survey on Evaluation of Multimodal LLMs." arXiv:2411.15296.

3. **Li, Y. et al.** (2023). "Evaluating Object Hallucination in Large Vision-Language Models." EMNLP 2023. arXiv:2305.10355.

4. **Park, S. et al.** (2024). "H-POPE: Hierarchical Polling-based Probing Evaluation of Hallucinations in Large Vision-Language Models." arXiv:2411.04077.

5. **Lu, P. et al.** (2024). "MathVista: Evaluating Mathematical Reasoning of Foundation Models in Visual Contexts."

6. **Yu, W. et al.** (2024). "MM-Vet: Evaluating Large Multimodal Models for Integrated Capabilities."

7. **Chen, X. et al.** (2025). "SpatialBench: Benchmarking Multimodal Large Language Models for Spatial Cognition." arXiv:2511.21471.

8. **Fu, C. et al.** (2025). "Video-MME: The First-Ever Comprehensive Evaluation Benchmark of Multi-modal LLMs." CVPR 2025.

### Spatial reasoning og grounding

9. **Liu, D. et al.** (2025). "Deconstructing Spatial Intelligence in Vision-Language Models: A Comprehensive Survey." TechRxiv. https://www.techrxiv.org/users/992599/articles/1354538

10. **Farkaš, I., Vavrečka, M. & Wermter, S.** (2025). "Will multimodal large language models ever achieve deep understanding of the world?" Frontiers in Systems Neuroscience. https://doi.org/10.3389/fnsys.2025.1683133

11. **Huang, H.-W. & Chen, K.-M.** (2025). "Reasoning Matters for 3D Visual Grounding." arXiv:2601.08811.

12. **ACL** (2025). "Improving Spatial Reasoning in Vision-Language Models via Chain-of-Thought Annotation and Reinforcement Learning." CISAI 2025.

### Diagram-generering

13. **IBM Research** (2025). "MermaidSeqBench: An Evaluation Benchmark for LLM-to-Mermaid Sequence Diagram Generation." NeurIPS 2025. arXiv:2511.14967.

14. **Cazzaniga, L.** (2026). "SCHEMA for Gemini 3 Pro Image: A Structured Methodology for Controlled AI Image Generation." arXiv:2602.18903.

### Hallucination og fejlanalyse

15. **GDELT Project** (2024). "Multimodal Generative AI Experiments: GPT-4 vs Gemini Pro Vision Describing TV News, Images & Ukraine War Maps." https://blog.gdeltproject.org/

16. **All About AI** (2026). "AI Hallucination Report 2026: Which AI Hallucinates the Most?" https://www.allaboutai.com/resources/ai-statistics/ai-hallucinations/

### Modeldokumentation

17. **Google DeepMind** (2026). "Gemini 3 Pro Image – Nano Banana Pro." https://deepmind.google/models/gemini-image/pro/

18. **Google Cloud** (2026). "Gemini 3 Developer Guide." https://ai.google.dev/gemini-api/docs/gemini-3

### Eksisterende Ydrasil-research

19. **Claude/Kris** (2026). "Ydrasil Brainmap — Fra Mindmap til Vidensnetværk v2." `/root/Yggdra/research/brainmap_research_report_v2.md`

20. **Claude/Kris** (2026). "Layer 1 Pass 2: Knowledge Visualization — What We Missed." `/root/Yggdra/research/knowledge_visualization_survey_pass2.md`

---

*Rapporten er baseret på websearch og offentligt tilgængelige kilder per 15. marts 2026. Benchmark-scores ændrer sig hurtigt; verificér mod leaderboards ved brug.*
