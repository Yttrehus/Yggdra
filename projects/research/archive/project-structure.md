# Professional Developer Project Structure — Research

Research conducted 2026-03-10.

---

## 1. How Developers Organize ~/dev/ on Their Machines

### Common Top-Level Names
Developers use one of these as their root development directory:
- `~/dev/` — most common, short
- `~/code/` — clear intent
- `~/projects/` — broader scope
- `~/workspace/` — Go-community origin (GOPATH style)
- `~/src/` — Unix tradition

The key principle: **one single root** for all development work, directly in $HOME.

### Three Real-World Organization Patterns

**Pattern A — By project status (most common for solo devs):**
```
~/dev/
  projects/        # Active, real projects
  sandbox/         # Experiments, throwaway code
  archive/         # Finished/abandoned projects (still git-tracked)
  tools/           # CLI tools, scripts, utilities you maintain
  learning/        # Tutorials, course work, exercises
  config/          # Dotfiles repo, VS Code workspaces, terminal config
```

**Pattern B — By Git hosting platform (common in open source):**
```
~/workspace/
  github.com/
    username/
      project-a/
      project-b/
    other-org/
      contributed-project/
  gitlab.com/
    company/
      work-project/
```
This mirrors GOPATH convention. Advantage: unambiguous origin for every repo.

**Pattern C — By domain/client (freelancers, consultants):**
```
~/dev/
  client-a/
    frontend/
    backend/
  client-b/
    app/
  personal/
    blog/
    dotfiles/
  oss/
    contributions/
```

### Conventions That Recur Everywhere
- **Flat is better than nested** — max 2 levels before you hit actual project roots
- **Archive, don't delete** — move dead projects to `archive/`, keep git history
- **Sandbox for mess** — a guilt-free folder for experiments. Delete contents freely.
- **Keep dotfiles separate** — either in `~/dotfiles/` or `~/dev/config/dotfiles/`

---

## 2. Folder Naming Conventions

### Names
- **lowercase-kebab-case** for all folder and file names (universal convention)
- Avoid spaces, underscores are acceptable but kebab-case is dominant
- Project folders match their git repo names exactly

### Common Top-Level Subdirectories
| Folder | Purpose |
|--------|---------|
| `projects/` | Active work |
| `archive/` | Dead/completed projects |
| `sandbox/` or `playground/` | Throwaway experiments |
| `tools/` or `scripts/` | Personal utilities |
| `learning/` | Courses, tutorials |
| `config/` or `dotfiles/` | Machine configuration |
| `docs/` | Personal reference docs (rare at this level) |
| `templates/` | Project boilerplates |

---

## 3. Monorepo vs Polyrepo for Personal Workspaces

### The Short Answer
**Polyrepo is the norm for personal workspaces.** Each project gets its own git repo.

### When Monorepo Makes Sense Personally
- Multiple packages that share code (e.g., a shared UI library used by 3 apps)
- A personal "tools" collection where scripts depend on each other
- When you want one CI pipeline for everything

### When Polyrepo Is Better (Most Cases)
- Projects are unrelated (blog, CLI tool, web app)
- Different languages/toolchains per project
- You want clean, independent git histories
- Simpler mental model

### Hybrid Approach (Common)
- Each real project = own repo (polyrepo)
- One monorepo for "dotfiles" (cross-machine config)
- One monorepo for "scripts/tools" (personal automation)
- One repo for "learning" (notes, exercises)

---

## 4. Per-Project Config Files

### The Essential Checklist (Every Project)
```
project-root/
  .git/                 # Git repository
  .gitignore            # Files to exclude from tracking
  .gitattributes        # Line ending normalization, diff drivers, language detection
  .editorconfig         # Editor-agnostic formatting (indent, line endings, trailing whitespace)
  README.md             # What is this, how to run it, how to contribute
  LICENSE               # Legal terms (MIT, ISC, etc.)
```

### Common Additional Files
```
  .prettierrc           # Code formatter config (JS/TS ecosystem)
  .eslintrc.json        # Linter config
  .env.example          # Template for environment variables (never commit .env itself)
  .vscode/              # VS Code workspace settings
    settings.json       # Editor settings for this project
    extensions.json     # Recommended extensions
    launch.json         # Debug configurations
    tasks.json          # Build/run tasks
  .github/              # GitHub-specific
    FUNDING.yml
    workflows/          # CI/CD via GitHub Actions
  Makefile              # Build automation (language-agnostic)
  Dockerfile            # Container definition
  docker-compose.yml    # Multi-container setup
  CHANGELOG.md          # Version history
  CONTRIBUTING.md       # Contribution guidelines (open source)
```

### What .editorconfig Looks Like
```ini
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

### What .gitattributes Does
```
# Normalize line endings
* text=auto

# Force LF for these
*.js    text eol=lf
*.ts    text eol=lf
*.json  text eol=lf
*.md    text eol=lf
*.yml   text eol=lf
*.sh    text eol=lf

# Binary files
*.png   binary
*.jpg   binary
*.ico   binary
*.woff  binary
*.woff2 binary
```

### Key Principle
`.editorconfig` = how your editor behaves while typing
`.prettierrc` = how your formatter rewrites code on save
`.gitattributes` = how git handles files on commit/checkout
These three work together to guarantee consistent formatting regardless of OS or editor.

---

## 5. Dotfiles Repos — What They Are and Why

### Concept
A "dotfiles repo" is a git repository that tracks your personal configuration files (files starting with `.` in Unix). It lets you:
- Version-control your setup
- Restore your environment on a new machine in minutes
- Share configs between machines (laptop, desktop, VPS)

### What Goes In a Dotfiles Repo

**Shell:**
- `.bashrc`, `.bash_profile`, `.zshrc`, `.zshenv`
- `.aliases` (custom command shortcuts)
- Starship config (`~/.config/starship.toml`)

**Git:**
- `.gitconfig` (user, aliases, default branch, diff tool)
- `.gitignore_global` (system-wide ignores: .DS_Store, Thumbs.db, .env)

**Editor:**
- `.vimrc` or `~/.config/nvim/init.lua`
- VS Code `settings.json`, `keybindings.json`, `snippets/`

**Terminal:**
- `.tmux.conf`
- Windows Terminal `settings.json`
- Alacritty/Ghostty/WezTerm config

**Tools:**
- `.npmrc`, `.yarnrc`
- `.pythonrc`, `.inputrc`
- `.curlrc`, `.wgetrc`
- SSH config (`~/.ssh/config` — NOT keys!)

**Scripts:**
- `install.sh` or `bootstrap.sh` — automates setup on new machine
- `Makefile` — alternative to install script

### What Does NOT Go in Dotfiles
- SSH private keys
- API tokens, passwords, secrets
- `.env` files with credentials
- Anything machine-specific that can't be templated

### Three Management Approaches

**1. Bare Git Repo (simplest, no dependencies)**
```bash
git init --bare $HOME/.dotfiles
alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
# Then: dotfiles add ~/.zshrc && dotfiles commit -m "add zshrc"
```
Files stay at their real paths. No symlinks needed.

**2. GNU Stow (symlink manager)**
```
~/dotfiles/
  zsh/
    .zshrc
  git/
    .gitconfig
    .gitignore_global
  nvim/
    .config/nvim/init.lua
```
Run `stow zsh` from ~/dotfiles/ and it symlinks `.zshrc` into `$HOME`.
Advantage: modular — stow only what you need per machine.

**3. Chezmoi (full-featured, templating, encryption)**
```bash
chezmoi init
chezmoi add ~/.zshrc
chezmoi edit ~/.zshrc
chezmoi apply
```
Advantage: templates for machine-specific config, encrypted secrets support.
Disadvantage: another tool to learn.

### Recommended for Beginners
Start with **bare git repo** or **GNU Stow**. They require no extra tools and teach you what's actually happening. Move to chezmoi later if you need templating across many machines.

---

## 6. VS Code Workspace Files

### What They Are
A `.code-workspace` file is a JSON file that tells VS Code which folders to open together, with what settings, and which extensions to recommend.

### Single-Folder Workspace
When you open a folder in VS Code, it creates an implicit workspace. Settings go in `.vscode/settings.json` inside that folder.

### Multi-Root Workspace
A `.code-workspace` file lets you combine multiple unrelated folders into one window.

```jsonc
// my-workspace.code-workspace
{
  "folders": [
    { "path": "./frontend" },
    { "path": "./backend" },
    { "path": "./shared-lib" }
  ],
  "settings": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "files.exclude": {
      "**/node_modules": true,
      "**/.git": true
    }
  },
  "extensions": {
    "recommendations": [
      "esbenp.prettier-vscode",
      "dbaeumer.vscode-eslint",
      "eamodio.gitlens"
    ]
  }
}
```

### Settings Priority (lowest to highest)
1. **User settings** — global, applies everywhere (`settings.json` in user profile)
2. **Workspace settings** — defined in `.code-workspace` file
3. **Folder settings** — `.vscode/settings.json` inside each folder

### Best Practices
- Store `.code-workspace` files in the project root if it's a monorepo
- For a personal "all projects" workspace, store it in `~/dev/` or `~/dev/config/`
- Use `extensions.recommendations` so collaborators get prompted to install needed extensions
- Use folder-level `.vscode/settings.json` for project-specific overrides
- Don't commit personal preferences (font size, theme) — only project-relevant settings

### What Goes in .vscode/ (Per Project)
| File | Purpose | Commit? |
|------|---------|---------|
| `settings.json` | Project-specific editor settings | Yes (project settings only) |
| `extensions.json` | Recommended extensions | Yes |
| `launch.json` | Debug configurations | Yes |
| `tasks.json` | Build/run tasks | Yes |
| `*.code-snippets` | Project-specific snippets | Yes |

---

## 7. MCP/Skills for Project Scaffolding

Found on mcpmarket.com:
- **Go CLI Builder** — scaffolds Go CLI apps with Makefile, GitHub Actions
- **NestJS Project Scaffold** — scaffolds NestJS backends with production-ready folder layout
- **Payload CMS** — scaffolds Payload CMS projects

These are language/framework-specific. No general "project structure" MCP server exists yet. The universal approach remains: templates in a `~/dev/templates/` folder or use `git init` + copy your standard files.

---

## Summary: What Real Developers Actually Do

1. **One root folder** (`~/dev/` or `~/code/`) with flat sub-organization
2. **Polyrepo** for unrelated projects, monorepo only when sharing code
3. **Every project** gets `.gitignore`, `.editorconfig`, `.gitattributes`, `README.md`
4. **Dotfiles** tracked in a separate repo, managed with bare git, stow, or chezmoi
5. **VS Code workspace** files for multi-folder projects; `.vscode/` folder for per-project settings
6. **Archive, don't delete** — old projects go to `archive/`
7. **Consistency over cleverness** — pick a convention and stick to it

---

## Sources

- [My Development Folder Structure — DEV Community](https://dev.to/jmorjsm/my-development-folder-structure-3e5n)
- [My Development Directory Structure — DEV Community](https://dev.to/httpjunkie/my-development-directory-structure-3p1g)
- [How I Organize My Local Development Environment — Boot.dev](https://blog.boot.dev/misc/how-i-organize-my-local-development-environment/)
- [How Do You Organize Development Projects? — DEV Community](https://dev.to/andrewmcodes/how-do-you-organize-development-projects-on-your-computer-4dja)
- [Ask HN: How Do You Organise Your Hard Drive? — Hacker News](https://news.ycombinator.com/item?id=18836472)
- [Ask HN: How Do You Organise Your Files and Folders? — Hacker News](https://news.ycombinator.com/item?id=23404900)
- [The Ultimate Guide to Mastering Dotfiles — Daytona](https://www.daytona.io/dotfiles/ultimate-guide-to-dotfiles)
- [Dotfiles: Bare Git Repository — Atlassian](https://www.atlassian.com/git/tutorials/dotfiles)
- [Dotfiles — MIT Missing Semester](https://missing.csail.mit.edu/2019/dotfiles/)
- [Dotfiles Inspiration — dotfiles.github.io](https://dotfiles.github.io/inspiration/)
- [awesome-dotfiles — GitHub](https://github.com/webpro/awesome-dotfiles)
- [thoughtbot/dotfiles — GitHub](https://github.com/thoughtbot/dotfiles)
- [Managing Dotfiles with GNU Stow — DEV Community](https://dev.to/luxcih/dotfiles-managing-with-gnu-stow-and-git-5100)
- [Managing Dotfiles with Chezmoi — Jerry Ng](https://jerrynsh.com/how-to-manage-dotfiles-with-chezmoi/)
- [EditorConfig — editorconfig.org](https://editorconfig.org/)
- [Git's Magic Files — Andrew Nesbitt](https://nesbitt.io/2026/02/05/git-magic-files.html)
- [Preventing Mistranslations with Git Repos — dudley.codes](https://www.dudley.codes/posts/2020.02.16-git-lost-in-translation/)
- [VS Code Workspaces — Official Docs](https://code.visualstudio.com/docs/editing/workspaces/workspaces)
- [VS Code Multi-Root Workspaces — Official Docs](https://code.visualstudio.com/docs/editing/workspaces/multi-root-workspaces)
- [VS Code Multi-Root Workspaces Tips — ISE Developer Blog](https://devblogs.microsoft.com/ise/multi_root_workspaces_in_visual_studio_code/)
- [Recommended Extensions in VS Code — Leonardo Faria](https://leonardofaria.net/2023/02/10/using-recommended-extensions-and-settings-in-vs-code)
- [Monorepo vs Polyrepo — DEV Community](https://dev.to/bitdev_/monorepo-vs-polyrepo-j9)
- [Monorepo vs Polyrepo 2025 — DEV Community](https://dev.to/md-afsar-mahmud/monorepo-vs-polyrepo-which-one-should-you-choose-in-2025-g77)
- [Go CLI Builder — mcpmarket.com](https://mcpmarket.com/tools/skills/go-cli-builder)
- [NestJS Project Scaffold — mcpmarket.com](https://mcpmarket.com/tools/skills/nestjs-project-scaffold)
