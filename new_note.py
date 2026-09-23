#!/usr/bin/env python3
"""新建一篇读书笔记：python3 new_note.py
会在 reading/notes/ 下生成 Markdown 文件，并自动登记到 reading/notes.json。
"""
import json, re, datetime, pathlib, subprocess, os, sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "reading" / "notes.json"
NOTES = ROOT / "reading" / "notes"


def ask(prompt, default=""):
    hint = f"（回车默认：{default}）" if default else ""
    return input(f"{prompt}{hint}：").strip() or default


def main():
    notes = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else []
    last = notes[0] if notes else {}

    date = ask("日期", datetime.date.today().isoformat())
    book = ask("书名", last.get("book", ""))
    author = ask("作者", last.get("author", "") if book == last.get("book") else "")
    title = ask("这篇笔记的标题")
    progress = ask("读到哪里（章节/页码，可留空）")
    tags = [t for t in re.split(r"[,，\s]+", ask("标签（用逗号分隔，可留空）")) if t]
    excerpt = ask("一句话摘要（显示在列表里，可留空）")
    slug = ask("文件名里的英文短名（如 walden-ch2）", "note")
    slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-") or "note"

    note_id = f"{date}-{slug}"
    n = 2
    while any(x["id"] == note_id for x in notes):
        note_id = f"{date}-{slug}-{n}"; n += 1

    NOTES.mkdir(parents=True, exist_ok=True)
    md = NOTES / f"{note_id}.md"
    md.write_text("> 摘录的句子写在这里\n\n在这里写你的想法。\n\n## 小标题\n\n- 要点一\n- 要点二\n", encoding="utf-8")

    notes.append({"id": note_id, "date": date, "book": book, "author": author, "title": title,
                  "progress": progress, "tags": tags, "excerpt": excerpt})
    notes.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    INDEX.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n已创建 {md.relative_to(ROOT)}，并登记到 notes.json。")
    editor = os.environ.get("EDITOR")
    if editor:
        subprocess.call([editor, str(md)])
    elif sys.platform == "darwin":
        subprocess.call(["open", str(md)])


if __name__ == "__main__":
    main()
