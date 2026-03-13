# Architecture R&D (arkiveret)

## Metadata
- **Status:** Arkiveret — erstattet af CONTEXT.md-baseret struktur (session 13)
- **Oprettet:** 2026-03-11 (session 10-12)
- **Arkiveret:** 2026-03-13 (session 14)

## Hvad var det
Research & development af projekt-arkitektur for Yggdra. Undersøgte pipeline-stadier (RAW/DEV/STG/CORE → PoC/DLR/SIP/BMS), ADR-format, og mappestruktur med governance-lag.

## Hvorfor arkiveret
Alt blev droppet i session 13 (manifest v4). Pipeline-stadier, ADR-terminologi og README-baserede stage-dokumenter erstattet af:
- Flad `projects/`-struktur (ét projekt = én mappe)
- CONTEXT.md overalt (plain dansk status i stedet for stage-koder)
- Ingen governance-lag eller pipeline i mappenavne

## Indhold
- `ADR-template.md` — skabelon til Architecture Decision Records (droppet, erstattet af CONTEXT.md changelog)
- `README-BMS.md` — Built & Maintained System stage-dokument
- `README-Backlog.md` — Backlog stage-dokument
- `README-DLR.md` — Deliverable stage-dokument
- `README-PoC.md` — Proof of Concept stage-dokument
- `README-SIP.md` — Spike/Investigation stage-dokument
- `google-ai-samtale-rd-framework.md` — Google AI-samtale om maturity-stadier og pipeline-modellering (session 10, ekstern kilde)

## Beslutninger der førte hertil
- Session 10: Yttre sagde "ADR er i bund og grund blot en mini-context.md" → ét format overalt
- Session 12: Pipeline-stadier i mappenavne = overengineering → flad struktur
- Session 13: Manifest v4 implementeret, alt gammelt arkiveret
