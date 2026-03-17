# Syntese — De vigtigste principper fra alt materiale

Destilleret fra 16+ kilder: Anthropic, Manus, Zechner, Lance Martin, Nate B Jones (30 videoer + terraform-case), VPS-destillater, prompt mining af 1.270 egne prompts, loops-analyse af 148 episoder.

---

## De 10 principper

### 1. Context engineering > prompt engineering
Hvad du putter i vinduet er vigtigere end hvordan du formulerer det. Det rigtige kontekst-sæt med en middelmådig prompt slår en perfekt prompt med forkert kontekst.

**Kilder:** Anthropic (context rot, attention budget), Manus (KV-cache hit rate), agents_context_engineering (5-lags stack).
**Yggdra:** CLAUDE.md + CONTEXT.md er allerede context engineering. Men det er statisk — det opdateres ikke dynamisk baseret på opgaven.

### 2. Minimal prompt + frontier model = nok
4 tools (read/write/edit/bash) og <1000 tokens system prompt er nok til benchmark-konkurrencedygtig performance. Hvert ekstra tool/MCP-server koster 7-9% kontekst permanent.

**Kilder:** Zechner (pi), DESTILLAT_agents_automation (L0-L5 spektrum).
**Yggdra:** PC har 13 skills + hooks. VPS har 17 cron jobs. Spørgsmålet er: koster de mere kontekst end de sparer tid?

### 3. Struktureret opgave = first-shot success
3,5% af Yttres prompts er strukturerede (kontekst + output-spec + anti-patterns + DONE-kriterium). De giver næsten altid first-shot success. De resterende 96,5% er vage eller korte og kræver korrektioner.

**Kilder:** INSIGHTS.md (egne data), CH7_ADVANCED (Choose When/Avoid When per teknik).
**Yggdra:** PROMPT_KATALOG.md har 8 skabeloner. Ingen af dem bruges systematisk endnu.

### 4. Bevar fejl i konteksten
En agent der ikke kan se sine fejl kan ikke lære af dem. Fjern ikke fejlede forsøg fra konteksten — de er information.

**Kilder:** Manus ("keep errors in context"), Anthropic harnesses (failing/passing feature list).
**Yggdra:** VPS's save_checkpoint.py gemmer episoder inkl. fejl. PC's CONTEXT.md nævner kun succeser.

### 5. Compaction: start med recall, iterér mod precision
Max kontekst tidligt, komprimer progressivt. Aldrig start med at skære — start med alt og fjern det der ikke bruges.

**Kilder:** Anthropic (compaction strategy), strategic-compact skill.
**Yggdra:** PC har suggest-compact hook. VPS har PreCompact-flush. Men ingen af dem er data-drevet (de ved ikke hvad der faktisk blev brugt).

### 6. Filsystem som ekstern hukommelse
Disk > database for ephemeral state. Markdown > vectors for noget der skal læses af mennesker. Qdrant for semantisk søgning. Kombiner begge.

**Kilder:** Manus (filsystem som hukommelse), claude-mem (3-lags retrieval), Zechner (YOLO file-based state).
**Yggdra:** CONTEXT.md + PROGRESS.md + episodes.jsonl + Qdrant. Allerede hybrid. Men filerne vokser (CONTEXT.md er 200+ linjer, PROGRESS.md er 1000+).

### 7. Deterministisk kode som filter, LLM kun ved signal
Brug if/else, regex, cron, scripts til alt der kan specificeres deterministisk. LLM kun når der er ægte ambiguitet. Heartbeat-gate-keeper-mønstret.

**Kilder:** DESTILLAT_agents_automation (L0-L3 > L4-L5), heartbeat.py (regelbaseret, Groq kun til klassifikation), prompt_miner.py (regelbaseret klassifikation, Groq kun til scoring).
**Yggdra:** VPS gør dette godt. PC er mere manuelt.

### 8. Small bets — fejl kaskaderer eksponentielt
Ambitiøse one-shot sessioner fejler. Én feature, færdig, committed, videre. Progress-fil som kontrakt. Fejl kaskaderer **eksponentielt**, ikke lineært — step 4 af 12 går galt, steps 5-12 gør det værre. Ved 100 steps er det katastrofalt.

**Kilder:** Anthropic harnesses (feature list JSON), LOOPS (F5: planer≠produkter, F7: research>building), Nate Jones ("small bets" [12:10]).
**Yggdra:** PC-sessioner er ofte for brede (session 24: hukommelse + voice memo + VPS overlevering). VPS-sessioner er mere fokuserede.

### 9. Agent scaffold > agent regler
CLAUDE.md er Layer 1 — nødvendigt men utilstrækkeligt. Et agent scaffold (context file + workflow file + task list) gør det muligt at bygge stort ved at lade agenten genstarte midt i et forløb. "Save points for the agent run, not just the software."

**Kilder:** Nate Jones (Skill 2: agent scaffold [08:06]), Anthropic harnesses (progress file), Manus (todo.md recitation).
**Yggdra:** CONTEXT.md + PROGRESS.md + backlog er allerede et scaffold — men designet til mennesker. VPS's load_checkpoint.sh er tættere på et agent scaffold.

### 10. Feedback-loop fra brug til forbedring
Et system der analyserer sine egne prompts (prompt mining), benchmarker sin egen søgning (eval-suite), og tracker sine egne fejl (episodes + loops-analyse) kan forbedre sig selv. Uden feedback-loop er forbedring gætteri.

**Kilder:** INSIGHTS.md (prompt mining), LOOPS (148 episoder → 7 fejltyper), eval-suite (20 queries).
**Yggdra:** Pipeline eksisterer (prompt_miner, eval_suite). Men cirklen er brudt: analysen bliver til rapporter, ikke til ændret adfærd.

---

## Mønstre der går igen på tværs af alle kilder

1. **"Less is more" for kontekst.** Anthropic (mindste sæt high-signal tokens), Zechner (4 tools), Manus (logit masking > fjernelse), INSIGHTS (vage prompts er 54% men giver mindst). Alle siger det samme: færre, bedre tokens.

2. **State på disk, ikke i hovedet.** Manus (todo.md recitation), Anthropic harnesses (progress file), Zechner (YOLO file state), Yggdra (CONTEXT.md + NOW.md). Universelt princip.

3. **Trust benchmarks over intuition.** VPS eval: dense 83% > hybrid 61% (mod litteraturens anbefaling). METR-studie: AI-tools gør erfarne devs 19% langsommere (mod deres egen tro). Prompt mining: 54% vage kommandoer (mod Yttres tro at han prompter godt).

---

## Hvor vores praksis allerede følger best practice

- CLAUDE.md + CONTEXT.md er context engineering (princip 1)
- Filsystem som hukommelse (princip 6)
- State på disk (princip 6, 8)
- Deterministisk kode som filter på VPS (princip 7)
- Feedback-loop-infrastruktur eksisterer (princip 9)

## Hvor den afviger

- **Prompts er vage.** 54% korte kommandoer uden kontekst (princip 3 brydes)
- **Sessions er for brede.** Flere features per session (princip 8 brydes)
- **Fejl bevares ikke.** PC's CONTEXT.md nævner kun succeser (princip 4 brydes)
- **Feedback-cirklen er brudt.** Analyse → rapport → hylde. Ikke rapport → ændret adfærd (princip 9 brydes)
- **Kontekst vokser ukontrolleret.** CONTEXT.md 200+ linjer, PROGRESS.md 1000+ (princip 5 brydes)
