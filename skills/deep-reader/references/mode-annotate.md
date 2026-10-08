# 模式 2：重點批註（雙欄批註＋Worksheet 答題索引）

模板：`assets/annotate.html`（佔位符 `{{TITLE}}`、`{{BODY}}`）

> **輸出語言：整份頁面一律用英文**——介面文字、題目、圖例標籤、批註卡、答題卡、頁尾都是英文。這個模式不產出任何中文（中文只出現在模式 1 的譯文欄）。唯一例外：使用者給的題目若不是英文，在英文題目下方用 `<span class="orig">` 保留原文措辭，方便對照作業。

## 目標

使用者通常是修課學生，手上有一份 worksheet（幾道閱讀題），要在讀懂文章的同時找到每題的答案與證據。這份 HTML 要讓他：

1. 在原文裡**一眼看出哪些句子回答哪一題**（彩色高亮，顏色＝題號）；
2. 在右欄讀到**每段在全文中的作用**，以及它回答了哪題的哪個層次；
3. 在頁面底部拿到**有分析深度的答案**，可以直接作為寫作業的骨架。

## 題目

- 使用者提供題目：照原題、原順序使用，題號 Q1…Qn。題目不是英文時，譯成英文顯示，原文放在 `<span class="orig">`。
- 沒提供題目：擬 4–6 題（英文），並在課程資訊處註明 `AI-drafted guiding questions`。擬題原則是覆蓋全文骨幹，而不是細節測驗：
  - 論文／論說文：研究問題或爭點 → 核心主張 → 方法或論證策略 → 關鍵證據 → 貢獻與局限 → 延伸意涵
  - 小說／文學：情節與衝突 → 人物動機與變化 → 敘事手法 → 主題 → 象徵與意象
- 每題配一個 1–4 個英文單字的短標籤（例：`Core Argument`、`Method`、`Character Motive`），用在圖例與批註卡上。
- 最多 8 題（模板定義了 `q1`–`q8` 八種顏色）。`q0` 是中性灰，給不直接回答任何題目的段落（背景、過渡）。

## 「層次」（Level）的定義

每張批註卡都要說明「這段回答哪一題的哪個層次」。層次與底部答案的三個部分一一對應，讓使用者能從段落直接追到答案。頁面上一律用英文層次名稱：

| 層次（頁面用字） | 意思 | 對應答案區塊 |
|---|---|---|
| `Claim` | 這段直接提出或重述該題的核心答案 | Core Argument |
| `Evidence` | 這段提供支撐答案的例證、數據、引文、推理 | Key Evidence |
| `Limitation` | 這段提到反例、讓步、限定條件、或暴露論證弱點 | Counterpoints & Limits |
| `Context` | 這段提供理解該題所需的脈絡、定義 | （不直接進答案，但幫助理解） |

## 高亮原則

- 只 `<mark>` **直接相關**的關鍵詞或核心句，不要整段塗滿。一段通常 0–3 處；高亮太多等於沒有高亮。
- `<mark class="qN">` 的 N 就是題號。同一句與兩題相關時，選最主要的一題。
- 可加 `title` 屬性當作滑鼠提示：`<mark class="q2" title="Q2 · Claim">...</mark>`。

## 批註卡內容（每段一張；次要連續段落可合併）

1. **Function**（段落功能）：這段在全文結構中做什麼（raises the question, defines a term, gives an example, concedes, pivots, sums up…）。
2. **Reasoning**（論證邏輯）：這段怎麼推進論證——從什麼前提、經過什麼推理、得出什麼；與上一段是什麼關係（extends, contrasts, causes, illustrates）。
3. **Answers**（回應題目）：`Q2 · Claim: …` 寫出具體回答了什麼，而不只是貼標籤。

寫法要求：英文、具體、指向原文字句；每項 1–3 句，用清楚易讀的英文（使用者的母語不是英文，避免冷僻字與過長的句子）。避免 "This paragraph is important" "The author makes a point" 這類空話——使用者要的是看完就能用。原文特別難的句子，可以在批註裡附一句白話英文改寫（plain-English paraphrase）。

## 底部 Worksheet 答題索引

每題一張卡片，兩欄排列。每張卡片包含：

- **Core Argument**：2–4 句直接回答題目，要有自己的判斷，而不是複述原文。
- **Key Evidence**：2–4 條，每條＝原文短引文（附段落連結 `¶N`）＋一句說明它如何支撐論點。
- **Counterpoints & Limits**：1–3 條。可以是作者自己承認的限制、論證中的隱含前提、或讀者可能提出的反駁；能的話說明作者如何（或是否）回應。
- **Related paragraphs**：列出所有相關段落連結。

答案的深度標準：一個認真的研究生讀完這張卡，應該覺得「抓到重點、證據準確、也看到了問題」，而不是「這是摘要」。

## `{{BODY}}` 結構

```html
<header class="topbar">
  <div class="topbar-inner">
    <div class="brand">
      <div class="doc-title">Civil Disobedience</div>
      <div class="course">POLS 201 Political Thought · Week 5 · Thoreau (1849)</div>
    </div>
    <nav class="nav">
      <a href="#overview">Overview</a><a href="#reading">Annotated Text</a><a href="#worksheet">Worksheet</a>
    </nav>
  </div>
  <div class="legend" role="toolbar" aria-label="Question legend (click to focus)">
    <button type="button" class="chip q1" data-q="q1"><b>Q1</b>Role of Government</button>
    <button type="button" class="chip q2" data-q="q2"><b>Q2</b>Core Argument</button>
    <button type="button" class="chip q0" data-q="q0"><b>—</b>Context / Transition</button>
  </div>
</header>

<section class="overview" id="overview">
  <h1>Civil Disobedience <small>Henry David Thoreau · 1849</small></h1>
  <p class="gist"><b>In one sentence:</b> …</p>
  <ol class="questions">
    <li class="q1"><span class="tag q1">Q1</span> What does Thoreau think government is for?</li>
    <!-- 使用者的題目不是英文時： -->
    <li class="q2"><span class="tag q2">Q2</span> Why does Thoreau reject majority rule? <span class="orig">梭羅為什麼反對多數決？</span></li>
  </ol>
</section>

<main class="reading" id="reading">
  <div class="col-head"><span>Original Text</span><span>Annotations</span></div>

  <section class="pair h">
    <div class="src"><h2>Part I</h2></div>
    <div class="notes"><h2>Part I: …</h2></div>
  </section>

  <section class="pair" id="p1">
    <div class="src">
      <span class="pno">¶1</span>
      <p>I heartily accept the motto, — <mark class="q1" title="Q1 · Claim">"That government is best which governs least"</mark> ...</p>
    </div>
    <div class="notes">
      <article class="note q1">
        <div class="tags"><span class="tag q1">Q1 Role of Government</span></div>
        <dl>
          <dt>Function</dt><dd>…</dd>
          <dt>Reasoning</dt><dd>…</dd>
          <dt>Answers</dt><dd><b>Q1 · Claim</b>: …</dd>
        </dl>
      </article>
    </div>
  </section>

  <!-- 一段對應兩題：放兩張 note，或一張 note 放兩個 tag -->
  <!-- 合併的次要段落：pno 寫成 ¶5–6，src 內放兩個 <p> -->
</main>

<section class="worksheet" id="worksheet">
  <h2>Worksheet Answer Index</h2>
  <div class="answers">
    <article class="answer q1" id="a-q1">
      <header>
        <span class="tag q1">Q1</span>
        <h3>What does Thoreau think government is for?</h3>
        <!-- 題目不是英文時：<h3>English question<small>原文題目</small></h3> -->
      </header>
      <div class="block"><h4>Core Argument</h4><p>…</p></div>
      <div class="block"><h4>Key Evidence</h4>
        <ul>
          <li><q>Government is at best but an expedient</q> <a href="#p1">¶1</a> — shows …</li>
        </ul>
      </div>
      <div class="block counter"><h4>Counterpoints &amp; Limits</h4><ul><li>…</li></ul></div>
      <p class="links">Related paragraphs: <a href="#p1">¶1</a> <a href="#p3">¶3</a></p>
    </article>
  </div>
</section>

<footer class="foot">Generated by deep-reader · Annotations and answers are study aids — check them against the original text</footer>
```

## 規則

- 原文欄保留原文分段，不要翻譯原文（這個模式的右欄是英文批註，不是譯文）。
- 每個 `.pair` 的 `id` 用段落編號 `pN`，這樣答案卡的 `¶N` 連結才能跳轉。
- 圖例 chip、`<mark>`、`.tag`、`.note`、`.answer` 的 `qN` 必須一致；圖例順序＝題號順序。
- 點擊圖例會聚焦該題（其他題的高亮與批註變淡），這是模板內建的 JS，不需要額外撰寫。
