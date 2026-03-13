# ADR: Projekt-omdøbning
<!-- Filnavn: adr.projekt-omdobning.md -->

## 0. Metadata
- **Stage:** PoC
- **Status:** Active (venter på reformation fase 7)
- **Oprettet:** 2026-03-12
- **Sidst opdateret:** 2026-03-12
- **Ejer:** Yttre

## 1. Origin Story
Idéen opstod under session 4 (PLAN.md PDCA-evaluering af M4). "Basic Setup" var startet som opsætning af et udviklermiljø, men var vokset til et framework for hvordan Yttre arbejder med AI og kode. Navnet passede ikke længere — det var allerede Yggdra, ét system med ét navn. I session 10 blev beslutningen cementeret: repo omdøbes til Yggdra. Omdøbningen er planlagt som reformation fase 7 — efter at alt andet er på plads.

## 2. Current State
Venter. Omdøbningen er det sidste step i Project Reformation (fase 7). Alle interne referencer skal opdateres: GitHub repo-navn, workspace-fil, CLAUDE.md-filer, MEMORY.md, evt. remote URL.

## 3. Problem Statement
- **Hvad:** Repo hedder "Basic Setup" men er ikke basic og ikke bare setup. Det er Yggdra — et personligt AI-system.
- **Hvorfor:** Navnet skaber dissonans mellem hvad projektet *er* og hvad det *hedder*. Nye sessioner starter med forkert mental model.

## 4. Target State
Repo hedder "Yggdra" overalt: GitHub, lokal mappe, workspace-fil, alle CLAUDE.md-filer, MEMORY.md.

## 5. Architecture & Trade-offs
- **Beslutning:** Omdøb repo + alle referencer i ét samlet step (fase 7).
- **Risiko:** Stier i hooks, skills, og scripts kan bryde. Afbødes ved at gøre det som sidste reformation-step, efter alt er stabilt.
- **"Basic Setup" som koncept:** Kan genopstå som et *output* — en reproducerbar pakke (installationsguide + manifest). Men det er et fremtidigt projekt, ikke dette.

## 6. Evaluation
- Bryder noget efter omdøbning? (Hooks, skills, scripts, remote URL)
- Føles det rigtigt at navigere til ~/dev/projects/Yggdra/?

## 7. Exit Criteria
- **Promotion til BMS:** Omdøbningen er gennemført, alle referencer opdateret, intet bryder.
- **Sunset:** Hvis omdøbningen viser sig at skabe flere problemer end den løser (sti-afhængigheder overalt), kan den droppes.

## 8. Implementation
Se reformation ADR fase 7:
1. [ ] Omdøb repo: Basic Setup → Yggdra (GitHub + lokal)
2. [ ] Opdatér alle interne referencer
3. [ ] Commit: "reformation fase 7: Basic Setup → Yggdra"

## 9. Changelog
- 2026-03-10 (session 4): Idéen formuleret under M4 PDCA. "Basic Setup er ikke basic."
- 2026-03-12 (session 10): Beslutning cementeret. Repo omdøbes til Yggdra.
- 2026-03-12 (session 12): ADR skrevet retroaktivt som del af reformation fase 4.

## 10. Backlog
- "Basic Setup" som reproducerbar pakke (installationsguide + manifest) — fremtidigt projekt

## 11. Original ADR
Denne ADR er skrevet retroaktivt. Ingen original ADR eksisterer — beslutningen voksede organisk fra session 4 til session 10.
