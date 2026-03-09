# Infrastructure

## Architecture
- **PC (Yggdra):** WSL2 Ubuntu, Claude Code, Python venv
- **VPS (Ydrasil):** 72.62.61.51, Ubuntu, Docker
  - Qdrant: port 6333 (internal)
  - Webapp: port 3000 (nginx → public)
  - Mock API: port 3001
  - SecondBrain API: port 3002

## SSH
```bash
ssh vps                              # Quick connect (alias in ~/.ssh/config)
tunnel start                         # Qdrant tunnel (localhost:6333)
tunnel status                        # Check tunnel
tunnel stop                          # Kill tunnel
```

## VPS Services
```bash
ssh vps "docker ps"                  # Running containers
ssh vps "systemctl status qdrant"    # Qdrant service
ssh vps "curl -s localhost:6333/collections | jq '.result.collections[].name'"
```

## Key Paths (VPS)
- `/root/Ydrasil/app/` — webapp (production, volume-mounted)
- `/root/Ydrasil/scripts/` — automation scripts
- `/root/Ydrasil/data/` — route data, credentials
- Qdrant data: `/var/lib/qdrant/`

## Backups
- Daily 04:00 UTC via cron
- Hostinger VPS snapshots
- Qdrant snapshots: `ssh vps "curl -X POST localhost:6333/snapshots"`
