<p align="center"><a href="https://maco165.github.io/rust-patch-notes/zh/index.html"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/hero-zh-dark.png"><img src="assets/readme/hero-zh.png" alt="Rust Analysis" width="100%"></picture></a></p>

<p align="center"><a href="README.md"><img src="assets/readme/lang-ja.png" alt="日本語" height="40"></a> <a href="README.en.md"><img src="assets/readme/lang-en.png" alt="English" height="40"></a> <a href="README.zh.md"><img src="assets/readme/lang-zh-on.png" alt="简体中文" height="40"></a> <a href="README.ko.md"><img src="assets/readme/lang-ko.png" alt="한국어" height="40"></a> <a href="README.ru.md"><img src="assets/readme/lang-ru.png" alt="Русский" height="40"></a></p>

<p align="center"><b><a href="https://maco165.github.io/rust-patch-notes/zh/index.html">https://maco165.github.io/rust-patch-notes/</a></b></p>

关于游戏 Rust (Facepunch Studios) 的非官方个人网站：用日语整理官方更新日志，列出所有物品的数值，并提供 5 个计算器（抄家、制作、植物基因、茶与派、几发击倒）。本月、类别、工具和文章支持 5 种语言。

## 关于本站

**是什么** — 阅读官方更新日志以及游戏本体的数据和代码，来确认 Rust 运作方式的非官方分析网站。

**为什么做** — 此前没有一个网站从游戏代码的变化中整理更新内容和内部机制。

**优势**

- 读到代码为止：不只看数值，还读服务器代码 (IL) 来确认计算规则，计算器用例题和穷举来检验
- 2015 年以来的全部历史并每月更新：2015 年以来的全部变更，以及按月版本比较的物品设置差异
- 5 种语言、只需浏览器、免费：支持日语、英语、中文、韩语和俄语，无需注册、没有广告，全部在浏览器中运行

**理念** — 只写确认过的内容。未确认的内容会标明“未确认”。

**审核** — 每项变更在公开前都由 Anthropic 的 AI“Claude”检查差异，并经人工批准。

## 页面截图

<table><tr><td colspan="2" valign="top"><a href="https://maco165.github.io/rust-patch-notes/zh/index.html"><img src="assets/readme/shot-zh-month.png" alt="本月"></a><br><sub><b>本月</b></sub></td></tr><tr><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/zh/tools/raid.html"><img src="assets/readme/shot-zh-raid.png" alt="Raid Planner"></a><br><sub><b>Raid Planner</b></sub></td><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/zh/tools/gene.html"><img src="assets/readme/shot-zh-gene.png" alt="Gene Planner"></a><br><sub><b>Gene Planner</b></sub></td></tr><tr><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/zh/tools/buff.html"><img src="assets/readme/shot-zh-buff.png" alt="Buff Planner"></a><br><sub><b>Buff Planner</b></sub></td><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/zh/tools/ttk.html"><img src="assets/readme/shot-zh-ttk.png" alt="TTK Planner"></a><br><sub><b>TTK Planner</b></sub></td></tr></table>

## 系统结构

页面由 Python 脚本根据从游戏中读取的数据生成。没有外部 JS 文件：`build_site.py` 把每个页面的脚本直接写进页面里。

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/arch-dark.png"><img src="assets/readme/arch.png" alt="Rust Analysis: sources, Python scripts, data, build_site.py, GitHub Pages" width="100%"></picture></p>

- 每个页面都可以通过顶部导航栏前往所有主要页面。
- `tools/raid.html` 通过 URL (`m`、`o`、`c`、`r`) 把选好的数量传给 `tools/craft.html`；制作页面用 `r` 链接回去。
- `assets/style.css` 由 `design/tokens.json` 转成的 CSS 变量、`components.css`、`site.css` 以及 `item-icons/` 中每个图标的遮罩组成。

## 页面

| 页面 | 内容 | 数据来源 |
|---|---|---|
| [index.html](zh/index.html) | 本月更新：要点、数量、数值变化、全部改动 | 官方更新日志，用日语重写 |
| [history.html](history.html) (仅日语) · [genres.html](zh/genres.html) · [numbers.html](numbers.html) (仅日语) | 所有补丁（可按类别、年份、种类筛选）；各类别的数量；写有数值的改动 | 同一份更新日志；类别划分是本站自己的规则 |
| [items.html](items.html) (仅日语) · [spec.html](spec.html) (仅日语) | 每个物品的设置、掉落位置与概率；所有数值的表格 | 从服务器版本导出的数值，以及根据掉落表算出的概率 |
| [diffs.html](diffs.html) (仅日语) | 两个版本之间物品设置的变化 | 客户端每月版本的物品文件 |
| [columns.html](zh/columns.html) | 根据服务器代码和数据验证玩家说法的文章 | 服务器的代码 (IL) 与数据；出处在每篇文章末尾 |
| [tools/raid.html](zh/tools/raid.html) | Raid Planner：同时摧毁墙、门和设施所需的炸药、硫磺、材料和熔炉时间 | 服务器数据，以及从服务器代码读出的伤害与冶炼规则 |
| [tools/craft.html](zh/tools/craft.html) | Craft Planner：根据要制作的东西、持有的物资和熔炉，算出还缺什么、熔炉要多久 | 与 Raid Planner 相同的数据 |
| [tools/gene.html](zh/tools/gene.html) | Gene Planner：用手上的幼苗种出接近 GGGYYY 等目标基因的种法，以及基因的效果 | 服务器数据，以及从服务器代码读出的杂交规则 |
| [tools/buff.html](zh/tools/buff.html) | Buff Planner：茶和派的效果有多强、持续到何时，哪个会被替换，熊肉派会让哪些变短 | 服务器数据，以及从服务器代码读出的叠加规则 |
| [tools/ttk.html](zh/tools/ttk.html) | TTK Planner：根据护甲和插板算出各部位的防护，以及每把枪和弓打头、躯干、腿需要几发，每 10 m 一档 | 服务器数据，以及从服务器代码读出的伤害公式 |

## 语言

本月、类别、工具和文章有日语、英语、简体中文、韩语和俄语版本，其他页面（以及本月的全部变更列表）只有日语。第一次打开这些页面时，会跳转到浏览器语言的版本（用语言链接选择后，会记住所选语言）。物品名称在所有语言中都使用游戏的英文名称。更新日志是把官方英文改写成日语的，因此不会再译回其他语言：请阅读 https://rust.facepunch.com/changes 。

| 语言 | 状态 |
|---|---|
| 日本語 | 全部页面 |
| English | 本月、类别、工具、文章和 README |
| 简体中文 | 本月、类别、工具、文章和本 README |
| 한국어 | 本月、类别、工具、文章和 README |
| Русский | 本月、类别、工具、文章和 README |

## 须知

- 与 Facepunch Studios 无关。
- 数值是从游戏的数据和代码中读出的，并非在游戏里实测，不保证正确。
- 本仓库只存放生成的页面，请不要手动修改。
- 部分图标来自 [Lucide](https://lucide.dev/)（ISC License，`LICENSE-lucide.txt`）。未使用游戏的图标或图片。
- 结构图中的标志是各自所有者的商标（图标：svgl、Lucide；用 stack-diagram 绘制）。

## 关于游戏 Rust

Rust 是 Facepunch Studios 开发的多人生存游戏。玩家从海滩开始，手里只有一块石头，需要收集资源、制作工具、建造基地，并与其他玩家合作或争夺。游戏于 2013 年开始抢先体验，2018 年正式发售。每月第一个星期四会有大型更新，本站追踪这些变化。PC 版在 Steam 上发售，PlayStation 和 Xbox 平台则有 Rust Console Edition。

<p><a href="https://store.steampowered.com/app/252490/Rust/"><img src="assets/readme/steam-zh.png" alt="Steam" height="46"></a> &nbsp; <a href="https://rust.facepunch.com/">官方网站: rust.facepunch.com</a></p>
