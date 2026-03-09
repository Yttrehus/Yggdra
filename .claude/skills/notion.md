# Notion Integration

Two-way channel between Claude and Yttre. Python scripts called via bash.

## Setup
1. Yttre creates Notion workspace (Free Plan)
2. Create integration at https://www.notion.so/my-integrations
3. Save token in `data/CREDENTIALS.md` under Notion
4. Share pages with integration in Notion UI
5. Run: `notion search "test"` to verify

## Scripts
```bash
notion search "query"                # Find pages by title
notion read PAGE_ID                  # Read page content (markdown)
notion write "Title" "Content"       # Create new page
notion update PAGE_ID "Content"      # Update page content
notion list                          # List shared pages
```

## Architecture
- Simple CRUD → Python scripts call Notion API directly (no LLM needed)
- Complex content → Opus formulates → script writes to Notion
- Yttre edits in Notion → script reads → reports to Claude

## Workspace Structure
```
YGGDRA
├── SYSTEM (how the machine works)
├── PROJEKTER
│   ├── TI-App
│   ├── Revisor
│   ├── Rejsebureau
│   └── Research
└── PERSONLIGT (Yttre)
```

## API Reference
See `docs/external/notion-llms.txt` for full API index.
Detailed guides in `docs/external/notion/`.
