# 模式 3：邏輯梳理

模板：`assets/logic.html`（佔位符 `{{TITLE}}`、`{{BODY}}`）

> **輸出語言：整份頁面一律用英文**——區塊標題、節點、說明、評語、自我檢測、頁尾都是英文，不產出任何中文（中文只出現在模式 1 的譯文欄）。用清楚易讀的英文寫（使用者的母語不是英文）：短句、常用字，專業術語第一次出現時用一句話解釋。下方中文只是給你的說明。

## 目標

使用者讀完（或讀不下去）時最常卡在：「作者到底主張什麼？為什麼這樣推？哪裡站得住、哪裡有問題？」這份 HTML 要把文章的**論證骨架**攤開來，讓使用者能：

1. 用一句話說出作者的主張；
2. 看到主張 → 理由 → 證據 → 隱含前提的層級結構；
3. 跟著段落順序理解論證怎麼一步步推進；
4. 自己評估論證的強弱，而不只是接受作者的說法。

## 分析方法

先通讀全文，再依序建構以下六個區塊。每個判斷都要能指回原文段落（¶N），因為使用者會回原文核對。

### ① 核心主張（Thesis）
- 引用最能代表主張的原文句子，再用一句精確的英文重述主張（`.restate`）。作者沒有明說時，寫出你重建的主張，並標註 `(reconstructed)`。
- `In plain words`：一句白話版，讓高中生也聽得懂。
- 四格背景：**Question**（作者想回答什麼問題）、**Position**（在爭論中站哪邊、反對誰）、**Argument Type**（deductive, inductive, analogy, causal, reductio, value-based…可多選）、**Audience**。

### ② 論證地圖（Argument Map）
樹狀結構，節點類型：

| class | 頁面標籤 | 意思 |
|---|---|---|
| `claim` | Claim | 核心主張或分論點 |
| `reason` | Reason | 支持上一層主張的理由 |
| `evidence` | Evidence | 例子、數據、引文、經驗事實 |
| `assumption` | Hidden Assumption | 作者沒說出口、但推論需要它成立的前提（虛線框） |
| `objection` | Objection | 作者提到或可預期的反對意見 |
| `response` | Response | 作者對反駁的回應 |

原則：根節點是核心主張；深度通常 3–4 層；每個節點一兩句話，附 `¶N` 出處。隱含前提是這個區塊最有價值的部分——能把作者沒說的前提挖出來，使用者就真正懂了這個論證。

### ③ 推進脈絡（Flow）
依原文順序，把文章切成 4–10 個「論證步驟」（通常對應章節或幾段一組）。每步寫：段落範圍、這一步在做什麼（raises the problem / defines / gives evidence / concedes / rebuts / concludes）、與前一步的關係，以及原文中標示轉折的**路標詞**（However, Therefore, Moreover…）。

### ④ 論證拆解（Toulmin）
挑 1–3 個最關鍵的論證，用 Toulmin 模型拆解：主張 Claim、根據 Grounds、保證 Warrant、支援 Backing、限定 Qualifier、反駁 Rebuttal。作者沒寫的欄位寫 `(implicit)` 並補上你重建的內容。

### ⑤ 論證檢驗
- **Hidden Assumptions**：列出並評估每個前提是否站得住。
- **Evidence Strength**：每個主要分論點的證據類型與強度（1–5 顆點），附一句評語。
- **Gaps & Fallacy Risks**：只列真的存在的問題，說明在哪一段、為什麼是問題；不要為了湊數硬套謬誤名詞。
- **Strongest Objection**：替作者的論敵提出最有力的反駁（steelman），再評估作者的文本能否回應。

### ⑥ 關鍵概念
作者的論證依賴哪些概念？每個概念寫：術語、作者的用法或定義、在論證中的角色。特別注意作者**與日常用法不同**的定義。

### 讀後自我檢測（選用）
2–4 題理解檢測題，答案用 `<details>` 摺疊。

## 小說、散文等敘事文本

論證模型不適用時，把六個區塊換成敘事版本（class 名稱沿用，只改標題與內容）：

| 論說文 | 敘事文本（頁面標題） |
|---|---|
| 核心主張 | Story Core：一句話情節＋主題命題 |
| 論證地圖 | Causal Chain：事件 → 動機 → 衝突 → 轉折 → 結果（節點用 `claim`=Central Conflict、`reason`=Motive、`evidence`=Key Event、`assumption`=Hidden Social/Psychological Premise、`objection`/`response`=Opposing Force / Resolution） |
| 推進脈絡 | Narrative Structure：exposition, rising action, climax, falling action, resolution（或非線性敘事的時間線） |
| Toulmin 拆解 | Character Analysis：外在行為 → 內在動機 → 文本證據 → 變化弧線 |
| 論證檢驗 | Interpretive Debates：可能的不同詮釋，各自的文本證據 |
| 關鍵概念 | Symbols, Images & Motifs |

## `{{BODY}}` 結構

```html
<header class="topbar">
  <div class="topbar-inner">
    <div class="brand">
      <div class="doc-title">Civil Disobedience · Logic Map</div>
      <div class="sub">Henry David Thoreau · 1849</div>
    </div>
    <nav class="nav">
      <a href="#thesis">Thesis</a><a href="#map">Argument Map</a><a href="#flow">Flow</a>
      <a href="#toulmin">Toulmin</a><a href="#check">Evaluation</a><a href="#concepts">Key Concepts</a>
    </nav>
  </div>
</header>

<main class="wrap">
  <section id="thesis" class="card thesis">
    <p class="eyebrow">Thesis</p>
    <blockquote class="en">"That government is best which governs not at all" ... <cite>¶1</cite></blockquote>
    <p class="restate">…</p>
    <p class="plain"><b>In plain words:</b> …</p>
    <div class="meta-grid">
      <div><h4>Question</h4><p>…</p></div>
      <div><h4>Position</h4><p>…</p></div>
      <div><h4>Argument Type</h4><p><span class="pill">Value-based</span><span class="pill">Analogy</span></p></div>
      <div><h4>Audience</h4><p>…</p></div>
    </div>
  </section>

  <section id="map">
    <h2>Argument Map</h2>
    <div class="map-legend">
      <span class="node-key claim">Claim</span><span class="node-key reason">Reason</span>
      <span class="node-key evidence">Evidence</span><span class="node-key assumption">Hidden Assumption</span>
      <span class="node-key objection">Objection</span><span class="node-key response">Response</span>
    </div>
    <ul class="tree">
      <li>
        <div class="node claim"><span class="kind">Claim</span><p>…</p><span class="ref">¶1–2</span></div>
        <ul>
          <li>
            <div class="node reason"><span class="kind">Reason 1</span><p>…</p><span class="ref">¶3</span></div>
            <ul>
              <li><div class="node evidence"><span class="kind">Evidence</span><p>…</p><span class="ref">¶4</span></div></li>
              <li><div class="node assumption"><span class="kind">Hidden Assumption</span><p>…</p></div></li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </section>

  <section id="flow">
    <h2>Flow of the Argument</h2>
    <ol class="flow">
      <li class="step">
        <div class="range">¶1–2</div>
        <div class="body">
          <h3>Raises the problem: …</h3>
          <p>…</p>
          <p class="signpost">Signposts: <em>But</em>, <em>Yet</em> — mark the turn from accepting the motto to overturning it</p>
        </div>
      </li>
    </ol>
  </section>

  <section id="toulmin">
    <h2>Argument Breakdown (Toulmin Model)</h2>
    <article class="toulmin">
      <h3>Argument 1: …</h3>
      <div class="t-grid">
        <div class="t claim"><h4>Claim</h4><p>…</p></div>
        <div class="t grounds"><h4>Grounds</h4><p>…</p></div>
        <div class="t warrant"><h4>Warrant</h4><p>…</p></div>
        <div class="t backing"><h4>Backing</h4><p>…</p></div>
        <div class="t qualifier"><h4>Qualifier</h4><p>…</p></div>
        <div class="t rebuttal"><h4>Rebuttal</h4><p>…</p></div>
      </div>
    </article>
  </section>

  <section id="check">
    <h2>Evaluating the Argument</h2>
    <div class="check-grid">
      <article class="card"><h3>Hidden Assumptions</h3><ul><li><b>…</b>: assessment …</li></ul></article>
      <article class="card"><h3>Gaps &amp; Fallacy Risks</h3><ul><li>… (¶N)</li></ul></article>
    </div>
    <table class="strength">
      <thead><tr><th>Sub-claim</th><th>Evidence Type</th><th>Strength</th><th>Comment</th></tr></thead>
      <tbody>
        <tr><td>…</td><td>Analogy</td><td><span class="dots" data-score="3"></span></td><td>…</td></tr>
      </tbody>
    </table>
    <article class="card steelman"><h3>Strongest Objection &amp; the Author's Likely Reply</h3><p>…</p></article>
  </section>

  <section id="concepts">
    <h2>Key Concepts</h2>
    <table class="concepts">
      <thead><tr><th>Term</th><th>How the Author Uses It</th><th>Role in the Argument</th></tr></thead>
      <tbody><tr><td><b>expedient</b></td><td>…</td><td>…</td></tr></tbody>
    </table>
  </section>

  <section id="selfcheck">
    <h2>Check Your Understanding</h2>
    <details><summary>1. …?</summary><p>…</p></details>
  </section>
</main>

<footer class="foot">Generated by deep-reader · Argument analysis is a study aid — check it against the original text</footer>
```

## 規則

- `.dots` 的 `data-score` 填 1–5，模板會自動畫出圓點。
- 論證地圖的 `<ul class="tree">` 可以任意巢狀；每個 `<li>` 以一個 `.node` 開頭。
- 若沒有自我檢測，省略 `#selfcheck` 區塊，並從導覽列拿掉對應連結（導覽列裡目前沒有它，要加的話自行加上）。
- 敘事文本改用敘事版標題（英文）時，導覽列文字也一併修改。
