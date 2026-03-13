# Skill: chatlog-search

Find specifik kontekst fra tidligere sessioner. Se `projects/auto-chatlog/CONTEXT.md` for fuld dokumentation.

## Trigger
Når Yttre eller Claude har brug for at finde en beslutning, diskussion eller kontekst fra en tidligere session.

## Trin
1. Læs abstracts.json — find relevant sektion via dato/emne
2. Grep i chatlog.md inden for den sektion
3. Præsentér: dato, tid, hvem, relevant passage
4. Hvis ikke fundet: PROGRESS.md → CONTEXT.md → git log
