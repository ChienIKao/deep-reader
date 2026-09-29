# 模式 1：中英對照翻譯

模板：`assets/translate.html`（佔位符 `{{TITLE}}`、`{{BODY}}`）

## 目標

使用者要**逐段對照**閱讀：左邊英文原文，右邊中文譯文，每一段在同一列對齊。他們會一邊看英文一邊確認理解，所以對齊與完整度比什麼都重要。

## 翻譯標準

- **完整**：每一段都要翻，不省略、不摘要、不寫「以下略」。長文請分批產出（見 SKILL.md〈長文處理〉）。
- **忠實**：意思、語氣、立場、限定詞（may, likely, arguably）都要保留。學術文章的 hedging 是論證的一部分，不能譯成斬釘截鐵。
- **通順**：用自然的中文語序，不要逐字直譯。長句可以拆成兩三句中文，但不能改變論證順序。
- **術語**：關鍵術語第一次出現寫「中文（English）」，並收進文末術語表。同一術語全文譯法一致。
- **不翻的東西**：行文引用（Smith, 2020）、公式、程式碼、變數、網址、參考文獻清單。
- **文學作品**：保留敘事聲音、對話口吻、節奏與修辭；雙關或文化典故可加〔譯注〕。
- **譯注**：只在真的有助理解時加，格式 `<span class="tn">〔譯注：…〕</span>`，放在譯文段落內。

## `{{BODY}}` 結構

```html
<header class="topbar">
  <div class="topbar-inner">
    <div class="doc-title">Civil Disobedience｜公民不服從</div>
    <nav class="controls" aria-label="檢視模式">
      <button type="button" data-view="both" aria-pressed="true">雙語</button>
      <button type="button" data-view="en" aria-pressed="false">英文</button>
      <button type="button" data-view="zh" aria-pressed="false">中文</button>
      <span class="sep"></span>
      <button type="button" data-font="-1" aria-label="縮小字體">A−</button>
      <button type="button" data-font="1" aria-label="放大字體">A+</button>
    </nav>
  </div>
</header>

<section class="cover">
  <h1 class="en-title">Civil Disobedience</h1>
  <p class="zh-title">公民不服從</p>
  <p class="meta">Henry David Thoreau · 1849 · 來源：Project Gutenberg</p>
  <p class="summary">〔一句話導讀：這篇文章在講什麼、為什麼值得讀。可省略。〕</p>
</section>

<main class="doc">
  <div class="col-head"><span>English Original</span><span>中文翻譯</span></div>

  <!-- 章節標題 -->
  <section class="pair h">
    <div class="en"><h2>1. Introduction</h2></div>
    <div class="zh"><h2>1. 引言</h2></div>
  </section>

  <!-- 一般段落：data-p 為段落編號 -->
  <section class="pair" id="p1" data-p="1">
    <div class="en"><p>I heartily accept the motto, ...</p></div>
    <div class="zh"><p>我衷心接受這句格言……</p></div>
  </section>

  <!-- 引文 / 詩句 -->
  <section class="pair quote" id="p2" data-p="2">
    <div class="en"><blockquote>...</blockquote></div>
    <div class="zh"><blockquote>……</blockquote></div>
  </section>

  <!-- 圖表說明 -->
  <section class="pair figure">
    <div class="en"><p>Figure 1: ...</p></div>
    <div class="zh"><p>圖 1：……</p></div>
  </section>
</main>

<section class="glossary" id="glossary">
  <h2>術語對照表</h2>
  <table>
    <thead><tr><th>English</th><th>中文</th><th>說明</th></tr></thead>
    <tbody>
      <tr><td>expedient</td><td>權宜之計</td><td>作者用來形容政府只是工具、不是目的</td></tr>
    </tbody>
  </table>
</section>

<details class="references">
  <summary>References（保留原文）</summary>
  <ol><li>...</li></ol>
</details>

<footer class="foot">由 deep-reader 產生 · 譯文僅供學習參考</footer>
```

## 規則

- 一個原文段落 = 一個 `<section class="pair">`，左右各一個 `<p>`。不要把兩段原文塞進同一列，也不要把一段拆成兩列——對齊是這個模式存在的理由。
- 列表（ul/ol）整組放在同一個 pair 裡，左右各一份。
- 原文的斜體、粗體用 `<em>`、`<strong>` 保留，譯文對應處也標上。
- `data-p` 與 `id="pN"` 用 input.md 定義的段落編號；標題、圖說不編號。
- 術語表收 5–25 個對理解最關鍵的術語；文章很短或沒有專業術語時可以省略整個 `glossary` 區塊。
- 沒有參考文獻就省略 `references` 區塊。
