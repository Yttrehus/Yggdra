# Windows 11 Developer Setup — Research (marts 2026)

Research fra web-søgning: hvordan professionelle udviklere sætter Windows 11 op.

---

## 1. Taskbar & Desktop Organization

**Fjern clutter:**
- Unpin alt du ikke bruger dagligt (right-click > Unpin from taskbar)
- Slå Widgets fra: Settings > Personalization > Taskbar > Widgets OFF
- Slå Search fra (eller sæt til icon only): samme sted
- Slå Task View fra: samme sted
- Slå Copilot-knap fra hvis ubrugt: samme sted

**Taskbar alignment:**
- Mange power users sætter alignment til Left (Settings > Personalization > Taskbar > Taskbar behaviors > Left) — mere forudsigeligt end centered

**Auto-hide:**
- Settings > Personalization > Taskbar > Taskbar behaviors > Auto-hide — giver mere skærmplads, især på laptops

**Anbefalede pinned apps (developer):**
- File Explorer, Windows Terminal, VS Code, Browser — resten via launcher (PowerToys Run / Command Palette)

**Ekstra tools:**
- TranslucentTB (Microsoft Store, gratis) — transparent taskbar
- Windhawk (open source) — lightweight UI mods

**Kilder:**
- [HowToGeek: 6 Settings to Make Your Windows 11 Desktop More Minimalist](https://www.howtogeek.com/settings-to-make-your-windows-11-desktop-more-minimalist/)
- [XDA: Beautiful minimalistic Windows desktop](https://www.xda-developers.com/i-made-beautiful-minimalistic-windows-desktop/)
- [Microsoft Support: Customize the Taskbar](https://support.microsoft.com/en-us/windows/customize-the-taskbar-in-windows-0657a50f-0cc7-dbfd-ae6b-05020b195b07)

---

## 2. Essential Software (Developer)

### Tier 1 — Allerede installeret
- **VS Code** — editor
- **Git** — versionskontrol
- **Windows Terminal** — multi-shell (PowerShell, WSL, CMD)
- **WSL 2 + Ubuntu** — Linux-miljø
- **Python + uv** — scripting/pakker

### Tier 2 — Stærkt anbefalet
- **PowerToys** — se separat sektion nedenfor
- **Dev Home** (Microsoft) — GitHub integration, system monitoring, environment setup automation
- **winget** — CLI package manager (built-in, bruges til scripted installs)
- **Docker Desktop** — containers med WSL 2 backend (near-native performance)
- **Oh My Posh** eller **Starship** — shell prompt (allerede sat op via Starship)

### Tier 3 — Nice to have
- **Everything** (voidtools) — instant filsøgning (hurtigere end Windows Search)
- **7-Zip** — arkivering
- **Notepad++** — hurtig teksteditor til non-projekt filer
- **ShareX** — screenshots og screen recording
- **TreeSize Free** — visualisér diskforbrug
- **Process Explorer** (Sysinternals) — avanceret task manager
- **WinMerge** eller **Beyond Compare** — fil-diffing
- **Bitwarden** / **KeePass** — password manager

### Tier 4 — Situationsbestemt
- **Postman** eller **Bruno** — API testing
- **FileZilla** — FTP/SFTP (SSH er bedre, men nyttigt for legacy)
- **OBS Studio** — streaming/recording
- **VLC** — medieafspiller

**Kilder:**
- [Windows Central: 12 apps every power user should install](https://www.windowscentral.com/software-apps/windows-11/12-apps-every-power-user-should-install-on-a-new-pc-running-windows-11)
- [Usevoicy: 25 Best Windows 11 Productivity Apps 2025](https://usevoicy.com/blog/best-windows-11-apps-2025)
- [Indigo Software: Windows 11/12 for Developers 2026](https://indigosoftwarecompany.com/windows-11-12-for-developers-best-tools-settings-for-coding-in-2026/)
- [WinGeek: Best Software for Windows 11 Reddit 2025](https://wingeek.org/best-software-for-windows-11-reddit-2025/)

---

## 3. PowerToys — Nøglemoduler for udviklere

Installér via: `winget install Microsoft.PowerToys`

| Modul | Hvad det gør | Developer-relevans |
|---|---|---|
| **FancyZones** | Custom window layouts (grid, columns, overlap) | Editor + terminal + browser side-by-side. Flere layouts til forskellige workflows |
| **Command Palette** | Spotlight-agtig launcher (afløser PowerToys Run) | Hurtig app-launch, fil-søgning, system-kommandoer. Extensible med plugins |
| **PowerToys Run** | Ældre launcher (stadig tilgængelig) | Alt+Space til hurtig søgning |
| **Peek** | Quick preview med Ctrl+Space i File Explorer | Preview kode, billeder, markdown uden at åbne |
| **PowerRename** | Regex-baseret batch rename | Omdøb filer i bulk med regex |
| **Color Picker** | Win+Shift+C — pick farve fra skærmen | Frontend/CSS arbejde |
| **File Locksmith** | Vis hvilken process låser en fil | Debugging: "file in use" fejl |
| **Keyboard Manager** | Remap keys og shortcuts | Tilpas keyboard layout |
| **Image Resizer** | Batch resize i File Explorer context menu | Hurtig billedbehandling |
| **Workspaces** | Gem og gendan app-layouts med ét klik | "Coding workspace" vs "meeting workspace" |
| **Light Switch** | Automatisk dark/light mode skift | Tidsbaseret tema |
| **Mouse Without Borders** | Del mus/keyboard mellem PC'er | Multi-machine workflows |

**Anbefalet startpakke:** FancyZones + Command Palette + Peek + File Locksmith + Color Picker

**Kilder:**
- [Microsoft Learn: PowerToys](https://learn.microsoft.com/en-us/windows/powertoys/)
- [WindowsForum: PowerToys 2026 — 7 Essential Modules](https://windowsforum.com/threads/powertoys-2026-7-essential-windows-11-modules-to-boost-productivity.395308/)
- [TechRadar: Transforming Windows 11 with PowerToys 2026](https://www.techradar.com/computing/windows/im-transforming-windows-11-in-2026-using-powertoys-heres-how-you-can-too)
- [free-codecs: Complete Guide to All 25+ PowerToys Utilities 2026](https://www.free-codecs.com/guides/what_is_the_use_of_powertoys_.htm)

---

## 4. Privacy & Telemetry

**Basis (Settings UI):**
1. Settings > Privacy & Security > Diagnostics & feedback > Send optional diagnostic data: OFF
2. Settings > Privacy & Security > General > slå alle fire toggles fra (advertising ID, language list, app launch tracking, suggested content)
3. Settings > Privacy & Security > Activity history > Store my activity history: OFF
4. Settings > Privacy & Security > Search permissions > slå Cloud/Bing search fra

**Avanceret (Pro/Enterprise — Group Policy):**
- gpedit.msc > Computer Configuration > Administrative Templates > Windows Components > Data Collection and Preview Builds
- Sæt "Allow Diagnostic Data" til "Diagnostic data off" eller "Send required diagnostic data"

**Avanceret (Registry — alle editions):**
- `HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection` > AllowTelemetry = 0
- **NB:** På Home edition kan telemetry ikke slås helt fra — "Required" er minimum

**Tjenester der kan disables:**
- Connected User Experiences and Telemetry (`DiagTrack`) — `sc stop DiagTrack && sc config DiagTrack start=disabled`
- **Advarsel:** Aggressive disabling kan bryde Windows Update og andre funktioner

**Tools:**
- O&O ShutUp10++ — GUI til privacy settings (anbefalet af Privacy Guides community)
- Ikke anbefalet: scripts der sletter telemetry aggressivt — kan destabilisere systemet

**Developer-anbefaling:** Reducér via Settings først, tilføj Group Policy/Registry hvis Pro edition. Dokumentér ændringer. Undgå aggressive third-party scripts.

**Kilder:**
- [NinjaOne: How to Disable Telemetry in Windows 11](https://www.ninjaone.com/blog/how-to-disable-telemetry-in-windows-11/)
- [TheLinuxCode: Enable/Disable Telemetry 2026 Guide](https://thelinuxcode.com/how-to-enable-or-disable-telemetry-in-windows-11-practical-2026-guide/)
- [Privacy Guides Community: Best tool to disable telemetry](https://discuss.privacyguides.net/t/best-tool-to-disable-telemetry-on-win11/18516)
- [WindowsForum: Disable Windows Telemetry for Privacy](https://windowsforum.com/threads/how-to-disable-windows-telemetry-for-enhanced-privacy-in-windows-11.373581/)

---

## 5. File System Organization

**Top-level layout (konsensus):**
```
~/
├── dev/                    # Alt udvikling
│   ├── projects/           # Aktive projekter (git repos)
│   ├── sandbox/            # Eksperimenter, throwaway
│   ├── archive/            # Afsluttede/pauserede
│   └── scripts/            # Personlige scripts (eller dotfiles/bin/)
├── Documents/              # Ikke-kode dokumenter
├── Downloads/              # Temp — ryd op regelmæssigt
└── .dotfiles/              # Versioneret config (git bare repo eller symlinks)
```

**Principper:**
- Max 3-4 niveauer dybt — dybere = sværere at navigere
- Undgå "Misc" / "Stuff" mapper — brug beskrivende navne
- Working → Final → Archive flow for projekt-livscyklus
- Ét `dev/` rod i home directory — alt kode-relateret starter her
- Konsistent naming: enten kebab-case, snake_case, eller CamelCase — vælg ét

**Vedligeholdelse:**
- Regelmæssig oprydning af Downloads/
- Arkivér afsluttede projekter (flyt til archive/)
- Hold desktop tom eller med max 2-3 genveje

**Kilder:**
- [DEV.to: My development folder structure](https://dev.to/jmorjsm/my-development-folder-structure-3e5n)
- [Medium/DEV.to: Projects Folder Structures Best Practices](https://dev.to/mattqafouri/projects-folder-structures-best-practices-g9d)
- [Glarysoft: 15 Folder Structure Optimization Strategies](https://www.glarysoft.com/how-to/the-15-most-effective-folder-structure-optimization-strategies-for-windows-11/)

---

## 6. Automated Setup via winget

**Idé:** Scriptet install af al software ved fresh install.

**Simpel metode — PowerShell script:**
```powershell
$apps = @(
    "Microsoft.PowerToys"
    "Microsoft.VisualStudioCode"
    "Git.Git"
    "Python.Python.3.13"
    "7zip.7zip"
    "voidtools.Everything"
    "ShareX.ShareX"
    "Notepad++.Notepad++"
)
foreach ($app in $apps) {
    winget install --id $app --accept-package-agreements --accept-source-agreements
}
```

**Avanceret metode — WinGet Configuration (YAML):**
- Deklarativ YAML-fil der beskriver hele miljøet
- Idempotent: kan køres flere gange, ændrer kun hvad der mangler
- Kør med `winget configure <file.yaml>`
- Kombinerer app-installation med Windows-settings

**Kilder:**
- [Microsoft Dev Blog: WinGet Configuration](https://developer.microsoft.com/blog/winget-configuration-set-up-your-dev-machine-in-one-command)
- [GitHub: windows11-fresh-install-toolkit](https://github.com/Mantej-Singh/windows11-fresh-install-toolkit)
- [XDA: Simple script to install all apps using WinGet](https://www.xda-developers.com/made-simple-script-install-all-apps-new-pc-using-winget-you-can-make-your-own/)

---

## 7. Andre Windows Settings (Developer-relevant)

- **Developer Mode:** Settings > System > For developers > Developer Mode ON — tillader sideloading, symlinks uden elevation, mere
- **File Explorer:** Vis fil-extensions (View > Show > File name extensions), vis skjulte filer
- **Default terminal:** Sæt Windows Terminal som default (Settings > System > For developers > Terminal > Windows Terminal)
- **Clipboard history:** Win+V — Settings > System > Clipboard > Clipboard history ON
- **Focus Assist / Do Not Disturb:** Brug under kodning for at blokere notifikationer
- **Virtual Desktops:** Win+Ctrl+D for ny desktop, Win+Ctrl+Left/Right for at skifte — separér "kode" og "kommunikation"
- **Night Light:** Settings > System > Display > Night Light — reducér blue light om aftenen

**Kilder:**
- [Microsoft Learn: Settings for developers](https://learn.microsoft.com/en-us/windows/advanced-settings/developer-mode)
- [Microsoft Learn: Setup a development environment on Windows](https://learn.microsoft.com/en-us/windows/dev-environment/)
- [Medium: A Developer's Guide to Setting Up Windows 11](https://medium.com/@arishokri_94614/a-developers-guide-to-setting-up-windows-11-56cabf3dbd51)

---

## 8. Theme & Dark Mode

**Dark mode setup:**
- Settings > Personalization > Colors > Choose your mode: **Dark**
- Custom mode giver bedre kontrol: Windows-shell i Dark, Apps kan vælges separat (Light eller Dark)

**Accent color:**
- Settings > Personalization > Colors > Accent color
- **Automatic:** Tager farve fra wallpaper — holder palette konsistent
- **Manual:** Vælg selv — god til branding/præference
- Toggle: "Show accent color on Start and taskbar" og "Show accent color on title bars and window borders"

**Cursor customization:**
- Settings > Accessibility > Mouse pointer and touch — vælg sort, hvid, inverteret eller custom farve cursor
- Custom cursor themes: download .cur/.ani filer, installér via Settings > Bluetooth & devices > Mouse > Additional mouse settings > Pointers

**Automatisk skift (dag/nat):**
- [Auto Dark Mode](https://github.com/AutoDarkMode/Windows-Auto-Night-Mode) — open source, gratis
- Skifter tema baseret på solop/nedgang eller custom tider
- Kan også skifte wallpaper, accent color, og cursor theme automatisk

**Kilder:**
- [Microsoft Support: Personalize Your Colors](https://support.microsoft.com/en-us/windows/personalize-your-colors-in-windows-3290d30f-d064-5cfe-6470-2fe9c6533e37)
- [WindowsForum: Ultimate Guide to Dark Mode](https://windowsforum.com/threads/ultimate-guide-to-dark-mode-on-windows-11-benefits-setup-customization.365879/)
- [WindowsForum: Practical Dark Mode Step-by-Step](https://windowsforum.com/threads/practical-windows-11-dark-mode-a-system-wide-step-by-step-guide.381046/)
- [GitHub: Auto Dark Mode](https://github.com/AutoDarkMode/Windows-Auto-Night-Mode)

---

## 9. Default Apps & File Associations

**Sti:** Settings > Apps > Default apps (eller `ms-settings:defaultapps` i Run)

**Browser:**
- Søg efter "browser" eller klik på din foretrukne browser i app-listen
- Klik "Set default" knappen øverst — sætter alle browser-relaterede filtyper (.htm, .html, HTTP, HTTPS)
- **NB:** Microsoft kan nulstille til Edge efter store Windows-opdateringer — check efter updates

**PDF viewer:**
- Søg efter ".pdf" i Default apps
- Vælg din foretrukne app (Sumatra PDF, Acrobat Reader, Firefox, etc.)
- Edge er default — kræver manuelt skifte per extension

**Fil-associations (generelt):**
- Default apps > Vælg "Choose defaults by file type" i bunden
- Sæt associations for: .txt, .json, .md, .log → VS Code; .pdf → Sumatra/Acrobat; .zip → 7-Zip
- Windows 11 enforcer per-extension — apps kan ikke selv overtage associations

**Tip:** "Set as default" knapper i apps virker ikke altid pga. Windows 11 security — brug altid Settings UI.

**Kilder:**
- [Microsoft Support: Change Default Apps](https://support.microsoft.com/en-us/windows/change-default-apps-in-windows-e5d82cad-17d1-c53b-3505-f10a32e1894d)
- [Illinois State Help: Changing Default Browser and PDF Viewer](https://help.illinoisstate.edu/technology/support-topics/device-support/windows/windows-11-overview/changing-your-default-browser-and-pdf-viewer-in-windows-11)
- [Winaero: Change Default Apps](https://winaero.com/change-default-apps-windows-11/)
- [Digital Citizen: How to set default apps](https://www.digitalcitizen.life/how-associate-file-type-or-protocol-program/)

---

## 10. Touchpad Gestures

**Sti:** Settings > Bluetooth & devices > Touchpad

**Scroll:**
- Two-finger scroll: ON som default
- Scrolling direction: "Down motion scrolls down" (naturligt/omvendt) — vælg hvad der passer
- Scroll speed kan justeres

**Taps:**
- Touchpad sensitivity: vælg mellem Most sensitive, High, Medium, Low
- Taps: toggles for "Tap with a single finger to single-click", "Tap with two fingers to right-click", "Tap twice and drag to multi-select", "Press the lower right corner of the touchpad to right-click"

**Three-finger gestures (default):**
- Swipe up: Show all windows (Task View)
- Swipe down: Show desktop
- Swipe left/right: Switch apps
- Tap: Open search

**Four-finger gestures (default):**
- Swipe up: Show all windows
- Swipe down: Show desktop
- Swipe left/right: Switch virtual desktops
- Tap: Notification center / Play-pause

**Power user customization:**
- Settings > Bluetooth & devices > Touchpad > Advanced gestures
- Hvert gesture (3-finger tap, 3-finger swipe up/down/left/right, 4-finger ditto) kan tildeles individuel aktion
- Aktioner inkluderer: Custom keyboard shortcut, volume up/down, forward/back, snap window, switch desktop, open search, notification center, play/pause, m.fl.

**Anbefalinger for developer workflow:**
- 3-finger tap: Open search (hurtigt åben apps/filer)
- 3-finger swipe up: Task View
- 3-finger swipe down: Show desktop
- 4-finger swipe left/right: Switch virtual desktops (kode vs. kommunikation)
- 4-finger tap: Custom shortcut (f.eks. Win+V for clipboard history)

**Kilder:**
- [Microsoft: Touchpad Gestures for Windows 11](https://www.microsoft.com/en-us/windows/learning-center/touchpad-gestures)
- [Windows Central: How to Customize Touchpad Settings](https://www.windowscentral.com/software-apps/windows-11/how-to-customize-touchpad-settings-on-windows-11)
- [XDA: Customize Touchpad Gestures](https://www.xda-developers.com/how-customize-touchpad-gestures-windows-11/)
- [SlashGear: Hidden Windows 11 Touchpad Setting](https://www.slashgear.com/1056429/this-hidden-windows-11-setting-lets-you-customize-touchpad-gestures-to-your-style/)

---

## 11. Display Scaling (High-DPI / 2.8K OLED)

**Sti:** Settings > System > Display > Scale

**Generelle guidelines for 2.8K (2880x1800) på 14" laptop:**
- Windows anbefaler typisk 175% eller 200% — start med recommended
- 150% giver mere skærmplads men mindre tekst
- 200% giver stor, skarp tekst men mindre workspace
- **Test i praksis:** Åbn VS Code + terminal + browser side-by-side og vurder læsbarhed

**Tekststørrelse (separat justering):**
- Settings > Accessibility > Text size — slider fra 100% til 225%
- Ændrer kun tekst, ikke hele UI — god til finjustering efter scaling er sat

**Per-app scaling fix (legacy apps):**
- Højreklik app > Properties > Compatibility > Change high DPI settings
- "Override high DPI scaling behavior" > "Application" eller "System (Enhanced)"
- Relevant for ældre apps der ser slørede ud

**ClearType:**
- Søg "ClearType" i Start > "Adjust ClearType text" — kør wizard for skarpere tekst
- Specielt vigtigt for OLED hvor subpixel-rendering fungerer anderledes

**Night Light:**
- Settings > System > Display > Night Light — reducér blåt lys om aftenen
- Sæt schedule (solop/nedgang eller custom tider)

**OLED-specifikt:**
- Brug mørke temaer (Dark mode) — reducerer strømforbrug og potentiel burn-in
- Overvej en screensaver eller kortere screen timeout

**Kilder:**
- [ElevenForum: Change Display DPI Scaling](https://www.elevenforum.com/t/change-display-dpi-scaling-level-in-windows-11.934/)
- [Winaero: How to Change DPI Display Scaling](https://winaero.com/how-to-change-dpi-display-scaling-in-windows-11/)
- [MundoBytes: Adjust DPI — Scaling and Sharpness Guide](https://mundobytes.com/en/adjust-dpi-in-windows-11/)
- [Microsoft Support: Scaling Issues for High-DPI Devices](https://support.microsoft.com/en-us/topic/windows-scaling-issues-for-high-dpi-devices-surface-pro-3-surface-pro-4-or-surface-book-508483cd-7c59-0d08-12b0-960b99aa347d)

---

## 12. Power Settings (Laptop)

**Sti:** Settings > System > Power & battery

**Screen & sleep timeouts:**
- Settings > System > Power & battery > Screen, sleep, & hibernate timeouts
- On battery: Screen off efter 5 min, Sleep efter 10-15 min (anbefalet)
- Plugged in: Screen off efter 10-15 min, Sleep efter 30 min eller Never (developer-workflow)

**Lid close action:**
- Settings > System > Power & battery > Lid & power button controls
- "Closing the lid will make my PC": vælg separat for On battery / Plugged in
- Muligheder: Do nothing, Sleep, Hibernate, Shutdown
- **Developer-tip:** "Do nothing" når plugged in (brug ekstern skærm med lukket låg), "Sleep" on battery
- Alternativ sti: Control Panel > Power Options > "Choose what closing the lid does"

**Power modes:**
- Settings > System > Power & battery > Power mode
- **Best performance:** Til tung kompilering, Docker, VM'er
- **Balanced:** Daglig brug — bedste kompromis
- **Best power efficiency:** Batteri-bevarende, lavere performance

**Hibernate:**
- Gem alt til disk og sluk helt — bedre end Sleep for lang transport
- Aktivér: Control Panel > Power Options > "Choose what the power buttons do" > "Change settings that are currently unavailable" > check "Hibernate"

**Kilder:**
- [Microsoft Support: Power Settings](https://support.microsoft.com/en-us/windows/power-settings-in-windows-11-0d6a2b6b-2e87-4611-9980-ac9ea2175734)
- [Windows Central: How to Manage Power Settings](https://www.windowscentral.com/how-manage-power-settings-windows-11)
- [Pureinfotech: Change Lid Close Action](https://pureinfotech.com/change-close-lid-action-windows-11/)
- [HowToGeek: Keep Laptop On With Lid Closed](https://www.howtogeek.com/822524/how-to-keep-your-laptop-on-with-the-lid-closed-on-windows-11/)

---

## 13. Mouse Settings

**Sti:** Settings > Bluetooth & devices > Mouse

**Pointer speed:**
- Slider i Settings > Bluetooth & devices > Mouse
- Justér til preference — ikke en "korrekt" værdi, men konsistens er vigtig

**Enhance Pointer Precision (mouse acceleration):**
- **Slå FRA for konsistent pointer-bevægelse** — specielt vigtigt for præcist arbejde
- Sti: Settings > Bluetooth & devices > Mouse > Additional mouse settings > Pointer Options > untick "Enhance pointer precision"
- Alternativ: Control Panel > Mouse > Pointer Options > untick
- Registry (persistent): `HKCU\Control Panel\Mouse` — sæt MouseSpeed, MouseThreshold1, MouseThreshold2 alle til 0

**Scroll:**
- Settings > Bluetooth & devices > Mouse > "Lines to scroll at a time" — default 3, justér til preference
- "Scroll inactive windows when I hover over them": ON (god for multi-window workflows)

**Kilder:**
- [Microsoft Support: Change Mouse Settings](https://support.microsoft.com/en-us/windows/change-mouse-settings-e81356a4-0e74-fe38-7d01-9d79fbf8712b)
- [HowToGeek: Turn Off Mouse Acceleration](https://www.howtogeek.com/how-and-why-to-turn-off-mouse-acceleration-on-windows-11/)
- [ElevenForum: Enhance Pointer Precision](https://www.elevenforum.com/t/turn-on-or-off-enhance-pointer-precision-in-windows-11.7327/)
- [Windows Central: Customize Mouse Settings](https://www.windowscentral.com/software-apps/windows-11/how-to-customize-mouse-settings-on-windows-11)

---

## 14. Sound & Audio Devices

**Sti:** Settings > System > Sound

**Default output device:**
- Settings > System > Sound > Output > vælg device
- Eller: Klik volume-ikon i system tray > klik pilen ved slider > vælg device

**Per-app audio routing:**
- Settings > System > Sound > Volume mixer (bunden)
- Hvert kørende app kan tildeles separat output-device og volume
- Eksempel: Discord → headset, Spotify → speakers, Teams → headset

**Hurtigt skift mellem devices:**
- Klik volume-ikon i system tray > klik device-navn > vælg nyt device
- Eller: Win+G (Game Bar) har audio-widget med hurtig device-switching

**Bluetooth headset gotchas:**
- Bluetooth headsets registrerer sig som to devices: "Headset (Hands-Free)" (lavere kvalitet, mic) og "Headphones (Stereo)" (høj kvalitet, ingen mic)
- Sæt default communication device til Hands-Free og default output til Stereo

**Kommende features (Insider builds):**
- Shared audio: Send lyd til to Bluetooth LE Audio devices samtidig
- Forbedret per-app routing direkte fra Quick Settings
- Kræver Bluetooth LE Audio-kompatibel hardware

**Kilder:**
- [Windows Central: Share Audio to Multiple Devices](https://www.windowscentral.com/microsoft/windows-11/windows-11-will-finally-let-you-share-audio-to-multiple-devices-at-once)
- [Windows Insider Blog: Bluetooth LE Audio Shared Audio](https://blogs.windows.com/windows-insider/2025/10/31/extending-bluetooth-le-audio-on-windows-11-with-shared-audio-preview/)
- [WindowsForum: Per-App Audio Routing](https://windowsforum.com/threads/windows-11-insider-shared-audio-with-le-audio-and-per-app-routing.403640/)

---

## 15. OneDrive — Disable/Kontrol

**Vurdering først:** OneDrive er nyttigt til backup af Documents. Problemet er at det overtager Desktop, Documents, Pictures mapper og syncer alt automatisk.

**Stop folder backup (behold OneDrive):**
- OneDrive tray-ikon > Settings > Sync and backup > Manage backup
- Slå fra for Desktop, Documents, Pictures individuelt
- Filer flyttes tilbage til lokale mapper

**Fjern fra startup (behold installeret):**
- Ctrl+Shift+Esc (Task Manager) > Startup apps > Microsoft OneDrive > Disable
- OneDrive kører ikke ved boot, men kan stadig åbnes manuelt

**Unlink PC (behold installeret, stop al sync):**
- OneDrive tray-ikon > Settings > Account > Unlink this PC
- Al sync stopper, lokale filer forbliver

**Fuld afinstallation:**
- Settings > Apps > Installed apps > Microsoft OneDrive > Uninstall
- **NB:** Tjek at Desktop/Documents/Pictures er flyttet TILBAGE til lokale mapper først
- Mapper kan sidde fast i OneDrive-stien efter uninstall — flyt manuelt via Properties > Location

**Group Policy (Pro edition):**
- gpedit.msc > Computer Configuration > Administrative Templates > Windows Components > OneDrive
- "Prevent the usage of OneDrive for file storage": Enabled

**Developer-anbefaling:**
1. Behold OneDrive installeret men slå folder backup fra
2. Brug det kun til specifikke mapper du vil have i cloud (manuelt)
3. Sørg for at `~/dev/` IKKE syncer til OneDrive — det ødelægger git repos (node_modules, .git, etc.)

**Kilder:**
- [Microsoft Support: Turn Off, Disable, or Uninstall OneDrive](https://support.microsoft.com/en-us/office/turn-off-disable-or-uninstall-onedrive-f32a17ce-3336-40fe-9c38-6efb09f944b0)
- [GeeksForGeeks: Disable OneDrive in Windows 11](https://www.geeksforgeeks.org/techtips/how-to-disable-onedrive-in-windows-11/)
- [ElevenForum: Enable or Disable OneDrive](https://www.elevenforum.com/t/enable-or-disable-onedrive-in-windows-11.2318/)
- [IT Trip: Disable OneDrive on Windows 11 Pro](https://en.ittrip.xyz/onedrive/disable-onedrive-win11pro)

---

## 16. Power User Tips & Tricks

**Keyboard shortcuts (mest nyttige):**
| Shortcut | Funktion |
|---|---|
| Win+V | Clipboard history (aktivér først: Settings > System > Clipboard) |
| Win+Shift+S | Screenshot (Snipping Tool) |
| Win+Z | Snap Layouts — vælg window arrangement |
| Win+X | Quick Link menu (Terminal, Device Manager, Disk Management, etc.) |
| Win+H | Voice typing i enhver tekstboks |
| Win+. | Emoji picker |
| Win+Ctrl+D | Ny virtual desktop |
| Win+Ctrl+Left/Right | Skift virtual desktop |
| Win+L | Lås PC |
| Ctrl+Shift+Esc | Task Manager direkte (skip Ctrl+Alt+Del) |
| Shift+F10 | Fuld højreklik-menu (legacy, alle options — skip "Show more options") |
| Win+Tab | Task View (alle vinduer + desktops) |
| Alt+Tab | App switcher |
| Win+E | File Explorer |
| Win+I | Settings |
| Win+A | Quick Settings |
| Win+N | Notification center |

**Clipboard history:**
- Win+V åbner historik med op til 25 items
- Pin op til 5 items der overlever reboot
- Synkroniserer på tværs af devices (hvis slået til)

**Dynamic Lock:**
- Settings > Accounts > Sign-in options > Dynamic lock
- Par Bluetooth-telefon — PC låser automatisk når telefon er uden for rækkevidde

**Title Bar Shake (Aero Shake):**
- Grib et vindue og ryst — minimerer alle andre vinduer
- Settings > System > Multitasking > Title bar window shake: ON

**Focus / Do Not Disturb:**
- Win+N > Focus timer — Pomodoro-agtig timer der blokerer notifikationer
- Settings > System > Notifications > Do not disturb — manuelt

**God Mode (alle Control Panel settings på én gang):**
- Opret mappe med navn: `GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}`
- Giver ét vindue med ALLE system-settings

**End Task fra Taskbar:**
- Settings > System > For developers > End Task: ON
- Giver "End task" option når du højreklikker apps i taskbar (som Task Manager men hurtigere)

**Kilder:**
- [Tom's Guide: 15 Top Windows 11 Tips](https://www.tomsguide.com/computing/windows-operating-systems/15-top-windows-11-tips-everyone-needs-to-know)
- [Digital Trends: 10 Hidden Settings You Need to Try](https://www.digitaltrends.com/computing/windows-11-tips-and-tricks-10-hidden-settings/)
- [WindowsForum: 73 Essential Keyboard Shortcuts](https://windowsforum.com/threads/master-windows-11-with-73-essential-keyboard-shortcuts-for-boosted-productivity.370568/)
- [TechRepublic: 9 Windows 11 Features You're Not Using](https://www.techrepublic.com/article/news-windows-11-hidden-features-tips/)
- [WindowsForum: Unlock Hidden Power in Windows 11](https://windowsforum.com/threads/unlock-hidden-power-in-windows-11-tips-tools-and-features-for-ultimate-productivity.374862/)
