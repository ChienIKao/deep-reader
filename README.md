# Deep Reader｜英文閱讀夥伴

把英文論文、文章、小說（PDF／網址／貼上的文字）變成**可以直接用瀏覽器打開的學習頁面**：中英對照翻譯，以及英文的重點批註與邏輯梳理。
遵循 [Agent Skills 開放標準](https://agentskills.io)，同一份 skill 可用於 **Claude**（網頁／桌面／Claude Code）、**ChatGPT**、**Codex**，以及 Gemini CLI、Cursor、GitHub Copilot 等支援 `SKILL.md` 的工具。

## 三種模式

| 模式 | 你可以這樣說 | 產出 | 範例 |
|---|---|---|---|
| **① 中英對照翻譯** | 「把這篇翻成中文，中英對照」 | 左英文原文／右中文譯文，逐段對齊；可切換雙語／只看英文／只看中文、調整字級；附術語對照表 | [預覽](https://htmlpreview.github.io/?https://github.com/ChienIKao/deep-reader/blob/main/examples/civil-disobedience-translate.html) · [原始檔](examples/civil-disobedience-translate.html) |
| **② 重點批註** | 「幫我做重點批註，這是 worksheet 題目：…」 | 頂部導航＋題號顏色圖例；左欄原文依題號彩色高亮；右欄逐段英文批註（Function／Reasoning／回答哪題的哪個層次）；底部 Worksheet 答題索引（Core Argument＋Key Evidence＋Counterpoints & Limits） | [預覽](https://htmlpreview.github.io/?https://github.com/ChienIKao/deep-reader/blob/main/examples/civil-disobedience-annotate.html) · [原始檔](examples/civil-disobedience-annotate.html) |
| **③ 邏輯梳理** | 「幫我梳理這篇的論證邏輯」 | 核心主張、可收合的論證地圖（主張／理由／證據／隱含前提／反駁）、推進脈絡、Toulmin 拆解、論證檢驗（證據強度、謬誤風險、最強反駁）、關鍵概念、自我檢測 | [預覽](https://htmlpreview.github.io/?https://github.com/ChienIKao/deep-reader/blob/main/examples/civil-disobedience-logic.html) · [原始檔](examples/civil-disobedience-logic.html) |

範例使用梭羅《公民不服從》（1849，公有領域）開篇七段。小說等敘事文本在「邏輯梳理」中會自動改用因果鏈、人物動機、敘事結構等分析框架。

輸出的 HTML 是單一檔案、不依賴網路，支援深色模式、手機閱讀與列印。

## 安裝

先到 [Releases](https://github.com/ChienIKao/deep-reader/releases/latest) 下載 `deep-reader.zip`（或自行執行 `python scripts/package.py` 產生）。

### Claude（claude.ai 網頁／桌面／手機）
1. 確認已開啟「程式碼執行與檔案建立」功能。
2. 到 **Settings → Capabilities → Skills**（介面名稱可能隨版本略有不同），上傳 `deep-reader.zip`。
3. 之後直接丟 PDF 或網址給 Claude，說「翻譯成中英對照」即可自動觸發。

### Claude Code
```bash
npx skills add ChienIKao/deep-reader -a claude-code -g
```
或手動把 `skills/deep-reader/` 複製到 `~/.claude/skills/deep-reader/`。

### ChatGPT
**方式 A：Skills**（若你的 ChatGPT 側邊欄已有 Skills）— 新增自訂技能並匯入 `deep-reader.zip`。

**方式 B：自訂 GPT（所有付費方案皆可用，最通用）**
1. ChatGPT → Explore GPTs → Create → Configure。
2. **Instructions**：貼上 [`chatgpt/instructions.md`](chatgpt/instructions.md) 的全部內容。
3. **Knowledge**：上傳以下 7 個檔案
   - `skills/deep-reader/references/` 裡的 `input.md`、`mode-translate.md`、`mode-annotate.md`、`mode-logic.md`
   - `skills/deep-reader/assets/` 裡的 `translate.html`、`annotate.html`、`logic.html`
4. **Capabilities**：勾選 Web Search 與 Code Interpreter & Data Analysis（用來抓網頁、讀 PDF、產生可下載的 HTML 檔）。

**方式 C：Projects** — 建立專案，把同一份 instructions 貼進專案指示，並上傳同樣 7 個檔案。

### Codex CLI 與其他工具
```bash
npx skills add ChienIKao/deep-reader -a codex -g
```
Codex 也可手動複製到 `~/.agents/skills/deep-reader/`。Gemini CLI、Cursor、GitHub Copilot 等工具將 `-a` 換成對應名稱即可（見 [skills CLI](https://github.com/vercel-labs/skills)）。

## 使用範例

```
（上傳 paper.pdf）幫我翻成中英對照
```
```
https://example.com/article 幫我梳理這篇文章的論證邏輯
```
```
（上傳 reading.pdf）幫我做重點批註。
課程：社會學理論 Week 3
Q1 What is the author's main argument about modernity?
Q2 What evidence does the author use?
Q3 How does this reading relate to Weber?
```
```
（上傳 novel-chapter.pdf）三種都要
```

沒給題目時，批註模式會自動擬 4–6 題導讀題並標示「AI-drafted」。

**輸出語言：**只有譯文是中文（預設繁體中文、台灣用語；用簡體提問會改為簡體）。其他部分——頁面介面、重點批註、答題索引、邏輯梳理——都用英文輸出。想改成其他語言，修改 `SKILL.md` 的〈輸出語言〉一節。

## 專案結構

```
skills/deep-reader/          ← skill 本體（Agent Skills 格式）
├── SKILL.md                 ← 觸發條件與總流程
├── references/              ← 各模式的詳細規格（按需載入）
│   ├── input.md             ← PDF／網頁取文與清理
│   ├── mode-translate.md
│   ├── mode-annotate.md
│   └── mode-logic.md
├── assets/                  ← HTML 模板（CSS＋互動 JS，佔位符 {{TITLE}}／{{BODY}}）
│   ├── translate.html
│   ├── annotate.html
│   └── logic.html
└── scripts/
    ├── build_page.py        ← 模板＋內容片段 → 完整 HTML，並檢查標籤是否成對
    └── extract_text.py      ← PDF／網址 → 分段乾淨文字（僅需 Python 標準庫；PDF 需 pymupdf 或 pypdf）
chatgpt/instructions.md      ← ChatGPT 自訂 GPT／Projects 用的精簡指示（< 8000 字元）
examples/                    ← 三種模式的範例輸出
scripts/package.py           ← 打包 dist/deep-reader.zip
```

## 自訂

- **換配色／字體**：修改 `assets/*.html` 的 `:root` CSS 變數。批註模式的題號顏色在 `.q1`–`.q8`。
- **改批註卡欄位或答題結構**：修改 `references/mode-annotate.md`（AI 依規格產出），必要時同步調整模板 CSS。
- 修改後執行 `python scripts/package.py` 重新打包。

## License

[MIT](LICENSE)
