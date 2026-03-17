---
title: "Context Engineering for AI Agents: Lessons from Building Manus"
author: "Yichao 'Peak' Ji"
date: 2025-07-18
url: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
fetched: 2026-03-08
---

# Context Engineering for AI Agents: Lessons from Building Manus

## Introduction

The Manus team chose to build their AI agent using context engineering with frontier models rather than training end-to-end models. This decision prioritized rapid iteration—shipping improvements in hours instead of weeks—while keeping the product independent of underlying model progress.

The article shares lessons from rebuilding their agent framework four times, referring to their experimental process as "Stochastic Graduate Descent."

---

## Design Around the KV-Cache

**Key Metric:** KV-cache hit rate is "the single most important metric for a production-stage AI agent," affecting both latency and cost.

### How Agents Work

Agents receive input, select actions from a predefined space, execute them in an environment, collect observations, and append these to context for the next iteration. This creates a highly skewed input-to-output token ratio (approximately 100:1 in Manus compared to chatbots).

### Cost Implications

KV-cache dramatically reduces time-to-first-token and inference costs. With Claude Sonnet, cached tokens cost $0.30/million tokens versus $3/million uncached—a 10-fold difference.

### Best Practices

1. **Keep prompt prefix stable** — Even single-token differences invalidate cache. Avoid timestamps in system prompts.

2. **Make context append-only** — Don't modify prior actions or observations. Ensure deterministic serialization with stable JSON key ordering.

3. **Mark cache breakpoints explicitly** — Some frameworks require manual breakpoint insertion in context, accounting for potential expiration.

4. **Enable distributed caching** — Use session IDs to route requests consistently across workers in self-hosted frameworks like vLLM.

---

## Mask, Don't Remove

### The Problem with Dynamic Tool Spaces

As agent capabilities expand, tool counts explode. RAG-based dynamic loading seems intuitive but fails because:

1. **Cache invalidation** — Tool definitions near the context front mean changes invalidate all subsequent cached tokens.

2. **Reference confusion** — When prior actions reference tools no longer defined, models generate schema violations or hallucinate actions.

### The Solution: Logit Masking

Rather than removing tools, Manus masks token logits during decoding to enforce action constraints based on current state. This preserves KV-cache while controlling action selection.

### Function Calling Modes

Three implementation patterns exist:

- **Auto** — Model chooses whether to call functions
- **Required** — Model must call a function, choice unconstrained
- **Specified** — Model must select from a specific function subset

Deliberately naming tools with consistent prefixes (like `browser_` or `shell_`) enables logit masking "without using stateful logits processors."

---

## Use the File System as Context

### Limitations of Large Context Windows

Despite 128K+ token windows, real-world agentic scenarios face three problems:

1. **Huge observations** — Web pages and PDFs easily exceed limits
2. **Performance degradation** — Models underperform beyond certain lengths
3. **Expense** — Long inputs remain costly even with prefix caching

### File System as Extended Memory

Rather than aggressive compression (which loses information irreversibly), Manus treats "the file system as the ultimate context: unlimited in size, persistent by nature, and directly operable by the agent."

Models learn to write and read files on demand, using the filesystem for structured, externalized memory.

### Restorable Compression

All compression is reversible—web page content drops but URLs remain; document contents omit but file paths persist. This allows context shrinkage without permanent information loss.

### Future Implications

The author speculates that State Space Models (SSMs), which lack full attention but excel at speed and efficiency, could become viable agentic architectures if they master file-based external memory, potentially succeeding Neural Turing Machines.

---

## Manipulate Attention Through Recitation

### The Todo.md Pattern

Manus creates and updates a `todo.md` file step-by-step during complex tasks, checking off completed items. This behavior deliberately manipulates attention.

### Why It Works

Typical Manus tasks require approximately 50 tool calls. Long loops leave agents vulnerable to drifting from goals or forgetting objectives. By constantly rewriting the todo list, the agent recites objectives into the context end, pushing plans into "the model's recent attention span, avoiding lost-in-the-middle issues."

This uses natural language to bias focus toward task objectives without architectural changes.

---

## Keep the Wrong Stuff In

### Learning from Failure

Agents inevitably make mistakes—hallucinations, environment errors, tool failures, edge cases. Common impulse: hide errors, retry, or reset state.

However, "erasing failure removes evidence. And without evidence, the model can't adapt."

### The Solution

Leave failed actions in context. When models see failures and resulting observations or stack traces, they implicitly update beliefs, shifting priors away from similar actions.

Error recovery represents "one of the clearest indicators of true agentic behavior," yet remains underrepresented in academic work and public benchmarks focusing on ideal-condition success.

---

## Don't Get Few-Shotted

### The Pattern-Following Problem

Language models are "excellent mimics; they imitate the pattern of behavior in the context." When filled with similar action-observation pairs, models follow patterns even when suboptimal.

### Practical Example

Reviewing 20 resumes, agents fall into rhythm, repeating similar actions simply because the context shows this pattern, leading to drift, overgeneralization, or hallucination.

### The Fix: Controlled Diversity

Manus introduces structured variation in actions and observations—"different serialization templates, alternate phrasing, minor noise in order or formatting." This controlled randomness breaks patterns and adjusts model attention.

The principle: don't few-shot into brittleness. Uniform contexts produce fragile agents.

---

## Conclusion

Context engineering remains emerging science but essential for agent systems. Model improvements don't replace need for memory, environment, and feedback. Context shaping determines agent behavior across speed, recovery quality, and scalability.

Manus learned these patterns through "repeated rewrites, dead ends, and real-world testing across millions of users." While not universal truth, these principles proved effective internally.

**Final principle:** "The agentic future will be built one context at a time. Engineer them well."
