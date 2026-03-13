# Skill: new-project

Bootstrapper et nyt projekt med standard-skabelon og feedback-loop.

## Trigger

`/new-project <navn> [sti]` — default sti: `~/dev/projects/`

## Hvad den gør

1. Tjek at mappen ikke eksisterer
2. Opret projektmappen
3. Generér filer fra template/:
   - `.editorconfig` — kopiér uændret
   - `.gitattributes` — kopiér uændret
   - `.gitignore` — kopiér uændret
   - `<navn>.code-workspace` — kopiér fra `project.code-workspace`, omdøb
   - `CLAUDE.md` — udfyld projektnavn + kort beskrivelse fra prompten
   - `CONTEXT.md` — udfyld projektnavn, dato, "Projekt oprettet"
4. `git init` + `git add -A` + initial commit
5. Bekræft: "Projektet er klar i [sti]"

## Feedback-loop (indbygget i skabelonen)

Hvert projekt har en sektion i CONTEXT.md under skabelon-feedback:

```markdown
## Skabelon-feedback
Ved PDCA-evaluering, besvar:
- Hvilke template-filer blev brugt som de var?
- Hvilke blev ændret inden for de første 2 sessioner?
- Hvilke blev aldrig åbnet?
- Forslag til ændringer i template/?
```

Denne feedback bruges til at justere template/ og denne skill over tid. Mønstret:
- 1 projekt ændrer noget → notér det
- 2+ projekter ændrer det samme → opdatér skabelonen
- En fil aldrig åbnet i 3+ projekter → overvej at fjerne den

## Parametre

| Param | Påkrævet | Default | Beskrivelse |
|---|---|---|---|
| navn | ja | — | Projektets mappenavn (kebab-case) |
| sti | nej | ~/dev/projects/ | Hvor projektet oprettes |
| beskrivelse | nej | — | Kort beskrivelse til CLAUDE.md (kan promptes) |

## Begrænsninger

- Genererer ikke sprogspecifikke filer (package.json, requirements.txt) — det er projektspecifikt
- Opretter ikke GitHub repo — det er et separat step
