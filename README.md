# Raymond 的个人网站

## 文件结构
- index.html          主页（About / Research / Publications / CV / Notebook / 最新读书笔记）
- reading.html        读书笔记页
- assets/style.css    全站共用样式（颜色、字体、导航）
- assets/notes.js     读书笔记的共用脚本
- reading/notes.json  笔记目录（标题、日期、书名等）
- reading/notes/*.md  每篇笔记的正文（Markdown）
- images/             放照片
- cv.pdf              你的简历（自己放进来）
- new_note.py         新建笔记的小脚本

## 每天写笔记
    python3 new_note.py
    # 编辑生成的 reading/notes/日期-xxx.md
    git add . && git commit -m "notes" && git push

## 本地预览
    python3 -m http.server
    # 打开 http://localhost:8000
