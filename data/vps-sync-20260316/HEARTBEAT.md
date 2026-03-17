# HEARTBEAT.md — Heartbeat Configuration

enabled: true
interval: 30m
time_window: 08:00-22:00 CET

## Checks (deterministiske, 0 tokens)

Aktive checks markeres med [x], deaktiverede med [ ].

- [ ] trello: Stale cards, deadlines (DROPPET 4/3-2026)
- [x] gmail: Nye ulæste mails i inbox
- [x] calendar: Google Calendar events inden for 2 timer
- [x] google_tasks: Overdue items i Google Tasks
- [x] voice_pipeline: Ubehandlede voice memos i data/inbox/
- [x] prompt_miner: Daglig prompt-mining og analyse (kill: 14 dage ubrugt)

## Kill-switch

Opret `/tmp/heartbeat_kill` for at stoppe heartbeat helt.
Slet filen for at genaktivere.

## Notes

- Trello deaktiveret: Kris droppede Trello 4/3-2026
- Kører via cron: `*/30 8-21 * * *`
- Timeout: 120s via cron_guard.sh
- Output: Telegram notifikation (kun ved nye alerts)
- prompt_miner: dagligt kl 06:30, timeout 300s, kill condition 14 dage
- Sidst opdateret: 2026-03-16
