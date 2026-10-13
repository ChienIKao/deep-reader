# 重點整理模式（Key Points）

頁籤：`Key Points`（panel id `tab-summary`）。組裝方式見 `SKILL.md` 第 5 步。

> **輸出語言：英文。** 用清楚易讀的英文（使用者的母語不是英文）：短句、常用字，術語第一次出現時用幾個字解釋。

## 目標

使用者打開檔案第一眼看到的頁面。讀完 3 分鐘內要能回答：

1. 作者究竟想論證什麼？（Argument）
2. 作者如何一步步建立論點？（Argumentation）
3. 作者用了哪些文本證據？（Evidence）
4. 文章各部分在整體論證中扮演什麼角色？（Structure）
5. 哪些概念、分析與問題值得記住？（Key Insights）

這不是摘要文章內容，而是幫使用者**釐清論證**。每個區塊寫成**一小段 passage 或簡短條列**，不要長篇大論：整頁大約 400–700 字。

## 五個區塊的寫法

| 區塊 | 形式 | 內容 |
|---|---|---|
| **Argument** | 一段 passage，3–6 句 | 作者的核心主張＋為什麼這樣主張＋立場的限度。第一句就說出主張。 |
| **Argumentation** | 有序條列，4–7 步 | 依論證順序，每步一個粗體短標題＋一句說明＋段落出處 `¶N`。寫「作者在做什麼動作」（提出前提、類比、讓步、反駁、應用），不是重述內容。 |
| **Evidence** | 條列，3–6 條 | 原文短引文 `<q>`（必須逐字出自原文）＋`¶N`＋一句說明它支撐了哪個論點。挑最關鍵的，不是每段都列。 |
| **Structure** | 段落範圍＋角色，3–7 列 | 每列：段落範圍、粗體角色名（Setup / Hinge / Core / Counterargument / Application / Conclusion…）、一句說明這部分為什麼在這裡。 |
| **Key Insights** | 三欄短條列，每欄 2–4 條 | `Concepts`（關鍵術語與作者的用法）、`Analytical moves`（作者用的分析方法，值得學起來的寫法）、`Questions to discuss`（值得在課堂或報告中追問的問題）。 |

頂部的 `In one sentence` 用一句話總結全文主旨。

## 不同文本類型

- **文學批評（literary criticism）、人文論文**：常常沒有明確的 thesis statement，而是透過文本細讀逐步形成論點。此時從分析過程**重建**主張，並在 Argument 開頭註明 `(reconstructed)`；Argumentation 寫作者如何從細讀的細節推向詮釋；Evidence 優先列作者分析的那幾段原著引文；Analytical moves 寫作者的批評方法（close reading、historicist、feminist、psychoanalytic…）。
- **實證研究論文**：Argument 寫研究問題與主要發現；Argumentation 依 問題 → 方法 → 結果 → 詮釋 寫；Evidence 可列關鍵數據與圖表（`Table 2`、`Fig. 3`）。
- **小說與敘事文本**：五個區塊改成 `Story & Theme`（一句話情節＋主題）、`Plot Development`（關鍵轉折）、`Key Passages`（關鍵段落引文）、`Narrative Structure`（敘事結構）、`Key Insights`（`Symbols & Motifs` / `Characters` / `Questions to discuss`）。

## 這個頁籤的 HTML（`#tab-summary` 內容）

```html
<main class="kp-wrap">
  <header class="kp-head">
    <p class="eyebrow">Critical Reading Notes</p>
    <h1>On the Duty of Civil Disobedience <small>Henry David Thoreau · 1849 · POLS 201</small></h1>
    <p class="kp-gist"><b>In one sentence:</b> …</p>
  </header>

  <section class="kp" id="kp-argument">
    <h2><span class="kp-n">1</span>Argument <small>What is the author arguing?</small></h2>
    <p>…</p>
  </section>

  <section class="kp" id="kp-argumentation">
    <h2><span class="kp-n">2</span>Argumentation <small>How is the argument built, step by step?</small></h2>
    <ol>
      <li><b>Start from the reader’s own belief.</b> … <span class="ref">¶1</span></li>
    </ol>
  </section>

  <section class="kp" id="kp-evidence">
    <h2><span class="kp-n">3</span>Evidence <small>What textual evidence supports it?</small></h2>
    <ul>
      <li><q>Government is at best but an expedient</q> <span class="ref">¶1</span> — …</li>
    </ul>
  </section>

  <section class="kp" id="kp-structure">
    <h2><span class="kp-n">4</span>Structure <small>What role does each part play?</small></h2>
    <ul class="kp-structure">
      <li><span class="range">¶1–2</span><span><b>Setup.</b> …</span></li>
    </ul>
  </section>

  <section class="kp" id="kp-insights">
    <h2><span class="kp-n">5</span>Key Insights <small>What is worth remembering?</small></h2>
    <div class="kp-insights">
      <div><h3>Concepts</h3><ul><li><b>expedient</b>: …</li></ul></div>
      <div><h3>Analytical moves</h3><ul><li>…</li></ul></div>
      <div><h3>Questions to discuss</h3><ul><li>…</li></ul></div>
    </div>
  </section>
</main>
```

## 規則

- 每個判斷都要能指回原文段落 `¶N`；引文必須逐字出自原文。
- 和其他頁籤一起產出時，這裡的主張、步驟與邏輯梳理（Logic Map）要一致，但寫得更短；細節留給其他頁籤。
- 區塊的 `<small>` 副標可以保留範例中的問句，敘事文本改成對應的問句。
