# Skill: chatlog-search

Find specifik kontekst fra tidligere sessioner. Hvad blev sagt, hvornår, og hvorfor.

## Trigger

Når Yttre eller Claude har brug for at finde en beslutning, diskussion eller kontekst fra en tidligere session. Eksempler:
- "Hvorfor besluttede vi X?"
- "Hvad sagde vi om Y?"
- "Hvornår blev Z implementeret og hvad var tankerne?"
- "Find den diskussion vi havde om..."

## Hvad den gør

### 1. Søg i chatlogs/
```bash
grep -n -i "<søgeord>" "C:/Users/Krist/dev/projects/Basic Setup/chatlogs/chatlog-"*.md
```
Brug flere søgeord hvis første søgning er for bred. Kombiner med kontekst (-B/-C flag) for at se omgivende beskeder.

### 2. Find og præsentér
- Vis dato, tidspunkt, og hvem der sagde det (YTTRE/CLAUDE)
- Vis den relevante passage — ikke hele chatloggen
- Hvis beslutningen strækker sig over flere beskeder, sammenfat diskussionen

### 3. Tvungen rapportering
**OBLIGATORISK efter hver brug.** Append til `.claude/implementationlogs/chatlog-search.md`:

| Dato | Forespørgsel | Fundet? | Kilde | Kommentar |
|------|-------------|---------|-------|-----------|

- **Forespørgsel:** Hvad blev søgt efter (kort)
- **Fundet?:** Ja/Nej/Delvist
- **Kilde:** Fil + linje eller T-nummer (f.eks. chatlog-2026-03-10.md T142)
- **Kommentar:** Var resultatet brugbart? Manglede kontekst? Tog det for lang tid?

### 4. Hvis ikke fundet i chatlogs
Søg derefter i:
1. PROGRESS.md (narrativ historik)
2. references/ (research-noter)
3. git log (commit-beskeder)

Rapportér stadig i journalen — "ikke fundet i chatlog, fundet i PROGRESS.md" er vigtig feedback om chatloggens værdi.

## Regler

- Søg ALTID chatlog først, derefter andre kilder
- Vis kun det relevante — aldrig hele filer
- Rapportering er IKKE valgfri — den er hele pointen med dette skill
- Hvis søgningen tager mere end 3 forsøg, notér det i journalen

## Evaluering

Efter 5 brug: Er chatloggen faktisk nyttig som kilde? Eller er PROGRESS.md tilstrækkeligt? Svar bruges til at vurdere om chatlog-dump bør fortsætte i /checkpoint.
