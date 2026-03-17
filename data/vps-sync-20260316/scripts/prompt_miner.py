#!/usr/bin/env python3
"""
prompt_miner.py — Mine, analysér og forbedr bruger-prompts fra Claude Code sessioner.

OpenClaw-princip: heartbeat, episodisk log, behavior-as-config.
Pipeline: regelbaseret pre-filter → AI kun på signal.

CLI:
    python prompt_miner.py scan       # Parse JSONL → struktureret prompt-index
    python prompt_miner.py analyze    # Groq-baseret kvalitetsanalyse
    python prompt_miner.py suggest    # Generer forbedringsforslag
    python prompt_miner.py daily      # scan + analyze + suggest i én kørsel
    python prompt_miner.py stats      # Vis statistik

Kill condition: Fjernes hvis ikke brugt i 14 dage.
  Check: stat data/prompt_mining/last_used.txt — hvis >14 dage gammel, slet cron + script.
"""

import json
import sys
import os
import re
import hashlib
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# ── Config ────────────────────────────────────────────────────────────
sys.path.insert(0, "/root/Yggdra/scripts")

JSONL_DIRS = [
    Path("/root/.claude/projects/-root-Ydrasil"),
    Path("/root/.claude/projects/-root-Yggdra"),
]
OUTPUT_DIR = Path("/root/Yggdra/data/prompt_mining")
PROMPTS_FILE = OUTPUT_DIR / "prompts.jsonl"
ANALYSIS_FILE = OUTPUT_DIR / "analysis.jsonl"
SUGGESTIONS_FILE = OUTPUT_DIR / "suggestions.jsonl"
DAILY_REPORT = OUTPUT_DIR / "daily_report.md"
LAST_USED = OUTPUT_DIR / "last_used.txt"
SCAN_STATE = OUTPUT_DIR / "scan_state.json"  # tracks already-scanned files
EPISODES_FILE = Path("/root/Yggdra/data/episodes.jsonl")
LOG_FILE = OUTPUT_DIR / "pipeline.log"

# Groq config — rate limiting håndteres af credentials.groq_call
GROQ_RATE_LIMIT_PAUSE = 2  # seconds between Groq calls (ekstra buffer udover harness)
MAX_GROQ_CALLS_PER_RUN = 30  # hard cap per daily run
MAX_PROMPT_LENGTH = 2000  # truncate for Groq

# ── Logging (VAR-kamera) ─────────────────────────────────────────────
def log(step: str, msg: str, data: dict = None):
    """Pipeline logger — hvert step logger input→output→beslutning."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "step": step,
        "message": msg,
    }
    if data:
        entry["data"] = data
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    if "--verbose" in sys.argv or "-v" in sys.argv:
        print(f"  [{step}] {msg}")


def touch_last_used():
    """Update kill-condition timestamp."""
    LAST_USED.write_text(datetime.now().isoformat())


# ── Prompt Classification (regelbaseret, 0 tokens) ───────────────────
def classify_prompt(text: str) -> str:
    """
    Klassificér prompt-type uden AI. Regelbaseret = gratis + hurtigt.

    Kategorier:
      - korrektion: bruger retter fejl, siger "nej", "forkert", "prøv igen"
      - meta: handler om systemet selv, arkitektur, hooks, cron
      - struktureret: lang prompt med klare instruktioner, bullet points, overskrifter
      - kommando: kort imperativ (<20 ord, ingen forklaring)
      - kør-løs: alt andet (frit formuleret opgavebeskrivelse)
    """
    lower = text.lower().strip()
    words = lower.split()
    word_count = len(words)

    # Korrektion — bruger retter noget
    correction_patterns = [
        r'\bnej\b', r'\bforkert\b', r'\bike\b.*\bdet\b', r'\bprøv igen\b',
        r'\bdet var ikke\b', r'\bsådan mente jeg ikke\b', r'\bwrong\b',
        r'\bnot what i\b', r'\btry again\b', r'\bfix\b.*\berror\b',
        r'\bdet virker ikke\b', r'\bstadig forkert\b',
    ]
    for p in correction_patterns:
        if re.search(p, lower):
            return "korrektion"

    # Meta — handler om systemet
    meta_keywords = [
        'hook', 'cron', 'checkpoint', 'episode', 'heartbeat', 'pipeline',
        'arkitektur', 'system', 'qdrant', 'docker', 'nginx', 'venv',
        'credential', 'backup', 'migration', 'infrastructure',
    ]
    meta_hits = sum(1 for k in meta_keywords if k in lower)
    if meta_hits >= 2:
        return "meta"

    # Struktureret — har overskrifter, bullet points, nummerering
    structure_signals = [
        text.count('\n- ') >= 2,
        text.count('\n* ') >= 2,
        bool(re.search(r'\n\d+\.', text)),
        bool(re.search(r'\n#{1,3} ', text)),
        bool(re.search(r'\*\*[A-ZÆØÅ]', text)),
        text.count('```') >= 2,
        word_count > 100,
    ]
    if sum(structure_signals) >= 2:
        return "struktureret"

    # Kommando — kort imperativ
    if word_count <= 20:
        return "kommando"

    return "kør-løs"


def prompt_hash(text: str) -> str:
    """Dedupliker: sha256 af normaliseret prompt."""
    normalized = re.sub(r'\s+', ' ', text.strip().lower())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


# ── SCAN: Parse JSONL → struktureret prompt-index ─────────────────────
def scan():
    """
    Parse alle session JSONL filer. Udtræk bruger-prompts.
    Inkrementel: gemmer state for hvilke filer der allerede er scannet.
    """
    log("scan", "Start scan")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load scan state (already processed files + their sizes)
    state = {}
    if SCAN_STATE.exists():
        try:
            state = json.loads(SCAN_STATE.read_text())
        except (json.JSONDecodeError, OSError):
            state = {}

    # Load existing prompt hashes to deduplicate
    seen_hashes = set()
    if PROMPTS_FILE.exists():
        with open(PROMPTS_FILE) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    seen_hashes.add(obj.get("hash", ""))
                except json.JSONDecodeError:
                    pass

    new_prompts = []
    files_scanned = 0
    files_skipped = 0

    for jsonl_dir in JSONL_DIRS:
        if not jsonl_dir.exists():
            continue
        for jsonl_file in sorted(jsonl_dir.glob("*.jsonl")):
            fpath = str(jsonl_file)
            fsize = jsonl_file.stat().st_size

            # Skip if already scanned at this size
            if state.get(fpath) == fsize:
                files_skipped += 1
                continue

            files_scanned += 1
            session_id = jsonl_file.stem

            try:
                with open(jsonl_file) as f:
                    for line in f:
                        try:
                            obj = json.loads(line.strip())
                        except json.JSONDecodeError:
                            continue

                        # Only user messages
                        if obj.get("type") != "user":
                            continue
                        msg = obj.get("message", {})
                        if not isinstance(msg, dict) or msg.get("role") != "user":
                            continue

                        content = msg.get("content", "")
                        if not isinstance(content, str):
                            # Kan være list (multimodal) — udtræk tekst
                            if isinstance(content, list):
                                content = " ".join(
                                    p.get("text", "") for p in content
                                    if isinstance(p, dict) and "text" in p
                                )
                            else:
                                continue

                        # Skip system/command messages
                        if content.startswith(("<local-command", "<command-name", "<command-message")):
                            continue
                        # Skip very short (< 10 chars) or empty
                        if len(content.strip()) < 10:
                            continue

                        h = prompt_hash(content)
                        if h in seen_hashes:
                            continue
                        seen_hashes.add(h)

                        prompt_entry = {
                            "hash": h,
                            "session_id": session_id,
                            "timestamp": obj.get("timestamp", ""),
                            "category": classify_prompt(content),
                            "text": content,
                            "word_count": len(content.split()),
                            "char_count": len(content),
                        }
                        new_prompts.append(prompt_entry)

            except (OSError, UnicodeDecodeError) as e:
                log("scan", f"Error reading {fpath}: {e}")
                continue

            # Update state
            state[fpath] = fsize

    # Append new prompts
    if new_prompts:
        with open(PROMPTS_FILE, "a") as f:
            for p in new_prompts:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")

    # Save scan state
    SCAN_STATE.write_text(json.dumps(state))

    summary = {
        "files_scanned": files_scanned,
        "files_skipped": files_skipped,
        "new_prompts": len(new_prompts),
        "total_hashes": len(seen_hashes),
        "categories": dict(Counter(p["category"] for p in new_prompts)),
    }
    log("scan", f"Scan complete: {len(new_prompts)} new prompts from {files_scanned} files", summary)
    print(f"Scan: {len(new_prompts)} nye prompts fra {files_scanned} filer ({files_skipped} uændrede)")
    for cat, count in sorted(summary["categories"].items()):
        print(f"  {cat}: {count}")

    return new_prompts


# ── ANALYZE: Groq-baseret kvalitetsanalyse ────────────────────────────
def _groq_call(messages: list, max_tokens: int = 500) -> str:
    """Call Groq API via rate-limited harness. Returns response text or empty string."""
    try:
        from credentials import groq_call
        return groq_call(messages, max_tokens=max_tokens, temperature=0.3)
    except ImportError:
        log("analyze", "groq_call not available")
        return ""
    except Exception as e:
        log("analyze", f"Groq error: {e}")
        return ""


def _load_episodes_by_session() -> dict:
    """Load episodes indexed by session_id for cross-referencing."""
    episodes = {}
    if not EPISODES_FILE.exists():
        return episodes
    with open(EPISODES_FILE) as f:
        for line in f:
            try:
                obj = json.loads(line)
                sid = obj.get("session_id", "")
                if sid:
                    episodes.setdefault(sid, []).append(obj)
            except json.JSONDecodeError:
                pass
    return episodes


def analyze():
    """
    Analysér prompt-kvalitet via Groq.
    Kører kun på prompts der ikke allerede er analyseret.
    Pipeline: regelbaseret pre-filter → AI kun på signal.
    """
    log("analyze", "Start analyze")

    if not PROMPTS_FILE.exists():
        print("Ingen prompts at analysere. Kør 'scan' først.")
        return []

    # Load already analyzed hashes
    analyzed_hashes = set()
    if ANALYSIS_FILE.exists():
        with open(ANALYSIS_FILE) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    analyzed_hashes.add(obj.get("hash", ""))
                except json.JSONDecodeError:
                    pass

    # Load prompts
    prompts = []
    with open(PROMPTS_FILE) as f:
        for line in f:
            try:
                obj = json.loads(line)
                if obj["hash"] not in analyzed_hashes:
                    prompts.append(obj)
            except (json.JSONDecodeError, KeyError):
                pass

    if not prompts:
        print("Alle prompts allerede analyseret.")
        return []

    # Load episodes for session context
    episodes = _load_episodes_by_session()

    # Pre-filter: prioritér strukturerede og kør-løs prompts.
    # Kommandoer under 15 ord → regelbaseret score, ingen Groq.
    groq_queue = []
    rule_results = []

    for p in prompts:
        if p["category"] == "kommando" and p["word_count"] <= 15:
            # Regelbaseret: korte kommandoer scorer baseret på specificitet
            specificity = min(p["word_count"] / 15.0, 1.0)
            has_context = 1 if any(k in p["text"].lower() for k in ["fil", "script", "data/", "app/", "projects/"]) else 0
            score = round(0.3 + 0.4 * specificity + 0.3 * has_context, 2)
            rule_results.append({
                "hash": p["hash"],
                "session_id": p["session_id"],
                "category": p["category"],
                "score": score,
                "method": "rule",
                "corrections_needed": 0,
                "token_cost": 0,
                "patterns": ["short_command"],
                "text_preview": p["text"][:100],
            })
        else:
            groq_queue.append(p)

    # Cap Groq calls
    groq_queue = groq_queue[:MAX_GROQ_CALLS_PER_RUN]
    groq_results = []
    groq_calls = 0

    for p in groq_queue:
        # Build context from episodes
        session_episodes = episodes.get(p["session_id"], [])
        episode_context = ""
        if session_episodes:
            ep = session_episodes[0]
            episode_context = f"\nSession-outcome: {ep.get('summary', 'Ukendt')}"

        prompt_text = p["text"][:MAX_PROMPT_LENGTH]

        system_msg = """Du er en prompt-kvalitetsanalytiker. Analysér bruger-prompten og returnér JSON.
Returnér KUN valid JSON, ingen anden tekst.
Format:
{
  "score": 0.0-1.0,
  "corrections_likely": 0-5,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "patterns": ["pattern_name"],
  "improvement": "Kort forslag til forbedring"
}

Scoring:
- 0.9-1.0: Klar, specifik, giver kontekst, definerer output-format
- 0.7-0.8: God intention men mangler detaljer
- 0.5-0.6: Vag, kræver opfølgning
- 0.0-0.4: Uklar, modsætningsfuld, eller for kort til at være nyttig

Patterns at genkende:
- "clear_output_spec": definerer eksplicit hvad output skal være
- "provides_context": giver baggrund/kontekst
- "iterative_refinement": bygger på tidligere svar
- "vague_request": for uspecifik
- "missing_constraints": mangler begrænsninger
- "typo_heavy": mange tastefejl (tyder på mobil-input)
- "well_structured": har overskrifter, bullet points, klar struktur"""

        user_msg = f"Prompt-kategori: {p['category']}\nPrompt:\n{prompt_text}{episode_context}"

        response = _groq_call([
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ])
        groq_calls += 1

        if response:
            try:
                # Extract JSON from response (handle markdown code blocks)
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    analysis = json.loads(response)

                groq_results.append({
                    "hash": p["hash"],
                    "session_id": p["session_id"],
                    "category": p["category"],
                    "score": round(float(analysis.get("score", 0.5)), 2),
                    "method": "groq",
                    "corrections_needed": int(analysis.get("corrections_likely", 0)),
                    "token_cost": len(prompt_text.split()) + 200,  # estimate
                    "patterns": analysis.get("patterns", []),
                    "strengths": analysis.get("strengths", []),
                    "weaknesses": analysis.get("weaknesses", []),
                    "improvement": analysis.get("improvement", ""),
                    "text_preview": p["text"][:100],
                })
            except (json.JSONDecodeError, ValueError) as e:
                log("analyze", f"Failed to parse Groq response for {p['hash']}: {e}")
                groq_results.append({
                    "hash": p["hash"],
                    "session_id": p["session_id"],
                    "category": p["category"],
                    "score": 0.5,
                    "method": "groq_parse_error",
                    "corrections_needed": 0,
                    "token_cost": 0,
                    "patterns": [],
                    "text_preview": p["text"][:100],
                })

        # Rate limit
        if groq_calls < len(groq_queue):
            time.sleep(GROQ_RATE_LIMIT_PAUSE)

    # Write results
    all_results = rule_results + groq_results
    if all_results:
        with open(ANALYSIS_FILE, "a") as f:
            for r in all_results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary = {
        "rule_based": len(rule_results),
        "groq_analyzed": len(groq_results),
        "groq_calls": groq_calls,
        "avg_score": round(
            sum(r["score"] for r in all_results) / max(len(all_results), 1), 2
        ),
    }
    log("analyze", f"Analysis complete", summary)
    print(f"Analyse: {len(rule_results)} regelbaseret, {len(groq_results)} via Groq")
    print(f"  Gennemsnitlig score: {summary['avg_score']}")

    return all_results


# ── SUGGEST: Generer prompt-forbedringer ──────────────────────────────
def suggest():
    """
    Baseret på analyse-mønstre: generer konkrete forbedringsforslag.
    Finder de mest effektive og mindst effektive prompts og udtrækker mønstre.
    """
    log("suggest", "Start suggest")

    if not ANALYSIS_FILE.exists():
        print("Ingen analyser fundet. Kør 'analyze' først.")
        return

    # Load all analyses
    analyses = []
    with open(ANALYSIS_FILE) as f:
        for line in f:
            try:
                analyses.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    if len(analyses) < 5:
        print(f"Kun {len(analyses)} analyser — venter på flere data (minimum 5).")
        return

    # Already suggested hashes
    suggested_hashes = set()
    if SUGGESTIONS_FILE.exists():
        with open(SUGGESTIONS_FILE) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    suggested_hashes.add(obj.get("hash", ""))
                except json.JSONDecodeError:
                    pass

    # Find patterns
    all_patterns = Counter()
    high_score_patterns = Counter()  # score >= 0.8
    low_score_patterns = Counter()   # score <= 0.5

    for a in analyses:
        for p in a.get("patterns", []):
            all_patterns[p] += 1
            if a["score"] >= 0.8:
                high_score_patterns[p] += 1
            elif a["score"] <= 0.5:
                low_score_patterns[p] += 1

    # Category stats
    cat_scores = {}
    for a in analyses:
        cat = a.get("category", "ukendt")
        cat_scores.setdefault(cat, []).append(a["score"])

    cat_avg = {
        cat: round(sum(scores) / len(scores), 2)
        for cat, scores in cat_scores.items()
    }

    # Generate suggestions for low-scoring prompts that haven't been suggested
    low_scoring = [
        a for a in analyses
        if a["score"] <= 0.6
        and a["hash"] not in suggested_hashes
        and a.get("method") == "groq"
    ]

    suggestions = []

    # Pattern-based suggestions (no Groq needed)
    for a in low_scoring[:10]:
        improvement = a.get("improvement", "")
        weaknesses = a.get("weaknesses", [])

        if not improvement and not weaknesses:
            continue

        suggestion = {
            "hash": a["hash"],
            "timestamp": datetime.now().isoformat(),
            "original_preview": a.get("text_preview", ""),
            "score": a["score"],
            "category": a.get("category", ""),
            "weaknesses": weaknesses,
            "suggestion": improvement,
            "actionable": True,
        }
        suggestions.append(suggestion)

    # Write suggestions
    if suggestions:
        with open(SUGGESTIONS_FILE, "a") as f:
            for s in suggestions:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # Generate daily report
    report_lines = [
        f"# Prompt Mining Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Oversigt",
        f"- Totale prompts analyseret: {len(analyses)}",
        f"- Gennemsnitlig score: {round(sum(a['score'] for a in analyses) / len(analyses), 2)}",
        f"- Nye forslag: {len(suggestions)}",
        "",
        "## Score per kategori",
    ]
    for cat, avg in sorted(cat_avg.items(), key=lambda x: x[1]):
        count = len(cat_scores[cat])
        report_lines.append(f"- **{cat}**: {avg} (n={count})")

    report_lines.extend(["", "## Top mønstre (succesfulde prompts)"])
    for pattern, count in high_score_patterns.most_common(5):
        report_lines.append(f"- `{pattern}`: {count} gange")

    report_lines.extend(["", "## Problemmønstre (svage prompts)"])
    for pattern, count in low_score_patterns.most_common(5):
        report_lines.append(f"- `{pattern}`: {count} gange")

    if suggestions:
        report_lines.extend(["", "## Forbedringsforslag"])
        for s in suggestions[:5]:
            report_lines.append(f"")
            report_lines.append(f"### Score {s['score']} — {s['category']}")
            report_lines.append(f"> {s['original_preview']}...")
            if s["weaknesses"]:
                report_lines.append(f"- Svagheder: {', '.join(s['weaknesses'])}")
            report_lines.append(f"- **Forslag:** {s['suggestion']}")

    report_lines.extend([
        "",
        "---",
        f"*Genereret af prompt_miner.py — kill condition: slet hvis ubrugt 14 dage*",
    ])

    DAILY_REPORT.write_text("\n".join(report_lines))

    log("suggest", f"Generated {len(suggestions)} suggestions", {
        "cat_avg": cat_avg,
        "top_patterns": dict(high_score_patterns.most_common(5)),
    })

    print(f"Forslag: {len(suggestions)} nye forbedringsforslag")
    print(f"Rapport: {DAILY_REPORT}")
    for cat, avg in sorted(cat_avg.items(), key=lambda x: x[1]):
        print(f"  {cat}: {avg}")


# ── DAILY: Alt i én kørsel ────────────────────────────────────────────
def daily():
    """Cron-egnet: scan + analyze + suggest i én kørsel."""
    log("daily", "=== Daily run start ===")
    t0 = time.time()

    scan()
    analyze()
    suggest()

    elapsed = round(time.time() - t0, 1)
    log("daily", f"=== Daily run complete in {elapsed}s ===")
    print(f"\nDaily komplet på {elapsed}s")
    touch_last_used()


# ── STATS: Vis statistik ─────────────────────────────────────────────
def stats():
    """Vis statistik over indsamlede prompts og analyser."""
    print("=== Prompt Mining Stats ===\n")

    if PROMPTS_FILE.exists():
        cats = Counter()
        total = 0
        with open(PROMPTS_FILE) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    cats[obj.get("category", "?")] += 1
                    total += 1
                except json.JSONDecodeError:
                    pass
        print(f"Prompts indekseret: {total}")
        for cat, count in cats.most_common():
            print(f"  {cat}: {count} ({round(100*count/total)}%)")
    else:
        print("Ingen prompts scannet endnu.")

    print()

    if ANALYSIS_FILE.exists():
        scores = []
        methods = Counter()
        with open(ANALYSIS_FILE) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    scores.append(obj.get("score", 0))
                    methods[obj.get("method", "?")] += 1
                except json.JSONDecodeError:
                    pass
        if scores:
            print(f"Analyser: {len(scores)}")
            print(f"  Gennemsnit: {round(sum(scores)/len(scores), 2)}")
            print(f"  Min: {min(scores)}, Max: {max(scores)}")
            print(f"  Metoder: {dict(methods)}")
    else:
        print("Ingen analyser endnu.")

    print()

    if SUGGESTIONS_FILE.exists():
        count = sum(1 for _ in open(SUGGESTIONS_FILE))
        print(f"Forbedringsforslag: {count}")
    else:
        print("Ingen forslag endnu.")

    # Kill condition check
    if LAST_USED.exists():
        last = datetime.fromisoformat(LAST_USED.read_text().strip())
        age = (datetime.now() - last).days
        print(f"\nSidst brugt: {last.strftime('%Y-%m-%d')} ({age} dage siden)")
        if age > 14:
            print("  ⚠ KILL CONDITION: Ikke brugt i >14 dage. Overvej at fjerne cron job.")


# ── KILL CHECK: kan kaldes af heartbeat ───────────────────────────────
def check_kill_condition() -> bool:
    """Returnér True hvis kill condition er opfyldt (>14 dage ubrugt)."""
    if not LAST_USED.exists():
        return False  # Aldrig brugt = for nyt til at slå ihjel
    last = datetime.fromisoformat(LAST_USED.read_text().strip())
    return (datetime.now() - last).days > 14


# ── CLI ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Prompt Mining — mine, analysér og forbedr bruger-prompts"
    )
    parser.add_argument(
        "command",
        choices=["scan", "analyze", "suggest", "daily", "stats"],
        help="Kommando: scan/analyze/suggest/daily/stats",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose pipeline logging")

    args = parser.parse_args()
    touch_last_used()

    if args.command == "scan":
        scan()
    elif args.command == "analyze":
        analyze()
    elif args.command == "suggest":
        suggest()
    elif args.command == "daily":
        daily()
    elif args.command == "stats":
        stats()


if __name__ == "__main__":
    main()
