# Basic Setup — Forløbsplan

**Mål:** Professionelt udviklermiljø på Windows 11 med WSL, VS Code, Git og god struktur.
**Tilgang:** Yttre gør det selv — Claude guider fra sidelinjen. Steps listes kort → ét ad gangen → venter på respons.

---

## Hvem er Yttre

Ingen formel uddannelse. Intens egeninteresse i software engineering siden november 2025. Har prøvet alt: Grok med fuld adgang til Google Drive ("den kunne jo bo der"), ChatGPT, Claude chat, nu Claude Code. Hver gang samme mønster — lang kontekst-opbygning, så glemmer modellen det hele. Nu ved han om context windows, hallucination, og at state skal på disk.

Ejer anparter i vens rejseselskab (vores-rejsebureau.dk). Hjælper med kunder. Har VPS med Yggdra-system (7 projekter, Qdrant søgning, TransportIntra webapp i produktion). Alt det er bygget med Claude.

Emails: k.yttrehus@gmail.com (GitHub, subscriptions, AI, betalinger). kristoffer.yttrehus@hotmail.com (personlig — skriver til og fra). GitHub: Yttrehus.

Har mange halvfærdige projekter på VPS, PC (C:\Users\Krist), Google Drive. Arbejdede primært fra tablet og mobil indtil han købte PC. VS Code var ikke noget han kendte — men det er præcis det han drømte om.

**Vision:** Professionelt setup i VS Code + parallelt i Notion. Samme struktur begge steder, genkendeligt uanset hvor han arbejder. Notion MCP er sat op men virker "uimponerende". VS Code-strukturen sætter standarden, Notion spejler den bagefter.

**Kommunikation:** Hedder Yttre — ikke Kris, ikke Kristoffer. Vil selv gøre tingene. Gider ikke "skal jeg...?" — bare gør det. Multi-step: alle steps kort først, derefter ét ad gangen.

---

## Beslutninger taget (og rationalet)

- **Git i WSL, ikke Windows** — koden lever i WSL (~/dev/), SSH-nøglen er der, undgår CRLF-problemer. En pro bruger git der hvor koden lever.
- **Rækkefølge: Git → VS Code → Terminal → SSH → resten** — Git er fundament. VS Code bruges under hele forløbet. Terminal og SSH bygger på git-forståelsen.
- **Python før JavaScript** — Yttre har allerede Python-scripts på VPS, lettere at lære i kendt kontekst. JS kommer når vi rører webappen.
- **Dokumentation undervejs** — hvert modul efterlader en referencefil. Ikke tutorials, men Yttres egne valg og konfiguration. "Næste gang jeg starter forfra..."
- **Notion spejler VS Code** — ikke omvendt. VS Code-strukturen sætter standarden.
- **JetBrains Mono** — anbefalet kodefont med ligatures. Ikke installeret endnu — VS Code falder tilbage på Consolas.

---

## M0: Meta-opsætning ✅

- [x] Kommunikationsstil skrevet ind i CLAUDE.md
- [x] Skills kopieret fra .claude/ (infrastructure.md, notion.md)
- [x] ~/dev/ oprettet i WSL

---

## M1: Git ✅

Alle steps gennemført med Yttre i WSL terminalen.

- [x] Git 2.43.0 i WSL (han kørte først `git --version` i Windows Git Bash — fik 2.53.0 — måtte lære at skelne WSL fra Windows)
- [x] `git config --global`: name="Yttre", email=k.yttrehus@gmail.com, defaultBranch=main, editor="code --wait"
  - Han ville først bruge "Kristoffer Yttrehus" men rettede til "Yttre"
- [x] `~/.gitignore_global` oprettet — OS-filer, secrets, deps, editors, build
  - Havde problemer med heredoc (EOF manglede) — lærte hvad heredoc er
- [x] SSH-nøgle: havde allerede `id_ed25519` i WSL, men den var ikke tilføjet til GitHub. Tilføjet som "Yttre WSL"
- [x] Test-repo: `~/dev/test-repo` → github.com/Yttrehus/test-repo (bad om SSH-url, fik HTTPS-url — lærte forskellen)
- [x] Aliases: `git st`, `git co`, `git br`, `git lg` — testet med `git lg`

**Produceret:**
- [references/git.md](references/git.md) — kommando-reference (Claude skrev den, Yttre ville egentlig skrive selv men bad om hjælp)
- [setup/git-concepts.md](setup/git-concepts.md) — konceptforklaring: repo, commit, staging, branches, PR, workflows, SSH vs HTTPS

Yttre bad specifikt om: dybere forklaring af git-koncepter, GitHub/repo/commit/push/pull, professionelle arbejdsgange, og praktisk info (hvilken terminal til hvad, hvordan SSH fungerer).

---

## M2: VS Code ✅

- [x] **Step 1: Extensions** — GitLens, WSL, Remote-SSH, Prettier, Python, ESLint
  - Han spurgte "hvad er GitLens?" og "burde jeg vide noget om disse?" → fik kort forklaring af alle seks
  - Havde problemer med at finde den rigtige Prettier (mange varianter)
  - Foreslog selv at der burde laves en "VS Code håndbog"
- [x] **Step 2: settings.json** (`C:\Users\Krist\AppData\Roaming\Code\User\settings.json`)
  - Kunne ikke finde filen — vidste ikke om Preferences: Open User Settings (JSON)
  - Forvekslede den med .claude/settings.local.json
  - Indhold: formatOnSave, Prettier default, JetBrains Mono (fallback Consolas), minimap fra, wordWrap, tabSize 2, rulers 80+120, autoSave onFocusChange, terminal=Ubuntu WSL
  - Spurgte hvad hver linje gør — fik forklaring
- [x] **Step 3: Keybindings** — Ctrl+½ → toggle terminal
  - Ctrl+` virker ikke på dansk layout — åbnede settings i stedet for terminal
  - Åbnede den forkerte keybindings-fil (standard/skrivebeskyttet, 5796 linjer) → crashede sessionen (prompt too long)
  - Løst i ny session: `oem_5` i `C:\Users\Krist\AppData\Roaming\Code\User\keybindings.json`
- [x] **Step 4: Workspace-filer** — forklaret. Ikke nødvendigt endnu (Open Folder dækker ét projekt). Relevant når flere mapper skal samles.
- [x] **Repo oprettet** — github.com/Yttrehus/Basic-setup (renamed fra test-repo, force-pushed)
- [x] **CLAUDE.md workflow-regler** — commit+push efter ændringer, PLAN.md som levende dokument, state på disk

---

## M3: Terminal/Shell (WSL) ✅

- [x] Zsh installeret + sat som default shell (chsh)
- [x] Oh My Zsh installeret (framework for plugins/temaer)
- [x] Starship prompt (moderne, informativ — viser mappe, git-branch, sprog)
- [x] Plugins: zsh-autosuggestions (historik-forslag), zsh-syntax-highlighting (farver kommandoer)
- [x] Shell-aliases i ~/.zshrc: gs, ga, gc, gp, gd, gl, ll, .., ...
- [ ] Dotfiles-strategi → udskudt til M4

**Vigtige filer:**
- `~/.zshrc` — shell-config (Oh My Zsh + Starship + plugins + aliases)
- `~/.oh-my-zsh/` — Oh My Zsh framework
- Starship binary: `/usr/local/bin/starship`

**Bemærkninger:**
- WSL sudo-password blev reset via `wsl -u root passwd yttre` (Yttre huskede ikke det originale)
- Starship scan_timeout warning i store mapper (kosmetisk, ikke et problem)

---

## M4: Projekt-struktur — ikke startet

- [ ] ~/dev/ layout og konventioner
- [ ] Standard mappestruktur per projekt
- [ ] Dotfiles-repo (gemme gitconfig, zshrc etc. i git)
- [ ] Koble til Notion-struktur

---

## M5: Context engineering + workflow — ikke startet

Yttre er meget bevidst om context window-problemer — har tabt kontekst mange gange. Relevant:
- [ ] CLAUDE.md per projekt som levende dokument
- [ ] Plan-filer som dette dokument
- [ ] `strategic-compact` skill (allerede installeret)
- [ ] State på disk, aldrig kun i chat

---

## Filer i projektet

| Fil | Hvad |
|-----|------|
| CLAUDE.md | Projektinstruktioner til Claude |
| PLAN.md | Denne fil — levende plan |
| references/git.md | Git kommando-håndbog |
| setup/git-concepts.md | Git koncepter, workflows, SSH |
| .claude/skills/infrastructure.md | VPS/Yggdra skill |
| .claude/skills/notion.md | Notion MCP skill |
| session-history.md | Dump af forrige session (midlertidig) |
| dump-session.js | Script til at dumpe sessioner (midlertidig) |

---

## Åbne idéer (nævnt men ikke planlagt)

- VS Code håndbog (Yttre foreslog det)
- Context engineering som M5
- Notion parallelt med VS Code-struktur
- Programmeringssprog: ingen præference endnu — "lærer det ikke hvis jeg ikke bruger det, og med AI behøver man det ikke i samme grad"
