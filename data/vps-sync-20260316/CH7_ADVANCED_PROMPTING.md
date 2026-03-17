# Chapter 7: Advanced Patterns — Context Engineering and Production Prompting

**Written:** 2026-02-09
**Research base:** 3 parallel agents — context engineering evolution, production prompt systems, multi-turn failure modes
**Sources:** 30+ papers, production reports, framework docs, and practitioner accounts (cited inline)

---

## 7.1 The Death of "Prompt Engineering"

In June 2025, Shopify CEO Tobi Lutke posted a tweet that named what practitioners had been feeling for a year: "I really like the term 'context engineering' over prompt engineering. It describes the core skill better: the art of providing all the context for the task to be plausibly solvable by the LLM."

Andrej Karpathy immediately co-signed: "In every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step." He listed the components: task descriptions, few-shot examples, RAG, multimodal data, tools, state and history, and compacting.

This wasn't branding. It was a correction. "Prompt engineering" had acquired an inferred definition — Simon Willison's term — that trivialized the work to "typing clever sentences into a chatbot." The actual skill had outgrown the name.

**What changed:** Early prompting (2023) was about crafting the perfect instruction. Context engineering (2025+) is about assembling the right information environment — instructions, retrieved knowledge, conversation state, tool definitions, examples, and memory — so the model can succeed. The prompt itself might be 5% of the context window. The other 95% is scaffolding.

**Why this matters for practitioners:** If you're still optimizing your instruction text while ignoring what documents get retrieved, what conversation history gets included, and how your tools are described, you're optimizing the wrong 5%.

### Our Setup as a Case Study

The Ydrasil system is context engineering without calling it that:

- **CLAUDE.md** (~200 lines, always loaded): Identity, frameworks, working principles, infrastructure map. This isn't a "prompt" — it's a persistent context layer that shapes every interaction.
- **Skills** (modular, loaded on trigger): Domain-specific knowledge files — route lookup, webapp dev, infrastructure, advisor. Only the relevant skill loads, keeping the context window focused.
- **Qdrant vector search** (dynamic, per-query): `ctx "query" --limit 5` retrieves the most relevant chunks from 40,000+ vectors. This is RAG providing query-specific context.
- **Conversation state** (accumulated): tmux session logging, auto-embedding, session history.

None of these are "prompts" in the old sense. Together, they form the context that makes every interaction useful. Remove any one layer and quality drops dramatically.

### Choose Context Engineering When / Stay with Simple Prompts When

**Invest in context engineering when:**
- Your use case involves domain knowledge that changes (routes, customers, documentation)
- You need consistent behavior across sessions and users
- Multiple people or agents interact with the same system
- The quality gap between "good prompt" and "good prompt + right context" is measurable

**Simple prompting is enough when:**
- One-off tasks with no domain knowledge needed
- The entire relevant context fits in the user message
- You're exploring, not producing

### Failure Modes

- **Context overload:** Stuffing everything in because you can. More context is not better context. Retrieval precision matters more than recall.
- **Stale context:** Memory systems that never forget. Old patterns override new information.
- **Context rot:** Accumulated noise across long sessions degrades performance. The fix is periodic compaction — summarize and reset.
- **Ignoring the 80/20:** Spending weeks on the model choice while the CLAUDE.md is 3 lines. The scaffolding *is* the product.

---

## 7.2 Prompt Composition — From Monolith to Modules

The natural evolution of prompt engineering follows the same arc as software engineering: monolith to modules to composable systems.

**Stage 1: The Monolith.** One massive system prompt. 2,000 words. Every instruction, every example, every edge case. Works until it doesn't — and when it breaks, you can't tell which part caused the failure.

**Stage 2: Modular.** Separate files for separate concerns. Miessler's 77-skill system is the clearest example: each skill has a SKILL.md (routing), context files (domain knowledge), and Workflows/ (procedures). When you say "write a blog post," only the Blogging skill loads. The Research skill stays dormant.

**Stage 3: Composable.** Prompts reference other prompts. Template variables inject dynamic content. Conditional sections activate based on context. Langfuse's prompt composability feature (March 2025) formalized this: prompts can include `{{other_prompt}}` references, enabling inheritance and override patterns.

### The Architecture That Works

The pattern that scales in production has three layers:

```
[System Layer]     — Identity, constraints, formatting rules (always loaded)
[Domain Layer]     — Skill-specific knowledge, examples, procedures (loaded on trigger)
[Query Layer]      — Retrieved context, user input, conversation state (dynamic per-turn)
```

**The system layer** is your CLAUDE.md. It changes rarely, defines personality and constraints, and sets the floor for quality.

**The domain layer** is your skills. Modular, version-controlled, testable in isolation. When the advisor skill degrades, you fix the advisor skill. The infrastructure skill is unaffected.

**The query layer** is everything assembled at runtime — RAG results, user message, recent conversation turns, tool outputs. This is where context engineering lives.

### Choose When / Avoid When

**Compose prompts when:**
- Multiple use cases share common instructions (identity, formatting)
- You need to test and version individual components
- Different users or agents need different domain layers on the same system layer
- Your prompt exceeds ~500 words and you can't tell what affects what

**Keep it simple (single prompt) when:**
- One use case, one user, stable requirements
- The prompt fits in your head
- You're prototyping (composition adds overhead before it adds value)

### Failure Modes

- **Over-engineering:** 47 template variables for a chatbot that answers 3 question types. The MIT Sloan observation: "Prompt engineering is so 2024. Try these prompt templates instead" — but templates without judgment about what to template are just organized complexity.
- **Composition without testing:** Modular prompts that have never been tested in combination. The system layer says "be concise," the domain layer says "provide thorough explanations." Nobody noticed the contradiction.
- **The God Prompt:** A system layer that tries to do everything. If your CLAUDE.md is 2,000 lines, it's not a system prompt — it's an untested codebase.

---

## 7.3 Meta-Prompting — Using LLMs to Write Prompts

Meta-prompting is using an LLM to generate, refine, or optimize prompts for another LLM (or itself). The concept is simple. The judgment about when to use it is not.

**Three production patterns:**

1. **Automatic Prompt Engineer (APE):** Generate a pool of candidate prompts, evaluate each on a test set, select the best. This is A/B testing automated. Works when you have clear evaluation metrics and enough test cases.

2. **Contrastive refinement (LCP):** Compare successful prompts against failed ones on identical inputs. The LLM identifies what distinguishes them. Works when you have examples of success and failure — the contrast is the signal.

3. **Conductor pattern:** A meta-model breaks a complex task into subtasks, generates specialized prompts for each, dispatches to specialist instances, and synthesizes results. This is the pattern behind multi-agent research systems. It works when sub-tasks are genuinely independent and the synthesis step has clear criteria.

### Choose When / Avoid When

**Use meta-prompting when:**
- You have clear, measurable evaluation criteria (accuracy, format compliance, user satisfaction scores)
- Scale justifies the investment (100+ daily uses of the same prompt)
- You're optimizing for a well-defined objective — classification accuracy, extraction precision
- You've already written the best prompt you can manually and hit a ceiling

**Avoid meta-prompting when:**
- You don't know what "good" looks like. An LLM optimizing a prompt without clear evaluation criteria is a random walk with expensive compute.
- The bottleneck is context, not instruction. If your prompt is fine but your RAG retrieves garbage, meta-prompting optimizes the wrong layer.
- Judgment calls. Meta-prompting can optimize for measurable metrics. It cannot optimize for taste, tone, or "does this feel right for our brand." That's still human.

### Failure Modes

- **Metric gaming:** The meta-optimizer finds prompts that score well on your test set but fail on real inputs. Goodhart's Law applies: when a measure becomes a target, it ceases to be a good measure.
- **Complexity injection:** Meta-prompted outputs tend toward verbosity. The generated prompt is 800 words when the human-written 50-word version performed 90% as well. Check whether the complexity actually buys you something.
- **Recursive confusion:** Using an LLM to optimize prompts for the same LLM. The model has systematic biases. It will optimize toward those biases. Use a different (ideally stronger) model as the meta-prompter.

---

## 7.4 Prompt Optimization and Testing — The Eval-Driven Workflow

DSPy (Stanford, 16K GitHub stars, 160K monthly downloads) represents the clearest articulation of where prompting is heading: **programming, not prompting.**

DSPy's core idea: define what you want (input/output signatures), provide examples, and let the framework optimize the prompt. MIPROv2, its optimizer, uses Bayesian optimization to search over instruction phrasings and few-shot example selections. You define the objective function. It finds the prompt.

**The practical version for most teams:**

You don't need DSPy. You need a testing loop:

```
1. Write prompt
2. Run against 20-50 representative test cases
3. Measure: accuracy, format compliance, hallucination rate
4. Identify failure patterns
5. Modify prompt to address failures
6. Run again
7. Ship when regression-free
```

This is eval-driven prompting. The key insight: **you need test cases before you need a better prompt.** Most teams iterate on prompts by vibes. "This one feels better." Then they ship it and discover the 15% of inputs where it fails catastrophically.

### What to Measure

| Metric | What It Catches | How to Measure |
|--------|----------------|----------------|
| **Task completion** | Does it actually do the thing? | Binary pass/fail on test set |
| **Format compliance** | JSON that parses, markdown that renders | Schema validation |
| **Hallucination rate** | Claims without basis in provided context | LLM-as-judge against source docs |
| **Regression** | New version breaks old cases | Run full test suite after every change |
| **Latency/cost** | Prompt bloat | Track tokens in/out per query |

### LLM-as-Judge

The 2025-2026 standard for evaluation at scale: use a strong model (Claude Opus, GPT-4) to evaluate outputs from your production model. When configured with rubrics and reference answers, LLM judges achieve near-human agreement on quality metrics.

**The catch:** LLM judges have systematic biases — they prefer verbose answers, their own style, and confident-sounding text. Calibrate with human evaluation on a subset. Don't grade your own homework (same model evaluating its own outputs).

### Choose When / Avoid When

**Invest in eval infrastructure when:**
- The prompt runs 100+ times daily
- Failure has cost (wrong classification, bad extraction, user-facing errors)
- Multiple people modify the prompt (you need regression testing)
- You're comparing models or prompt versions

**Skip the infrastructure when:**
- Research and exploration (the feedback is your own judgment)
- Low-volume, human-reviewed outputs
- The prompt changes weekly and you have 3 test cases. Build the test set first.

### Failure Modes

- **Eval theater:** 500-line test suite that doesn't test the failure modes that actually matter. Optimize for coverage of *edge cases*, not coverage of easy cases.
- **Overfitting to evals:** Prompt that aces the test set, fails in production. Your test set isn't representative. Add adversarial examples.
- **The "it works" trap:** No testing at all because "it works when I try it." Your 5 manual tests don't represent the 10,000 variations real users will send.

---

## 7.5 Multi-Turn Conversation Design

This is where most production systems break, and almost nobody talks about it.

### The Number

**39% average accuracy drop** when the same task is delivered across multiple conversation turns instead of a single prompt. This is from "LLMs Get Lost In Multi-Turn Conversation" (arxiv, May 2025) — tested across all major models. Not a small model problem. GPT-4 and Gemini 2.5 Pro show 30-40% drops. Worst case: 73% degradation with long prior context.

This means your carefully designed multi-turn workflow might perform *half as well* as simply batching all the information into one message.

### Why It Happens

Four documented causes:

1. **Premature answering.** Models attempt solutions in early turns before having all information. Responses in the first 20% of turns score ~31% accuracy. Responses in the last 20% score ~64%.

2. **Assumption accumulation.** The model makes assumptions to fill gaps in early turns, then treats those assumptions as facts in later turns. Wrong assumptions don't get corrected — they compound.

3. **Lost in the middle.** The well-documented finding that models disproportionately attend to the beginning and end of their context window. Information delivered in middle turns gets less weight.

4. **Verbosity inflation.** Each turn adds more text. More text means more opportunities for noise and contradiction. Code responses grow from ~700 to 1,400+ characters across turns, with the extra length being mostly incorrect additions.

### The Consolidation Pattern

The single most effective fix: **batch all collected context into one fresh prompt before generating the final output.**

Instead of:
```
Turn 1: "I need a report"
Turn 2: "About Q4 sales"
Turn 3: "For the EU region"
Turn 4: "In markdown format"
→ Model generates from degraded 4-turn context
```

Do:
```
[System gathers all info across turns]
Final prompt: "Generate a markdown report about Q4 sales for the EU region."
→ Model generates from clean single-turn context
```

This is the "context window as a shared workspace" mental model. The conversation collects information. The generation happens from a clean, consolidated context.

### Production Patterns for Multi-Turn

| Pattern | What It Does | When to Use |
|---------|-------------|-------------|
| **Consolidate before generate** | Batch all info into single prompt | Any multi-turn workflow with final output |
| **Sliding window** | Keep last N turns, summarize older ones | Long-running assistants |
| **Hierarchical context** | Summaries at top, details available on demand | Complex multi-session workflows |
| **Periodic reset** | Summarize, start fresh conversation | When quality degrades noticeably |
| **Context budget** | Stay within 80% of practical window limit | Cost and quality optimization |

### Choose Multi-Turn When / Avoid When

**Multi-turn is appropriate when:**
- Information genuinely arrives incrementally (user doesn't know everything upfront)
- Exploration and refinement are the point (brainstorming, editing)
- The human-in-the-loop needs to steer at each step

**Prefer single-turn (or consolidation) when:**
- All information is available at the start
- You need maximum accuracy on the final output
- The task is well-defined and doesn't benefit from iterative refinement

### Failure Modes

- **Infinite conversation:** Session runs for 50 turns. Quality has degraded since turn 15, but nobody notices because the outputs are still *plausible*. Plausible and correct are different things.
- **Context amnesia:** Trusting the model to "remember" instructions from turn 3 when you're on turn 25. It won't — or it will remember them with drift.
- **The sunk cost conversation:** "We've had 20 turns of discussion, so we should continue." No. Start fresh. A new conversation with a good summary prompt will outperform a degraded 20-turn context.

---

## 7.6 Claude-Specific Patterns — What Anthropic Recommends

Every model has idiosyncrasies. Claude's are documented. Using them is free performance.

### XML Tags for Structure

Claude is specifically trained to understand XML tags as structural markers. This isn't prompting advice — it's architecture advice.

```xml
<context>
{{retrieved_documents}}
</context>

<instructions>
Analyze the documents above and extract all customer complaints.
Return as JSON array.
</instructions>

<format>
[{"complaint": "...", "severity": "high|medium|low", "customer_id": "..."}]
</format>
```

**Why it works:** XML tags create unambiguous boundaries between instruction types. The model doesn't have to infer where context ends and instructions begin. This eliminates an entire category of "the model mixed up my examples with my instructions" failures.

**Choose when:** Any prompt with multiple distinct sections. System + context + instructions + format. The more sections, the more XML tags help.

**Avoid when:** Simple single-purpose prompts. Don't wrap "What's the weather?" in XML tags.

### Prefilling — Claude's Unique Feature

Claude allows you to start the assistant's response with specific text. The model continues from where you left off.

```python
messages = [
    {"role": "user", "content": "Extract entities from: ..."},
    {"role": "assistant", "content": '{"entities": ['}  # Claude continues from here
]
```

**Production uses:**
- **Force JSON output:** Prefill with `{` — Claude never adds preamble text
- **Skip disclaimers:** Prefill with the first word of the actual answer
- **Maintain persona:** Prefill with `[CHARACTER_NAME]:` to keep role consistency

**Limitation:** Not available with extended thinking mode. For guaranteed JSON schema compliance, use Structured Outputs instead (more reliable than prefilling for production).

### Extended Thinking

When enabled, Claude shows its reasoning process before answering. This is chain-of-thought made visible and controllable.

**Choose when:** Complex reasoning, math, multi-step analysis, decisions that need auditability. When you want to *see* where the model's reasoning goes wrong, not just that it went wrong.

**Avoid when:** Simple extraction, formatting, or classification tasks. Extended thinking adds latency and tokens for no accuracy gain on straightforward tasks. Also: you cannot prefill when extended thinking is on.

### Role Prompting via System Message

Claude's system parameter sets persistent context for the entire conversation. This is where identity, constraints, and behavioral rules go — not in the user message.

```python
system = """You are a waste management route advisor for Aarhus.
You have access to route data via the ctx tool.
Always respond in Danish unless asked otherwise.
When uncertain, say so rather than guessing."""
```

**The insight:** System prompts are not suggestions. They're the strongest behavioral anchors available. Put your non-negotiable constraints here. Put your nice-to-haves in user messages.

### Failure Modes

- **Ignoring model-specific patterns:** Using Claude the same way you use GPT-4. They respond differently to the same techniques. XML tags matter more for Claude. Markdown headers matter more for GPT.
- **Prefill overreach:** Prefilling 500 tokens of the response. The model has less room to reason. Prefill the minimum needed to constrain format.
- **Extended thinking everywhere:** 3x the tokens, 2x the latency, no accuracy improvement on tasks that don't need reasoning. Use it surgically.

---

## 7.7 The Practitioner's Hierarchy

When you encounter a prompt quality problem, work through this hierarchy in order. Most problems are solved at level 1-2. Most people start at level 4.

| Level | Action | Effort | Impact |
|-------|--------|--------|--------|
| **1** | Fix the context (what information does the model see?) | Low | Highest |
| **2** | Fix the structure (XML tags, clear sections, examples) | Low | High |
| **3** | Fix the instruction (what you're asking for) | Low | Medium |
| **4** | Add evaluation (test cases, metrics, regression) | Medium | Medium |
| **5** | Optimize with meta-prompting / DSPy | High | Low-Medium |
| **6** | Change the model | High | Variable |

The Ladder of AI Solutions applies here too. Level 1 (fix the context) solves 80% of problems. Level 5 (automated optimization) solves the last 5%. Most of the blog posts are about level 5. Most of the value is at level 1.

Context > instruction > structure > optimization > model.

That is the order. Memorize it.

---

## Sources

**Context Engineering:**
- [Tobi Lutke tweet (June 2025)](https://x.com/tobi/status/1935533422589399127)
- [Andrej Karpathy tweet (June 2025)](https://x.com/karpathy/status/1937902205765607626)
- [Simon Willison, "Context Engineering" (June 2025)](https://simonwillison.net/2025/jun/27/context-engineering/)
- [Addy Osmani, "Context Engineering: Bringing Engineering Discipline to Prompts"](https://addyo.substack.com/p/context-engineering-bringing-engineering)
- [Philipp Schmid, "The New Skill in AI is Not Prompting, It's Context Engineering"](https://www.philschmid.de/context-engineering)

**Prompt Composition:**
- [Daniel Miessler, "When to Use Skills vs Commands vs Agents" (Oct 2025)](https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents)
- [Langfuse, "Prompt Composability" (March 2025)](https://langfuse.com/changelog/2025-03-12-prompt-composability)
- [MIT Sloan, "Prompt engineering is so 2024"](https://mitsloan.mit.edu/ideas-made-to-matter/prompt-engineering-so-2024-try-these-prompt-templates-instead)

**Meta-Prompting:**
- [Prompt Engineering Guide, "Meta Prompting"](https://www.promptingguide.ai/techniques/meta-prompting)
- [OpenAI Cookbook, "Enhance your prompts with meta prompting"](https://cookbook.openai.com/examples/enhance_your_prompts_with_meta_prompting)
- [IntuitionLabs, "Meta-Prompting: LLMs Crafting Their Own Prompts"](https://intuitionlabs.ai/articles/meta-prompting-llm-self-optimization)

**Optimization & Testing:**
- [DSPy Framework (Stanford)](https://dspy.ai/)
- [arxiv, "Is It Time To Treat Prompts As Code?" (2025)](https://arxiv.org/html/2507.03620v1)
- [Braintrust, "The 5 best prompt evaluation tools in 2025"](https://www.braintrust.dev/articles/best-prompt-evaluation-tools-2025)

**Multi-Turn Degradation:**
- [arxiv, "LLMs Get Lost In Multi-Turn Conversation" (May 2025)](https://arxiv.org/abs/2505.06120)
- [PromptHub, "Why LLMs Fail in Multi-Turn Conversations"](https://www.prompthub.us/blog/why-llms-fail-in-multi-turn-conversations-and-how-to-fix-it)
- [JetBrains Research, "Smarter Context Management for LLM-Powered Agents" (Dec 2025)](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)

**Claude-Specific:**
- [Anthropic, "Use XML tags to structure your prompts"](https://docs.anthropic.com/en/docs/use-xml-tags)
- [Anthropic, "Prefill Claude's response"](https://docs.anthropic.com/en/docs/prefill-claudes-response)
- [LangChain, "Context Engineering for Agents"](https://blog.langchain.com/context-engineering-for-agents/)
