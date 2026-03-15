# VPS Prompt — V6 Research Consolidation

## Formål
Konsolidér VPS research-banken. Gamle filer der er absorberet i destillater skal slettes. Resultatet sammenholdes med PC-projektmappen (klonet fra GitHub) for at vurdere overlap, huller og næste skridt.

## Start

```bash
cd /root/Yggdra
git -C /root/Yggdra/yggdra-pc pull origin main
```

## Fase 1 — Identifikér hvad der er absorberet (iteration 1-2)

### Iteration 1: Mapping
Læs RESEARCH_CATALOG.md og begge DESTILLAT-filer. For HVER gammel research-fil, vurdér:
- Er den **fuldt absorberet** i et destillat? → mærk SLET
- Er den **delvist absorberet** men har unikt indhold? → mærk MERGE (specificér hvad der mangler)
- Er den **ikke dækket** af noget destillat? → mærk BEHOLD

Skriv resultatet til `/root/Yggdra/research/CONSOLIDATION_MAP.md`:
```
| Fil | Status | Absorberet af | Unikt indhold |
```

### Iteration 2: Slet og verificér
- Slet alle filer mærket SLET
- For filer mærket MERGE: tilføj det unikke indhold til det relevante destillat, derefter slet
- Tæl filer før og efter. Rapportér reduktion.

## Fase 2 — Sammenhold med PC-projekt (iteration 3-4)

### Iteration 3: Scan PC-repo
Læs `/root/Yggdra/yggdra-pc/` — specifikt:
- `CONTEXT.md` (overordnet state)
- `BLUEPRINT.md` (arkitektur)
- `projects/0_backlog/TRIAGE.md` (backlog)
- `projects/2_research/` (hvad PC allerede har af V4 output)
- `projects/REF.vps-sandbox/CONTEXT.md` (VPS historik)
- Alle CONTEXT.md filer i projektmapper

Sammenhold med hvad VPS har i `/root/Yggdra/research/` efter konsolidering.

### Iteration 4: Vurdering
Skriv `/root/Yggdra/research/VPS_PC_ALIGNMENT.md`:
1. **Overlap**: Hvad findes begge steder? Er versionen på PC eller VPS nyere/bedre?
2. **Kun på VPS**: Hvad har VPS som PC mangler? Er det værd at hente?
3. **Kun på PC**: Hvad har PC som VPS ikke kender til?
4. **Huller**: Hvad mangler begge steder?
5. **Anbefalinger**: Konkrete handlinger med prioritet

## Fase 3 — Briefs og oprydning (iteration 5-6)

### Iteration 5: Nye briefs
Baseret på VPS_PC_ALIGNMENT og RED_TEAM_EVALUERING, opret nye briefs i `/root/Yggdra/yggdra-pc/projects/0_backlog/`:
- Brug `raw.` præfiks for sketches, `brief.` for gennemtænkte
- Opdatér TRIAGE.md med de nye briefs
- Opdatér eksisterende briefs der er påvirket af ny viden

### Iteration 6: Final review
- Tæl research-filer før og efter hele processen
- Kvalitetsvurdér de overlevende filer (1-10, med kriterier: korrekthed, aktualitet, actionability)
- Skriv CONSOLIDATION_REPORT.md med:
  - Filer slettet (med begrundelse)
  - Filer merged (hvad og hvorhen)
  - Filer beholdt (med kvalitetsscore)
  - Anbefalinger til PC
  - Ærlig vurdering: er research-banken nu i en tilstand der understøtter implementering?

## Regler
- Build > Research. Du sorterer og rydder op, du producerer IKKE ny research.
- Slet modigt. En fil der er absorberet i et destillat har ingen værdi som selvstændig fil.
- Vær ærlig i vurderingen. Red team's pointe ("IMPLEMENTATION_LOG, ikke RESEARCH") er korrekt.
- Brug PC-repoet som sandhed for hvad der allerede er gjort.

## Start-kommando

```bash
cd /root/Yggdra && for i in $(seq 1 6); do echo "=== Iteration $i === $(date)"; timeout 600 /root/.local/bin/claude --print "Du er iteration $i af 6. Læs denne fil for kontekst: /root/Yggdra/yggdra-pc/projects/0_backlog/vps-prompt-v6-consolidation.md — følg instrukserne for iteration $i."; sleep 10; done
```
