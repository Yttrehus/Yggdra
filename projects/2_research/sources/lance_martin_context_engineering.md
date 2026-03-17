---
title: "Context Engineering for Agents"
author: Lance Martin
date: 2025-06-23
url: https://rlancemartin.github.io/2025/06/23/context_engineering/
fetched: 2026-03-08
---

# Context Engineering for Agents

## TL;DR

Agents require strategic context management to perform effectively. Context engineering involves thoughtfully populating the context window with essential information at each step of an agent's operation.

## Context Engineering

As Andrej Karpathy notes, LLMs function as a novel operating system where "the LLM is like the CPU and its context window is like the RAM." The context window has finite capacity, requiring deliberate curation—what Karpathy describes as the "delicate art and science of filling the context window with just the right information for the next step."

### Types of Context

Context engineering encompasses three primary categories:

- **Instructions** -- prompts, memories, few-shot examples, tool descriptions
- **Knowledge** -- facts and background information
- **Tools** -- feedback from tool execution

## Context Engineering for Agents

Agent systems interleave LLM invocations with tool calls, frequently handling extended tasks that accumulate significant token usage. Long-running operations can exhaust context windows, increase costs and latency, and degrade performance through issues like:

- **Context Poisoning** -- hallucinations persisting in context
- **Context Distraction** -- overwhelming context disrupting reasoning
- **Context Confusion** -- superfluous information affecting responses
- **Context Clash** -- contradictory context elements

Cognition identifies context engineering as "effectively the #1 job of engineers building AI agents," while Anthropic emphasizes that "agents often engage in conversations spanning hundreds of turns, requiring careful context management strategies."

---

## Four Core Strategies

### Write Context

**Scratchpads** enable agents to save information outside the context window. Anthropic's multi-agent researcher demonstrates this: agents "save their plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated."

Scratchpads can be implemented as tool calls (writing to files) or runtime state fields. They allow agents to preserve useful information across a task's lifecycle.

**Memories** extend scratchpads across multiple sessions. Reflexion introduced reflection-based memory generation, while Generative Agents synthesized periodic memories from accumulated feedback. Products like ChatGPT, Cursor, and Windsurf now auto-generate long-term memories from user-agent interactions.

### Select Context

**Scratchpad Selection** depends on implementation. Tool-based scratchpads allow agents to read via tool calls, while state-integrated scratchpads let developers expose selective context at each turn.

**Memory Selection** retrieves relevant stored information. Agents might select episodic memories (few-shot examples), procedural memories (behavioral instructions), or semantic memories (task-relevant facts).

Simple implementations use fixed files (like `CLAUDE.md` or rules files), but larger memory collections require sophisticated indexing. Embeddings and knowledge graphs facilitate selection, though challenges persist. Simon Willison shared an example where ChatGPT unexpectedly injected location data from memory into requested images, illustrating how unwanted retrieval can make users feel the context "no longer belongs to them."

**Tool Selection** benefits from RAG applied to tool descriptions. Recent research shows semantic similarity-based tool retrieval improves selection accuracy threefold.

**Knowledge Retrieval** (RAG) presents significant challenges, especially in code agents. Complex codebases require multifaceted approaches: "AST parsing code and chunking along semantically meaningful boundaries," combined with grep, knowledge graphs, and re-ranking rather than embeddings alone.

### Compressing Context

**Context Summarization** manages token-heavy interactions spanning hundreds of turns. Claude Code implements "auto-compact" after reaching 95% context capacity, summarizing the full agent trajectory using recursive or hierarchical approaches.

Summarization works effectively post-processing tool calls or at agent-agent boundaries. However, Cognition uses fine-tuned models for this step, indicating significant complexity in capturing critical events and decisions.

**Context Trimming** filters rather than distills, using heuristics like removing older messages or trained pruners like Provence for selective removal.

### Isolating Context

**Multi-agent Systems** distribute context across specialized agents. OpenAI's Swarm emphasizes "separation of concerns," where each agent maintains focused contexts with specific tools and instructions operating in parallel.

Anthropic's multi-agent researcher demonstrates superiority over single-agent approaches because "subagents operate in parallel with their own context windows, exploring different aspects of the question simultaneously." Tradeoffs include increased token usage (reportedly 15x more than chat) and coordination complexity.

**Environment-Based Isolation** uses sandboxing. HuggingFace's CodeAgent outputs executable code containing tool calls that run in sandboxes, with selected return values passing back to the LLM. This approach isolates token-heavy objects like images or audio as runtime variables.

**State Objects** provide structured isolation. Runtime state schemas (using Pydantic models) can designate specific fields for LLM exposure while isolating other information for selective use.

---

## Conclusion

Effective agent development centers on four context engineering strategies:

- **Write:** Save context externally for later access
- **Select:** Pull relevant context into the window
- **Compress:** Retain only essential tokens
- **Isolate:** Distribute context across subsystems

Mastering these patterns is fundamental to building capable agents today.
