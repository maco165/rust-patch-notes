<p align="center"><a href="https://maco165.github.io/rust-patch-notes/ko/index.html"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/hero-ko-dark.png"><img src="assets/readme/hero-ko.png" alt="Rust Analysis" width="100%"></picture></a></p>

<p align="center"><a href="README.md"><img src="assets/readme/lang-ja.png" alt="日本語" height="40"></a> <a href="README.en.md"><img src="assets/readme/lang-en.png" alt="English" height="40"></a> <a href="README.zh.md"><img src="assets/readme/lang-zh.png" alt="简体中文" height="40"></a> <a href="README.ko.md"><img src="assets/readme/lang-ko-on.png" alt="한국어" height="40"></a> <a href="README.ru.md"><img src="assets/readme/lang-ru.png" alt="Русский" height="40"></a></p>

<p align="center"><b><a href="https://maco165.github.io/rust-patch-notes/ko/index.html">https://maco165.github.io/rust-patch-notes/</a></b></p>

게임 Rust (Facepunch Studios)에 관한 비공식 개인 사이트입니다. 공식 변경 사항을 일본어로 정리하고, 모든 아이템의 수치와 계산기 5개 (레이드, 제작, 식물 유전자, 차와 파이, 몇 발에 쓰러지는지)를 제공합니다. 이번 달, 장르, 도구, 글은 5개 언어로 볼 수 있습니다.

## 이 사이트에 대해

**무엇인가** — 공식 변경 사항과 게임 본체의 데이터와 코드를 읽어 Rust의 작동 방식을 확인하는 비공식 분석 사이트입니다.

**왜 만들었나** — 게임 코드의 변경에서 업데이트 내용과 내부 구조를 정리한 사이트가 없었기 때문입니다.

**강점**

- 코드까지 읽고 확인: 수치만이 아니라 서버 코드 (IL)를 읽어 계산 규칙을 확인하고, 계산기는 예제와 전수 검사로 검증합니다
- 2015년부터의 전체 기록과 매달 업데이트: 2015년부터의 모든 변경 사항과 월별 판의 아이템 설정 차이
- 5개 언어, 브라우저만, 무료: 일본어, 영어, 중국어, 한국어, 러시아어로 볼 수 있고, 가입도 광고도 없이 브라우저 안에서만 작동합니다

**원칙** — 확인한 것만 씁니다. 확인하지 않은 것은 '미확인'이라고 씁니다.

**검토** — 모든 변경은 공개 전에 Anthropic의 AI 'Claude'가 차이를 확인하고 사람이 승인합니다.

## 화면

<table><tr><td colspan="2" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ko/index.html"><img src="assets/readme/shot-ko-month.png" alt="이번 달"></a><br><sub><b>이번 달</b></sub></td></tr><tr><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ko/tools/raid.html"><img src="assets/readme/shot-ko-raid.png" alt="Raid Planner"></a><br><sub><b>Raid Planner</b></sub></td><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ko/tools/gene.html"><img src="assets/readme/shot-ko-gene.png" alt="Gene Planner"></a><br><sub><b>Gene Planner</b></sub></td></tr><tr><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ko/tools/buff.html"><img src="assets/readme/shot-ko-buff.png" alt="Buff Planner"></a><br><sub><b>Buff Planner</b></sub></td><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ko/tools/ttk.html"><img src="assets/readme/shot-ko-ttk.png" alt="TTK Planner"></a><br><sub><b>TTK Planner</b></sub></td></tr></table>

## 시스템 구성

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/arch-dark.png"><img src="assets/readme/arch.png" alt="Rust Analysis: sources, Python scripts, data, build_site.py, GitHub Pages" width="100%"></picture></p>

## 언어

이번 달, 장르, 도구, 글은 일본어, 영어, 중국어(간체), 한국어, 러시아어로 볼 수 있고, 다른 페이지(와 이번 달의 전체 변경 목록)는 일본어뿐입니다. 이 페이지들은 처음 열 때 브라우저 언어의 판으로 이동합니다(언어 링크로 고르면 그 언어를 기억합니다). 아이템 이름은 모든 언어에서 게임의 영어 이름입니다. 변경 사항은 공식 영어 문장을 일본어로 옮긴 것이라 다른 언어로 옮기지 않습니다. https://rust.facepunch.com/changes 를 보세요.

## 알아 둘 점

- Facepunch Studios와 관계가 없습니다.
- 수치는 게임의 데이터와 코드에서 읽은 것이며, 게임 안에서 측정한 것이 아닙니다. 정확함을 보장하지 않습니다.
- 이 저장소에는 생성된 페이지만 있습니다. 직접 고치지 마세요.
- 일부 아이콘은 [Lucide](https://lucide.dev/) (ISC License, `LICENSE-lucide.txt`)입니다. 게임의 아이콘이나 이미지는 쓰지 않았습니다.
- 구성도의 로고는 각 소유자의 상표입니다 (아이콘: svgl, Lucide. stack-diagram으로 작성).

## 게임 Rust 소개

Rust는 Facepunch Studios가 개발한 멀티플레이 생존 게임입니다. 돌 하나만 든 채 해변에서 시작해 자원을 모으고, 도구를 만들고, 기지를 지으며 다른 플레이어와 협력하거나 빼앗습니다. 2013년에 앞서 해보기로 시작해 2018년에 정식 출시되었습니다. 게임과 서버는 Unity 엔진 위에서 C#으로 만들어져 있습니다. 매달 첫째 목요일에 큰 업데이트가 있으며, 이 사이트는 그 변화를 따라갑니다. PC판은 Steam에서, PlayStation과 Xbox용으로는 Rust Console Edition이 있습니다.

<p><a href="https://store.steampowered.com/app/252490/Rust/"><img src="assets/readme/steam-ko.png" alt="Steam" height="46"></a></p>

### 무엇으로 돌아가나

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/engine-dark.png"><img src="assets/readme/engine.png" alt="Rust: C# code (Assembly-CSharp, Rust.*, Facepunch.*) on the Unity 6 engine" width="100%"></picture></p>

게임과 서버는 Unity 6 위에서 돌아가는 C# 프로그램입니다. 전용 서버 (RustDedicated, 2026-10-22 판)의 C# 구성 요소 (DLL)로 확인했으며, Unity 버전은 공식 변경 사항 (2026-11-05: 6000.3.26f1)에 따릅니다.

### 공식 링크

- [공식 사이트: rust.facepunch.com](https://rust.facepunch.com/)
- [업데이트 정보 (공식 변경 사항)](https://rust.facepunch.com/changes)
- [뉴스](https://rust.facepunch.com/news)
- [개발 커밋 로그](https://commits.facepunch.com/r/rust_reboot)

