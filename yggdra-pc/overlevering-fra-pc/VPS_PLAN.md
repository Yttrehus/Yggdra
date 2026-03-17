# VPS-plan mens PC er offline

**Dato:** 16. marts 2026
**Kontekst:** PC session 24 byggede hukommelsesarkitektur v1 (Qdrant hybrid search). Yttre er muligvis offline resten af dagen. VPS kan arbejde selvstændigt med opgaver der ikke kræver PC.

---

## Prioritet 1: Qdrant hygiejne (VPS-side)

PC har oprettet to nye collections (knowledge, episodes) med hybrid search. VPS har stadig 5 legacy collections der fylder og forvirrer.

**Opgave:** Analysér om noget i legacy collections har værdi der IKKE allerede er i knowledge/episodes.

Tjek disse:
- `sessions` (43.511 points) — hvad er indholdet? Er det session-tekst der bør re-ingesttes i episodes?
- `advisor_brain` (453 points) — hvad er payloads? Er det viden der bør i knowledge?
- `docs` (1.466 points) — hvilke dokumenter? Overlapper de med det PC allerede har ingestet?
- `miessler_bible` (102 points) — Daniel Miessler materiale. Sandsynligvis værd at beholde som knowledge.
- `conversations` (81 points) — voice memos/chat. Bør i episodes.

**Output:** En rapport i denne mappe: `QDRANT_LEGACY_AUDIT.md` med anbefaling per collection: slet, migrer til knowledge, migrer til episodes, eller behold.

**Vigtigt:** SLET INTET. Kun analysér og anbefal. PC sletter når Yttre godkender.

---

## Prioritet 2: Eval-suite for memory.py

PC mangler en eval-suite. VPS kan forberede den.

**Opgave:** Skriv 20 test-queries med forventede svar baseret på det indhold der ER i knowledge-collectionen (62 research-filer). Formatet:

```json
{
  query: hybrid search best practices,
  expected_file: personal_data_pipeline_best_practices.md,
  expected_section: Hybrid search,
  relevance: Bør være top-3 resultat
}
```

**Output:** `EVAL_SUITE.json` i denne mappe.

**Kilder at kigge i:**
- `DESTILLAT_memory_retrieval.md` (553 linjer, memory + retrieval)
- `DESTILLAT_agents_automation.md` (501 linjer, agents + automation)
- `openclaw_deep_dive_2026-03-15.md` (OpenClaw arkitektur)
- `personal_data_pipeline_best_practices.md` (pipeline patterns)
- `zero_token_pipeline_architecture.md` (zero-token patterns)
- `klinisk_profilering_frameworks.md` (psykologi)
- `skattepenge_ekspertkilder_2026.md` (skat/politik)
- LLM-landskab filerne (7 provider-profiler)

---

## Prioritet 3: Mini-claw arkitektur research

Voice memoen (session 24) beskriver en vision for automatiserede OpenClaw-inspirerede mini-agents. VPS kan researche og forberede en arkitekturplan.

**Kontekst fra voice memoen:**
- Filesystem-watcher der registrerer ændringer (ikke AI, bare Python)
- Checkpoint-agent der læser event-log + session-data, opdaterer CONTEXT.md/PROGRESS.md
- Knowledge-agent der scanner research, tjekker kildehenvisninger, vurderer forfald
- Alle starter read-only med egen dagbog
- OpenClaw deep dive allerede analyseret: "Yttre behøver ikke OpenClaw. Yttre behøver 3-4 mini-claws i Python."

**Opgave:** Design en konkret arkitektur for den første mini-claw (checkpoint-agent). Inkluder:
1. Hvad trigger den (filændring, cron, manuelt)
2. Hvad læser den (event-log, session JSON, CONTEXT.md)
3. Hvad skriver den (dagbog, forslag, opdateret CONTEXT.md)
4. Hvilken model (Haiku for billigt, Opus for kvalitet)
5. Sikkerhedsmekanismer (read-only start, kill-switch, budget)
6. Estimeret token-cost per kørsel

**Output:** `MINI_CLAW_ARCHITECTURE.md` i denne mappe.

**Brug som input:**
- `openclaw_deep_dive_2026-03-15.md` (heartbeat pattern, 3-lags hukommelse, mini-claw pattern)
- `DESTILLAT_agents_automation.md` (compounding reliability, zero-token patterns)
- `zero_token_pipeline_architecture.md` (regelbaserede pipelines)
- VPS-ens egne hooks som reference (save_checkpoint.py, load_checkpoint.sh)

---

## Prioritet 4: Backlog-struktur research (lav prioritet)

Voice memoen foreslår at opløse projects/-mappen og bruge kapitel-nummerering. PC-Claude var delvist uenig. VPS kan researche fordele/ulemper og komme med et konkret forslag.

**Output:** `BACKLOG_STRUCTURE_PROPOSAL.md` i denne mappe. Kort, max 200 linjer.

---

## Regler
- Alt output i `/root/Yggdra/yggdra-pc/overlevering-fra-pc/`
- Slet INTET i Qdrant eller på disk
- Analysér og foreslå — PC/Yttre godkender
- Brug adversarial metode hvor det giver mening (steelman/red team)
- Hold rapporter under 300 linjer (destillater, ikke rapporter)
