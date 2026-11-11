# Rust Analysis (公開ページ)

ゲーム Rust (Facepunch Studios) の公式の変更点を日本語にまとめ、アイテムの値を表にした、個人の非公式のサイトです。

**https://maco165.github.io/rust-patch-notes/**

- Facepunch Studios とは関係がありません。
- 変更点は、公式の変更点の一覧 (https://rust.facepunch.com/changes) を自分の言葉で日本語にしたものです。各回に出典のリンクがあります。
- アイテムの値は、サーバー本体のデータから読んだものです。正しさは保証しません。
- このリポジトリには、生成したページだけを置いています。ページを作る仕組みとデータは別の非公開のリポジトリにあります。
- アイコンの一部は [Lucide](https://lucide.dev/) (ISC License。`LICENSE-lucide.txt`) です。ゲームのアイコンや画像は使っていません。

## 構成

```
rust-patch-notes/
├── index.html      今月のアップデートのまとめ
├── history.html    これまでの全パッチの変更点 (ジャンル・年・分類・名前で絞り込み)
├── genres.html     ジャンルごとの件数と年ごとの推移
├── numbers.html    公式の文章に前後の値や割合が書かれた変更
├── items.html      アイテムごとの設定と、版の間の差、変更の履歴
├── spec.html       全アイテムの値を種類ごとの表にしたもの
├── columns.html    コラムの一覧
├── columns/        コラムの記事 (1 本 1 ファイル)
├── assets/         スタイル、ファビコン、共有用の画像
└── sitemap.xml
```

ページはすべて生成物です。直接は編集せず、元のリポジトリで作り直して置き換えます。
