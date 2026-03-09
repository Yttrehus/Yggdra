# Basic Setup — Plan v2

**Mål:** Professionelt udviklermiljø på Windows 11 med WSL, VS Code, Git og god struktur.
**Tilgang:** Yttre gør det selv — Claude guider. Steps kort først → ét ad gangen.
**Metode:** Byg → Evaluér → Notér → Parkér idéer (Popper-loop per modul).

---

## Afsluttede moduler

### M1: Git ✅
### M2: VS Code ✅
### M3: Terminal/Shell ✅

Detaljer i PLAN.v1.md.

---

## M4: Projekt-struktur — NÆSTE

**Formål:** Organisér ~/dev/ så projekter har konsistent struktur og config-filer er versioneret.

1. [ ] Research: hvad gør professionelle? Mappestruktur, konventioner
2. [ ] ~/dev/ layout og konventioner
3. [ ] Standard per-projekt skabelon (CLAUDE.md, PLAN.md, NOW.md, .gitignore)
4. [ ] Dotfiles-repo — versionér .zshrc, .gitconfig, starship.toml i git
5. [ ] Workspace-fil skabelon for VS Code

**Done-kriterie:** Nyt projekt kan startes med `cp -r template/ ~/dev/nyt-projekt` og have al infrastruktur klar.

---

## M5: PC-setup (Windows)

**Formål:** Windows konfigureret som en professionels arbejdsstation. Fuldt professionelt.

1. [ ] Taskbar og startmenu — hvad skal være der, hvad skal væk
2. [ ] Software-audit — installeret, mangler, skal fjernes
3. [ ] Filsystem — C:\Users\Krist organiseret med klar mappestruktur
4. [ ] Windows settings — privacy, startup-apps, notifications
5. [ ] Poppler PATH-verifikation (installeret, mangler restart)
6. [ ] JetBrains Mono font
7. [ ] Mermaid Preview extension i VS Code

**Done-kriterie:** Skrivebord, taskbar og filsystem organiseret. Alle tools installeret. Reference-fil.

---

## M6: Terminal-automatisering

**Formål:** VS Code åbner med de terminaler du bruger dagligt.

1. [ ] Definér terminaler per workspace (WSL, SSH VPS, claude)
2. [ ] .vscode/tasks.json med runOn: folderOpen
3. [ ] Test og tilpas

**Done-kriterie:** Åbn workspace → terminaler klar.

---

## M7: Context engineering

**Formål:** Systematisér hvordan Claude Code bruges effektivt. Samler indsigter fra alle moduler.

1. [ ] CLAUDE.md best practices (under 200 linjer, progressive disclosure)
2. [ ] Compaction-strategi (hvornår, hvordan, hooks)
3. [ ] Skills-arkitektur (hvad er et skill, hvornår laves et nyt)
4. [ ] Session-management (NOW.md, plan-filer, hooks)
5. [ ] Subagent-strategi

**Done-kriterie:** CLAUDE.md template + context engineering reference-fil. Compaction-hook kører automatisk.

---

## M8: Skabeloner til nye projekter

**Formål:** Nye projekter starter med det fundament vi har bygget. Syntese af alt.

1. [ ] Projekt-skabelon (CLAUDE.md, PLAN.md, NOW.md, .gitignore, workspace-fil)
2. [ ] Checkliste for nyt projekt
3. [ ] Reference-samling
4. [ ] Scope-definition template (hvad er projektet, hvad er det IKKE)

**Done-kriterie:** Nyt projekt på under 5 minutter med al infrastruktur klar.

---

## Popper-loop (per modul)

1. **Byg** — gennemfør steps
2. **Evaluér** — opfyldte vi done-kriteriet? Hvad overraskede?
3. **Notér** — kort retrospektiv med timestamp
4. **Parkér idéer** — nye idéer i Idé-parkering, ikke i planen

---

## Idé-parkering

- Research/vidensbank som separat projekt ("personligt forskningsinstitut")
- Visualisering/infographics som separat projekt
- Notion-spejling af VS Code-struktur
- Voice-integration
- Adobe Acrobat Pro (afvent behov)

---

## Automatiseringer

Dokumenteret i references/automation.md. Opdateres ved hver ændring.

---

## Scope-grænse

Basic Setup er opsætning af professionelt udviklermiljø. Alt der vokser ud over dette (research, visualisering, TI-appen) bliver separate projekter med egen CLAUDE.md, PLAN.md, og repo.

---

## Rækkefølge

M4 → M5 → M6 → M7 → M8

M7 samler løbende indsigter undervejs men har sit eget dedikerede modul til sidst.
