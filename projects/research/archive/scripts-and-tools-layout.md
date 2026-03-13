# Scripts, Tools & Utilities — Developer Workspace Conventions

Research: how professionals organize personal scripts, tools, and utilities.
Sources: GitHub dotfiles repos, Hacker News, dev.to, MIT Missing Semester, Arch Wiki, various blogs.

---

## 1. Top-Level Dev Directory

**What people actually call it:**

| Name | Usage | Notes |
|------|-------|-------|
| `~/dev/` | Very common | Short, generic. Allows sub-dirs like sandbox/, tools/ |
| `~/code/` | Common | Simple, unambiguous |
| `~/projects/` | Common | More descriptive, but longer |
| `~/src/` | Common (esp. Go devs) | Unix tradition (FreeBSD has /usr/src) |
| `~/workspace/` | Less common | Java/Go heritage (GOPATH style) |

**Internal organization patterns:**

1. **Flat** — `~/dev/project-name/` (most beginners, fine up to ~20 projects)
2. **By owner/namespace** — `~/dev/github.com/owner/repo/` or `~/dev/owner/repo/` (Go-inspired, scales well)
3. **By category** — `~/dev/projects/`, `~/dev/sandbox/`, `~/dev/archive/` (what you already have)
4. **By date** — `~/dev/2024/0419-project/` (niche, used by some academics)

**Source:** [Bryan Braun](https://www.bryanbraun.com/2017/08/29/how-i-organize-the-code-folder-on-my-computer/) uses `~/Code/owner/repo/`. [Boot.dev](https://www.boot.dev/blog/misc/how-i-organize-my-local-development-environment/) uses `~/workspace/github.com/owner/repo/`. [Dev.to discussion](https://dev.to/heroku/what-do-you-call-your-folder-where-you-keep-your-code-9gp) shows ~equal split between dev/code/projects/src.

---

## 2. bin/ vs scripts/ vs tools/ — The Key Distinction

This is the most important finding. There are **three separate concerns** that people conflate:

### A. `~/bin/` or `~/.local/bin/` — Personal executables on PATH

- **Purpose:** Finished scripts/binaries you run by name from anywhere
- **Convention:** Added to `$PATH`. Contains short, polished commands
- **Examples:** `git-cleanup`, `serve`, `weather`, `note`
- **XDG standard:** `~/.local/bin/` is the XDG-blessed location
- **Practical note:** `~/.local/bin/` gets polluted by pip, npm etc. Many devs prefer `~/bin/` for hand-written scripts to keep them separate from tool-installed binaries

**Source:** [Arch Wiki XDG](https://wiki.archlinux.org/title/XDG_Base_Directory), [HN discussion](https://news.ycombinator.com/item?id=36337441), [Lemmy thread](https://lemmy.ml/post/29303982)

### B. `scripts/` inside a project repo — Project-specific automation

- **Purpose:** Scripts that only make sense in that project's context
- **Convention:** Lives in the repo root as `scripts/` or `script/`
- **Examples:** `scripts/setup.sh`, `scripts/deploy.sh`, `scripts/seed-db.sh`
- **GitHub convention:** [Scripts to Rule Them All](https://github.com/github/scripts-to-rule-them-all) pattern: `script/bootstrap`, `script/setup`, `script/test`, `script/server`

### C. `tools/` inside a project — Helper utilities for the project

- **Purpose:** Things that support the project but aren't the app itself
- **Convention:** `tools/` directory in repo root
- **Examples:** `tools/check-payment.py`, `tools/prune-db.sh`, `tools/generate-fixtures.sh`
- **Distinction from scripts/:** `scripts/` = build/deploy/CI lifecycle. `tools/` = ad-hoc operational utilities

### D. Cross-project utilities — The gray area

This is where conventions diverge most. Common approaches:

1. **Own repo in ~/dev/** — Make a `dev-scripts` or `dotfiles` repo, put it on PATH
2. **Inside dotfiles repo** — `dotfiles/bin/` symlinked or added to PATH (most popular)
3. **Separate `~/scripts/` dir** — Less common, some people do this
4. **`~/dev/tools/`** — What you already have, reasonable choice

**Source:** [Boot.dev](https://www.boot.dev/blog/misc/how-i-organize-my-local-development-environment/): "If useful generally, create a dedicated Git repo within ~/workspace; if scoped to a project, store it in the project's scripts directory."

---

## 3. Dotfiles Repo Organization

### Pattern A: Flat (mathiasbynens/dotfiles)

```
dotfiles/
  .aliases
  .bash_profile
  .bashrc
  .bash_prompt
  .exports
  .functions
  .gitconfig
  .vimrc
  .tmux.conf
  bin/           ← personal scripts, added to PATH
  init/          ← one-time setup scripts
  bootstrap.sh   ← installer
  brew.sh        ← package list
```

**Key insight:** `bin/` contains personal scripts. Shell config is split into purpose files (.aliases, .exports, .functions) all sourced by .bashrc/.bash_profile.

**Source:** [mathiasbynens/dotfiles](https://github.com/mathiasbynens/dotfiles)

### Pattern B: Topical (holman/dotfiles)

```
dotfiles/
  bin/           ← personal scripts on PATH
  git/
    aliases.zsh
    gitconfig.symlink
  zsh/
    zshrc.symlink
    prompt.zsh
  ruby/
    rbenv.zsh
  editors/
    vscode.zsh
  system/
    env.zsh
  script/        ← repo management (bootstrap, install)
```

**Convention:** Files named `*.symlink` get symlinked to `~/`. Files named `*.zsh` get auto-sourced. Each topic is a directory.

**Key insight:** `bin/` = user scripts for daily use. `script/` = dotfiles-repo management scripts (bootstrap, install). These are **two different things** in one repo.

**Source:** [holman/dotfiles](https://github.com/holman/dotfiles)

### Pattern C: XDG-first

```
~/.config/
  git/config
  zsh/.zshrc
  starship.toml
  ...
```

Track `~/.config` as a git repo (or symlink into it). Scripts go in `~/.local/bin/`.

**Source:** [Arch Wiki dotfiles](https://wiki.archlinux.org/title/Dotfiles), [HN XDG discussion](https://news.ycombinator.com/item?id=36337441)

### Where do personal scripts go?

**Strong consensus: scripts go IN the dotfiles repo, in a `bin/` directory.**

- mathiasbynens: `dotfiles/bin/` on PATH
- holman: `dotfiles/bin/` on PATH
- thoughtbot: `dotfiles/bin/` on PATH
- MIT Missing Semester: recommends dotfiles repo with symlinks

The alternative (separate `~/scripts/` repo) exists but is much less common.

**Source:** [MIT Missing Semester](https://missing.csail.mit.edu/2019/dotfiles/)

---

## 4. XDG Base Directory Spec — Relevance for Windows/WSL

### The spec (Linux standard, increasingly adopted elsewhere):

| Variable | Default | Purpose |
|----------|---------|---------|
| `XDG_CONFIG_HOME` | `~/.config` | User config files |
| `XDG_DATA_HOME` | `~/.local/share` | User data files |
| `XDG_CACHE_HOME` | `~/.cache` | Non-essential cached data |
| `XDG_STATE_HOME` | `~/.local/state` | Persistent state (logs, history) |
| n/a | `~/.local/bin` | User executables (not env var, just convention) |

### Windows/WSL relevance:

- **WSL:** Full XDG works since it's Linux. Many tools respect it.
- **Native Windows:** Not standard. Windows uses `%APPDATA%`, `%LOCALAPPDATA%` instead.
- **CLI tools on Windows:** Many Rust/Go CLI tools follow XDG even on Windows (starship, bat, etc.)
- **Practical advice:** For CLI-focused tools, XDG works fine. For GUI apps, Windows conventions win.

**Source:** [XDG spec](https://specifications.freedesktop.org/basedir/basedir-spec-latest.html), [Arch Wiki](https://wiki.archlinux.org/title/XDG_Base_Directory)

---

## 5. Summary: Concrete Patterns

### "Things I built for myself" vs "Things I installed"

| Type | Where | On PATH? |
|------|-------|----------|
| Personal scripts (daily use) | `dotfiles/bin/` or `~/bin/` | Yes |
| Tool-installed binaries (pip, npm, cargo) | `~/.local/bin/` | Yes |
| Project-specific scripts | `project/scripts/` | No (run explicitly) |
| Project operational tools | `project/tools/` | No |
| Cross-project utilities | `dotfiles/bin/` or own repo in ~/dev/ | Yes |
| Dotfiles management scripts | `dotfiles/script/` or `dotfiles/install.sh` | No |

### Most common professional setup:

```
~/
  bin/ or dotfiles/bin/    ← personal scripts, on PATH
  .config/                 ← tool configs (XDG)
  .local/bin/              ← tool-installed binaries, on PATH
  dev/ (or code/ or src/)
    projects/
      my-app/
        scripts/           ← project lifecycle (build, deploy)
        tools/             ← project utilities
    sandbox/
    archive/
  dotfiles/                ← version-controlled configs + bin/
```

### The one thing almost everyone agrees on:

**Keep personal scripts in version control** (usually dotfiles repo), and put them on PATH via `~/bin/` or `dotfiles/bin/`. Don't scatter scripts across random directories.
