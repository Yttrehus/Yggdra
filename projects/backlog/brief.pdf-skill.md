# PDF Official Toolkit Skill

**Dato:** 2026-03-10
**Klar til:** Backlog (mangler: faktura-layout fra rejseselskab, weasyprint test, Tesseract installation)

## Opsummering
- Claude Code skill til PDF-generering (fakturaer, rejseplaner), tekst-udtræk, merge/split, OCR
- Poppler allerede installeret. Mangler: weasyprint (Python), Tesseract (WSL)
- MVP: faktura-generering fra JSON → HTML → PDF. Phase 2: OCR

## Origin Story
Opstod fra idé-parkering: "PDF Official Toolkit skill (professionel PDF-generering: fakturaer, rapporter, OCR — til bogføring/rejseselskab)." To konkrete use cases: (1) rejseselskabet skal lave fakturaer/tilbud som PDF, (2) bogføring modtager kvitteringer som scan der skal OCR'es.

## Rå input
**Parallel-tasks outputs:**
- ~/parallel-tasks/output-03-pdf-skill-spec.md (253 linjer) — specifikation med capabilities, værktøj-kravmatrix, arkitektur
- ~/parallel-tasks/output-03-pdf-SKILL.md (689 linjer) — komplet SKILL.md udkast med commands, templates, eksempler

**Fra PLAN.md idé-parkering:**
> PDF Official Toolkit skill (professionel PDF-generering: fakturaer, rapporter, OCR — til bogføring/rejseselskab)
