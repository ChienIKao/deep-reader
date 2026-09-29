# 模式 2：重點批註（雙欄批註＋Worksheet 答題索引）

模板：`assets/annotate.html`（佔位符 `{{TITLE}}`、`{{BODY}}`）

## 目標

使用者通常是修課學生，手上有一份 worksheet（幾道閱讀題），要在讀懂文章的同時找到每題的答案與證據。這份 HTML 要讓他：

1. 在原文裡**一眼看出哪些句子回答哪一題**（彩色高亮，顏色＝題號）；
2. 在右欄讀到**每段在全文中的作用**，以及它回答了哪題的哪個層次；
3. 在頁面底部拿到**有分析深度的答案**，可以直接作為寫作業的骨架。

## 題目

- 使用者提供題目：照原題、原順序使用，題號 Q1…Qn。題目若是英文，卡片上保留英文並附中文翻譯。
- 沒提供題目：擬 4–6 題，並在頁首課程資訊處註明「AI 擬定導讀題」。擬題原則是覆蓋全文骨幹，而不是細節測驗：
  - 論文／論說文：研究問題或爭點 → 核心主張 → 方法或論證策略 → 關鍵證據 → 貢獻與局限 → 延伸意涵
  - 小說／文學：情節與衝突 → 人物動機與變化 → 敘事手法 → 主題 → 象徵與意象
- 每題配一個 2–6 字的短標籤（例：「核心論點」「研究方法」「人物動機」），用在圖例與批註卡上。
- 最多 8 題（模板定義了 `q1`–`q8` 八種顏色）。`q0` 是中性灰，給不直接回答任何題目的段落（背景、過渡）。

## 「層次」的定義

每張批註卡都要說明「這段回答哪一題的哪個層次」。層次與底部答案的三個部分一一對應，讓使用者能從段落直接追到答案：

| 層次 | 意思 | 對應答案區塊 |
|---|---|---|
| 論點層 | 這段直接提出或重述該題的核心答案 | 核心論點 |
| 證據層 | 這段提供支撐答案的例證、數據、引文、推理 | 關鍵證據 |
| 限制層 | 這段提到反例、讓步、限定條件、或暴露論證弱點 | 潛在反駁／局限 |
| 背景層 | 這段提供理解該題所需的脈絡、定義 | （不直接進答案，但幫助理解） |

## 高亮原則

- 只 `<mark>` **直接相關**的關鍵詞或核心句，不要整段塗滿。一段通常 0–3 處；高亮太多等於沒有高亮。
- `<mark class="qN">` 的 N 就是題號。同一句與兩題相關時，選最主要的一題。
- 可加 `title` 屬性當作滑鼠提示：`<mark class="q2" title="Q2 論點層">...</mark>`。

## 批註卡內容（每段一張；次要連續段落可合併）

1. **段落功能**：這段在全文結構中做什麼（提出問題、定義概念、舉例、讓步、轉折、總結……）。
2. **論證邏輯**：這段怎麼推進論證——從什麼前提、經過什麼推理、得出什麼；與上一段是什麼關係（延伸、對比、因果、舉證）。
3. **回應題目**：「Q2・論點層：……」寫出具體回答了什麼，而不只是貼標籤。

寫法要求：中文、具體、指向原文字句；每項 1–3 句。避免「本段很重要」「作者提出了觀點」這類空話——使用者要的是看完就能用。

## 底部 Worksheet 答題索引

每題一張卡片，兩欄排列。每張卡片包含：

- **核心論點**：2–4 句直接回答題目，要有自己的判斷，而不是複述原文。
- **關鍵證據**：2–4 條，每條＝原文短引文（英文，附段落連結 `¶N`）＋一句中文說明它如何支撐論點。
- **潛在反駁／局限**：1–3 條。可以是作者自己承認的限制、論證中的隱含前提、或讀者可能提出的反駁；能的話說明作者如何（或是否）回應。
- **相關段落**：列出所有相關段落連結。

答案的深度標準：一個認真的研究生讀完這張卡，應該覺得「抓到重點、證據準確、也看到了問題」，而不是「這是摘要」。

## `{{BODY}}` 結構

```html
<header class="topbar">
  <div class="topbar-inner">
    <div class="brand">
      <div class="doc-title">Civil Disobedience</div>
      <div class="course">POLS 201 政治思想 · Week 5 · Thoreau (1849)</div>
    </div>
    <nav class="nav">
      <a href="#overview">導讀</a><a href="#reading">原文批註</a><a href="#worksheet">答題索引</a>
    </nav>
  </div>
  <div class="legend" role="toolbar" aria-label="題目圖例（點擊可聚焦）">
    <button type="button" class="chip q1" data-q="q1"><b>Q1</b>政府的角色</button>
    <button type="button" class="chip q2" data-q="q2"><b>Q2</b>核心論點</button>
    <button type="button" class="chip q0" data-q="q0"><b>—</b>背景／過渡</button>
  </div>
</header>

<section class="overview" id="overview">
  <h1>Civil Disobedience <small>公民不服從</small></h1>
  <p class="gist"><b>一句話主旨：</b>……</p>
  <ol class="questions">
    <li class="q1"><span class="tag q1">Q1</span> What does Thoreau think government is for? <span class="zh">梭羅認為政府的功能是什麼？</span></li>
  </ol>
</section>

<main class="reading" id="reading">
  <div class="col-head"><span>Original Text</span><span>中文批註</span></div>

  <section class="pair h">
    <div class="src"><h2>Part I</h2></div>
    <div class="notes"><h2>第一部分：……</h2></div>
  </section>

  <section class="pair" id="p1">
    <div class="src">
      <span class="pno">¶1</span>
      <p>I heartily accept the motto, — <mark class="q1" title="Q1 論點層">"That government is best which governs least"</mark> ...</p>
    </div>
    <div class="notes">
      <article class="note q1">
        <div class="tags"><span class="tag q1">Q1 政府的角色</span></div>
        <dl>
          <dt>段落功能</dt><dd>……</dd>
          <dt>論證邏輯</dt><dd>……</dd>
          <dt>回應題目</dt><dd><b>Q1・論點層</b>：……</dd>
        </dl>
      </article>
    </div>
  </section>

  <!-- 一段對應兩題：放兩張 note，或一張 note 放兩個 tag -->
  <!-- 合併的次要段落：pno 寫成 ¶5–6，src 內放兩個 <p> -->
</main>

<section class="worksheet" id="worksheet">
  <h2>Worksheet 答題索引</h2>
  <div class="answers">
    <article class="answer q1" id="a-q1">
      <header>
        <span class="tag q1">Q1</span>
        <h3>What does Thoreau think government is for?<small>梭羅認為政府的功能是什麼？</small></h3>
      </header>
      <div class="block"><h4>核心論點</h4><p>……</p></div>
      <div class="block"><h4>關鍵證據</h4>
        <ul>
          <li><q>Government is at best but an expedient</q> <a href="#p1">¶1</a> —— 說明……</li>
        </ul>
      </div>
      <div class="block counter"><h4>潛在反駁／局限</h4><ul><li>……</li></ul></div>
      <p class="links">相關段落：<a href="#p1">¶1</a> <a href="#p3">¶3</a></p>
    </article>
  </div>
</section>

<footer class="foot">由 deep-reader 產生 · 批註與答案僅供學習參考，請搭配原文自行判斷</footer>
```

## 規則

- 原文欄保留原文分段，不要翻譯原文（這個模式的右欄是批註，不是譯文）。原文中特別難的句子可以在批註裡附中文意譯。
- 每個 `.pair` 的 `id` 用段落編號 `pN`，這樣答案卡的 `¶N` 連結才能跳轉。
- 圖例 chip、`<mark>`、`.tag`、`.note`、`.answer` 的 `qN` 必須一致；圖例順序＝題號順序。
- 點擊圖例會聚焦該題（其他題的高亮與批註變淡），這是模板內建的 JS，不需要額外撰寫。
