#!/usr/bin/env python3
"""
Heartbeat daemon: checker kilder hvert 30 min og notificerer via Telegram
hvis noget kræver opmærksomhed.

Kilder (alle swappable):
- Trello: stale cards, deadlines
- Gmail: nye vigtige mails
- Google Calendar: events inden for 2 timer
- Google Tasks: overdue items
- Telegram: (indgående håndteres af telegram_bridge)

Kører som cron hvert 30. minut, 08:00-22:00 dansk tid.
Cron entry: */30 8-21 * * * python3 /root/Yggdra/scripts/heartbeat.py

Princip: Hvis intet kræver handling → HEARTBEAT_OK (stille).
Kun notificer ved reelt nyt.
"""
import json
import os
import sys
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Config
TELEGRAM_BOT_TOKEN = "8480078786:AAH7Zo3jSs5-zTWPbBxd9rpzkiF2v3oqcRw"
TELEGRAM_CHAT_ID = "8527329039"
STATE_FILE = "/tmp/heartbeat_state.json"
LOG_FILE = "/root/Yggdra/data/heartbeat.log"
KILL_FILE = "/tmp/heartbeat_kill"
CONFIG_FILE = "/root/Yggdra/data/HEARTBEAT.md"

# Trello
TRELLO_CREDS = "/root/Yggdra/data/gmail/trello_creds.json"
TRELLO_BOARDS = "/root/Yggdra/data/gmail/trello_boards.json"

# Google APIs
sys.path.insert(0, "/root/Yggdra/scripts/integrations")


def log(msg):
    """Append to heartbeat log."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + "\n")
    except Exception:
        pass


def send_telegram(text):
    """Send notification via Telegram."""
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text[:4000]},
            timeout=10,
        )
        return resp.status_code == 200
    except Exception:
        return False


def load_state():
    """Load previous heartbeat state (for dedup)."""
    try:
        return json.loads(Path(STATE_FILE).read_text())
    except Exception:
        return {}


def save_state(state):
    """Save heartbeat state."""
    try:
        Path(STATE_FILE).write_text(json.dumps(state, default=str))
    except Exception:
        pass


# ─── SOURCES ─────────────────────────────────────────────

def check_trello():
    """Check Trello for deadlines and stale cards."""
    alerts = []
    try:
        if not os.path.exists(TRELLO_CREDS) or not os.path.exists(TRELLO_BOARDS):
            return alerts
        creds = json.loads(Path(TRELLO_CREDS).read_text())
        boards = json.loads(Path(TRELLO_BOARDS).read_text())
        key, token = creds['api_key'], creds['token']

        now = datetime.now(tz=timezone.utc)
        for board_name, board_id in boards.items():
            try:
                cards = requests.get(
                    f'https://api.trello.com/1/boards/{board_id}/cards',
                    params={'key': key, 'token': token, 'fields': 'name,due,dateLastActivity'},
                    timeout=15,
                ).json()
                if not isinstance(cards, list):
                    continue
                for card in cards:
                    # Overdue deadlines
                    due = card.get('due')
                    if due:
                        try:
                            due_dt = datetime.fromisoformat(due.replace('Z', '+00:00')).replace(tzinfo=None)
                            if due_dt < now:
                                alerts.append(f"OVERDUE [{board_name}]: {card['name']} (deadline {due[:10]})")
                            elif due_dt < now + timedelta(hours=24):
                                alerts.append(f"Deadline i dag [{board_name}]: {card['name']}")
                        except Exception:
                            pass

                    # Stale cards (no activity 7+ days)
                    last = card.get('dateLastActivity', '')
                    if last:
                        try:
                            last_dt = datetime.fromisoformat(last.replace('Z', '+00:00')).replace(tzinfo=None)
                            if (now - last_dt).days >= 7:
                                alerts.append(f"Stale [{board_name}]: {card['name']} ({(now - last_dt).days}d)")
                        except Exception:
                            pass
            except Exception:
                continue
    except Exception as e:
        log(f"Trello check fejlede: {e}")
    return alerts


def check_gmail():
    """Check for new unread emails via Google API."""
    alerts = []
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-c", """
import sys, json
sys.path.insert(0, '/root/Yggdra/scripts')
from integrations.gmail_api import read_inbox
mails = read_inbox(max_results=5, label="INBOX")
print(json.dumps(mails))
"""],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            mails = json.loads(result.stdout.strip())
            for m in mails:
                subj = m.get('subject', '(intet emne)')
                sender = m.get('from', '?')
                alerts.append(f"Mail: {subj} (fra {sender})")
    except Exception as e:
        log(f"Gmail check fejlede: {e}")
    return alerts


def check_calendar():
    """Check Google Calendar for events in next 2 hours."""
    alerts = []
    try:
        # Use subprocess to avoid relative import issues
        import subprocess
        result = subprocess.run(
            [sys.executable, "-c", """
import sys
sys.path.insert(0, '/root/Yggdra/scripts')
from integrations.calendar_api import list_events
import json
events = list_events(max_results=5, days_ahead=1)
print(json.dumps(events))
"""],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            events = json.loads(result.stdout.strip())
            now = datetime.now()
            for ev in events:
                start = ev.get('start', '')
                summary = ev.get('summary', '(ingen titel)')
                if isinstance(start, str) and 'T' in start:
                    try:
                        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).replace(tzinfo=None)
                        hours_until = (start_dt - now).total_seconds() / 3600
                        if 0 <= hours_until <= 2:
                            alerts.append(f"Kalender om {int(hours_until*60)}min: {summary}")
                    except Exception:
                        pass
    except Exception as e:
        log(f"Calendar check fejlede: {e}")
    return alerts


def check_google_tasks():
    """Check Google Tasks for overdue items."""
    alerts = []
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-c", """
import sys
sys.path.insert(0, '/root/Yggdra/scripts')
from integrations.google_tasks import api, get_default_list_id
import json
list_id = get_default_list_id()
result = api("GET", f"/lists/{list_id}/tasks", params={"showCompleted": "false", "maxResults": "20"})
print(json.dumps(result))
"""],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            from datetime import timezone
            now = datetime.now(timezone.utc).isoformat()
            for task in data.get("items", []):
                due = task.get("due", "")
                title = task.get("title", "")
                if due and due < now and title:
                    alerts.append(f"Overdue task: {title}")
    except Exception as e:
        log(f"Google Tasks check fejlede: {e}")
    return alerts


def check_voice_pipeline():
    """Check for unprocessed voice memos."""
    alerts = []
    try:
        inbox = Path("/root/Yggdra/data/inbox")
        if inbox.exists():
            mp3s = list(inbox.glob("*.mp3")) + list(inbox.glob("*.m4a"))
            unprocessed = []
            for f in mp3s:
                md_file = f.with_suffix('.md')
                if not md_file.exists():
                    unprocessed.append(f.name)
            if unprocessed:
                alerts.append(f"Voice memos ubehandlet: {len(unprocessed)} ({', '.join(unprocessed[:3])})")
    except Exception as e:
        log(f"Voice pipeline check fejlede: {e}")
    return alerts


def check_prompt_miner():
    """Check prompt_miner kill condition: fjern hvis last_used > 14 dage."""
    alerts = []
    try:
        last_used = Path("/root/Yggdra/data/prompt_mining/last_used.txt")
        if last_used.exists():
            last_date = last_used.read_text().strip()[:10]
            days_ago = (datetime.now() - datetime.strptime(last_date, "%Y-%m-%d")).days
            if days_ago > 14:
                alerts.append(f"prompt_miner KILL CONDITION: {days_ago} dage siden sidst brugt (grænse: 14)")
        else:
            alerts.append("prompt_miner: last_used.txt mangler — kør 'python scripts/prompt_miner.py stats'")
    except Exception as e:
        log(f"Prompt miner check fejlede: {e}")
    return alerts


# ─── MAIN ────────────────────────────────────────────────

def load_config():
    """Load HEARTBEAT.md config. Returns dict with enabled, checks list."""
    config = {"enabled": True, "checks": ["trello", "gmail", "calendar", "google_tasks", "voice_pipeline"]}
    try:
        if not os.path.exists(CONFIG_FILE):
            return config
        with open(CONFIG_FILE, "r") as f:
            content = f.read()
        if "enabled: false" in content.lower():
            config["enabled"] = False
        # Parse checked items (- [x] name) as active, unchecked (- [ ] name) as disabled
        active_checks = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("- [x]"):
                check_name = line[5:].strip().split(":")[0].strip().lower().replace(" ", "_")
                active_checks.append(check_name)
            elif line.startswith("- [ ]"):
                pass  # Disabled check
        if active_checks:
            config["checks"] = active_checks
    except Exception:
        pass
    return config


def main():
    log("Heartbeat start")

    # Kill-switch
    if os.path.exists(KILL_FILE):
        log("Kill-switch aktiv. Exit.")
        return

    # Load config
    config = load_config()
    if not config["enabled"]:
        log("Disabled via HEARTBEAT.md. Exit.")
        return

    active_checks = config["checks"]

    # Check dansk tid (08:00-22:00)
    try:
        from subprocess import check_output
        dk_hour = int(check_output(
            ['date', '+%H'], env={**os.environ, 'TZ': 'Europe/Copenhagen'}
        ).decode().strip())
        if dk_hour < 8 or dk_hour >= 22:
            log(f"Uden for aktive timer (kl. {dk_hour}). Skip.")
            return
    except Exception:
        pass  # Kør alligevel hvis tidscheck fejler

    state = load_state()
    last_alerts = set(state.get("last_alerts", []))

    # Collect alerts from active sources (configured in HEARTBEAT.md)
    check_map = {
        "trello": check_trello,
        "gmail": check_gmail,
        "calendar": check_calendar,
        "google_tasks": check_google_tasks,
        "voice_pipeline": check_voice_pipeline,
        "prompt_miner": check_prompt_miner,
    }
    all_alerts = []
    for name, fn in check_map.items():
        if name in active_checks:
            all_alerts.extend(fn())

    # Deduplicate: only notify about NEW alerts
    new_alerts = [a for a in all_alerts if a not in last_alerts]

    if new_alerts:
        header = f"Heartbeat {datetime.now().strftime('%H:%M')}"
        msg = f"{header}\n\n" + "\n".join(f"- {a}" for a in new_alerts)
        send_telegram(msg)
        log(f"Sendte {len(new_alerts)} nye alerts via Telegram")
    else:
        log("HEARTBEAT_OK — intet nyt")

    # Save state for dedup
    save_state({
        "last_run": datetime.now().isoformat(),
        "last_alerts": all_alerts,  # Gem ALLE (ikke kun nye) så næste kørsel kan sammenligne
        "new_count": len(new_alerts),
    })

    log("Heartbeat done")


if __name__ == "__main__":
    main()
