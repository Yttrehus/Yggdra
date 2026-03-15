# Yggdra PC Scan — Systemstate

Scan af PC-repoet (`/root/Yggdra/yggdra-pc/yggdra-repo/`) pr. 2026-03-15.

---

## Systemidentitet

Yggdra er et personligt kognitivt exoskeleton for Yttre (Kristoffer, 36, chauffør rute 256, 40% ejer rejseselskab). To instanser:

- **VPS (Ydrasil)** — driftsmiljø: Qdrant (84K vektorer), Docker, 17 cron jobs, TransportIntra webapp, intelligence pipelines
- **PC (Yggdra)** — udvikler-fundament: research, context engineering, projektstruktur, skills

20 sessioner gennemført + 3 autonome VPS sandbox loops (v1: 6 iter, v2: 10 iter, v3: 6 iter).

## Arkitektur (BLUEPRINT.md)

5 emergente lag identificeret i VPS v1-analyse:

| Lag | Funktion | Status |
|-----|----------|--------|
| 1. Epistemisk fundament | Research, vidensorganisering | Designet |
| 2. Temporal kontinuitet | Session-hooks, compaction, episodisk log | **Bygget** (4 hooks) |
| 3. Handlingsevne | Automation, scripts, MCP/skills | Kortlagt |
| 4. Tilgængelighed | Notion-spejling, voice, mobil | Uadresseret |
| 5. Situationsbevidsthed | Self-audit, peer review | Uadresseret |

Hook-system: SessionStart, PreCompact, UserPromptSubmit, Stop — alle 4 aktive og testede.

## Aktive Projekter (5)

| Projekt | Status | Substans |
|---------|--------|----------|
| **auto-chatlog** | v3 fungerer | Chatlog-engine, gap-sektioner, subagent-abstracts, secret-redaction. Mangler automatisering |
| **mcp-skills-kompendium** | v1 færdig | Adversarial evaluering afsluttet. 7+ skills bygget |
| **transportintra** | Arkiv | INDEX.md (194L crown jewels), PROGRESS.md (103L), api-reference (519L), 8 subprojects |
| **session-blindhed** | Fase 1 | Fundament oprettet, episode 001 dokumenteret |
| **vps-sandbox** | V3 done | Output hentet til PC. V4 venter |

## Backlog (TRIAGE.md — 12 briefs)

### Klar (kan startes nu)
1. **context-engineering** — Hooks fase 1-2 done. Fase 3-5 (progressive disclosure, auto-trim, context scoring) venter
2. **automation-index** — Quick win: index eksisterende hooks/cron/workflows
3. **research-architecture** — INDEX.md v3 hentet (54 Key Insights). Fase 2+ venter

### Næste op
4. **notion-spejling** — Kræver Notion MCP
5. **pdf-skill** — Faktura-layout, weasyprint, Tesseract
6. **abonnement-overblik** — Daglige udgifter, årsopgørelse
7. **cross-session-peer-review** — Parallel session workflow

### Kræver skærpning
8. **integrationer** — Gmail MCP done, GDrive/Calendar scope uklart
9. **visualisering** — Scope-valg mangler
10. **voice-integration** — Tre retninger, ingen valgt

### Lav prioritet
11. **project-taxonomy** — 7-stage lifecycle, kræver migration
12. **work-intake** — Meta-brief

### VPS Sandbox briefs (nye, ikke i TRIAGE)
13. **ai-frontier** — AI frontier topics research
14. **llm-landskab** — Provider profiler og sammenligning
15. **videns-vedligeholdelse** — Denne pipeline (aktiv nu)
16. **youtube-pipeline-v2** — YouTube intelligence pipeline redesign

## Skills (11 stk)

Installerede i `.claude/skills/`:
- context-search, debugging-wizard, dialectic-pipeline, infrastructure, mcp-builder, notion, session-resume, sitrep, spec-miner, strategic-compact, the-fool, verification-loop

## Videns-state

### Hvad PC har
- 54 Key Insights i research INDEX.md (verificeret, 3/3 spot-checks accurate)
- TransportIntra komplet arkiv (API reference, getrute schema, N8N workflows)
- 5 research rapporter (direction-analysis, context-eng, research-arch, automation, session-drift)
- ~160 VPS Ydrasil-æra research filer (downloaded session 16)
- Chatlog med ~2500 beskeder over 20 sessioner

### Hvad PC mangler
- **Ingen live data-adgang** — afhænger af SSH tunnel til VPS for Qdrant, intelligence output, cron logs
- **Ingen automatisk synk** — VPS og PC state divergerer mellem sessioner
- **Lag 4 (tilgængelighed) helt uadresseret** — ingen Notion, ingen voice, ingen mobil-adgang
- **Lag 5 (situationsbevidsthed) helt uadresseret** — ingen self-audit, ingen peer review
- **Ingen decay-tracking** — research filer har ingen markering af alder/aktualitet

## Relevans for Videns-vedligeholdelse

### Direkte relevant
1. **Research INDEX.md** har 54 Key Insights uden aktualitets-markering. Decay model bør anvendes
2. **COMPARISON.md** fra llm-landskab loopet indeholder model-data der forældes hurtigt (Elo, pricing)
3. **VPS intelligence pipelines** producerer output som PC ikke automatisk modtager
4. **research-architecture brief** adresserer vidensorganisering men ikke vedligeholdelse

### Gaps dette loop bør lukke
1. PC har ingen mekanisme til at vide hvornår VPS-produceret viden er forældet
2. Ingen bro mellem VPS intelligence output og PC research INDEX
3. Skills som context-search kræver SSH tunnel — fragil forbindelse
4. Backlog brief `videns-vedligeholdelse` er nu under udførelse på VPS men PC ved det ikke

## System-styrker
- Solid projektstruktur (CONTEXT.md overalt, TRIAGE.md, backlog briefs)
- Hook-system giver temporal kontinuitet
- TransportIntra er velarkiveret (crown jewels bevaret)
- Adversarial evaluerings-praksis (dialectic-pipeline skill)

## System-svagheder
- VPS-PC kløft: to systemer der ikke automatisk synkroniserer
- Research aldringsblindhed: ingen ved hvornår 54 Key Insights er forældede
- Backlog vokser (16 briefs) uden at projekter lukkes proportionelt
- Tilgængelighed (lag 4) er ikke bare uadresseret — det er aktivt smertepunkt (Yttre har kun telefon + PC)
