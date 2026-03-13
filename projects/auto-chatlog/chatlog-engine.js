// Chatlog Engine v2 — parses Claude Code session JSONL into one document:
//   chatlog.md — all sessions with main index + session chapters + time blocks
//
// Output location: repo root (state file alongside CONTEXT.md)
//
// Usage:
//   node projects/auto-chatlog/chatlog-engine.js
//
// Timestamps: Danish time (Europe/Copenhagen)

const fs = require("fs");
const path = require("path");

const PROJECT_DIR =
  "c:/Users/Krist/.claude/projects/c--Users-Krist-dev-projects-Basic-Setup";
const OUTPUT_FILE = path.resolve(__dirname, "../../chatlog.md");
const TIMEZONE = "Europe/Copenhagen";

// --- Time helpers ---

function toDanish(utcTimestamp) {
  const d = new Date(utcTimestamp);
  const parts = new Intl.DateTimeFormat("sv-SE", {
    timeZone: TIMEZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(d);

  const get = (type) => parts.find((p) => p.type === type)?.value || "??";
  return {
    date: `${get("year")}-${get("month")}-${get("day")}`,
    time: `${get("hour")}:${get("minute")}`,
    hour: parseInt(get("hour"), 10),
  };
}

function danishNow() {
  return toDanish(new Date().toISOString());
}

// --- Parse all sessions ---

function parseSessionFiles() {
  const files = fs
    .readdirSync(PROJECT_DIR)
    .filter((f) => f.endsWith(".jsonl"))
    .map((f) => path.join(PROJECT_DIR, f));

  if (files.length === 0) {
    console.error("No session files found.");
    process.exit(1);
  }

  console.log(`Reading ${files.length} session file(s)...`);
  const messages = [];

  for (const file of files) {
    const sessionId = path.basename(file, ".jsonl").substring(0, 8);
    const lines = fs
      .readFileSync(file, "utf8")
      .split("\n")
      .filter((l) => l.trim());

    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        const msg = entry.message || {};
        const role = msg.role;
        if (role !== "user" && role !== "assistant") continue;

        let content = msg.content || "";
        if (Array.isArray(content)) {
          content = content
            .filter((b) => b.type === "text")
            .map((b) => b.text)
            .join("\n");
        }
        content = content.trim();
        if (!content) continue;

        // Skip system noise
        if (content.startsWith("<system-reminder>")) continue;
        if (content.startsWith("<ide_")) continue;
        if (content.startsWith("<local-command")) continue;
        if (content.startsWith("<command-name>")) continue;

        const danish = toDanish(
          entry.timestamp || "1970-01-01T00:00:00Z",
        );

        messages.push({
          timestamp: entry.timestamp || "1970-01-01T00:00:00",
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

// --- Keyword extraction ---

function extractKeywords(messages, max = 5) {
  const userTexts = messages
    .filter((m) => m.role === "user")
    .map((m) => m.content.toLowerCase())
    .join(" ");

  const stopwords = new Set([
    "det",
    "er",
    "en",
    "et",
    "den",
    "de",
    "og",
    "i",
    "på",
    "med",
    "til",
    "for",
    "af",
    "at",
    "vi",
    "jeg",
    "du",
    "der",
    "som",
    "har",
    "kan",
    "vil",
    "skal",
    "var",
    "fra",
    "om",
    "ikke",
    "men",
    "hvad",
    "så",
    "bare",
    "godt",
    "okay",
    "ja",
    "nej",
    "done",
    "her",
    "nu",
    "lige",
    "the",
    "is",
    "a",
    "to",
    "and",
    "of",
    "in",
    "for",
    "it",
    "that",
    "this",
    "be",
    "was",
    "are",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "been",
    "being",
    "having",
    "doing",
    "if",
    "or",
    "an",
    "my",
    "your",
    "we",
    "they",
    "them",
    "our",
    "its",
    "his",
    "her",
    "også",
    "lad",
    "mig",
    "dig",
    "sig",
    "sin",
    "sit",
    "sine",
    "hele",
    "alle",
    "alt",
    "noget",
    "nogen",
    "meget",
    "mere",
    "efter",
    "over",
    "under",
    "ved",
    "mod",
    "hos",
    "mellem",
    "når",
    "hvordan",
    "hvor",
    "burde",
    "bliver",
    "blev",
    "ville",
    "gør",
    "gerne",
    "fordi",
    "helt",
    "lidt",
    "før",
    "siden",
    "igen",
    "need",
    "want",
    "just",
    "like",
    "get",
    "one",
    "use",
    "know",
    "see",
    "new",
    "now",
    "way",
    "out",
    "how",
    "what",
    "think",
    "make",
    "good",
    "well",
    "back",
    "then",
    "than",
  ]);

  const words = userTexts
    .replace(/[^a-zæøå0-9\s-]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2 && !stopwords.has(w));

  const freq = {};
  for (const w of words) {
    freq[w] = (freq[w] || 0) + 1;
  }

  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, max)
    .map(([w]) => w)
    .join(", ");
}

// --- Time block helpers ---

function timeBlockLabel(hour) {
  const start = Math.floor(hour / 2) * 2;
  const end = start + 2;
  const pad = (n) => String(n).padStart(2, "0");
  return `${pad(start)}:00–${pad(end)}:00`;
}

function timeBlockAnchor(date, hour) {
  const start = Math.floor(hour / 2) * 2;
  return `${date}-${String(start).padStart(2, "0")}`;
}

// --- Generate chatlog.md ---

function generateChatlog(messages) {
  // Group by date
  const byDate = {};
  for (const msg of messages) {
    if (!byDate[msg.date]) byDate[msg.date] = [];
    byDate[msg.date].push(msg);
  }

  const dates = Object.keys(byDate).sort();
  const now = danishNow();

  // --- Main index ---
  let md = `# Chatlog — Yggdra (Basic Setup)\n\n`;
  md += `**Sidst opdateret:** ${now.date} ${now.time}  \n`;
  md += `**Sessions:** ${dates.length} dage · ${messages.length} beskeder\n\n`;
  md += `## Hovedindeks\n\n`;

  for (const date of dates) {
    const msgs = byDate[date];
    const keywords = extractKeywords(msgs);
    md += `- **[${date}](#${date})** (${msgs.length} beskeder) — ${keywords}\n`;
  }

  md += `\n---\n\n`;

  // --- Date sections ---
  for (let i = 0; i < dates.length; i++) {
    const date = dates[i];
    const msgs = byDate[date];
    const sessions = [...new Set(msgs.map((m) => m.sessionId))];
    const prevDate = i > 0 ? dates[i - 1] : null;
    const nextDate = i < dates.length - 1 ? dates[i + 1] : null;

    // Session header with navigation
    md += `## ${date}\n\n`;

    // Navigation links
    const navParts = [];
    if (prevDate) navParts.push(`[← ${prevDate}](#${prevDate})`);
    navParts.push(`[Hovedindeks](#hovedindeks)`);
    if (nextDate) navParts.push(`[${nextDate} →](#${nextDate})`);
    md += navParts.join(" | ") + "\n\n";

    md += `**Sessions:** ${sessions.join(", ")} · **${msgs.length} beskeder**\n\n`;

    // Group by 2-hour blocks
    const byBlock = {};
    for (const msg of msgs) {
      const block = timeBlockLabel(msg.hour);
      if (!byBlock[block]) byBlock[block] = [];
      byBlock[block].push(msg);
    }

    const blocks = Object.keys(byBlock).sort();

    // Sub-index
    md += `### Indeks\n\n`;
    for (const block of blocks) {
      const blockMsgs = byBlock[block];
      const anchor = timeBlockAnchor(date, blockMsgs[0].hour);
      const keywords = extractKeywords(blockMsgs, 4);
      md += `- [${block}](#${anchor}) (${blockMsgs.length} beskeder) — ${keywords}\n`;
    }
    md += `\n`;

    // Messages grouped by time block
    for (const block of blocks) {
      const blockMsgs = byBlock[block];
      const anchor = timeBlockAnchor(date, blockMsgs[0].hour);
      md += `### ${block} <a id="${anchor}"></a>\n\n`;
      md += `[Hovedindeks](#hovedindeks) | [${date}](#${date})\n\n`;

      for (const msg of blockMsgs) {
        const prefix = msg.role === "user" ? "YTTRE" : "CLAUDE";
        let content = msg.content;
        if (content.length > 5000)
          content = content.substring(0, 5000) + "\n...[truncated]";
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

const chatlog = generateChatlog(messages);
fs.writeFileSync(OUTPUT_FILE, chatlog);
console.log(`chatlog.md: ${messages.length} messages → ${OUTPUT_FILE}`);

console.log("Done.");
