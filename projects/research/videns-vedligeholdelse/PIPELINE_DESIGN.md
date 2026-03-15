# Pipeline Design — Udvidelser

Baseret på _audit.md, DECAY_MODEL.md og SOURCE_REGISTRY.md. Fokus: lukke de kritiske gaps med minimal effort.

---

## Udvidelse 1: Blog-RSS Pipeline

**Problem:** Anthropic blog, OpenAI blog, Google DeepMind blog overvåges ikke direkte. Officielle announcements fanges kun via HN proxy — ofte med forsinkelse eller slet ikke.

**Effort:** 2-3 timer

**Ændringer i:** `scripts/ai_intelligence.py` (tilføj `fetch_rss_feeds()` funktion), `data/intelligence_sources.json` (tilføj feeds)

**Ny kode:**
```python
def fetch_rss_feeds():
    """Hent nyeste posts fra RSS feeds i sources.json."""
    items = []
    sources = json.loads(Path(SOURCES_FILE).read_text())
    feeds = sources.get("rss_feeds", [])

    for feed_cfg in feeds:
        try:
            parsed = feedparser.parse(feed_cfg["url"])
            for entry in parsed.entries[:5]:
                pub_date = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub_date = time.strftime("%Y-%m-%d", entry.published_parsed)

                # Kun posts fra sidste 7 dage
                if pub_date >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"):
                    items.append({
                        "source": f"rss/{feed_cfg['name']}",
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "date": pub_date,
                        "summary": entry.get("summary", "")[:300],
                    })
        except Exception as e:
            log(f"  RSS {feed_cfg['name']} fejl: {e}")
    return items
```

**Nye RSS-feeds at tilføje i sources.json:**
```json
{"name": "Anthropic Research", "url": "https://www.anthropic.com/research/rss", "priority": "high"},
{"name": "OpenAI Blog", "url": "https://openai.com/blog/rss/", "priority": "high"},
{"name": "Google DeepMind", "url": "https://deepmind.google/blog/rss.xml", "priority": "medium"},
{"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "priority": "medium"}
```

**Test:**
1. `python3 -c "import feedparser; f=feedparser.parse('https://simonwillison.net/atom/everything/'); print(len(f.entries), f.entries[0].title)"`
2. Kør `ai_intelligence.py --test` og verificér RSS items i output

**Integration:** Tilføj `("RSS feeds", fetch_rss_feeds)` til `collect_all_items()` i linje ~515.

**Kill condition:** Fjern feeds der producerer 0 items i 4 uger.

---

## Udvidelse 2: Pricing Diff-checker

**Problem:** API-priser ændrer sig stille. Kris kan betale for meget (eller misse billigere alternativer) uden at vide det. Ingen pipeline fanger dette.

**Effort:** 4-6 timer

**Ændringer i:** Nyt script `scripts/pricing_monitor.py`, cron entry (ugentlig søndag kl. 07:00)

**Ny kode:**
```python
PRICING_PAGES = {
    "anthropic": "https://docs.anthropic.com/en/docs/about-claude/models",
    "openai": "https://openai.com/api/pricing/",
}
SNAPSHOT_DIR = "/root/Yggdra/data/intelligence/pricing_snapshots"

def check_pricing():
    for provider, url in PRICING_PAGES.items():
        try:
            resp = requests.get(url, timeout=15, headers=UA)
            new_hash = hashlib.md5(resp.text.encode()).hexdigest()
            snapshot = Path(f"{SNAPSHOT_DIR}/{provider}_latest.hash")

            if snapshot.exists():
                old_hash = snapshot.read_text().strip()
                if old_hash != new_hash:
                    # Page ændret — gem diff og alert
                    save_snapshot(provider, resp.text)
                    send_telegram_alert(f"⚠️ {provider} pricing page ændret!")

            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(new_hash)
        except Exception as e:
            log(f"Pricing check {provider}: {e}")
```

**Test:** Kør manuelt, verificér at snapshots gemmes i `data/intelligence/pricing_snapshots/`.

**Kill condition:** Fjern hvis ingen prisændringer fanget i 3 måneder.

---

## Udvidelse 3: Decay-baseret Re-scan

**Problem:** Ældre viden re-scannes aldrig. COMPARISON.md fra llm-landskab loopet viser data der allerede kan være forældet (Elo-scores, priser). Ingen mekanisme prioriterer hvad der skal opdateres.

**Effort:** 3-4 timer

**Ændringer i:** `scripts/ai_intelligence.py` (tilføj `check_decay()` i daglig kørsel)

**Ny kode:**
```python
DECAY_CONFIG = {
    "model_releases": {"scan_interval_days": 7, "sources": ["github", "hn"]},
    "api_pricing": {"scan_interval_days": 14, "sources": ["pricing_monitor"]},
    "agent_patterns": {"scan_interval_days": 30, "sources": ["youtube", "substack"]},
    "research_papers": {"scan_interval_days": 30, "sources": ["arxiv"]},
}
DECAY_STATE = f"{OUTPUT_DIR}/decay_state.json"

def check_decay():
    """Check hvilke videns-kategorier der er forældede og bør re-scannes."""
    state = json.loads(Path(DECAY_STATE).read_text()) if Path(DECAY_STATE).exists() else {}
    overdue = []

    for category, cfg in DECAY_CONFIG.items():
        last_scan = state.get(category, "2000-01-01")
        days_since = (datetime.now() - datetime.strptime(last_scan, "%Y-%m-%d")).days
        if days_since >= cfg["scan_interval_days"]:
            overdue.append({
                "category": category,
                "days_overdue": days_since - cfg["scan_interval_days"],
                "sources": cfg["sources"]
            })

    if overdue:
        # Sortér efter mest forældet
        overdue.sort(key=lambda x: x["days_overdue"], reverse=True)
        log(f"DECAY: {len(overdue)} kategorier overdue")
        for item in overdue:
            log(f"  {item['category']}: {item['days_overdue']} dage overdue")

    return overdue
```

**Output:** Decay-status i daglig digest. Overdue items inkluderes som sektion i daily markdown.

**Test:** Kør med tom decay_state.json, verificér at alle kategorier rapporteres som overdue.

**Kill condition:** Fjern hvis decay-rapporter aldrig fører til handling (3 måneder).

---

## Udvidelse 4: Pipeline Health Monitor

**Problem:** Hvis ai_intelligence.py eller youtube_monitor.py crasher, opdager ingen det. Ingen alerting ved pipeline-fejl.

**Effort:** 2-3 timer

**Ændringer i:** `scripts/daily_sweep.py` (tilføj `check_pipeline_health()`)

**Ny kode:**
```python
PIPELINE_EXPECTATIONS = {
    "ai_intelligence": {
        "output_pattern": "data/intelligence/daily_{date}.md",
        "max_age_hours": 28,  # Kører kl 06:30, check kl 08:00
        "cron": "daglig 06:30",
    },
    "youtube_monitor": {
        "log_file": "/var/log/ydrasil/intelligence.log",
        "max_age_hours": 28,
        "cron": "daglig 07:00",
    },
}

def check_pipeline_health():
    """Verificér at alle pipelines har produceret output inden for forventet tidsramme."""
    today = datetime.now().strftime("%Y-%m-%d")

    for name, cfg in PIPELINE_EXPECTATIONS.items():
        if "output_pattern" in cfg:
            expected = cfg["output_pattern"].replace("{date}", today)
            path = Path(f"/root/Yggdra/{expected}")
            if not path.exists():
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                path_y = Path(f"/root/Yggdra/{cfg['output_pattern'].replace('{date}', yesterday)}")
                if not path_y.exists():
                    findings.append(f"ALERT: {name} har ikke produceret output i 2 dage")
                    send_telegram(f"Pipeline-fejl: {name} mangler output")
```

**Integration:** Tilføj `check_pipeline_health()` i daily_sweep.py's main flow.

**Test:** Omdøb midlertidigt en daily fil og kør sweep. Verificér alert.

**Kill condition:** Fjern når bedre monitoring er på plads (Docker healthchecks eller lignende).

---

## Udvidelse 5: Discovered Sources Cleanup

**Problem:** `discovered_sources` i intelligence_sources.json har 21 entries der mestendels er noise ("prize", "Tools/Platforms", "Ukendt kanal"). Forurener konfigurationen.

**Effort:** 1 time

**Ændringer i:** `scripts/source_discovery.py` (tilføj quality filter), `data/intelligence_sources.json` (cleanup)

**Ny kode:**
```python
NOISE_PATTERNS = [
    r"^ukendt",
    r"^ikke specificeret",
    r"^tools/platforms$",
    r"^prize$",
]

def clean_discovered(sources):
    """Fjern low-quality discovered sources."""
    cleaned = []
    for src in sources.get("discovered_sources", []):
        name = src.get("name", "").lower()
        if not any(re.match(p, name) for p in NOISE_PATTERNS):
            cleaned.append(src)
    sources["discovered_sources"] = cleaned
    return sources
```

**Øjeblikkelig handling:** Rens de 21 entries ned til ~5 meningsfulde. Tilføj quality-filter i source_discovery.py så fremtidige discoveries filtreres.

**Test:** Kør cleanup, verificér at intelligence_sources.json stadig er valid JSON med færre discovered_sources.

**Kill condition:** Fjern cleanup-kode når source_discovery.py selv genererer kvalitets-output.

---

## Prioriteret Implementerings-rækkefølge

| # | Udvidelse | Effort | Impact | Prioritet |
|---|-----------|--------|--------|-----------|
| 1 | Blog-RSS Pipeline | 2-3 timer | Lukker kritisk gap (officielle announcements) | KRITISK |
| 2 | Pipeline Health Monitor | 2-3 timer | Forhindrer tavse fejl | HØJ |
| 3 | Pricing Diff-checker | 4-6 timer | Forhindrer overforbrug | HØJ |
| 4 | Discovered Sources Cleanup | 1 time | Reducerer noise | MIDDEL |
| 5 | Decay-baseret Re-scan | 3-4 timer | Systematisk vedligeholdelse | MIDDEL |

**Total estimat:** 12-17 timer for alle 5 udvidelser.

**Note:** RSS-feed funktionen (`fetch_rss_feeds`) er allerede delvist understøttet — `rss_feeds` sektion eksisterer i sources.json med Simon Willison og AlphaSignal. Men funktionen er IKKE kaldt i `collect_all_items()`. Det er en bug eller et uafsluttet feature.
