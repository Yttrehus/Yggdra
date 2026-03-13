# Research Architecture

**Dato:** 2026-03-12
**Klar til:** Backlog — høj prioritet post-reformation
**Prioritet:** Høj — fundamentalt for alt andet

## Opsummering
- Etablér formidabel research-praksis: struktur, kvalitetssikring, multi-LLM strategi
- Al eksisterende research er pre-reformation og ligger i research/_ARC/ — kræver revision
- research/ mappen ER dette projekts hjem. research/_ARC/ er input til den nye praksis

## Origin Story
Opstod fra idé-parkering: "Research/vidensbank som separat projekt ('personligt forskningsinstitut')." Voksede i session 12 til en erkendelse af at research-arkitektur er lige så fundamental som Yggdras kernearchitektur. Praksisser, infrastruktur, planlægningsstrategier bygger alle på forskning — men hvor velkonstrureret er fundamentet? Kilder: Anthropic, OpenAI, Perplexity, forskningsinstitutter, eksperter, communities. VPS har 60+ research-filer der skal auditeres efter reformation.

## Rå input
**Parallel-tasks output:** ~/parallel-tasks/output-07-vidensbank-scope.md (253 linjer, dato 2026-03-10). Indeholder: problem-analyse, eksisterende assets (VPS research/, DAGBOG.md, Qdrant, lokale references/), genbrug-mønstre, arkitektur-forslag (minimum viable = distributed reference system), scope-grænse (IN/OUT), anbefaling.

**Session 12 beslutninger:**
- Research er en *praksis*, ikke bare en mappe
- Al eksisterende research er "pre-reformation" — intet har gennemgået kvalitetssikret process
- VPS research lægges i arkiv/vps efter reformation, gennemgås med ny praksis
- Multi-LLM strategi: "de rigtige LLM'er til de rigtige ting"

**Fra PLAN.md idé-parkering:**
> Research/vidensbank som separat projekt ("personligt forskningsinstitut")
