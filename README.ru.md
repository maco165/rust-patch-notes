<p align="center"><a href="https://maco165.github.io/rust-patch-notes/ru/index.html"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/hero-ru-dark.png"><img src="assets/readme/hero-ru.png" alt="Rust Analysis" width="100%"></picture></a></p>

<p align="center"><a href="README.md"><img src="assets/readme/lang-ja.png" alt="日本語" height="40"></a> <a href="README.en.md"><img src="assets/readme/lang-en.png" alt="English" height="40"></a> <a href="README.zh.md"><img src="assets/readme/lang-zh.png" alt="简体中文" height="40"></a> <a href="README.ko.md"><img src="assets/readme/lang-ko.png" alt="한국어" height="40"></a> <a href="README.ru.md"><img src="assets/readme/lang-ru-on.png" alt="Русский" height="40"></a></p>

<p align="center"><b><a href="https://maco165.github.io/rust-patch-notes/ru/index.html">https://maco165.github.io/rust-patch-notes/</a></b></p>

Неофициальный сайт одного автора об игре Rust (Facepunch Studios): официальные списки изменений, пересказанные на японском, значения всех предметов и пять калькуляторов (рейд, крафт, гены растений, чаи и пироги, число попаданий до смерти). Этот месяц, категории, инструменты и статьи доступны на пяти языках.

## О сайте

**Что это** — Неофициальный аналитический сайт: он читает официальные списки изменений, данные и код самой игры, чтобы проверить, как устроен Rust.

**Зачем** — Не было сайта, который по изменениям в коде игры собирал бы содержание обновлений и внутреннее устройство.

**Сильные стороны**

- Читаем до кода: не только значения, но и код сервера (IL), чтобы проверить правила расчёта; калькуляторы проверены на примерах и полным перебором
- Вся история с 2015 года и ежемесячные обновления: все патчи с 2015 года и различия настроек предметов по месячным сборкам
- Пять языков, только браузер, бесплатно: японский, английский, китайский, корейский и русский, без регистрации и рекламы, всё работает в браузере

**Принцип** — Пишем только то, что проверено. Непроверенное помечаем как неподтверждённое.

**Проверка** — Каждое изменение перед публикацией проверяет по диффу Claude — ИИ от Anthropic, — и одобряет человек.

## Экраны

<table><tr><td colspan="2" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ru/index.html"><img src="assets/readme/shot-ru-month.png" alt="Этот месяц"></a><br><sub><b>Этот месяц</b></sub></td></tr><tr><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ru/tools/raid.html"><img src="assets/readme/shot-ru-raid.png" alt="Raid Planner"></a><br><sub><b>Raid Planner</b></sub></td><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ru/tools/gene.html"><img src="assets/readme/shot-ru-gene.png" alt="Gene Planner"></a><br><sub><b>Gene Planner</b></sub></td></tr><tr><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ru/tools/buff.html"><img src="assets/readme/shot-ru-buff.png" alt="Buff Planner"></a><br><sub><b>Buff Planner</b></sub></td><td width="50%" valign="top"><a href="https://maco165.github.io/rust-patch-notes/ru/tools/ttk.html"><img src="assets/readme/shot-ru-ttk.png" alt="TTK Planner"></a><br><sub><b>TTK Planner</b></sub></td></tr></table>

## Устройство системы

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/arch-dark.png"><img src="assets/readme/arch.png" alt="Rust Analysis: sources, Python scripts, data, build_site.py, GitHub Pages" width="100%"></picture></p>

## Языки

Этот месяц, категории, инструменты и статьи есть на японском, английском, китайском (упрощённом), корейском и русском, остальные страницы (и список всех изменений месяца) — только на японском. При первом открытии эти страницы переходят на язык браузера (язык, выбранный ссылкой, запоминается). Названия предметов на всех языках — английские названия из игры. Списки изменений — это официальный английский текст, пересказанный на японском, поэтому на другие языки их не переводим: читайте https://rust.facepunch.com/changes.

## Важно знать

- Не связан с Facepunch Studios.
- Значения прочитаны из данных и кода игры, а не измерены в игре. Их правильность не гарантируется.
- В этом репозитории только сгенерированные страницы. Не правьте их вручную.
- Часть иконок — из [Lucide](https://lucide.dev/) (ISC License, `LICENSE-lucide.txt`). Иконки и изображения игры не используются.
- Логотипы на схеме — товарные знаки их владельцев (иконки: svgl, Lucide; схема сделана stack-diagram).

## Об игре Rust

Rust — многопользовательская игра на выживание от Facepunch Studios. Вы начинаете на берегу с одним камнем в руках, добываете ресурсы, создаёте инструменты, строите базу и объединяетесь с другими игроками или сражаетесь с ними. Игра вышла в раннем доступе в 2013 году и полностью — в 2018-м. Игра и сервер написаны на C# на движке Unity. В первый четверг каждого месяца выходит крупное обновление, и этот сайт следит за этими изменениями. Версия для ПК — в Steam, для PlayStation и Xbox есть Rust Console Edition.

<p><a href="https://store.steampowered.com/app/252490/Rust/"><img src="assets/readme/steam-ru.png" alt="Steam" height="46"></a></p>

### На чём работает

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme/engine-dark.png"><img src="assets/readme/engine.png" alt="Rust: C# code (Assembly-CSharp, Rust.*, Facepunch.*) on the Unity 6 engine" width="100%"></picture></p>

Игра и сервер — программы на C# поверх Unity 6. Проверено по сборкам C# (DLL) выделенного сервера (RustDedicated, сборка 2026-10-22); версия Unity — из официального списка изменений (2026-11-05: 6000.3.26f1).

### Официальные ссылки

- [Официальный сайт: rust.facepunch.com](https://rust.facepunch.com/)
- [Обновления (официальные изменения)](https://rust.facepunch.com/changes)
- [Новости](https://rust.facepunch.com/news)
- [Журнал коммитов разработки](https://commits.facepunch.com/r/rust_reboot)

