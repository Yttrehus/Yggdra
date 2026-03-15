# Source Registry — Alle Videns-kilder

Komplet register over kilder Yggdra bruger eller bør bruge til at holde AI-viden aktuel.

## Aktive Kilder (automatiserede)

| # | Kilde | Type | Frekvens | Kvalitet (1-5) | Dækning | Pipeline | URL/Metode |
|---|-------|------|----------|----------------|---------|----------|------------|
| 1 | Anthropic SDK releases | GitHub | Daglig | 5 | Anthropic tools | ai_intelligence.py | github.com/anthropics/* |
| 2 | Claude Code releases | GitHub | Daglig | 5 | Claude Code updates | ai_intelligence.py | github.com/anthropics/claude-code |
| 3 | MCP servers + spec | GitHub | Daglig | 4 | MCP ecosystem | ai_intelligence.py | github.com/modelcontextprotocol/* |
| 4 | Qdrant releases | GitHub | Daglig | 4 | Vector DB | ai_intelligence.py | github.com/qdrant/qdrant |
| 5 | Fabric releases | GitHub | Daglig | 3 | Prompt patterns | ai_intelligence.py | github.com/danielmiessler/fabric |
| 6 | Picovoice Porcupine | GitHub | Daglig | 2 | Wake word | ai_intelligence.py | github.com/picovoice/porcupine |
| 7 | HN AI stories | Web API | Daglig | 4 | Bred AI | ai_intelligence.py | hn.algolia.com |
| 8 | Reddit r/ClaudeAI | Web scrape | Daglig | 4 | Claude community | ai_intelligence.py | reddit.com/r/ClaudeAI |
| 9 | Reddit r/LocalLLaMA | Web scrape | Daglig | 3 | Open source AI | ai_intelligence.py | reddit.com/r/LocalLLaMA |
| 10 | Reddit r/MachineLearning | Web scrape | Daglig | 3 | ML research | ai_intelligence.py | reddit.com/r/MachineLearning |
| 11 | arXiv cs.AI + cs.CL | Atom API | Daglig | 3 | Research papers | ai_intelligence.py | arxiv.org/api |
| 12 | Nate B Jones | YouTube RSS | Daglig | 5 | Agents, second brain | youtube_monitor.py | Channel RSS |
| 13 | Daniel Miessler | YouTube RSS | Daglig | 5 | Security, personal AI | youtube_monitor.py | Channel RSS |
| 14 | Andrej Karpathy | YouTube RSS | Daglig | 5 | Deep learning, LLMs | youtube_monitor.py | Channel RSS |
| 15 | Cognitive Revolution | YouTube RSS | Daglig | 5 | Research interviews | youtube_monitor.py | Channel RSS |
| 16 | latent.space (YT) | YouTube RSS | Daglig | 4 | AI engineering | youtube_monitor.py | Channel RSS |
| 17 | Cole Medin | YouTube RSS | Daglig | 3 | Claude Code, Obsidian | youtube_monitor.py | Channel RSS |
| 18 | AI Automators | YouTube RSS | Daglig | 3 | RAG, n8n | youtube_monitor.py | Channel RSS |
| 19 | Matthew Berman | YouTube RSS | Daglig | 3 | AI news, benchmarks | youtube_monitor.py | Channel RSS |
| 20 | AI Jason | YouTube RSS | Daglig | 3 | Agents, tutorials | youtube_monitor.py | Channel RSS |
| 21 | IndyDevDan | YouTube RSS | Daglig | 4 | Claude Code, MCP | youtube_monitor.py | Channel RSS |
| 22 | Import AI | Substack | Daglig | 5 | AI research, policy | ai_intelligence.py | importai.substack.com |
| 23 | latent.space (blog) | Substack | Daglig | 5 | AI engineering | ai_intelligence.py | latent.space |
| 24 | One Useful Thing | Substack | Daglig | 4 | Practical AI use | ai_intelligence.py | oneusefulthing.org |
| 25 | TheSequence | Substack | Daglig | 3 | ML engineering | ai_intelligence.py | thesequence.substack.com |
| 26 | TLDR AI | Substack | Daglig | 3 | AI news digest | ai_intelligence.py | tldrai.substack.com |
| 27 | Simon Willison | RSS | Daglig | 5 | LLM tooling, practical | ai_intelligence.py | simonwillison.net |
| 28 | AlphaSignal | RSS | Daglig | 3 | Trending repos | ai_intelligence.py | alphasignal.ai |
| 29 | Source Discovery | Mixed | Ugentlig | 3 | Nye kilder | source_discovery.py | OpenAI + Qdrant |

## Manglende Kilder (bør tilføjes)

| # | Kilde | Type | Forventet kvalitet | Dækning | Effort |
|---|-------|------|--------------------|---------|--------|
| 30 | Anthropic Blog/Docs | Blog RSS | 5 | Officielle announcements | Lav — RSS feed: anthropic.com/research/rss |
| 31 | OpenAI Blog | Blog RSS | 4 | Konkurrent-announcements | Lav — RSS feed |
| 32 | Google DeepMind Blog | Blog RSS | 4 | Forskning, Gemini updates | Lav — RSS feed |
| 33 | Hugging Face Blog | Blog RSS | 4 | Open source ML, model releases | Lav — RSS feed |
| 34 | LMArena (Chatbot Arena) | Web scrape | 5 | Model rankings, Elo | Medium — ingen RSS, kræver scrape |
| 35 | Anthropic pricing page | Web scrape | 5 | Prisændringer | Lav — diff-check ugentligt |
| 36 | OpenAI pricing page | Web scrape | 4 | Konkurrent-priser | Lav — diff-check ugentligt |
| 37 | Docker Hub (qdrant, traefik) | API | 3 | Container updates | Lav — Docker Hub API |
| 38 | MCP awesome-list | GitHub | 3 | Nye MCP servers | Lav — commits watch |

## Kilde-kvalitet Kriterier

| Score | Betydning | Eksempler |
|-------|-----------|-----------|
| 5 | Primær kilde, direkte relevant, højt signal/noise | Anthropic blog, Claude Code releases, Nate Jones |
| 4 | Stærk kilde, relevant med noget noise | HN, Reddit r/ClaudeAI, One Useful Thing |
| 3 | Bred dækning, moderat noise | arXiv bulk, Matthew Berman, TLDR AI |
| 2 | Niche eller lav relevans | Picovoice (kun wake word) |
| 1 | Eksperimentel eller uverificeret | Nye discovery-kilder |

## Kilde-overlap og Redundans

Visse emner dækkes af flere kilder. Det er en styrke (robusthed) men også en risiko (noise-multiplikation):

- **Claude Code updates:** GitHub releases (primær) + HN (sekundær) + Reddit (tertiær) — GOD redundans
- **Nye modeller:** HN + Reddit + arXiv + YouTube — GOD redundans
- **API pricing:** INGEN primær kilde — kun indirekte via community. KRITISK gap
- **MCP ecosystem:** GitHub repos (primær) + IndyDevDan (sekundær) — OK
- **Agent patterns:** YouTube (primær) + Substack (sekundær) — OK men ingen re-scan

## Kilde-sundhed

| Problem | Berørte kilder | Impact |
|---------|---------------|--------|
| YouTube transcript-blokering | Alle 10 YT-kanaler | YouTube monitor kan ikke hente transcripts fra VPS uden Tor, og Tor blokeres ofte |
| Substack betalingsmur | latent.space, One Useful Thing | Kan kun hente preview, ikke fuldt indhold |
| Reddit rate limiting | 3 subreddits | .json endpoint kan blokeres ved hyppig brug |
| arXiv overfladisk scan | arXiv cs.AI/cs.CL | Top 20 pr dag misser potentielt vigtige papers |
| Source discovery noise | discovered_sources | 21 entries hvoraf ~15 er noise. Ingen cleanup-mekanisme |
