# Session State Management

## Hvorfor dette skill eksisterer

LLM'er har ikke hukommelse mellem sessions. Chatten er ephemeral — den kan crashe, context window kan fyldes, sessionen kan lukkes. Hver gang det sker, starter en ny Claude fra nul.

Dette skill opstod efter en session crashede og al kontekst gik tabt. Yttre havde brugt timer på at forklare sin baggrund, sine beslutninger, sin vision — og den næste Claude vidste ingenting. Det skete fordi den forrige Claude kun holdt state i chatten, ikke på disk.

Løsningen: NOW.md og PLAN.md som levende filer i hvert projekt. Chatten er arbejdshukommelse. Filerne er langtidshukommelse.

## Regler

- NOW.md opdateres automatisk efter vigtige beslutninger, afsluttede steps, og ved session-slut
- PLAN.md opdateres når steps afsluttes eller planen ændres
- Claude committer og pusher selv via Windows git efter opdateringer
- Commit-besked skal være meningsfuld (ikke "update files")

## Commit flow

```bash
cd "C:/Users/Krist/[projekt]" && git add -A && git commit -m "besked" && git push
```

## NOW.md format

```markdown
# NOW — Hvor vi er

**Sidst opdateret:** [dato]
**Status:** [kort status]

## Næste step
[hvad der skal ske nu]

## Seneste session
[hvad der skete]

## Vigtig kontekst
[hvad en ny Claude skal vide]

## Åbne tråde
[ting der venter]
```

## Hvornår

- Efter hvert afsluttet step/milestone
- Når vigtige beslutninger tages
- Før session slutter
- Når Yttre beder om commit
