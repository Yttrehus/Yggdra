---
title: "Building Effective Agents"
author: Erik Schluntz and Barry Zhang (Anthropic)
date: 2024-12-19
url: https://www.anthropic.com/research/building-effective-agents
fetched: 2026-03-08
---

# Building Effective Agents

## Introduction

Over the past year, Anthropic has collaborated with numerous teams developing large language model (LLM) agents across various industries. A consistent finding emerges: the most successful implementations rely on simple, composable patterns rather than complex frameworks. This article shares lessons learned from both customer work and internal agent development, offering practical guidance for developers.

## What Are Agents?

The term "agent" has multiple definitions. Some define agents as fully autonomous systems operating independently over extended periods using various tools. Others describe more prescriptive implementations following predefined workflows. Anthropic categorizes all variations as **agentic systems**, distinguishing between:

- **Workflows**: Systems where LLMs and tools operate through predefined code paths
- **Agents**: Systems where LLMs dynamically direct their own processes and tool usage

## When (and When Not) to Use Agents

Building LLM applications requires finding the simplest viable solution, only increasing complexity when necessary. Agentic systems trade latency and cost for improved task performance—a tradeoff worth considering carefully.

Workflows provide predictability for well-defined tasks, while agents suit situations requiring flexibility and model-driven decision-making at scale. For many applications, optimizing single LLM calls with retrieval and in-context examples suffices.

## When and How to Use Frameworks

Several frameworks facilitate agentic system implementation:

- Claude Agent SDK
- Strands Agents SDK by AWS
- Rivet (drag-and-drop GUI builder)
- Vellum (GUI tool for workflows)

These frameworks simplify standard tasks like LLM calling and tool chaining. However, they introduce abstraction layers that obscure underlying prompts and responses, complicating debugging. They may also encourage unnecessary complexity.

**Recommendation**: Start with LLM APIs directly—many patterns require only a few lines of code. If using frameworks, thoroughly understand the underlying implementation. Incorrect assumptions about what lies "under the hood" frequently cause customer issues.

## Building Blocks, Workflows, and Agents

### Building Block: The Augmented LLM

The foundational element is an LLM enhanced with retrieval, tools, and memory. Modern models actively generate search queries, select appropriate tools, and determine information retention. Focus on tailoring these capabilities to specific use cases while providing clear interfaces. The Model Context Protocol offers one approach for integrating third-party tools through straightforward client implementation.

### Workflow: Prompt Chaining

This approach decomposes tasks into sequential steps where each LLM call processes the previous output. Programmatic checks ("gates") ensure the process remains on track.

**When to use**: Ideal for tasks decomposable into fixed subtasks, prioritizing accuracy over latency.

**Examples**:
- Generating marketing copy, then translating it
- Writing document outlines, verifying them against criteria, then writing the full document

### Workflow: Routing

Routing classifies inputs and directs them to specialized followup tasks, enabling separation of concerns and specialized prompt development.

**When to use**: Best for complex tasks with distinct categories handled separately, with accurate classification possible.

**Examples**:
- Directing customer service queries (general questions, refunds, technical support) to different processes
- Routing simple questions to cost-efficient models and complex questions to capable models

### Workflow: Parallelization

LLMs work simultaneously on tasks with programmatically aggregated outputs. Two variations exist:

- **Sectioning**: Breaking tasks into independent parallel subtasks
- **Voting**: Running identical tasks multiple times for diverse outputs

**When to use**: Effective when subtasks parallelize for speed or when multiple perspectives increase confidence.

**Examples**:
- *Sectioning*: One model processes queries while another screens for inappropriate content; automating evaluations where each call assesses different performance aspects
- *Voting*: Reviewing code for vulnerabilities across multiple prompts; evaluating content appropriateness with multiple perspectives

### Workflow: Orchestrator-Workers

A central LLM dynamically breaks down tasks, delegates to worker LLMs, and synthesizes results. Unlike parallelization, subtasks aren't predefined but determined based on specific input.

**When to use**: Suited for complex tasks where required subtasks cannot be predicted in advance.

**Examples**:
- Coding products making complex multi-file changes
- Search tasks requiring information gathering from multiple sources

### Workflow: Evaluator-Optimizer

One LLM generates responses while another provides evaluation and feedback in iterative loops.

**When to use**: Effective with clear evaluation criteria and when iterative refinement demonstrably improves results. Signs of fit: responses improve with human feedback, and LLMs can provide such feedback.

**Examples**:
- Literary translation requiring nuanced refinement
- Complex search tasks needing multiple rounds of searching and analysis

### Agents

Agents emerge as production systems as LLMs mature in understanding complex inputs, reasoning, planning, tool usage, and error recovery. They receive commands or engage in interactive discussion, then operate independently, returning for information or judgment as needed. Crucially, agents must gain "ground truth" from the environment at each step (tool results, code execution) to assess progress. They may pause for human feedback at checkpoints or when encountering blockers, with completion occurring upon task success or stopping conditions (maximum iterations).

Agents handle sophisticated tasks through straightforward implementation—essentially LLMs using tools based on environmental feedback in loops. This makes tool design and documentation critical. Best practices appear in Appendix 2.

**When to use**: For open-ended problems where step requirements cannot be predicted and fixed paths cannot be hardcoded. The LLM operates many turns and must have decision-making trust. Their autonomy makes them ideal for scaling in trusted environments.

**Important consideration**: Autonomous agents incur higher costs with potential for compounding errors. Recommend extensive sandboxed testing with appropriate guardrails.

**Examples**:
- Coding agents resolving SWE-bench tasks involving multi-file edits
- Computer use reference implementation where Claude accomplishes computer-based tasks

## Combining and Customizing Patterns

These building blocks aren't prescriptive—they're common patterns developers can shape and combine. Success requires measuring performance and iterating implementations. Add complexity only when it demonstrably improves outcomes.

## Summary

Success isn't about sophisticated systems; it's about **right** systems for specific needs. Start with simple prompts, optimize through comprehensive evaluation, and add multi-step agentic systems only when simpler approaches fall short.

Three core implementation principles:

1. **Simplicity**: Maintain simple agent design
2. **Transparency**: Explicitly show agent planning steps
3. **Documentation and Testing**: Carefully craft agent-computer interfaces through thorough tool documentation and testing

Frameworks accelerate development, but reduce abstraction layers and build with basic components when moving to production. Following these principles creates powerful, reliable, maintainable agents trusted by users.

---

## Appendix 1: Agents in Practice

Customer work reveals two particularly promising agent applications demonstrating pattern value. Both require conversation and action, feature clear success criteria, enable feedback loops, and integrate meaningful human oversight.

### A. Customer Support

Customer support combines familiar chatbot interfaces with enhanced tool capabilities. Natural fit for open-ended agents because:

- Support naturally flows conversationally while requiring external information and actions
- Tools integrate customer data, order history, and knowledge base articles
- Actions like refunds or ticket updates are programmatically handled
- Success measures through user-defined resolutions

Several companies demonstrate viability through usage-based pricing for successful resolutions, showing confidence in agent effectiveness.

### B. Coding Agents

Software development shows remarkable LLM potential, evolving from code completion to autonomous problem-solving. Agents excel because:

- Code solutions verify through automated tests
- Agents iterate using test results as feedback
- Problem spaces are well-defined and structured
- Output quality measures objectively

Internal implementations now solve real GitHub issues in SWE-bench Verified benchmark from pull request descriptions alone. While automated testing verifies functionality, human review remains crucial for alignment with broader system requirements.

---

## Appendix 2: Prompt Engineering Your Tools

Tools are typically crucial agent components. "Tools enable Claude to interact with external services and APIs by specifying their exact structure and definition." When Claude responds, tool use blocks appear if tool invocation is planned. Tool definitions merit equivalent prompt engineering attention as overall prompts.

Multiple ways exist to specify identical actions. File edits may use diffs or full rewrites. Structured output may use markdown or JSON code. While cosmetically different, some formats prove harder for LLMs to write. Diffs require knowing chunk header line counts before writing new code. JSON code requires newline and quote escaping beyond markdown.

### Format Selection Suggestions:

- Give models sufficient tokens to "think" before writing themselves into corners
- Keep formats close to naturally occurring internet text
- Eliminate formatting "overhead"—avoid accurate line counts or string-escaping requirements

Think of agent-computer interfaces (ACI) as deserving human-computer interface (HCI) investment equivalence. Practical considerations:

- **Model perspective**: Are tool purposes obvious from descriptions and parameters, or require careful thought? Model usage likely mirrors human needs. Include example usage, edge cases, input format requirements, and clear boundaries from other tools.
- **Parameter optimization**: Adjust parameter names and descriptions for clarity, like writing excellent junior developer docstrings. Particularly important with similar tools.
- **Testing**: Run many example inputs through workbenches to identify model mistakes and iterate.
- **Poka-yoke**: Design arguments to make mistakes harder.

During SWE-bench agent development, more time went to tool optimization than overall prompt optimization. When relative file paths caused post-directory-move errors, changing tools to require absolute filepaths eliminated the problem entirely—models then used this method flawlessly.
