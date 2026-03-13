# Notion-spejling af VS Code-struktur

**Dato:** 2026-03-10
**Klar til:** Backlog (mangler: oprettelse af Notion-database, test af mobiltilgang)

## Opsummering
- Notion som "andet vindue" ind i projekter: mobiltilgang, Kanban, hurtige noter
- Disk forbliver master for kode-kontekst, Notion ejer overblik og mobil-noter
- Synk-script skeleton klar (Python), starter manuelt, automatiseres senere

## Origin Story
Opstod fra idé-parkering: "Notion-spejling af VS Code-struktur." Problemet: markdown-filer er kun tilgængelige i VS Code. Yttre vil se projektstatus fra telefon (på vej til arbejde, i pauser). Notion MCP allerede installeret — Claude kan læse/skrive direkte.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-05-notion-spejling.md (334 linjer, dato 2026-03-10). Indeholder: designprincipper, database-design ("Projekter" med 8 properties), views (Fokus, Alt, Arkiv), synkroniseringsmodel (disk→Notion + Notion-only noter), implementeringsplan (dag 1-4+), sync-to-notion.py skeleton, risici.

**Fra PLAN.md idé-parkering:**
> Notion-spejling af VS Code-struktur
