# Auto-chatlog — brugsjournal

Parallel test af automatiseret chatlog-system (chatlog-engine.js).
Evaluering: er outputtet bedre end det manuelle checkpoint-chatlog system?

| # | Dato | Observation | Vurdering |
|---|------|-------------|-----------|
| 1 | 2026-03-11 | Første kørsel af chatlog-engine.js. Parsede 494 beskeder fra 3 sessions korrekt. Splittede på dato (live vs archive). Tidszone var UTC — fikset til dansk tid (UTC+1). Index-rækkefølge var forkert (nyeste øverst) — fikset til kronologisk. 2-timers tidsblokke tilføjet i archive. |
| 2 | 2026-03-11 | Nøgleord-extraction er frekvensbaseret og utilstrækkelig. Giver generiske ord, ikke meningsfuld kontekst. Kræver intelligens (lokal LLM) — parkeret som fremtidig iteration. |
| 3 | 2026-03-12 | live.md var 30+ min bagud da engine kun kører manuelt. Scriptet rebuilder alt fra scratch (brute-force, ikke inkrementelt). Funktionelt korrekt men ikke "live". File-watcher er designet men ikke bygget endnu. |
| 4 | 2026-03-12 | Datoskift d.11→d.12 håndteret korrekt ved manuel kørsel. D.11's samtale arkiveret, live.md nulstillet til d.12. Engine parser nu 1098 beskeder fra 6 sessions. |
| 5 | 2026-03-12 | Manglende features diskuteret: navigationslinks mellem tidsblokke (billig template-logik), referater (kræver LLM), retskrivning af bruger-input (kræver LLM), session-ID markering ved parallelle sessions. Alt parkeret — format først, automatisering bagefter. |
