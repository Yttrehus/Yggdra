"""
Centraliseret credentials-modul.
Alle scripts importerer herfra i stedet for at parse CREDENTIALS.md selv.

Usage:
    from credentials import OPENAI_KEY, GROQ_KEY, GEMINI_KEY, GROQ_MODEL
    from credentials import groq_call  # rate-limited Groq wrapper
"""
import re
import os
import time
import json
import threading

CREDENTIALS_FILE = os.environ.get(
    "YGGDRA_CREDENTIALS",
    "/root/Yggdra/data/CREDENTIALS.md"
)

def _parse_credentials():
    with open(CREDENTIALS_FILE) as f:
        text = f.read()

    def extract(pattern):
        m = re.search(pattern, text)
        return m.group(1) if m else ""

    return {
        "openai": extract(r'OpenAI[^`]*`([^`]+)`'),
        "groq": extract(r'Groq[^`]*`([^`]+)`'),
        "gemini": extract(r'Gemini[^`]*`([^`]+)`'),
        "anthropic": extract(r'Anthropic[^`]*`([^`]+)`'),
        "elevenlabs": extract(r'ElevenLabs[^`]*`([^`]+)`'),
        "hostinger": extract(r'Hostinger[^`]*`([^`]+)`'),
    }

_creds = _parse_credentials()

OPENAI_KEY = _creds["openai"]
GROQ_KEY = _creds["groq"]
GEMINI_KEY = _creds["gemini"]
ANTHROPIC_KEY = _creds["anthropic"]
ELEVENLABS_KEY = _creds["elevenlabs"]
HOSTINGER_KEY = _creds["hostinger"]

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ─── Groq Rate Limiter ───────────────────────────────────
# Groq free tier: 30 req/min, 14.400 req/dag
# Harness: max 25 req/min (buffer), max 10.000 req/dag (buffer)

_GROQ_STATE_FILE = "/tmp/groq_rate_state.json"
_GROQ_MAX_PER_MIN = 25
_GROQ_MAX_PER_DAY = 10000
_groq_lock = threading.Lock()


def _load_groq_state():
    try:
        with open(_GROQ_STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"calls": [], "daily_count": 0, "daily_date": ""}


def _save_groq_state(state):
    try:
        with open(_GROQ_STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception:
        pass


def groq_call(messages, model=None, max_tokens=1024, temperature=0.3):
    """Rate-limited Groq API call. Returns response text or raises exception.

    Usage:
        from credentials import groq_call
        result = groq_call([{"role": "user", "content": "Hej"}])
    """
    import requests as _requests

    with _groq_lock:
        state = _load_groq_state()
        now = time.time()
        today = time.strftime("%Y-%m-%d")

        # Reset daglig tæller ved ny dag
        if state.get("daily_date") != today:
            state["daily_count"] = 0
            state["daily_date"] = today

        # Daglig grænse
        if state["daily_count"] >= _GROQ_MAX_PER_DAY:
            raise RuntimeError(f"Groq daglig grænse nået ({_GROQ_MAX_PER_DAY} calls). Prøv igen i morgen.")

        # Rens gamle timestamps (ældre end 60s)
        state["calls"] = [t for t in state["calls"] if now - t < 60]

        # Per-minut grænse — vent hvis nødvendigt
        if len(state["calls"]) >= _GROQ_MAX_PER_MIN:
            wait = 60 - (now - state["calls"][0])
            if wait > 0:
                time.sleep(wait)
                now = time.time()
                state["calls"] = [t for t in state["calls"] if now - t < 60]

        # Registrér kald
        state["calls"].append(now)
        state["daily_count"] += 1
        _save_groq_state(state)

    resp = _requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        json={
            "model": model or GROQ_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        timeout=30,
    )

    if resp.status_code == 429:
        # Rate limited — vent og prøv én gang mere
        retry_after = int(resp.headers.get("Retry-After", "10"))
        time.sleep(min(retry_after, 30))
        resp = _requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": model or GROQ_MODEL,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=30,
        )

    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
