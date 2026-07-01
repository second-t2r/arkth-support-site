# arkth-support-site

Arkth 幹部代行サポート 仮案＋競合に勝つ戦略（新屋さん限定・議論用たたき台）のHTMLスライド限定公開サイト。

- 様式: セコンド標準デザイン（B2B・ネイビー基調＋アクセント1色）。`canpass-training-site` と同じHTML化・公開パターン。
- 限定公開の方式: 推測されにくいURL ＋ パスワードゲート（クライアント側JS）＋ `noindex` ＋ `robots.txt`。
  - ⚠ 厳密なアクセス制御ではない。パスワードはHTMLソースに含まれ、画像の直URLは技術的に取得可能。実名・競合戦略を含むため取り扱い注意。
- 中身は最終版ではなく、新屋さんと議論して変える前提の仮案。数字は公開情報ベースで本人確認前のものを含む。

## 構成
- `index.html` … 資料一覧（PWゲート）
- `deck.html` … スライドビューア（矢印キー／クリックで送り）
- `assets/deck/*.jpg` … スライド画像（全15枚）
- `robots.txt` / `.nojekyll` … 検索除外・Jekyll無効化

## 再生成
元PPTX（`../slide/20260701_arkth-support-and-strategy_v1.pptx`）を更新後:

```bash
python3 build.py   # soffice でPDF化 → PyMuPDFでJPG化 → HTML生成
git add -A && git commit -m "update" && git push
```

閲覧パスワードは `build.py` の `PASSWORD` を参照。
