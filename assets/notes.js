/* Shared helpers for the reading notes (used by index.html and reading.html) */
const NOTES_INDEX = 'reading/notes.json';
const NOTES_DIR = 'reading/notes/';
const BOOK_PALETTE = ['#F4A236', '#E8645A', '#5ABFA1', '#6DAEDB', '#B8A9C9', '#F2C4CE', '#3D3B8E', '#E9C46A'];
const WEEKDAY = ['日', '一', '二', '三', '四', '五', '六'];

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
function strHash(str) { let h = 0; for (const ch of str) h = (h * 31 + ch.codePointAt(0)) >>> 0; return h; }
const bookColor = book => BOOK_PALETTE[strHash(book) % BOOK_PALETTE.length];
const parseDate = s => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
const ymd = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

async function loadNotes() {
  const res = await fetch(NOTES_INDEX, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`notes.json: ${res.status}`);
  const notes = await res.json();
  return notes.sort((a, b) => b.date.localeCompare(a.date) || b.id.localeCompare(a.id));
}

function readingStreak(notes) {
  const days = new Set(notes.map(n => n.date));
  const d = new Date();
  if (!days.has(ymd(d))) d.setDate(d.getDate() - 1); // not written yet today doesn't break it
  let n = 0;
  while (days.has(ymd(d))) { n++; d.setDate(d.getDate() - 1); }
  return n;
}

const LOCAL_FILE_HINT = `如果你是直接双击打开的本地文件，浏览器会拦截读取。请在网站根目录运行 <code>python3 -m http.server</code>，再访问 http://localhost:8000`;
