# Skill: checkpoint

Session-checkpoint. Se `projects/auto-chatlog/CONTEXT.md` for fuld dokumentation.

## Trigger
`/checkpoint` eller ved milestone/pause/vigtig beslutning.

## Trin
1. Opdatér CONTEXT.md + PROGRESS.md + relevante projekt-CONTEXT.md
2. Kør chatlog-engine `--digest` → spawn subagent (abstracts) → kør chatlog-engine
3. Git commit + push
4. Bekræft kort
