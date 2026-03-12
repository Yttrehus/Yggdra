// Chatlog Engine — parses Claude Code session JSONL into two documents:
//   live.md    — today's conversation (continuously updated)
//   archive.md — past dates with index + date sections (with sub-index per time block)
//
// Usage:
//   node chatlog-engine.js              — full rebuild from all sessions
//   node chatlog-engine.js --watch      — watch mode (future)
//
// Timestamps: Danish time (Europe/Copenhagen)

const fs = require('fs');
const path = require('path');

const PROJECT_DIR = 'c:/Users/Krist/.claude/projects/c--Users-Krist-dev-projects-Basic-Setup';
const OUTPUT_DIR = path.join(__dirname);
const TIMEZONE = 'Europe/Copenhagen';

// --- Time helpers ---

function toDanish(utcTimestamp) {
  const d = new Date(utcTimestamp);
  const parts = new Intl.DateTimeFormat('sv-SE', {
    timeZone: TIMEZONE,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false,
  }).formatToParts(d);

  const get = (type) => parts.find(p => p.type === type)?.value || '??';
  return {
    date: `${get('year')}-${get('month')}-${get('day')}`,
    time: `${get('hour')}:${get('minute')}`,
    hour: parseInt(get('hour'), 10),
  };
}

function danishNow() {
  return toDanish(new Date().toISOString());
}

// --- Parse all sessions ---

function parseSessionFiles() {
  const files = fs.readdirSync(PROJECT_DIR)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => path.join(PROJECT_DIR, f));

  if (files.length === 0) {
    console.error('No session files found.');
    process.exit(1);
  }

  console.log(`Reading ${files.length} session file(s)...`);
  const messages = [];

  for (const file of files) {
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
        content = content.trim();
        if (!content) continue;

        // Skip system noise
        if (content.startsWith('<system-reminder>')) continue;
        if (content.startsWith('<ide_')) continue;
        if (content.startsWith('<local-command')) continue;
        if (content.startsWith('<command-name>')) continue;

        const danish = toDanish(entry.timestamp || '1970-01-01T00:00:00Z');

        messages.push({
          timestamp: entry.timestamp || '1970-01-01T00:00:00',
          date: danish.date,
          time: danish.time,
          hour: danish.hour,
          role,
          content,
          sessionId,
        });
      } catch (e) {}
    }
  }

  messages.sort((a, b) => a.timestamp.localeCompare(b.timestamp));
  return messages;
}

// --- Format a message ---

function formatMessage(msg) {
  const prefix = msg.role === 'user' ? 'YTTRE' : 'CLAUDE';
  let content = msg.content;
  if (content.length > 5000) content = content.substring(0, 5000) + '\n...[truncated]';
  return `### ${prefix} — ${msg.time}\n\n${content}\n`;
}

// --- Time block label (2-hour blocks) ---

function timeBlockLabel(hour) {
  const start = Math.floor(hour / 2) * 2;
  const end = start + 2;
  const pad = (n) => String(n).padStart(2, '0');
  return `${pad(start)}:00–${pad(end)}:00`;
}

function timeBlockAnchor(date, hour) {
  const start = Math.floor(hour / 2) * 2;
  return `${date}-${String(start).padStart(2, '0')}`;
}

// --- Keyword extraction ---

function extractKeywords(messages, max = 5) {
  const userTexts = messages
    .filter(m => m.role === 'user')
    .map(m => m.content.toLowerCase())
    .join(' ');

  const stopwords = new Set([
    'det', 'er', 'en', 'et', 'den', 'de', 'og', 'i', 'på', 'med', 'til',
    'for', 'af', 'at', 'vi', 'jeg', 'du', 'der', 'som', 'har', 'kan',
    'vil', 'skal', 'var', 'fra', 'om', 'ikke', 'men', 'hvad', 'så',
    'bare', 'godt', 'okay', 'ja', 'nej', 'done', 'her', 'nu', 'lige',
    'the', 'is', 'a', 'to', 'and', 'of', 'in', 'for', 'it', 'that',
    'this', 'be', 'was', 'are', 'have', 'has', 'had', 'do', 'does',
    'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'been', 'being', 'having', 'doing', 'if', 'or', 'an', 'my',
    'your', 'we', 'they', 'them', 'our', 'its', 'his', 'her',
    'også', 'lad', 'mig', 'dig', 'sig', 'sin', 'sit', 'sine',
    'hele', 'alle', 'alt', 'noget', 'nogen', 'meget', 'mere',
    'efter', 'over', 'under', 'ved', 'mod', 'hos', 'mellem',
    'når', 'hvordan', 'hvor', 'burde', 'bliver', 'blev', 'ville',
    'gør', 'gerne', 'fordi', 'helt', 'lidt', 'før', 'siden',
    'igen', 'need', 'want', 'just', 'like', 'get', 'one', 'use',
    'know', 'see', 'new', 'now', 'way', 'out', 'how', 'what',
    'think', 'make', 'good', 'well', 'back', 'then', 'than',
  ]);

  const words = userTexts
    .replace(/[^a-zæøå0-9\s-]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 2 && !stopwords.has(w));

  const freq = {};
  for (const w of words) {
    freq[w] = (freq[w] || 0) + 1;
  }

  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, max)
    .map(([w]) => w)
    .join(', ');
}

// --- Generate live.md (today only) ---

function generateLive(messages, today) {
  const todayMsgs = messages.filter(m => m.date === today);
  if (todayMsgs.length === 0) return null;

  const sessions = [...new Set(todayMsgs.map(m => m.sessionId))];
  const now = danishNow();
  let md = `# Chatlog — ${today} (live)\n\n`;
  md += `**Sessions:** ${sessions.join(', ')}  \n`;
  md += `**Beskeder:** ${todayMsgs.length}  \n`;
  md += `**Sidst opdateret:** ${now.time}\n\n---\n\n`;

  for (const msg of todayMsgs) {
    md += formatMessage(msg) + '\n---\n\n';
  }

  return md;
}

// --- Generate archive.md (past dates with index + sub-index) ---

function generateArchive(messages, today) {
  const pastMsgs = messages.filter(m => m.date !== today);
  if (pastMsgs.length === 0) return null;

  // Group by date
  const byDate = {};
  for (const msg of pastMsgs) {
    if (!byDate[msg.date]) byDate[msg.date] = [];
    byDate[msg.date].push(msg);
  }

  const dates = Object.keys(byDate).sort(); // chronological: oldest first

  // --- Main index ---
  let md = `# Chatlog Archive — Basic Setup\n\n`;
  md += `## Index\n\n`;
  md += `| Dato | Beskeder | Nøgleord |\n`;
  md += `|------|----------|----------|\n`;

  for (const date of dates) {
    const msgs = byDate[date];
    const keywords = extractKeywords(msgs);
    md += `| [${date}](#${date}) | ${msgs.length} | ${keywords} |\n`;
  }

  md += `\n---\n\n`;

  // --- Date sections with sub-index ---
  for (const date of dates) {
    const msgs = byDate[date];
    const sessions = [...new Set(msgs.map(m => m.sessionId))];

    md += `## ${date}\n\n`;
    md += `**Sessions:** ${sessions.join(', ')} · **${msgs.length} beskeder**\n\n`;

    // Group by 2-hour blocks
    const byBlock = {};
    for (const msg of msgs) {
      const block = timeBlockLabel(msg.hour);
      if (!byBlock[block]) byBlock[block] = [];
      byBlock[block].push(msg);
    }

    // Sub-index table
    const blocks = Object.keys(byBlock).sort();
    md += `| Tidsrum | Beskeder | Nøgleord |\n`;
    md += `|---------|----------|----------|\n`;
    for (const block of blocks) {
      const blockMsgs = byBlock[block];
      const anchor = timeBlockAnchor(date, blockMsgs[0].hour);
      const keywords = extractKeywords(blockMsgs, 4);
      md += `| [${block}](#${anchor}) | ${blockMsgs.length} | ${keywords} |\n`;
    }
    md += `\n`;

    // Messages grouped by time block
    for (const block of blocks) {
      const blockMsgs = byBlock[block];
      const anchor = timeBlockAnchor(date, blockMsgs[0].hour);
      md += `### ${block} <a id="${anchor}"></a>\n\n`;

      for (const msg of blockMsgs) {
        const prefix = msg.role === 'user' ? 'YTTRE' : 'CLAUDE';
        let content = msg.content;
        if (content.length > 5000) content = content.substring(0, 5000) + '\n...[truncated]';
        md += `#### ${prefix} — ${msg.time}\n\n${content}\n\n---\n\n`;
      }
    }
  }

  return md;
}

// --- Main ---

const now = danishNow();
console.log(`Today (Danish): ${now.date} ${now.time}`);

const messages = parseSessionFiles();
console.log(`Parsed ${messages.length} messages total.`);

const live = generateLive(messages, now.date);
if (live) {
  fs.writeFileSync(path.join(OUTPUT_DIR, 'live.md'), live);
  console.log(`live.md: ${messages.filter(m => m.date === now.date).length} messages`);
} else {
  console.log('No messages for today.');
}

const archive = generateArchive(messages, now.date);
if (archive) {
  fs.writeFileSync(path.join(OUTPUT_DIR, 'archive.md'), archive);
  const pastCount = messages.filter(m => m.date !== now.date).length;
  console.log(`archive.md: ${pastCount} messages`);
} else {
  console.log('No past messages to archive.');
}

console.log('Done.');
