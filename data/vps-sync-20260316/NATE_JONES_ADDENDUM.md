# Addendum: Hvad Nate Jones-analysen ændrer ved session 25's output

Nate Jones' video + substack + Alexeys primærkilde + 30-video-analyse tilføjer et perspektiv der skærper flere af de 9 filer.

---

## Ændringer i Del A

### HELHEDSVURDERING.md — styrket

Red team'ets pointe om "35% bruges, 65% samler støv" er **præcis** Nates convenience-fælde anvendt på knowledge work: research produceres flydende → fluency ≠ reliability → det meste bliver aldrig til handling.

**Tilføjelse:** "Muren er ikke kode — den er management skills" gælder også Yggdra internt. Yttre er ikke stoppet af manglende teknisk viden. Han er stoppet af at organisere og bruge det der allerede er bygget. Det er et management-problem, ikke et building-problem.

### HANDLINGSPLAN.md — én ny handling

**Ny prioritet 1.5:** Implementér destruktiv-kommando-guard (PreToolUse:Bash hook). VPS kører med root, PC har SSH-adgang. Ét forkert `rm -rf` eller `docker system prune` kan koste dage. Nate-dokumentet har konkrete patterns klar. Effort: S (30 min).

### KONVERGENS.md — ny divergens

VPS har hooks der fanger destruktive operationer (via save_checkpoint, heartbeat). PC har **ingen** destruktiv-kommando-guard. Denne asymmetri er relevant: PC har SSH-adgang til VPS og kan via `ssh root@72.62.61.51 "rm -rf /data/"` slette VPS-data direkte.

---

## Ændringer i Del B

### SYNTESE.md — ét nyt princip, én skærpning

**Nyt princip (bør erstatte et af de mindre adfærdsændrende):**
**"Agent scaffold > agent regler."** CLAUDE.md er Layer 1 — nødvendigt men utilstrækkeligt. Agent scaffold (context file + workflow file + task list + planning file) er det der gør det muligt at bygge stort. Yggdra har allerede dette: CONTEXT.md + PROGRESS.md + backlog. Men det er designet til mennesker, ikke til agenter. VPS's load_checkpoint.sh er tættere på et agent scaffold.

**Skærpning af princip 3 (struktureret opgave):**
Nate bekræfter empirisk: "3.5% af prompts er strukturerede, de virker næsten altid" → hans ord: "a really, really well-defined, focused task." Small bets er ikke bare god praksis — det er matematisk nødvendigt fordi fejl kaskaderer eksponentielt.

### ARKITEKTUR.md — ingen ændring

Nate-indsigterne ændrer ikke filstrukturen. De ændrer **brugen.** Specifikt: "standing orders" vokser organisk (tilføj en linje per fejl) — det er præcis hvordan CLAUDE.md allerede fungerer i Yggdra.

### RED_TEAM.md — styrket

Red teamets stærkeste pointe ("vil det faktisk blive brugt?") får støtte fra Nate: *"You don't write a perfect rules file. You start with almost nothing. Then every time your agent does something wrong, you add a line."*

**Implikation:** SKABELONER.md skal ikke oprettes som 4 perfekte skabeloner. Den skal starte med ingenting og vokse organisk. Første skabelon tilføjes når Yttre næste gang skriver en lang prompt og tænker "det her har jeg skrevet før."

### IMPLEMENTERING.md — ændret handling 1

**Før:** "Opret SKABELONER.md med 4 mønstre"
**Efter:** "Opret SKABELONER.md med 0-1 mønstre. Tilføj en skabelon hver gang Yttre bruger et genkendt mønster. Organisk vækst, ikke top-down design."

**Ny handling 0 (før alt andet):**
"Implementér destruktiv-kommando-guard hook. 30 min. Patterns fra Nate Jones-dokumentet. Konkret: PreToolUse:Bash hook der blokerer rm -rf, docker rm, git push --force. Gør dette FØRST fordi det er den eneste handling der forhindrer datatab."

---

## Meta-observation

Nate Jones' video bekræfter noget HELHEDSVURDERING.md allerede sagde men ikke havde et navn for: **forskellen mellem builder mode og operator mode er management skills.** Yttre er en stærk builder (24 sessioner, 17 cron jobs, 6.626 knowledge points, TransportIntra i produktion). Men systemet mangler operations-skills: destruktiv-guard, review-gates, scaffold for agent-restart.

De næste 2 uger handler ikke om at bygge mere. De handler om at lære at drive det der er bygget.

*"Prompting was great. But you have to think much more broadly to handle agents this powerful."* — Nate Jones [20:16]
