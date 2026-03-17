# Research Kvalitetsframework

**Version:** 1.0 — 16. marts 2026
**Status:** Klar til implementering
**Forfatter:** Yggdra (Claude), baseret på APA-standarden og Yttre's voice memo (2026-03-16)
**Nota:** Dette framework er forfatter-designet til Yggdra-projektet. Templates og confidence-skalaen er ikke eksterne standarder — de er tilpasset vores behov. APA 7 referenceformatet er standarden; resten er vores implementation.

---

## 1. Kerneprincip

Al viden i Yggdra skal kunne spores til sin kilde. Hvis en påstand ikke har en reference, er den en mening — ikke viden. "Dårlig forskningspraksis" = markdown skrevet af AI uden dokumenteret oprindelse.

---

## 2. To Domæner: Knowledge Base vs Research

### Knowledge Base (`docs/kb/`)
Etableret, verificeret viden. Vores "grundlov lige nu." Ændres kun ved ny evidens.

- Fakta er bekræftet af mindst én pålidelig kilde
- Hver påstand har inline-citation (forfatter, år)
- Entries har confidence level og "sidst verificeret"-dato
- Graduering: en Research-fil promoveres til KB når den er peer-reviewed af Yttre

### Research (`research/`)
Igangværende undersøgelser. Work in progress. Kan indeholde foreløbige konklusioner.

- Skal have metodeafsnit (hvad blev søgt, hvor, hvornår)
- Skal have referenceliste (APA 7)
- Må indeholde spekulation — men markeret som sådan
- Promoveres til KB ved eksplicit beslutning

### Graduerings-kriterier (Research → KB)

| Krav | Beskrivelse |
|------|-------------|
| Verificeret | Mindst 2 uafhængige kilder bekræfter kernepåstande |
| Reproducerbar | Metodeafsnittet er detaljeret nok til at gentage søgningen |
| Citeret | Alle fakta-påstande har APA-reference |
| Reviewet | Yttre har læst og godkendt |
| Dateret | "Sidst verificeret" er sat |

---

## 3. Research Template

```markdown
# [Titel]: [Undertitel]

**Dato:** YYYY-MM-DD
**Forfatter:** Yggdra (Claude) / Yttre (Kristoffer)
**Status:** Draft | Review | Færdig
**Confidence:** Spekulativ | Foreløbig | Etableret

---

## Abstract

[3-5 sætninger. Hvad blev undersøgt, hvad blev fundet, hvad er implikationerne.]

## Metode

### Søgestrategi
- **Databaser:** [arXiv, OpenAlex, Semantic Scholar, Google Scholar, Web]
- **Søgetermer:** ["exact search terms used"]
- **Dato for søgning:** YYYY-MM-DD
- **Filtre:** [sprog, årstal, peer-reviewed only, etc.]
- **AI-prompts brugt:** [Hvis Claude/Gemini genererede dele af indholdet, dokumentér prompt]

### Udvælgelse & Begrænsninger
- [Inkl/ekskl-kriterier, antal fundet vs. inkluderet]
- [Begrænsninger: IP-restriktioner, sprog-bias, paywall, etc.]

## Findings

### [Overskrift 1]

[Tekst med inline-citations (Forfatter, år). Hver faktuel påstand citeret.]

### [Overskrift 2]

[Fortsæt med inline-citations.]

## Diskussion & Konklusion

[Hvad betyder fundene? Hvad er usikkert? Anbefalinger.]

## Referencer

[APA 7th edition. Alfabetisk. Se format nedenfor.]
```

---

## 4. Knowledge Base Entry Template

```markdown
# [Emne]

**Confidence:** Verified | Established | Preliminary | Speculative
**Sidst verificeret:** YYYY-MM-DD
**Kilder:** [research/filnavn.md] + eksterne referencer

---

## Etablerede Fakta

1. **[Påstand]** (Forfatter, år, s. X).
2. **[Påstand]** (Forfatter, år; Forfatter2, år).

## Praktisk Implikation

[Hvad betyder dette for Yggdra/vores arbejde?]

## Åbne Spørgsmål

- [Hvad er stadig usikkert?]

## Referencer

[APA 7. Kun de kilder der faktisk er citeret ovenfor.]
```

---

## 5. APA 7 Reference-format

### Journal-artikel
```
Eftername, F. N., & Eftername, F. N. (År). Artiklens titel. Journal Navn, volumen(nummer), sider. https://doi.org/xxxxx
```

### Bog
`Eftername, F. N. (År). Bogens titel (udgave). Forlag.`

### Webside / Blog
`Eftername, F. N. (År, dato). Titlen på siden. Site Navn. https://url`

### arXiv preprint
`Eftername, F. N. (År). Titel. arXiv. https://arxiv.org/abs/XXXX.XXXXX`

### Inline-citation
Én: (Miller, 1956) | To: (Craik & Lockhart, 1972) | Tre+: (Diamond et al., 2007) | Citat: (Miller, 1956, s. 81) | Flere: (Born & Wilhelm, 2012; Nader et al., 2000)

---

## 6. Confidence Scale

| Niveau | Betydning | Krav | Eksempel |
|--------|-----------|------|----------|
| **Verified** | Bekræftet af flere uafhængige kilder | 2+ peer-reviewed kilder, reproducerbar | Ebbinghaus' glemselskurve |
| **Established** | Bredt accepteret, én solid kilde | 1 peer-reviewed kilde eller officiel dokumentation | MemGPT arkitektur-beskrivelse |
| **Preliminary** | Lovende men ufuldstændig evidens | Preprint, blog fra troværdig kilde, egne tests | LightRAG vs GraphRAG pris-sammenligning |
| **Speculative** | Hypotese, ingen direkte evidens | Logisk ræsonnement, analogier, AI-genereret | "FSRS-scoring kan implementeres i Qdrant" |

Tidsdimension: Confidence falder over tid. Decay-rate: Kognitiv videnskab (5-10 år), AI/ML frameworks (3-6 mdr), API-docs (1-3 mdr).

---

## 7. Eksempel: GOD Praksis

**Fil:** `research/human_memory_research.md` (eksisterende fil)

Hvad den gør rigtigt:
- Inline-citations: "(Atkinson & Shiffrin, 1968)", "(Cowan, 2001)"
- Separat kildesektion med 20+ akademiske referencer
- Mange referencer har DOI-links eller PubMed-links
- Klar struktur med sektioner

Hvad den mangler (og skal opgraderes):
- Ingen eksplicit metode-sektion (hvad blev søgt, hvor, hvornår)
- Referencer mangler journal, volumen, sidetal
- Ingen confidence-markering
- Ingen "Abstract" eller "Diskussion"

**Eksempel — nuværende vs. korrekt:**
Nu: `Cowan, N. (2001). The magical number 4 in short-term memory.`
APA 7: `Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. Behavioral and Brain Sciences, 24(1), 87-114. https://doi.org/10.1017/S0140525X01003922`

---

## 8. Eksempel: DÅRLIG Praksis

**Fil:** `research/knowledge_visualization_survey.md` (eksisterende fil)

Problemer:
- Kilder er bare URL-lister uden forfatter, dato eller titel-format
- "Sources: [Storyflow Best Mind Mapping 2025], [Digital Project Manager...]" — ikke-reproducerbar
- Påstande som "FalkorDB achieved 90% hallucination reduction" uden kilde der kan verificeres
- "The global mind-mapping software market is projected to reach USD 6.3B by 2032" — hvem siger det? Hvilken rapport?
- Ingen metode: Hvor blev der søgt? Med hvilke termer?
- Ingen confidence-markering

**Burde have:** `FalkorDB opnåede 90% reduktion i hallucination (Chen et al., 2025, s. 12).` + fuld APA-reference i ## Referencer.

---

## 9. Migrations-plan (Inkrementel)

Opgrader IKKE alle 60+ filer på én gang. Prioritér efter brug.

### Fase 1: Nye filer (med det samme)
- Al ny research følger templaten fra sektion 3
- Ingen undtagelser. Hellere en kort fil med 3 gode kilder end en lang fil uden

### Fase 2: Top 10 mest brugte (næste 2 uger)
- Tilføj Abstract, Metode (retrospektivt), manglende APA-felter, Confidence
- Kandidater: `human_memory_research.md`, `memory_autonomy_research_2026-02-23.md`, `agents_context_engineering.md`

### Fase 3: Resten (løbende, "touch it fix it")
- Opgradér ved brug. Filer urørt i 3 mdr: arkivér til `research/archive/`

### Fase 4: KB-udtræk (efter fase 2)
- Udtræk etablerede fakta til `docs/kb/`. Hvert entry refererer til sin research-fil.

---

## 10. Regler for Kvalitets-agenten

Når Claude/Yggdra producerer research:

### Skal
1. Dokumentér ALLE kilder i APA 7 — INGEN undtagelser
2. Inkludér metode-sektion med søgetermer, databaser, dato
3. Markér confidence level på dokumentet
4. Skelne mellem "kilde siger X" og "jeg konkluderer X"
5. Ved AI-genereret indhold: dokumentér hvilken model og prompt

### Må ikke
1. Skrive fakta-påstande uden citation
2. Bruge "det er velkendt at..." eller "forskning viser at..." uden reference
3. Citere en kilde der ikke er læst (sekundær-citation skal markeres: "som citeret i...")
4. Blande Verified og Speculative påstande uden markering
5. Opgradere confidence uden ny evidens

### Pre-commit check (automatiserbar)
```
- [ ] Har filen en ## Referencer sektion?
- [ ] Er der mindst 1 inline-citation per fakta-afsnit?
- [ ] Er confidence level angivet i header?
- [ ] Er metode-sektion til stede (for research-filer)?
- [ ] Er "Sidst verificeret" dato sat (for KB-entries)?
```

---

## 11. Projekt-specifik Research

Projekter under `projects/` kan have egen research, men: fuld research hører i `research/` (kanonisk). Projektet refererer med `Se: research/filnavn.md`. Projekt-specifik kontekst kan ligge lokalt. Duplikér ALDRIG indhold — referér det.

---
---

## 12. Referencer

American Psychological Association. (2019). *Publication manual of the American Psychological Association* (7th ed.). https://doi.org/10.1037/0000165-000

Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*, 24(1), 87–114. https://doi.org/10.1017/S0140525X01003922

Atkinson, R. C., & Shiffrin, R. M. (1968). Human memory: A proposed system and its control processes. In K. W. Spence & J. T. Spence (Eds.), *The psychology of learning and motivation* (Vol. 2, pp. 89–195). Academic Press.

Ebbinghaus, H. (1885). *Über das Gedächtnis: Untersuchungen zur experimentellen Psychologie*. Duncker & Humblot. (Engelsk oversættelse: *Memory: A contribution to experimental psychology*, Teachers College Columbia University, 1913.)

Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as operating systems. *arXiv*. https://arxiv.org/abs/2310.08560

### Interne kilder (verificerbar på disk)
- Voice memo transkription: `data/inbox/voice_260316_transcript.txt` — referencekrav, APA-behov, knowledge base vs research
- Eksempel GOD: `research/human_memory_research.md`
- Eksempel DÅRLIG: `research/knowledge_visualization_survey.md`

---
*Framework v1.0. Revideres efter første måneds brug.*
