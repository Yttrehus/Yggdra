#!/usr/bin/env python3
"""
Hook: Gem session checkpoint + append til daglig log + episodisk log + projekt-NOW.md.
Trigges af Stop, PreCompact, og Notification hooks.

Flow:
1. Læs transcript, udtræk beskeder
2. Skriv global NOW.md (seneste snapshot)
3. Append til daglig checkpoint-log
4. Ved Stop: Groq destillerer episode + identificerer projekt → skriv til projects/*/NOW.md
5. Ved PreCompact: Groq flush af kritisk info

Kill condition: Fjern hvis hook-systemet erstattes.
"""
import json
import sys
import os
import time
import re
from datetime import datetime
from pathlib import Path

# Credentials
sys.path.insert(0, "/root/Yggdra/scripts")
try:
    from credentials import GROQ_KEY, GROQ_MODEL, groq_call
except ImportError:
    GROQ_KEY = ""
    GROQ_MODEL = "llama-3.3-70b-versatile"
    groq_call = None

NOW_FILE = "/root/Yggdra/data/NOW.md"
NOW_DIR = "/root/Yggdra/data"
CHECKPOINT_DIR = "/root/Yggdra/data/checkpoints"
EPISODES_FILE = "/root/Yggdra/data/episodes.jsonl"
PROJECTS_DIR = "/root/Yggdra/projects"
THROTTLE_FILE = "/tmp/claude_checkpoint_last"
KILL_FILE = "/tmp/checkpoint_kill"
TOKEN_LOG = "/root/Yggdra/data/token_usage.jsonl"
DAILY_TOKEN_BUDGET = 100000  # Hard stop at 100K tokens/day
THROTTLE_SECONDS = 600
MAX_MESSAGES = 15
MAX_DAILY_LOG_KB = 80
NOW_SESSION_MAX_AGE = 172800

# Valid project names (must match dirs in projects/)
VALID_PROJECTS = ["transport", "assistent", "rejse", "bogfoering", "forskning", "arkitektur", "automation"]


def is_killed():
    """Check kill-switch file."""
    return os.path.exists(KILL_FILE)


def log_tokens(model, prompt_tokens, completion_tokens, purpose):
    """Append token usage to daily log."""
    try:
        entry = {
            "ts": datetime.now().isoformat(),
            "model": model,
            "prompt": prompt_tokens,
            "completion": completion_tokens,
            "total": prompt_tokens + completion_tokens,
            "purpose": purpose,
        }
        with open(TOKEN_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def check_budget():
    """Return True if daily token budget is exceeded."""
    try:
        if not os.path.exists(TOKEN_LOG):
            return False
        today = datetime.now().strftime("%Y-%m-%d")
        total = 0
        with open(TOKEN_LOG, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("ts", "").startswith(today):
                        total += entry.get("total", 0)
                except (json.JSONDecodeError, KeyError):
                    pass
        return total >= DAILY_TOKEN_BUDGET
    except Exception:
        return False


def should_throttle(hook_event):
    if hook_event in ("Stop", "PreCompact"):
        return False
    try:
        if os.path.exists(THROTTLE_FILE):
            last = os.path.getmtime(THROTTLE_FILE)
            if time.time() - last < THROTTLE_SECONDS:
                return True
    except Exception:
        pass
    return False


def touch_throttle():
    try:
        Path(THROTTLE_FILE).touch()
    except Exception:
        pass


def extract_recent_messages(transcript_path):
    if not transcript_path or not os.path.exists(transcript_path):
        return []
    messages = []
    try:
        with open(transcript_path, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message", {})
                role = msg.get("role", "")
                if role not in ("user", "assistant"):
                    continue
                content = msg.get("content", "")
                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            text_parts.append(block)
                    content = "\n".join(text_parts)
                    if not content.strip():
                        continue
                elif not isinstance(content, str):
                    content = str(content)
                content = content.strip()
                if not content:
                    continue
                if content.startswith("<system-reminder>") or content.startswith("<local-command"):
                    continue
                if len(content) > 500:
                    content = content[:500] + "..."
                messages.append({"role": role, "content": content})
    except Exception:
        pass
    return messages[-MAX_MESSAGES:]


def extract_task_list(transcript_path):
    tasks = []
    if not transcript_path or not os.path.exists(transcript_path):
        return tasks
    try:
        with open(transcript_path, "r", errors="replace") as f:
            for line in f:
                if '"TaskCreate"' in line or '"TaskUpdate"' in line:
                    try:
                        entry = json.loads(line.strip())
                        msg = entry.get("message", {})
                        content = msg.get("content", [])
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "tool_use":
                                    inp = block.get("input", {})
                                    if "subject" in inp:
                                        tasks.append(inp.get("subject", ""))
                    except (json.JSONDecodeError, KeyError):
                        pass
    except Exception:
        pass
    return tasks[-10:]


def extract_session_id(transcript_path):
    try:
        with open(transcript_path, "r", errors="replace") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    sid = entry.get("sessionId", "")
                    if sid:
                        return sid[:8]
                except (json.JSONDecodeError, KeyError):
                    pass
    except Exception:
        pass
    return "unknown"


def build_checkpoint_text(messages, tasks, hook_event, cwd, session_id):
    now = datetime.now()
    lines = [
        "# Session Checkpoint",
        "",
        f"**Gemt:** {now.strftime('%Y-%m-%d %H:%M')} (trigger: {hook_event})",
        f"**Session:** {session_id}",
        f"**CWD:** {cwd}",
        "",
    ]
    if tasks:
        lines.append("## Aktive tasks")
        for t in tasks:
            lines.append(f"- {t}")
        lines.append("")
    if messages:
        lines.append("## Seneste samtale")
        lines.append("")
        for msg in messages:
            prefix = "**Kris:**" if msg["role"] == "user" else "**Claude:**"
            lines.append(f"{prefix} {msg['content']}")
            lines.append("")
    return "\n".join(lines)


def append_daily_log(messages, hook_event, session_id):
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    log_file = os.path.join(CHECKPOINT_DIR, f"{date_str}.md")
    if os.path.exists(log_file):
        size_kb = os.path.getsize(log_file) / 1024
        if size_kb > MAX_DAILY_LOG_KB:
            return
    hash_file = os.path.join(CHECKPOINT_DIR, f".{date_str}_hashes")
    seen_hashes = set()
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            seen_hashes = set(f.read().splitlines())
    new_messages = []
    new_hashes = []
    for msg in messages:
        h = str(hash(msg["content"]))
        if h not in seen_hashes:
            new_messages.append(msg)
            new_hashes.append(h)
    if not new_messages:
        return
    with open(log_file, "a") as f:
        f.write(f"\n### {now.strftime('%H:%M')} [{session_id}] ({hook_event})\n\n")
        for msg in new_messages:
            prefix = "**Kris:**" if msg["role"] == "user" else "**Claude:**"
            f.write(f"{prefix} {msg['content']}\n\n")
    with open(hash_file, "a") as f:
        for h in new_hashes:
            f.write(h + "\n")


def _call_groq(prompt, max_tokens=200, purpose="unknown"):
    if not GROQ_KEY or not groq_call:
        return None
    if check_budget():
        return None
    try:
        result = groq_call(
            [{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        # Estimér token usage for logging (groq_call returnerer kun tekst)
        log_tokens(GROQ_MODEL, len(prompt.split()) * 2, len(result.split()) * 2, purpose)
        return result.strip()
    except Exception:
        return None


def _build_conversation_text(messages, max_chars=3000):
    conv_lines = []
    total = 0
    for msg in messages:
        prefix = "Kris" if msg["role"] == "user" else "Claude"
        line = f"{prefix}: {msg['content']}"
        conv_lines.append(line)
        total += len(line)
        if total > max_chars:
            break
    return "\n".join(conv_lines)


def identify_project(messages):
    """Ask Groq which project this session is about."""
    if not messages or len(messages) < 2:
        return None

    conversation_text = _build_conversation_text(messages, max_chars=2000)

    result = _call_groq(f"""Which project is this conversation about? Reply with EXACTLY one word from this list:
transport, assistent, rejse, bogfoering, forskning, arkitektur, automation

If it spans multiple projects or you cannot determine, reply: unknown

Projects:
- transport: TransportIntra webapp, routes, stops, drivers
- assistent: mail, calendar, Google Drive, personal assistant
- rejse: travel, booking, trips
- bogfoering: accounting, tax, invoicing
- forskning: research, YouTube monitoring, AI intelligence, book project
- arkitektur: system architecture, files, memory, hooks, CLAUDE.md, infrastructure
- automation: cron jobs, pipelines, scripts, voice pipeline

Conversation:
{conversation_text}

Project (one word):""", max_tokens=10, purpose="project_id")

    if result:
        result = result.strip().lower().rstrip(".")
        if result in VALID_PROJECTS:
            return result
    return None


def update_project_now(project, summary, session_id):
    """Append session summary to the project's NOW.md."""
    now_path = os.path.join(PROJECTS_DIR, project, "NOW.md")
    if not os.path.exists(now_path):
        return

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    entry = f"- {date_str}: {summary}"

    try:
        with open(now_path, "r") as f:
            content = f.read()

        # Update the "Opdateret" line
        content = re.sub(
            r"Opdateret: \d{4}-\d{2}-\d{2}",
            f"Opdateret: {date_str}",
            content,
        )

        # Append to Seneste section (add entry after "## Seneste" header)
        if "## Seneste" in content:
            content = content.replace(
                "## Seneste\n",
                f"## Seneste\n{entry}\n",
            )
        else:
            content += f"\n## Seneste\n{entry}\n"

        with open(now_path, "w") as f:
            f.write(content)
    except Exception:
        pass


def distill_episode(messages, session_id):
    if not messages or len(messages) < 3:
        return

    conversation_text = _build_conversation_text(messages)

    summary = _call_groq(f"""Distill this conversation into a 3-5 line episode summary.
Format: What was discussed, what was decided, what's next. Be specific and concrete.
Write in the language the conversation uses (Danish/English).

Conversation:
{conversation_text}

Episode summary (3-5 lines, no bullet points, plain text):""", purpose="episode")

    if not summary:
        return

    # Identify project
    project = identify_project(messages)

    episode = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "project": project,
        "summary": summary,
        "message_count": len(messages),
    }

    with open(EPISODES_FILE, "a") as f:
        f.write(json.dumps(episode, ensure_ascii=False) + "\n")

    # Update project NOW.md if identified
    if project:
        # Extract a one-line summary for NOW.md
        one_liner = summary.split("\n")[0]
        if len(one_liner) > 120:
            one_liner = one_liner[:120] + "..."
        update_project_now(project, one_liner, session_id)


def precompact_flush(messages, session_id):
    if not messages or len(messages) < 3:
        return

    conversation_text = _build_conversation_text(messages, max_chars=6000)

    summary = _call_groq(f"""You are a memory manager. This conversation is about to be compressed and most content will be lost.

Extract ONLY what MUST survive:
1. FACTS: concrete things learned (file paths, names, amounts, decisions made)
2. DECISIONS: what was agreed on, what approach was chosen
3. ACTION ITEMS: what still needs to be done, what was promised
4. CONTEXT: anything needed to resume this work later

Be extremely specific. Include file paths, numbers, names. Skip pleasantries and process.
Write in the language the conversation uses (Danish/English).

Conversation:
{conversation_text}

Critical information to preserve (be specific and concrete):""", max_tokens=400, purpose="precompact")

    if not summary:
        return

    project = identify_project(messages)

    episode = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "type": "precompact_flush",
        "project": project,
        "summary": summary,
        "message_count": len(messages),
    }

    with open(EPISODES_FILE, "a") as f:
        f.write(json.dumps(episode, ensure_ascii=False) + "\n")

    if project:
        one_liner = "[FLUSH] " + summary.split("\n")[0]
        if len(one_liner) > 120:
            one_liner = one_liner[:120] + "..."
        update_project_now(project, one_liner, session_id)


def _cleanup_old_session_files():
    try:
        import glob
        for f in glob.glob(os.path.join(NOW_DIR, "NOW_*.md")):
            if f == NOW_FILE:
                continue
            age = time.time() - os.path.getmtime(f)
            if age > NOW_SESSION_MAX_AGE:
                os.remove(f)
    except Exception:
        pass


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Kill-switch: silent exit
    if is_killed():
        print(json.dumps({"continue": True}))
        return

    transcript_path = hook_input.get("transcript_path", "")
    hook_event = hook_input.get("hook_event_name", "unknown")
    cwd = hook_input.get("cwd", "/root/Yggdra")

    if not transcript_path or not os.path.exists(transcript_path):
        print(json.dumps({"continue": True}))
        return

    if should_throttle(hook_event):
        print(json.dumps({"continue": True}))
        return

    messages = extract_recent_messages(transcript_path)
    tasks = extract_task_list(transcript_path)

    if not messages:
        print(json.dumps({"continue": True}))
        return

    session_id = extract_session_id(transcript_path)

    # 1. Skriv global NOW.md
    checkpoint_text = build_checkpoint_text(messages, tasks, hook_event, cwd, session_id)
    os.makedirs(os.path.dirname(NOW_FILE), exist_ok=True)
    with open(NOW_FILE, "w") as f:
        f.write(checkpoint_text)

    # Session-aware NOW
    session_now = os.path.join(NOW_DIR, f"NOW_{session_id}.md")
    with open(session_now, "w") as f:
        f.write(checkpoint_text)

    _cleanup_old_session_files()

    # 2. Daglig log
    append_daily_log(messages, hook_event, session_id)

    # 3. Episodisk log + projekt-routing ved Stop
    if hook_event == "Stop":
        distill_episode(messages, session_id)

    # 4. Pre-compaction flush
    if hook_event == "PreCompact":
        precompact_flush(messages, session_id)

    touch_throttle()
    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
