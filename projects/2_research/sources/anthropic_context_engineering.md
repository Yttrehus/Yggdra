---
title: "Effective Context Engineering for AI Agents"
author: "Anthropic Applied AI team: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield, with Rafi Ayub, Hannah Moran, Cal Rueb, Connor Jennings"
date: 2025-09-29
url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
fetched: 2026-03-08
---

# Effective Context Engineering for AI Agents

## Introduction

After years of prompt engineering dominating applied AI discussions, **context engineering** has emerged as the new frontier. Rather than simply finding the right words for prompts, the field is now answering: "what configuration of context is most likely to generate our model's desired behavior?"

**Context** refers to the set of tokens included when sampling from an LLM. The **engineering** challenge involves optimizing token utility against LLM constraints to achieve consistent desired outcomes. This requires "thinking in context"—understanding the complete state available to the LLM and potential resulting behaviors.

---

## Context Engineering vs. Prompt Engineering

Anthropic views context engineering as the natural progression from prompt engineering. While prompt engineering focuses on "writing and organizing LLM instructions for optimal outcomes," context engineering addresses "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."

Early LLM engineering centered on optimizing single prompts for one-shot tasks. As agents evolved to operate across multiple inference turns over longer horizons, managing entire context states became essential—encompassing system instructions, tools, Model Context Protocol (MCP), external data, and message history.

Agents running in loops generate accumulating data that *could* be relevant for subsequent inferences. Context engineering represents "the art and science of curating what will go into the limited context window from that constantly evolving universe of possible information."

---

## Why Context Engineering Matters for Capable Agents

### Context Rot and Attention Budgets

Research on "needle-in-a-haystack" benchmarking has uncovered **context rot**: as token counts increase, models' ability to accurately recall contextual information decreases. Like humans with "limited working memory capacity," LLMs possess an "attention budget" depleted by each new token.

This constraint stems from LLM architecture. Transformer-based models enable "every token to attend to every other token" across context, creating n-squared pairwise relationships for n tokens. As context lengthens, capturing these relationships becomes stretched, creating tension between context size and attention focus.

Models trained on distributions favoring shorter sequences have "less experience with, and fewer specialized parameters for, context-wide dependencies." While techniques like position encoding interpolation enable longer sequences, degradation occurs—models remain capable but show "reduced precision for information retrieval and long-range reasoning compared to their performance on shorter contexts."

---

## The Anatomy of Effective Context

Effective context engineering means finding "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

### System Prompts

System prompts should be "extremely clear and use simple, direct language that presents ideas at the right altitude for the agent." The optimal approach balances two extremes:

- **Too prescriptive:** Hardcoding complex, brittle logic creates fragility and maintenance complexity
- **Too vague:** High-level guidance fails to provide concrete signals or assumes shared understanding

Prompts should organize into distinct sections using XML tags or Markdown headers: `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`, etc.

The principle: start with minimal prompts on the best available model, then add instructions iteratively based on identified failure modes.

### Tools

Tools define the contract between agents and their information/action space. They should promote efficiency through token-efficient returns and encouraging efficient agent behaviors.

Well-designed tools are "self-contained, robust to error, and extremely clear with respect to their intended use." Common failures include "bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use."

### Examples (Few-Shot Prompting)

Rather than stuffing prompts with edge cases, curate "diverse, canonical examples that effectively portray the expected behavior of the agent." For LLMs, examples function as "pictures worth a thousand words."

---

## Context Retrieval and Agentic Search

Agents are now defined simply as "LLMs autonomously using tools in a loop."

### Pre-Inference vs. Just-In-Time Retrieval

Traditional approaches use embedding-based pre-inference retrieval. The field increasingly adopts "just in time" strategies where agents maintain lightweight identifiers (file paths, queries, links) and dynamically load data via tools.

Anthropic's Claude Code exemplifies this approach: the model writes targeted queries and uses Bash commands (head, tail) to analyze data "without ever loading the full data objects into context." This mirrors human cognition—we don't memorize corpuses but instead use "external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."

### Progressive Disclosure

Autonomous navigation enables progressive disclosure—agents incrementally discover relevant context through exploration. File sizes suggest complexity; naming conventions hint at purpose; timestamps proxy relevance. Agents "assemble understanding layer by layer, maintaining only what's necessary in working memory."

### Trade-offs and Hybrid Approaches

Runtime exploration trades speed for relevance management. Without proper guidance, agents waste context through tool misuse or pursuing dead-ends.

Effective agents often employ hybrid strategies, retrieving some data upfront while pursuing autonomous exploration. Claude Code demonstrates this: CLAUDE.md files load initially while glob and grep enable just-in-time retrieval, "effectively bypassing the issues of stale indexing and complex syntax trees."

---

## Context Engineering for Long-Horizon Tasks

Long-horizon tasks require maintaining coherence across sequences exceeding context window limits. Three techniques address context pollution constraints:

### Compaction

Compaction summarizes conversations nearing context limits and reinitializes with the summary. Claude Code implements this by having the model summarize and compress critical details while "discarding redundant tool outputs or messages." The agent continues with compressed context plus five most recently accessed files.

The art involves choosing what to keep versus discard. Overly aggressive compaction risks losing subtle critical context. Engineers should "start by maximizing recall to ensure your compaction prompt captures every relevant piece of information from the trace, then iterate to improve precision."

### Structured Note-Taking (Agentic Memory)

Agents regularly write notes persisted outside the context window, later retrieved when relevant. This provides "persistent memory with minimal overhead."

Claude playing Pokemon demonstrates capability: the agent maintained precise tallies across thousands of game steps—"tracking objectives like 'for the last 1,234 steps I've been training my Pokemon in Route 1, Pikachu has gained 8 levels toward the target of 10.'"

Anthropic released a memory tool in public beta on the Claude Developer Platform enabling agents to "build up knowledge bases over time, maintain project state across sessions, and reference previous work without keeping everything in context."

### Sub-Agent Architectures

Rather than one agent maintaining state across entire projects, specialized sub-agents handle focused tasks with clean context windows. The lead agent coordinates high-level strategy while sub-agents perform deep work, returning "condensed, distilled summary of its work (often 1,000-2,000 tokens)."

This achieves clear separation—detailed search context remains isolated in sub-agents while the lead agent synthesizes results.

### Selection Criteria

- **Compaction:** Maintains conversational flow for extensive back-and-forth tasks
- **Note-taking:** Excels for iterative development with clear milestones
- **Multi-agent:** Handles complex research where parallel exploration pays dividends

---

## Conclusion

Context engineering represents fundamental shifts in LLM development. As models become more capable, the challenge extends beyond crafting perfect prompts to "thoughtfully curating what information enters the model's limited attention budget at each step."

Whether implementing compaction, designing token-efficient tools, or enabling just-in-time exploration, the guiding principle remains constant: "find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."

Smarter models require less prescriptive engineering, enabling greater autonomy. Yet "treating context as a precious, finite resource will remain central to building reliable, effective agents" regardless of capability improvements.
