// Dump Claude Code session JSONL → readable markdown, grouped by date
// Usage: node dump-chatlog.js [session-id]
// Without args: reads ALL session files
// Output: one chatlog-YYYY-MM-DD.md per date, messages merged chronologically

const fs = require('fs');
const path = require('path');

const PROJECT_DIR = 'c:/Users/Krist/.claude/projects/c--Users-Krist-dev-projects-Basic-Setup';
const OUTPUT_DIR = 'c:/Users/Krist/dev/projects/Basic Setup/chatlogs';

// Collect session files
let sessionFiles = [];
const arg = process.argv[2];

if (arg) {
  const exact = path.join(PROJECT_DIR, arg);
  if (fs.existsSync(exact)) {
    sessionFiles.push(exact);
  } else {
    const match = fs.readdirSync(PROJECT_DIR)
      .filter(f => f.endsWith('.jsonl') && f.includes(arg));
    sessionFiles = match.map(f => path.join(PROJECT_DIR, f));
  }
} else {
  // All JSONL files
  sessionFiles = fs.readdirSync(PROJECT_DIR)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => path.join(PROJECT_DIR, f));
}

if (sessionFiles.length === 0) {
  console.error('No session files found.');
  process.exit(1);
}

console.log(`Reading ${sessionFiles.length} session file(s)...`);

// Parse all messages from all sessions, tag with session ID
const allMessages = [];

for (const file of sessionFiles) {
  const sessionId = path.basename(file, '.jsonl').substring(0, 8);
  const lines = fs.readFileSync(file, 'utf8').split('\n').filter(l => l.trim());

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const msg = entry.message || {};
      const role = msg.role;
      if (role !== 'user' && role !== 'assistant') continue;

      let content = msg.content || '';
      if (Array.isArray(content)) {
        content = content.filter(b => b.type === 'text').map(b => b.text).join('\n');
      }
      if (!content.trim()) continue;
      if (content.startsWith('<system-reminder>')) continue;
      if (content.startsWith('<ide_')) continue;
      if (content.startsWith('<local-command')) continue;
      if (content.startsWith('<command-name>')) continue;

      allMessages.push({
        timestamp: entry.timestamp || '1970-01-01T00:00:00',
        date: (entry.timestamp || '1970-01-01').substring(0, 10),
        time: (entry.timestamp || 'T??:??:??').substring(11, 19),
        role,
        content: content.trim(),
        sessionId,
      });
    } catch(e) {}
  }
}

// Sort all messages chronologically
allMessages.sort((a, b) => a.timestamp.localeCompare(b.timestamp));

// Group by date
const byDate = {};
for (const msg of allMessages) {
  if (!byDate[msg.date]) byDate[msg.date] = [];
  byDate[msg.date].push(msg);
}

// Write one file per date
const dates = Object.keys(byDate).sort();
for (const date of dates) {
  const msgs = byDate[date];
  let md = `# Chatlog — ${date}\n\n`;

  // List sessions that contributed to this date
  const sessions = [...new Set(msgs.map(m => m.sessionId))];
  md += `**Sessions:** ${sessions.join(', ')}\n\n---\n\n`;

  let seq = 0;
  for (const msg of msgs) {
    seq++;
    const seqId = 'T' + String(seq).padStart(3, '0');
    const prefix = msg.role === 'user' ? 'YTTRE' : 'CLAUDE';
    let content = msg.content;
    if (content.length > 5000) content = content.substring(0, 5000) + '\n...[truncated]';

    md += `## ${seqId} [${prefix}] ${msg.time} (${msg.sessionId})\n\n`;
    md += content + '\n\n---\n\n';
  }

  const outFile = path.join(OUTPUT_DIR, `chatlog-${date}.md`);
  fs.writeFileSync(outFile, md);
  console.log(`${date}: ${seq} messages → ${path.basename(outFile)}`);
}

console.log(`Done: ${allMessages.length} total messages across ${dates.length} date(s)`);
