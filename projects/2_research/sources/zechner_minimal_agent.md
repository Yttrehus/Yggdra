---
title: "What I learned building an opinionated and minimal coding agent"
author: Mario Zechner
date: 2025-11-30
url: https://mariozechner.at/posts/2025-11-30-pi-coding-agent/
fetched: 2026-03-08
---

# What I learned building an opinionated and minimal coding agent

## Overview

Mario Zechner describes his journey building pi, a custom coding agent harness designed around the principle that unnecessary complexity should be eliminated. Rather than adopting existing solutions, he constructed four interconnected packages to gain precise control over context engineering and user experience.

## Core Components

### pi-ai: Unified LLM API

Zechner developed a multi-provider abstraction supporting Anthropic, OpenAI, Google, xAI, Groq, Cerebras, OpenRouter, and OpenAI-compatible endpoints. Key features include:

- **Provider Quirks:** Each LLM provider implements APIs differently. For instance, Cerebras and xAI reject certain fields while Mistral uses `max_tokens` instead of `max_completion_tokens`.

- **Context Handoff:** The system enables mid-session model switching by converting provider-specific formats (like Anthropic thinking traces) into standardized representations for other models.

- **Token Tracking:** Despite provider inconsistencies in reporting, the system performs "best-effort" cost tracking across different vendors.

- **Tool Result Splitting:** Tools can return both LLM-readable content and separate UI-display content, enabling structured data visualization without cluttering model context.

### pi-agent-core

This package provides the foundational agent loop handling tool execution, result validation, and event streaming. The architecture avoids artificial constraints like maximum step limits, preferring to loop "until the agent says it's done."

### pi-tui: Terminal UI Framework

Rather than adopting existing frameworks, Zechner built a retained-mode UI system with differential rendering. The approach:

- Compares current output against previously rendered lines
- Only redraws changed content from the first difference onward
- Uses synchronized output escape sequences to prevent flicker
- Maintains a scrollback buffer for natural terminal scrolling

This contrasts with full-screen TUI alternatives that lose terminal scrollback and require custom search implementation.

### pi-coding-agent: CLI Implementation

The complete system integrates session management, custom tools, themes, and project context files called AGENTS.md.

## Design Philosophy: Minimalism

### System Prompt

The entire system prompt occupies fewer than 1,000 tokens combined:

> "You are an expert coding assistant. You help users with coding tasks by reading files, executing commands, editing code, and writing new files."

Rather than the thousands of tokens found in Claude Code or opencode, this focused approach relies on frontier models' inherent understanding of agent behavior from training.

### Four Core Tools

The toolset consists exclusively of: read, write, edit, and bash. Additional read-only variants (grep, find, ls) remain optional. This stands in stark contrast to competitors whose tool definitions span several thousand tokens.

### Intentional Omissions

**No Built-in To-Dos:** Maintaining state through ephemeral lists confuses models. Instead, agents can read and update external TODO.md files, providing persistent, visible task tracking.

**No Plan Mode:** Rather than read-only planning sessions, Zechner advocates file-based planning documents updated collaboratively, offering full observability compared to Claude Code's opaque sub-agent planning.

**No MCP Support:** Popular MCP servers like Playwright (13.7k tokens) and Chrome DevTools (18k tokens) consume 7-9% of context upfront. CLI tools with README files offer better token efficiency—the agent only reads documentation when needed.

**No Background Bash:** Process management adds unnecessary complexity. tmux provides superior observability and enables direct human interaction with running processes.

**No Sub-Agents:** Full visibility matters. When sub-agents are necessary, Zechner spawns pi itself via bash, maintaining complete transparency.

**YOLO by Default:** The system assumes user competence and provides unrestricted filesystem access without permission prompts. As Simon Willison documented, preventing both data exfiltration and code execution proves impossible when models access multiple capabilities simultaneously.

## Observability and Control

A recurring theme emphasizes visibility: "I want to inspect every aspect of my interactions with the model." Existing harnesses inject context changes invisibly, making reproducible workflows difficult. Pi surfaces all decisions explicitly through its session format.

Zechner criticizes Claude Code specifically for lacking observability regarding sub-agent decisions and background process management, calling these "a black box within a black box."

## Benchmark Results

Terminal-Bench 2.0 results show pi with Claude Opus 4.5 competing favorably against Codex, Cursor, and Windsurf with native models. Notably, Terminus 2—a minimal agent providing raw tmux access without sophisticated tooling—holds its own against complex harnesses, supporting "the argument that a minimal approach can do just as well."

## Key Learnings

1. **Context engineering requires control:** Harnesses obscuring implementation details prevent effective optimization.

2. **Simple tools outperform special-purpose features:** CLI tools with documentation beat MCP servers and built-in modes.

3. **Observability enables better collaboration:** Users should see complete agent reasoning, not filtered summaries.

4. **Constraints enable focus:** Intentional limitations like refusing to-do lists and plan modes force cleaner workflows.

5. **Models understand agent behavior:** Minimal prompts suffice; frontier LLMs learned agent patterns during training.

Zechner concludes that while benchmarks prove minimal approaches work, his actual validation comes from "day-to-day work, where pi has been performing admirably" across hundreds of exchanges within single sessions.
