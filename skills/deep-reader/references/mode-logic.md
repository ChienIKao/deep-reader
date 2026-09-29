# 模式 3：邏輯梳理

模板：`assets/logic.html`（佔位符 `{{TITLE}}`、`{{BODY}}`）

## 目標

使用者讀完（或讀不下去）時最常卡在：「作者到底主張什麼？為什麼這樣推？哪裡站得住、哪裡有問題？」這份 HTML 要把文章的**論證骨架**攤開來，讓使用者能：

1. 用一句話說出作者的主張；
2. 看到主張 → 理由 → 證據 → 隱含前提的層級結構；
3. 跟著段落順序理解論證怎麼一步步推進；
4. 自己評估論證的強弱，而不只是接受作者的說法。

## 分析方法

先通讀全文，再依序建構以下六個區塊。每個判斷都要能指回原文段落（¶N），因為使用者會回原文核對。

### ① 核心主張（Thesis）
- 引用最能代表主張的原文句子（英文）＋中文翻譯。作者沒有明說時，寫出你重建的主張，並標註「（重建）」。
- 一句話白話版：讓高中生也聽得懂。
- 四格背景：**問題意識**（作者想回答什麼問題）、**立場**（在爭論中站哪邊、反對誰）、**論證類型**（演繹、歸納、類比、因果、反證、價值論證……可多選）、**目標讀者**。

### ② 論證地圖（Argument Map）
樹狀結構，節點類型：

| class | 中文 | 意思 |
|---|---|---|
| `claim` | 主張 | 核心主張或分論點 |
| `reason` | 理由 | 支持上一層主張的理由 |
| `evidence` | 證據 | 例子、數據、引文、經驗事實 |
| `assumption` | 隱含前提 | 作者沒說出口、但推論需要它成立的前提（虛線框） |
| `objection` | 反駁 | 作者提到或可預期的反對意見 |
| `response` | 回應 | 作者對反駁的回應 |

原則：根節點是核心主張；深度通常 3–4 層；每個節點一兩句話，附 `¶N` 出處。隱含前提是這個區塊最有價值的部分——能把作者沒說的前提挖出來，使用者就真正懂了這個論證。

### ③ 推進脈絡（Flow）
依原文順序，把文章切成 4–10 個「論證步驟」（通常對應章節或幾段一組）。每步寫：段落範圍、這一步在做什麼（提出問題／定義／舉證／讓步／反駁／總結）、與前一步的關係，以及原文中標示轉折的**路標詞**（However, Therefore, Moreover…）。

### ④ 論證拆解（Toulmin）
挑 1–3 個最關鍵的論證，用 Toulmin 模型拆解：主張 Claim、根據 Grounds、保證 Warrant、支援 Backing、限定 Qualifier、反駁 Rebuttal。作者沒寫的欄位寫「（未明示）」並補上你重建的內容。

### ⑤ 論證檢驗
- **隱含前提**：列出並評估每個前提是否站得住。
- **證據強度**：每個主要分論點的證據類型與強度（1–5 顆點），附一句評語。
- **邏輯漏洞／謬誤風險**：只列真的存在的問題，說明在哪一段、為什麼是問題；不要為了湊數硬套謬誤名詞。
- **最強反駁**：替作者的論敵提出最有力的反駁（steelman），再評估作者的文本能否回應。

### ⑥ 關鍵概念
作者的論證依賴哪些概念？每個概念寫：術語（英）、作者的用法或定義、在論證中的角色。特別注意作者**與日常用法不同**的定義。

### 讀後自我檢測（選用）
2–4 題理解檢測題，答案用 `<details>` 摺疊。

## 小說、散文等敘事文本

論證模型不適用時，把六個區塊換成敘事版本（class 名稱沿用，只改標題與內容）：

| 論說文 | 敘事文本 |
|---|---|
| 核心主張 | 故事核心：一句話情節＋主題命題 |
| 論證地圖 | 因果鏈：事件 → 動機 → 衝突 → 轉折 → 結果（節點用 `claim`=核心衝突、`reason`=動機、`evidence`=關鍵事件、`assumption`=隱含的社會／心理前提、`objection`/`response`=對立力量與其化解） |
| 推進脈絡 | 敘事結構：鋪陳、上升、高潮、下降、結局（或非線性敘事的時間線） |
| Toulmin 拆解 | 人物分析：外在行為 → 內在動機 → 文本證據 → 變化弧線 |
| 論證檢驗 | 解讀爭議：可能的不同詮釋，各自的文本證據 |
| 關鍵概念 | 象徵、意象、母題 |

## `{{BODY}}` 結構

```html
<header class="topbar">
  <div class="topbar-inner">
    <div class="brand">
      <div class="doc-title">Civil Disobedience｜邏輯梳理</div>
      <div class="sub">Henry David Thoreau · 1849</div>
    </div>
    <nav class="nav">
      <a href="#thesis">主旨</a><a href="#map">論證地圖</a><a href="#flow">推進脈絡</a>
      <a href="#toulmin">論證拆解</a><a href="#check">論證檢驗</a><a href="#concepts">關鍵概念</a>
    </nav>
  </div>
</header>

<main class="wrap">
  <section id="thesis" class="card thesis">
    <p class="eyebrow">核心主張 Thesis</p>
    <blockquote class="en">"That government is best which governs not at all" ... <cite>¶1</cite></blockquote>
    <p class="zh">……</p>
    <p class="plain"><b>白話版：</b>……</p>
    <div class="meta-grid">
      <div><h4>問題意識</h4><p>……</p></div>
      <div><h4>立場</h4><p>……</p></div>
      <div><h4>論證類型</h4><p><span class="pill">價值論證</span><span class="pill">類比</span></p></div>
      <div><h4>目標讀者</h4><p>……</p></div>
    </div>
  </section>

  <section id="map">
    <h2>論證地圖</h2>
    <div class="map-legend">
      <span class="node-key claim">主張</span><span class="node-key reason">理由</span>
      <span class="node-key evidence">證據</span><span class="node-key assumption">隱含前提</span>
      <span class="node-key objection">反駁</span><span class="node-key response">回應</span>
    </div>
    <ul class="tree">
      <li>
        <div class="node claim"><span class="kind">主張</span><p>……</p><span class="ref">¶1–2</span></div>
        <ul>
          <li>
            <div class="node reason"><span class="kind">理由 1</span><p>……</p><span class="ref">¶3</span></div>
            <ul>
              <li><div class="node evidence"><span class="kind">證據</span><p>……</p><span class="ref">¶4</span></div></li>
              <li><div class="node assumption"><span class="kind">隱含前提</span><p>……</p></div></li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </section>

  <section id="flow">
    <h2>推進脈絡</h2>
    <ol class="flow">
      <li class="step">
        <div class="range">¶1–2</div>
        <div class="body">
          <h3>提出問題：……</h3>
          <p>……</p>
          <p class="signpost">路標詞：<em>But</em>、<em>Yet</em> —— 標示從接受格言到推翻它的轉折</p>
        </div>
      </li>
    </ol>
  </section>

  <section id="toulmin">
    <h2>論證拆解（Toulmin 模型）</h2>
    <article class="toulmin">
      <h3>論證 1：……</h3>
      <div class="t-grid">
        <div class="t claim"><h4>主張 Claim</h4><p>……</p></div>
        <div class="t grounds"><h4>根據 Grounds</h4><p>……</p></div>
        <div class="t warrant"><h4>保證 Warrant</h4><p>……</p></div>
        <div class="t backing"><h4>支援 Backing</h4><p>……</p></div>
        <div class="t qualifier"><h4>限定 Qualifier</h4><p>……</p></div>
        <div class="t rebuttal"><h4>反駁 Rebuttal</h4><p>……</p></div>
      </div>
    </article>
  </section>

  <section id="check">
    <h2>論證檢驗</h2>
    <div class="check-grid">
      <article class="card"><h3>隱含前提</h3><ul><li><b>……</b>：評估……</li></ul></article>
      <article class="card"><h3>邏輯漏洞／謬誤風險</h3><ul><li>……（¶N）</li></ul></article>
    </div>
    <table class="strength">
      <thead><tr><th>分論點</th><th>證據類型</th><th>強度</th><th>評語</th></tr></thead>
      <tbody>
        <tr><td>……</td><td>類比</td><td><span class="dots" data-score="3"></span></td><td>……</td></tr>
      </tbody>
    </table>
    <article class="card steelman"><h3>最強反駁與作者的可能回應</h3><p>……</p></article>
  </section>

  <section id="concepts">
    <h2>關鍵概念</h2>
    <table class="concepts">
      <thead><tr><th>術語</th><th>作者的用法</th><th>在論證中的角色</th></tr></thead>
      <tbody><tr><td><b>expedient</b><br>權宜之計</td><td>……</td><td>……</td></tr></tbody>
    </table>
  </section>

  <section id="selfcheck">
    <h2>讀後自我檢測</h2>
    <details><summary>1. ……？</summary><p>……</p></details>
  </section>
</main>

<footer class="foot">由 deep-reader 產生 · 論證分析僅供學習參考</footer>
```

## 規則

- `.dots` 的 `data-score` 填 1–5，模板會自動畫出圓點。
- 論證地圖的 `<ul class="tree">` 可以任意巢狀；每個 `<li>` 以一個 `.node` 開頭。
- 若沒有自我檢測，省略 `#selfcheck` 區塊，並從導覽列拿掉對應連結（導覽列裡目前沒有它，要加的話自行加上）。
- 敘事文本改用敘事版標題時，導覽列文字也一併修改。
