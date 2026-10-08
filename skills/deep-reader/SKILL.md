---
name: deep-reader
description: Deep-reading companion for English papers, articles, and novels. Turns a PDF, URL, or pasted English text into polished standalone HTML study pages — (1) side-by-side English/Chinese bilingual translation, (2) color-coded annotated reading with paragraph-by-paragraph notes and a worksheet answer index, (3) argument/logic map. Only the translation is in Chinese; annotations, answers, the logic map, and all page UI are in English. Use this whenever the user shares an English PDF, link, or long English text and wants it translated into Chinese, summarized, annotated, explained, or its reasoning clarified — e.g. 翻譯這篇論文、中英對照、雙語對照、重點摘要、批註、導讀、讀書報告、worksheet、課堂作業、邏輯梳理、論證結構、幫我讀這篇、看不懂這篇 — even if they never mention HTML or this skill.
license: MIT
metadata:
  version: "1.1.0"
---

# Deep Reader｜英文閱讀夥伴

使用者常丟來英文論文、文章或小說（PDF、網址或直接貼上的文字），需要真正讀懂它。這個 skill 把原文轉成**可以直接在瀏覽器打開的單一 HTML 檔**，提供三種模式：

| 模式 | 觸發說法（範例） | 產出 | 細節規格 |
|---|---|---|---|
| **1. 中英對照翻譯** | 翻譯、中英對照、雙語、全文翻成中文 | 左英文原文／右中文譯文，逐段對齊 | `references/mode-translate.md` |
| **2. 重點批註** | 重點摘要、批註、導讀、worksheet、作業題目、讀書報告 | 左原文（依題號彩色高亮）／右逐段英文批註＋底部答題索引 | `references/mode-annotate.md` |
| **3. 邏輯梳理** | 邏輯、論證、結構、脈絡、看不懂作者在說什麼 | 核心主張、論證地圖、推進脈絡、Toulmin 拆解、論證檢驗 | `references/mode-logic.md` |

使用者可以一次要多個模式（例如「翻譯＋邏輯梳理」），每個模式各產出一個 HTML 檔。

## 工作流程

### 1. 判斷模式
從使用者的話判斷要哪個模式。如果只丟了檔案或連結、沒說要做什麼，用一句話問：「要做 ① 中英對照翻譯、② 重點批註、③ 邏輯梳理，還是全部？」——這比猜錯後產出一份長篇錯誤結果更省使用者的時間。

### 2. 取得完整原文
讀 `references/input.md`，照其中的方法取得並清理原文（PDF 抽字、網頁正文擷取、去除頁首頁尾與斷字）。重點是**拿到完整、分段正確的原文**：三個模式的品質都建立在段落切分上。若 PDF 是掃描圖檔、網頁需要登入或被擋，直接告訴使用者並請他改貼文字，不要憑印象補寫原文。

### 3. 補齊模式需要的資訊
- **模式 2** 需要「題目」和「課程資訊」。使用者若有提供 worksheet／作業題目，照原題使用；若沒有，自行擬 4–6 題能抓住全文骨幹的英文導讀題，並在頁面上標註 `AI-drafted guiding questions`。不要因為缺題目就停下來等。
- 其他模式不需要額外資訊。

### 4. 讀取該模式的規格與模板，然後產出
1. 讀對應的 `references/mode-*.md`（內容規格、品質標準、HTML 結構範例）。
2. 讀對應的 `assets/*.html` 模板。模板已含完整 CSS 與互動 JS，只留兩個佔位符：`{{TITLE}}`（頁面標題）與 `{{BODY}}`（`<body>` 內容）。
3. 依規格寫出 `{{BODY}}` 的 HTML。**只用規格裡定義的 class 名稱**，模板的樣式與互動才會生效。

### 5. 組裝與交付
依你所在環境選一種方式（能寫檔就寫檔）：

- **可執行程式碼**（Claude Code、Codex、Claude.ai / ChatGPT 的程式執行環境）：把 body 寫成一個或多個片段檔，再用腳本組裝：
  ```bash
  python scripts/build_page.py --template translate --title "論文標題" --body part-01.html part-02.html --out paper-translate.html
  ```
  腳本會依序串接片段、填入模板，並檢查結構是否平衡。
- **可寫檔但不能執行程式**：把模板內容複製一份，自行把兩個佔位符換掉後寫檔。
- **純聊天介面**：若平台支援 Artifact／Canvas，放進去；否則輸出一個完整的 ```html 程式碼區塊，請使用者存成 `.html` 後用瀏覽器開啟。

檔名建議：`<短標題>-translate.html`、`<短標題>-annotate.html`、`<短標題>-logic.html`（短標題用英文小寫加連字號）。

交付後在對話中用 3–5 行說明（用使用者對話的語言）：產出了什麼檔案、全文的一句話主旨、以及任何需要使用者注意的事（例如 PDF 某頁抽不到字、題目是 AI 擬定的）。不要在對話裡重貼整份內容。

## 長文處理

一篇 20 頁的論文翻譯後可能超過單次輸出上限。處理原則：

- **翻譯模式必須完整**：不可省略、摘要化或寫「（以下略）」。這是使用者最在意的一點——他們要逐段對照原文，缺段就失去意義。
- 以章節為單位分批產出：每批寫成一個片段檔（`part-01.html`、`part-02.html`…），最後用 `build_page.py` 一次組裝。這樣即使中途被截斷也能接續。
- 純聊天介面無法寫檔時：先告知共分幾部分，每則回覆輸出一部分，最後一部分附上完整組裝說明（或在最後一則輸出完整檔案）。
- 批註與邏輯模式可以對次要段落合併處理（例如「¶12–14 Literature review」一張批註卡），但核心論證段落要逐段處理。
- 參考文獻（References / Bibliography）保留英文原樣、不翻譯，放在可摺疊區塊中。

## 輸出語言

- **只有譯文是中文，其他一律英文。** 模式 1 的右欄譯文、中文標題、術語表的中文譯名、〔譯注〕用中文；其餘所有產出——三個模式的介面文字、導讀、模式 2 的題目／圖例／批註卡／答題卡、模式 3 的整份邏輯梳理——都用英文。即使使用者用中文跟你對話也一樣。
- 英文產出要清楚易讀：使用者的母語不是英文，用短句與常用字，專業術語第一次出現時用一句話解釋。
- 使用者明確要求某部分改用其他語言時，照使用者的要求。

## 翻譯原則（模式 1）

- 譯文預設**繁體中文（台灣用語）**。使用者以簡體中文提問或明確要求時改用簡體。
- 專有名詞與關鍵術語第一次出現時寫成「中文（English）」，之後用中文；人名第一次出現保留原文。
- 行文引用（Smith, 2020）、數學式、程式碼、變數名稱、書名原文保持不變。
- 小說與文學作品：保留語氣、節奏、對話口吻與修辭，不要為了「好懂」而改寫成說明文。
- 學術文章：精確優先，其次才是流暢；遇到歧義，在譯文後用〔譯注：…〕簡短說明。

## 品質自我檢查（交付前）

- 原文段落數與輸出段落數一致（翻譯模式逐段對齊，沒有漏段）。
- 每個 PDF 換頁處都檢查過：停在半句的段落已和下一頁的後半句接回成同一段，沒有被拆成兩段或漏翻後半句。
- 除了模式 1 的譯文欄、中文標題與術語表譯名，頁面上沒有中文（介面、批註、答案、邏輯梳理都是英文）。
- 所有 `<mark>`、題號標籤、批註卡的顏色 class 與圖例一致（模式 2）。
- 引用的原文句子確實出自原文，段落編號對得上——使用者會拿來寫作業，錯誤引用比沒有引用更糟。
- HTML 用瀏覽器開啟不會跑版：標籤成對、沒有殘留的 `{{…}}` 佔位符。
