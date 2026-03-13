# Claude Code Organization — Community Research (March 2026)

Research on how the Claude Code community organizes their setup.
Sources: official docs, GitHub repos, community discussions.

---

## 1. Skills Organization

### Official structure (code.claude.com/docs/en/skills)

Skills follow the [Agent Skills](https://agentskills.io) open standard. Each skill is a directory with `SKILL.md` as entrypoint:

```
my-skill/
├── SKILL.md           # Main instructions (required, YAML frontmatter + markdown)
├── template.md        # Optional: template for Claude to fill in
├── examples/          # Optional: example outputs
└── scripts/           # Optional: scripts Claude can execute
```

### Three scope levels

| Location | Path | Applies to |
|----------|------|------------|
| Enterprise | Managed settings | All users in org |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |

Higher priority wins: enterprise > personal > project.

**Monorepo support:** Claude auto-discovers skills from nested `.claude/skills/` in subdirectories (e.g. `packages/frontend/.claude/skills/`).

**Key:** Commands merged into skills. `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. Skills are the recommended path forward.

### Community patterns

**Trail of Bits** (`trailofbits/claude-code-config`):
- Three skill tiers: public skills, internal skills, curated third-party
- Managed via plugin marketplace (`/plugin marketplace add`)
- Global config repo symlinked into `~/.claude/`

**Brian Lovin** (`brianlovin/agent-config`):
- Each skill in its own subdirectory under `skills/`
- Includes: agent-browser, favicon, knip, rams, reclaude, simplify, deslop
- `install.sh` deploys via symlinks (local skills untouched)
- `sync.sh` for bidirectional syncing with timestamped backups
- Uses Bats (Bash Automated Testing System) for testing skills
- **Versioned in git, synced to `~/.claude/` via symlinks**

**Emerging convention:** Version skills in a dedicated config repo, symlink to `~/.claude/`.

### Built-in bundled skills (ship with Claude Code)

- `/simplify` — code quality review (spawns 3 parallel agents)
- `/batch <instruction>` — large-scale parallel changes across codebase
- `/debug` — troubleshoot session via debug log
- `/loop [interval] <prompt>` — recurring scheduled tasks
- `/claude-api` — load API reference for your language

---

## 2. MCP Server Setup

### Official conventions (code.claude.com/docs/en/mcp)

Two config files, merged automatically:
- `~/.mcp.json` — global servers (available in every session)
- `.mcp.json` (project root) — project-specific servers

### Transport types
- **stdio** — 80% of needs, local tools
- **HTTP** — recommended for cloud-based services (replaced SSE)
- **SSE** — deprecated in favor of HTTP

### Credential management
- `${VAR}` syntax in `.mcp.json` for environment variables
- Passed with `--env` / `-e` flag, stored encrypted locally
- **Never commit API keys** — use env vars

### Community patterns

**Trail of Bits:**
- Global: Context7, Exa in `~/.mcp.json`
- Project-specific in repo root `.mcp.json`
- MCP template (`mcp-template.json`) in config repo

**Practical starter set:** GitHub, Brave Search, Playwright covers 80% of use cases.

---

## 3. Hooks Organization

### Official: 16 lifecycle events

| Event | Purpose |
|-------|---------|
| SessionStart | Session begins/resumes |
| UserPromptSubmit | Before Claude processes prompt |
| **PreToolUse** | Before tool call — **can block it** |
| PermissionRequest | When permission dialog appears |
| **PostToolUse** | After tool call succeeds |
| PostToolUseFailure | After tool call fails |
| Notification | When Claude sends notification |
| SubagentStart/Stop | Subagent lifecycle |
| Stop | Claude finishes responding |
| TeammateIdle | Agent team teammate going idle |
| TaskCompleted | Task marked complete |
| InstructionsLoaded | CLAUDE.md loaded |
| ConfigChange | Config file changed |
| WorktreeCreate/Remove | Git worktree lifecycle |
| PreCompact | Before context compaction |
| SessionEnd | Session terminates |

### Hook locations (scope levels)

| Location | Scope | Shareable |
|----------|-------|-----------|
| `~/.claude/settings.json` | All projects | No (local) |
| `.claude/settings.json` | Single project | Yes (commit to repo) |
| `.claude/settings.local.json` | Single project | No (gitignored) |
| Managed policy | Organization-wide | Yes (admin) |
| Plugin `hooks/hooks.json` | When plugin enabled | Yes (bundled) |
| Skill/agent frontmatter | While component active | Yes (in component) |

### Community patterns

**Trail of Bits:**
- Hook scripts stored in `/hooks` directory
- PreToolUse: block dangerous patterns
- PostToolUse: audit logging, mutation tracking
- Stop: validation gates before session completion
- Exit codes: 0 = allow, 1 = non-blocking error, 2 = block

**PreToolUse is the power hook.** Can approve, deny, or modify tool inputs (since v2.0.10). Common uses:
- Block edits to production-critical files
- Prevent dangerous shell commands (`rm -rf`)
- Require verification before database operations
- Transparent sandboxing
- Team convention enforcement

---

## 4. The Taxonomy: Scripts vs Tools vs Skills vs MCP vs Hooks

### Clear hierarchy (as of 2026)

```
Plugin (packaging unit)
├── Skills       — what Claude KNOWS (markdown instructions, workflows)
├── Agents       — specialized subagent configurations
├── Hooks        — deterministic AUTOMATION (lifecycle events)
├── .mcp.json    — external TOOLS (MCP servers)
└── Commands     — (merged into skills, legacy)
```

### Each solves a different problem

| Component | What it does | Invoked by | Deterministic? |
|-----------|-------------|------------|----------------|
| **Skills** | Teach Claude workflows/knowledge | User (`/name`) or Claude (auto) | No (AI-driven) |
| **Hooks** | Fire at lifecycle events | System (automatic) | Yes |
| **MCP** | Connect external tools | Claude (via tool calls) | Yes (tool execution) |
| **Agents** | Isolated execution contexts | Skills or Claude | No (AI-driven) |
| **Plugins** | Bundle all of the above | User (`/plugin install`) | N/A (container) |

### Key insight from community

> "If Skills are knowledge and Hooks are automation, Plugins are the product."

Skills are AI-invoked (Claude decides when to use them based on context). Hooks are deterministic (fire on events regardless of AI). MCP provides capabilities (tools Claude can call). Plugins package everything together.

### Where do plain scripts fit?

Scripts (bash, python) are NOT a Claude Code concept — they're what hooks and skills *call*. A hook's `command` field points to a script. A skill's `scripts/` directory contains scripts Claude can execute. Scripts are the implementation; hooks/skills are the interface.

---

## 5. Iteration Cycle Terminology

### The established terms

**PDCA / Plan-Do-Check-Act** (Deming Cycle, 1950s)
- Origin: Walter Shewhart, popularized by W. Edwards Deming
- Domain: Manufacturing quality control, now universal
- The grandfather of all iteration frameworks
- Most established in process improvement / continuous improvement contexts

**Build-Measure-Learn** (Lean Startup, 2011)
- Origin: Eric Ries, "The Lean Startup"
- Domain: Product development, startups
- Fundamentally the same cycle as PDCA, rebranded for product context
- Most used when the question is "what should we build?"

**OODA Loop / Observe-Orient-Decide-Act** (1960s-70s)
- Origin: Col. John Boyd, U.S. Air Force
- Domain: Military strategy, competitive decision-making
- Key difference: doesn't require completing all steps sequentially
- Most used in fast-changing competitive environments

**Retrospective** (Agile/Scrum)
- Not a cycle — it's a single meeting/event within a sprint
- "What went well, what didn't, what to change"
- Sprint itself is the iteration cycle; retro is the reflection part

### Which is most used in software engineering?

**In software engineering specifically:**

1. **"Iterate"** — the most common informal term. Developers say "let's iterate on this" without referencing any framework.

2. **Retrospective** — most used *named practice* in day-to-day software teams (via Scrum adoption).

3. **PDCA** — most used in process improvement, DevOps, CI/CD pipeline optimization. The Agile Alliance explicitly maps Agile practices to PDCA.

4. **Build-Measure-Learn** — most used in product-oriented software teams, especially startups and feature validation.

5. **OODA** — rarely used in mainstream software engineering. Appears in incident response and competitive strategy discussions.

### The answer for your context

For a "build something, evaluate it, note learnings, iterate" cycle in a personal learning/development context, the closest established terms are:

- **PDCA** if you want the most academically established, universal term
- **Build-Measure-Learn** if you want the most intuitive, product-oriented term
- **"Iteration cycle"** or **"learning loop"** if you want plain language

None of them is wrong. PDCA has the deepest roots (70+ years). Build-Measure-Learn is the most recognizable in modern tech culture.

---

## Sources

- [Official skills docs](https://code.claude.com/docs/en/skills)
- [Official hooks reference](https://code.claude.com/docs/en/hooks)
- [Official MCP docs](https://code.claude.com/docs/en/mcp)
- [Trail of Bits claude-code-config](https://github.com/trailofbits/claude-code-config)
- [Brian Lovin agent-config](https://github.com/brianlovin/agent-config)
- [anthropics/claude-code plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
- [Claude Code Extensions taxonomy](https://www.morphllm.com/claude-code-skills-mcp-plugins)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [PDCA — Lean.org](https://www.lean.org/lexicon-terms/pdca/)
- [PDCA — Wikipedia](https://en.wikipedia.org/wiki/PDCA)
- [Lean Startup BML vs PDSA](http://www.kilkku.com/blog/2014/05/lean-startups-build-measure-learn-loop-and-the-pdsa-cycle/)
- [PDCA vs OODA comparison](https://www.learnleansigma.com/problem-solving/pdca-and-ooda-for-problem-solving/)
