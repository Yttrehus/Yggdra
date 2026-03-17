# Context Engineering Patterns for AI Agents

**Date:** 2026-03-08
**Scope:** Strategies for managing LLM context in long-running, tool-using agents
**Sources:** Anthropic engineering blog, Manus production reports, Karpathy/Lutke definitions, PI/Zechner architecture, Vercel experiments, claude-mem, GSD, 35+ papers and practitioner reports

---

## 1. The Problem: Why Context Engineering Exists

The term "context engineering" emerged in mid-2025 when Shopify CEO Tobi Lutke reframed "prompt engineering" as insufficient: the prompt itself is ~5% of the context window; the other 95% is scaffolding — retrieved documents, conversation history, tool definitions, memory, and state. Andrej Karpathy co-signed: *"In every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step."*

Three forces make this non-trivial for agents:

**Context rot.** As tokens accumulate, model performance degrades. Anthropic's own research documents this: accuracy of recall drops as context grows, with "lost in the middle" effects where information buried in the center of a long context is effectively invisible. Studies show things start falling apart around 100K tokens regardless of what benchmarks claim (Zechner, 2025).

**Token explosion.** Production agents like Manus report 100:1 input-to-output token ratios. Every tool call adds its full output to the conversation. A 50-step agent session can easily hit 200K+ tokens, most of which is stale tool output from steps 1-30.

**Cost scaling.** Tokens in context are paid at *every* API call. A 200K-token context costs the same whether those tokens are useful or dead weight. KV-cache misses (from context mutations) multiply this further.

The solutions fall into four categories: **Offload** (move state out of context), **Reduce** (compress what stays), **Isolate** (give sub-tasks fresh context), and **Disclose progressively** (load information on demand).

---

## 2. Offload: File System as External Memory

The most underappreciated pattern. Instead of keeping state in the conversation, write it to disk and read it back when needed. The file system is unlimited, persistent, and directly operable by the agent.

### 2.1 The PLAN.md / STATE.md Pattern

Mario Zechner (PI creator) articulated the principle clearly: *"Prompts are code, .json/.md files are state."* Instead of a "plan mode" in the UI, PI writes a PLAN.md to disk. It is version-controlled, observable, and survives across sessions.

GSD (26K+ stars) formalizes this with STATE.md — a slim pointer file (<150 lines) tracking current phase, progress, decisions, blockers, and session resume path. The orchestrator reads STATE.md at session start and writes it at session end.

```python
# Pattern: File-based state management
import json
from pathlib import Path

STATE_FILE = Path("STATE.md")
TODO_FILE = Path("todo.md")

def save_agent_state(phase: int, completed: list[str], pending: list[str], decisions: list[str]):
    """Write agent state to disk — survives context resets."""
    content = f"""# Agent State
## Current Phase: {phase}
## Progress: {len(completed)}/{len(completed) + len(pending)}

### Completed
{chr(10).join(f'- [x] {t}' for t in completed)}

### Pending
{chr(10).join(f'- [ ] {t}' for t in pending)}

### Key Decisions
{chr(10).join(f'- {d}' for d in decisions)}
"""
    STATE_FILE.write_text(content)

def load_agent_state() -> str:
    """Load state at session start — fresh context, full continuity."""
    if STATE_FILE.exists():
        return STATE_FILE.read_text()
    return "No prior state found. Starting fresh."
```

### 2.2 Manus: File System as Infinite Context

Manus treats the file system as the agent's external memory. Their key insight: rather than irreversible context truncation, implement *recoverable compression*. Web page content can be dropped from context if the URL is preserved. Document contents can be omitted if the file path remains accessible. The agent can always re-read from disk.

Their `todo.md` recitation pattern deserves special attention: when handling complex tasks, the agent creates a todo.md and updates it step-by-step. By constantly rewriting the todo list at the end of context, the agent is effectively *reciting its objectives* — counteracting goal drift that occurs in long contexts.

```python
# Pattern: Todo recitation against goal drift (Manus-style)
def update_todo(tasks: list[dict], context_position: str = "end"):
    """
    Write todo to disk AND keep a summary in context.
    The act of rewriting reinforces objectives.
    """
    todo_content = "# Current Objectives\n\n"
    for task in tasks:
        marker = "x" if task["done"] else " "
        todo_content += f"- [{marker}] {task['description']}\n"

    Path("todo.md").write_text(todo_content)
    # Return summary for injection at END of context (recency bias)
    return todo_content
```

### 2.3 When to Offload

Offload when: state must survive compaction or session boundaries, data exceeds ~2K tokens and is not needed every turn, the agent needs to "remember" across 20+ tool calls.

Keep in context when: the information is needed for the *current* reasoning step, it is small (<500 tokens), or latency of a file read is unacceptable.

---

## 3. Reduce: Compaction, Summarization, Filtering

When context grows, compress it. Three sub-patterns, from simple to sophisticated.

### 3.1 Sliding Window Compaction

The simplest approach: summarize old messages, keep recent ones in full. Google ADK implements this natively:

```python
# Pattern: Sliding window with overlap (Google ADK style)
from dataclasses import dataclass

@dataclass
class CompactionConfig:
    interval: int = 10        # Compact every N turns
    overlap: int = 2          # Keep N recent turns verbatim
    summary_model: str = "haiku"  # Cheap model for summaries

def compact_history(messages: list[dict], config: CompactionConfig) -> list[dict]:
    """Replace old messages with summary, keep recent ones intact."""
    if len(messages) <= config.interval:
        return messages

    # Split: old messages to summarize, recent to keep
    to_summarize = messages[:-config.overlap]
    to_keep = messages[-config.overlap:]

    # Summarize with cheap model
    summary = summarize_with_llm(
        to_summarize,
        model=config.summary_model,
        instruction="Summarize the key decisions, facts, and outcomes. "
                    "Preserve file paths, URLs, error messages verbatim."
    )

    return [{"role": "system", "content": f"[Summary of prior conversation]\n{summary}"}] + to_keep
```

Production results: Manus reports maintaining agent quality over 50+ tool calls with 60-80% token reduction.

### 3.2 Tool Output Compaction

Tool outputs are the biggest context polluters. A `git diff` or API response can dump 10K+ tokens into context when only 200 tokens of signal matter.

```python
# Pattern: Compact tool outputs before adding to context
def compact_tool_output(tool_name: str, raw_output: str, max_tokens: int = 500) -> str:
    """
    Reduce tool output while preserving recoverability.
    Key: keep enough metadata to re-fetch if needed.
    """
    if len(raw_output) < max_tokens * 4:  # ~4 chars per token
        return raw_output

    # Preserve metadata for recovery
    metadata = extract_metadata(raw_output)  # URLs, file paths, IDs

    # Summarize content
    summary = summarize_with_llm(
        raw_output,
        instruction=f"Summarize this {tool_name} output in <{max_tokens} tokens. "
                    "Preserve: file paths, error messages, key values, URLs."
    )

    return f"{summary}\n\n[Full output available — re-run {tool_name} to retrieve]"
```

Manus's principle: compression must be *recoverable*. Never discard information that cannot be re-fetched. Keep the URL, drop the page content. Keep the file path, drop the file content.

### 3.3 Filtering Irrelevant Context

Not everything in the conversation matters for the current step. The most aggressive (and effective) approach: before each LLM call, score context items by relevance and drop the bottom tier.

```python
# Pattern: Relevance-based context filtering
def filter_context(
    messages: list[dict],
    current_task: str,
    max_context_tokens: int = 80_000
) -> list[dict]:
    """Keep only messages relevant to current task."""
    scored = []
    for msg in messages:
        relevance = score_relevance(msg["content"], current_task)  # embedding similarity
        scored.append((relevance, msg))

    # Always keep: system prompt, last 3 messages, messages with errors
    mandatory = [m for m in messages if is_mandatory(m)]
    optional = sorted(scored, key=lambda x: x[0], reverse=True)

    result = mandatory[:]
    token_count = sum(count_tokens(m["content"]) for m in mandatory)

    for relevance, msg in optional:
        if msg in mandatory:
            continue
        msg_tokens = count_tokens(msg["content"])
        if token_count + msg_tokens > max_context_tokens:
            break
        result.append(msg)
        token_count += msg_tokens

    return sorted(result, key=lambda m: messages.index(m))  # preserve order
```

Anthropic's data: context engineering strategies (including filtering) yield **54% better agent performance** versus prompt optimization alone.

---

## 4. Isolate: Sub-agents with Fresh Context

The most powerful pattern for complex tasks. Instead of one agent with a bloated context, spawn sub-agents that start with clean 200K-token windows.

### 4.1 The Fresh Context Pattern

GSD implements this rigorously: each task plan is executed by a spawned sub-agent that loads *only* the plan file, config, and relevant state pointers — not the full session history. The orchestrator stays at 10-15% context utilization.

```python
# Pattern: Sub-agent with fresh context (GSD-style)
def execute_task_in_fresh_context(
    task_plan: str,
    project_config: str,
    state_pointers: str
) -> str:
    """
    Spawn sub-agent with minimal, focused context.
    The sub-agent sees: task plan + config + state pointers.
    It does NOT see: session history, decision logs, other task outputs.
    """
    sub_agent_context = f"""
{project_config}

## Current State
{state_pointers}

## Your Task
{task_plan}

## Rules
- Complete the task described above
- Write results to files (not just to output)
- If you hit an architectural decision, STOP and report back
- Auto-fix bugs, missing imports, and error handling
"""
    result = spawn_agent(
        system_prompt=sub_agent_context,
        max_turns=50,
        timeout_minutes=10
    )
    # Only the summary returns to the orchestrator
    return result.summary  # NOT result.full_transcript
```

### 4.2 PI's Session Branching

PI (Zechner/Ronacher) takes a different approach: sessions are tree structures, not linear conversations. You can branch a session, solve a sub-problem in the branch, and bring only the result back to the main session. This is sub-agent isolation without a separate process — it is isolation *within* the session structure.

```python
# Pattern: Session branching (PI-style, conceptual)
class SessionTree:
    def __init__(self):
        self.nodes = []  # JSONL entries with id + parentId

    def branch(self, from_node_id: str, task: str) -> "Branch":
        """Create a branch for isolated work. Main context is unchanged."""
        branch = Branch(parent_id=from_node_id, task=task)
        return branch

    def merge_result(self, branch: "Branch") -> str:
        """Bring only the result back — not the branch's full history."""
        return branch.get_summary()
```

### 4.3 When to Isolate vs. Share Context

**Isolate** when: the sub-task is self-contained (code review, test writing, research), the sub-task needs to iterate (debug loops pollute parent context), or the parent context is already >50% full.

**Share context** when: the task requires back-and-forth with the user, the sub-task depends on decisions made in the current conversation, or the overhead of context transfer exceeds the benefit.

Ronacher's heuristic: *"Sub-agent execution — run iterative tasks in a separate agent, report only the summary."* Errors in sub-agents should not pollute the main context, but *what didn't work* should be preserved (so the parent doesn't retry failed approaches).

---

## 5. Progressive Disclosure of Actions

The principle: load capabilities on demand, not all at once. This applies to tools, knowledge, and instructions.

### 5.1 The Vercel Experiment

Vercel's d0 data agent had dozens of specialized tools. They removed 80% of them. The result: **success rate went from 80% to 100%**, with fewer steps, fewer tokens, and faster responses. The tools they removed were solving problems the model could handle on its own — the team had underestimated the model's native capabilities and the overhead of tool descriptions in context.

This is the core tension: every tool added to an agent's context costs tokens (~100-500 tokens per tool description) and adds decision complexity. With 80+ tools active, the model spends significant reasoning capacity just choosing which tool to use.

### 5.2 Skills as Progressive Disclosure

Anthropic's Agent Skills framework implements three-level progressive disclosure:

1. **Metadata level** (~50 tokens per skill): name + one-line description. Loaded at startup.
2. **Instruction level** (~500 tokens): full instructions, loaded when the skill is triggered.
3. **Resource level** (variable): scripts, templates, reference data. Loaded dynamically if needed.

This means an agent can have 100+ skills available at a cost of ~5K tokens (metadata only), loading full instructions only for the 1-2 skills relevant to the current task.

```python
# Pattern: Progressive skill disclosure
from dataclasses import dataclass

@dataclass
class Skill:
    name: str
    summary: str          # ~50 tokens, always in context
    instructions: str     # ~500 tokens, loaded on trigger
    resources: list[str]  # File paths, loaded on demand

class SkillRegistry:
    def __init__(self, skills: list[Skill]):
        self.skills = {s.name: s for s in skills}

    def get_manifest(self) -> str:
        """Level 1: Return metadata only. Cheap. Always in context."""
        return "\n".join(
            f"- {s.name}: {s.summary}"
            for s in self.skills.values()
        )

    def load_skill(self, name: str) -> str:
        """Level 2: Return full instructions. Loaded on demand."""
        skill = self.skills[name]
        return skill.instructions

    def load_resource(self, name: str, resource_idx: int) -> str:
        """Level 3: Return specific resource. Loaded only if needed."""
        skill = self.skills[name]
        path = skill.resources[resource_idx]
        return Path(path).read_text()
```

### 5.3 claude-mem's 3-Layer Retrieval

claude-mem (33K+ stars) implements progressive disclosure for memory retrieval:

1. **`search(query)`** — returns compact index: observation IDs, titles, dates. ~50-100 tokens per result.
2. **`timeline(anchor=ID)`** — returns chronological context around one observation. ~200-300 tokens.
3. **`get_observations([IDs])`** — returns full content for specific IDs. ~500-1000 tokens per result.

There is no "get all" operation. The agent *must* pre-filter before reading full content. Scanning 20 results costs ~1-2K tokens versus ~10-20K for full content — a 10x reduction.

### 5.4 Tool Masking vs. Tool Removal

Manus discovered that dynamically adding/removing tools between turns breaks KV-cache (because the system prompt changes). Their solution: keep all tool definitions in the system prompt permanently, but use *logit masking* to prevent the model from selecting tools that are not relevant to the current step. The cache stays warm. The model cannot select masked tools. Both goals met.

```python
# Pattern: Tool masking (Manus-style, conceptual)
def get_allowed_tools(agent_state: str, all_tools: list[str]) -> list[str]:
    """
    Instead of removing tools from the prompt (breaks cache),
    mask them at the logit level.
    """
    if agent_state == "planning":
        return ["read_file", "search", "create_plan"]
    elif agent_state == "executing":
        return ["read_file", "write_file", "edit_file", "bash"]
    elif agent_state == "reviewing":
        return ["read_file", "search", "submit_result"]
    return all_tools

# At inference time:
# allowed = get_allowed_tools(state, all_tools)
# response = llm.generate(..., tool_choice={"allowed": allowed})
# Tools not in `allowed` are masked at logit level — still in prompt, but unselectable.
```

---

## 6. Tool Design Principles

How tools are *designed* is itself context engineering. Every tool description consumes tokens and adds decision surface.

### 6.1 Few General Tools > Many Specific Tools

PI's architecture is intentional: **4 tools — Read, Write, Edit, Bash.** That is the entire core. Zechner's argument: *"Models know how to use bash and have been trained on similar schemas."* Terminal-Bench benchmarks show that this minimal toolset matches or exceeds more sophisticated toolsets.

The math: 4 tools at ~200 tokens each = 800 tokens of tool context. 40 tools at ~200 tokens each = 8,000 tokens. The 40-tool agent spends 7,200 extra tokens *per API call* just describing capabilities the model may not need.

ECC's recommendation: keep under 10 MCP servers enabled and under 80 tools total active. Beyond that, 200K context effectively shrinks to ~70K of usable space.

```
# Tool context budget (rule of thumb)
#
# 4 tools  ×  200 tokens  =    800 tokens  (~0.4% of 200K)
# 20 tools ×  200 tokens  =  4,000 tokens  (~2% of 200K)
# 80 tools ×  200 tokens  = 16,000 tokens  (~8% of 200K)
#
# At 80 tools, you've lost 8% of context before the conversation starts.
# Add MCP tool descriptions (~500 tokens each) and it gets worse fast.
```

### 6.2 Tool Descriptions as Context Engineering

The tool description is not documentation for humans — it is context for the model. A well-written tool description reduces hallucinated parameters and incorrect tool selection. A poorly-written one wastes tokens and causes errors.

Zechner's principle: *"Inherent knowledge about standard tools beats in-context learning about previously unseen tools."* If a tool maps to something the model already knows (bash commands, file operations, HTTP requests), the description can be minimal. If the tool is novel, the description must be thorough — but at that point, consider whether a bash script wrapper would be simpler.

```python
# Anti-pattern: Over-described tool
{
    "name": "search_database",
    "description": "This tool allows you to search our proprietary database system. "
                   "The database contains customer records, order history, product catalog, "
                   "and inventory data. You can search by customer name, order ID, product SKU, "
                   "or any field. Results are returned as JSON arrays. The database uses PostgreSQL "
                   "and the search is case-insensitive. Maximum 100 results per query. "
                   "Fields include: id, name, email, phone, address, created_at, updated_at, "
                   "status, type, category, subcategory, price, quantity, description...",
    # ~150 tokens of description. Most of it is noise.
}

# Better: Let the model use what it knows
{
    "name": "sql_query",
    "description": "Execute a read-only SQL query against the application database. "
                   "Schema is in schema.sql.",
    # ~30 tokens. The model knows SQL. Give it the schema file, not a prose description.
}
```

### 6.3 The Bash-is-All-You-Need Argument

Ronacher and Zechner's strongest claim: most MCP servers should be bash scripts. MCP tool descriptions consume 7-9% of the context window regardless of whether they are used. A bash script costs zero tokens until invoked, and its README serves as progressive disclosure.

Benchmark data (Zechner, 120 tests): tmux-based CLI tools were 20-29% cheaper than equivalent MCP tools at 100% success rate on identical tasks.

The exception: MCP makes sense when no CLI equivalent exists, when the tool requires persistent state (database connections), or when the client has no built-in shell access.

---

## 7. Synthesis: The Context Engineering Stack

Putting it all together, effective context engineering for agents is a layered discipline:

```
Layer 5: PROGRESSIVE DISCLOSURE
          Load skills/tools/knowledge on demand, not upfront.
          Tool masking > tool removal. 3-layer retrieval.

Layer 4: ISOLATION
          Sub-agents with fresh context for self-contained tasks.
          Orchestrator stays lean (10-15% context utilization).
          Bring back summaries, not transcripts.

Layer 3: REDUCTION
          Compact old messages. Compress tool outputs.
          Filter by relevance. Recoverable compression only.

Layer 2: OFFLOAD
          File system = external memory. STATE.md, PLAN.md, todo.md.
          Write state to disk. Read it back when needed.
          Todo recitation against goal drift.

Layer 1: FOUNDATION
          Few general tools (4-10). Short, precise tool descriptions.
          Structured output. Cache-friendly prompt design.
          The prompt is 5%. The context is 95%.
```

Each layer builds on the one below. You cannot effectively isolate sub-agents (Layer 4) if they do not offload state to files (Layer 2). Progressive disclosure (Layer 5) requires a foundation of well-designed tools (Layer 1).

The order of implementation matters: start at Layer 1 (tool design), then Layer 2 (file-based state), then Layer 3 (compaction). Layers 4 and 5 are optimizations that compound on a solid foundation.

---

## Sources

### Primary references (read in full)
- Zechner, M. (2025). "What I learned building an opinionated and minimal coding agent." mariozechner.at
- Zechner, M. (2025). "Prompts are code, .json/.md files are state." mariozechner.at
- Zechner, M. (2025). "MCP vs CLI: Benchmarking Tools for Coding Agents." mariozechner.at
- Ronacher, A. (2026). "PI." lucumr.pocoo.org
- Ronacher, A. (2025). "Agents are hard." lucumr.pocoo.org

### Web sources
- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Manus: Context Engineering for AI Agents — Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Vercel: We removed 80% of our agent's tools](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
- [Lance Martin: Context Engineering for Agents](https://rlancemartin.github.io/2025/06/23/context_engineering/)
- [LangChain: Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/)
- [Karpathy: 2025 LLM Year in Review](https://karpathy.bearblog.dev/year-in-review-2025/)
- [Anthropic: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Inkeep: Fighting Context Rot](https://inkeep.com/blog/fighting-context-rot)

### Community tools referenced
- [GSD (get-shit-done)](https://github.com/gsd-build/get-shit-done) — 26.1K stars, spec-driven workflow with STATE.md
- [claude-mem](https://github.com/thedotmack/claude-mem) — 33.4K stars, progressive disclosure memory
- [ECC (everything-claude-code)](https://github.com/affaan-m/everything-claude-code) — 65.8K stars, skills + hooks + learning
- [PI](https://shittycodingagent.ai) — minimal 4-tool coding agent
