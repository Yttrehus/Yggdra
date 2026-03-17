---
title: "Effective Harnesses for Long-Running Agents"
author: Justin Young (Anthropic)
date: 2025-11-26
url: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
fetched: 2026-03-08
---

# Effective Harnesses for Long-Running Agents

## Overview

As AI agents become increasingly capable, developers demand they handle complex tasks spanning hours or days. Yet maintaining consistent progress across multiple context windows remains challenging. This article presents solutions developed for the Claude Agent SDK to enable effective long-running agent work.

## The Core Problem

Long-running agents face a fundamental constraint: they operate in discrete sessions, with each new session beginning without memory of prior work. This mirrors a software project where engineers work in shifts with no knowledge of previous shifts' progress.

The issue manifests in two primary failure patterns:

1. **Over-ambitious execution**: Agents attempt to complete entire projects at once, exhausting context mid-implementation and leaving features undocumented for the next session.

2. **Premature completion claims**: After witnessing some progress, later agent instances declare tasks finished despite incomplete functionality.

## The Two-Part Solution

### Initializer Agent

The first session employs specialized prompting to establish the foundational environment:
- `init.sh` script for running the development server
- `claude-progress.txt` file documenting agent activities
- Initial git commit showing added files

### Coding Agent

Subsequent sessions follow these directives:
- Make incremental progress on single features
- Leave structured, mergeable code updates
- Maintain clear documentation through git commits and progress files

## Environment Management Components

### Feature List

The initializer creates comprehensive JSON files listing all features as initially "failing." The example claude.ai clone contained over 200 features, each with specific steps. Coding agents modify only the `passes` field status, preventing accidental deletion or corruption that could hide bugs.

### Incremental Progress

Rather than attempting large implementations, agents work on one feature per session. This approach, combined with git commits and progress summaries, enables agents to recover from mistakes and understand what transpired previously.

### Testing Strategy

Explicit prompting to use browser automation tools (like Puppeteer MCP) dramatically improved verification. Agents successfully tested features end-to-end when instructed to interact with applications as human users would.

## Session Startup Protocol

Each coding agent session begins with:

1. Running `pwd` to confirm working directory
2. Reading git logs and progress files for context
3. Selecting the highest-priority incomplete feature from the feature list

This routine saves tokens and ensures agents immediately identify any broken states before adding new functionality.

## Common Failure Modes and Solutions

| Problem | Initializer Agent Behavior | Coding Agent Behavior |
|---------|---------------------------|----------------------|
| Premature victory declaration | Create comprehensive feature list as JSON | Read feature list; work on single features only |
| Buggy or undocumented code | Write init.sh and git repository | Start by testing existing functionality; end with commits |
| Features marked complete prematurely | Establish feature list | Thoroughly test before marking features passing |
| Time wasted discovering how to run app | Create init.sh script | Read init.sh at session start |

## Future Directions

Current research demonstrates one approach to long-running agents. Open questions remain:

- Whether specialized agents (testing, QA, cleanup) outperform single general-purpose agents
- How these principles generalize beyond web development to scientific research or financial modeling

## Key Insights

The solution draws inspiration from effective human engineering practices. By establishing clear environmental setup, maintaining detailed progress logs, and enforcing incremental work with thorough testing, agents can successfully navigate extended projects across multiple context windows.

---

**Acknowledgements**

This work involved teams across Anthropic, particularly the code RL and Claude Code teams. Contributors included David Hershey, Prithvi Rajasakeran, Jeremy Hadfield, Naia Bouscal, Michael Tingley, Jesse Mu, Jake Eaton, Marius Buleandara, Maggie Vo, Pedram Navid, Nadine Yasser, and Alex Notov.
