#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arkth 限定公開スライドサイト ビルダー。
slide/ の pptx を soffice でPDF化（intermediate/）→ PyMuPDF で assets/deck/*.jpg に書き出し、
自己完結HTMLスライド（矢印キー操作・外部依存なし・noindex・PWゲート）を生成する。
canpass-training-site/build.py を踏襲。

再生成: python3 build.py
前提: soffice / PyMuPDF(fitz) 利用可。
"""
import os, glob, subprocess, fitz

ROOT = os.path.dirname(os.path.abspath(__file__))
PJ = os.path.dirname(ROOT)
PPTX = os.path.join(PJ, "slide", "20260701_arkth-support-and-strategy_v1.pptx")
INTER = os.path.join(PJ, "intermediate")
PDF = os.path.join(INTER, "20260701_arkth-support-and-strategy_v1.pdf")
PASSWORD = "arkth2026"  # 軽いゲート（限定URL+noindexと併用）。真のアクセス制御ではない。

DECK = {"key": "deck",
        "title": "Arkth 幹部代行サポート 仮案＋競合に勝つ戦略",
        "note": "新屋さん限定・議論用たたき台（最終版ではない）"}


def ensure_pdf():
    need = (not os.path.exists(PDF)) or (os.path.getmtime(PPTX) > os.path.getmtime(PDF))
    if need:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", INTER, PPTX], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return PDF


def render():
    out = os.path.join(ROOT, "assets", DECK["key"])
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, "*.jpg")):
        os.remove(f)
    d = fitz.open(PDF)
    n = d.page_count
    for i in range(n):
        d[i].get_pixmap(matrix=fitz.Matrix(1.7, 1.7)).save(os.path.join(out, f"{i+1:02d}.jpg"))
    d.close()
    return n


DECK_HTML = """<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{title}</title>
<style>
:root{{--bg:#0b1426;--ink:#14213a;--muted:#6b7c92;--line:#d6e0ec;--accent:#2e6be6}}
*{{box-sizing:border-box}}html,body{{margin:0;height:100%}}
body{{background:var(--bg);font-family:'Hiragino Kaku Gothic ProN','Yu Gothic',sans-serif;color:#fff;overflow:hidden}}
#gate{{position:fixed;inset:0;background:#0b1426;display:flex;align-items:center;justify-content:center;z-index:10}}
#gate .box{{background:#fff;color:var(--ink);padding:28px 26px;border-radius:14px;max-width:340px;width:88%;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.4)}}
#gate h1{{font-size:18px;margin:0 0 4px}}#gate p{{font-size:12px;color:var(--muted);margin:0 0 16px;line-height:1.6}}
#gate input{{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:8px;font-size:15px;margin-bottom:10px}}
#gate button{{width:100%;padding:11px;border:0;border-radius:8px;background:var(--accent);color:#fff;font-size:15px;cursor:pointer}}
#gate .err{{color:#b23b3b;font-size:12px;height:14px;margin-top:6px}}
#app{{display:none;height:100%;flex-direction:column}}
#stage{{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;padding:14px}}
#stage img{{max-width:100%;max-height:100%;border-radius:6px;box-shadow:0 6px 30px rgba(0,0,0,.5)}}
#bar{{display:flex;align-items:center;justify-content:center;gap:18px;padding:8px 14px;background:#070f1d;font-size:13px;color:#9fb1c8}}
#bar button{{background:#1c3257;color:#fff;border:0;border-radius:6px;padding:7px 14px;font-size:14px;cursor:pointer}}
#bar a{{color:#9fb1c8;text-decoration:none;font-size:12px}}
#count{{min-width:64px;text-align:center}}
</style></head><body>
<div id="gate"><form class="box" onsubmit="return unlock(event)">
<h1>Arkth サポート資料</h1><p>{note}<br>閲覧パスワードを入力してください</p>
<input id="pw" type="password" autocomplete="off" placeholder="パスワード" autofocus>
<button type="submit">開く</button><div class="err" id="err"></div></form></div>
<div id="app">
<div id="stage"><img id="slide" alt="slide"></div>
<div id="bar">
<a href="./index.html">&#8592; 一覧</a>
<button onclick="go(-1)">&#8249; 前</button><span id="count"></span><button onclick="go(1)">次 &#8250;</button>
<span style="color:#5d7088">{title}</span>
</div></div>
<script>
var N={n},i=0,dir="assets/{key}/";
function pad(x){{return (x<10?'0':'')+x}}
function show(){{document.getElementById('slide').src=dir+pad(i+1)+'.jpg';document.getElementById('count').textContent=(i+1)+' / '+N}}
function go(d){{i=Math.max(0,Math.min(N-1,i+d));show()}}
function open_(){{document.getElementById('gate').style.display='none';document.getElementById('app').style.display='flex';show()}}
function unlock(e){{e.preventDefault();if(document.getElementById('pw').value==='{password}'){{sessionStorage.setItem('ak_ok','1');open_()}}else{{document.getElementById('err').textContent='パスワードが違います'}}return false}}
if(sessionStorage.getItem('ak_ok')==='1'){{open_()}}
document.addEventListener('keydown',function(e){{if(document.getElementById('app').style.display==='none')return;if(e.key==='ArrowRight'||e.key===' ')go(1);if(e.key==='ArrowLeft')go(-1)}});
document.getElementById('stage').addEventListener('click',function(){{go(1)}});
</script></body></html>"""


INDEX_HTML = """<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Arkth 幹部代行サポート 資料</title>
<style>
:root{{--bg:#0b1426;--ink:#14213a;--muted:#6b7c92;--line:#d6e0ec;--accent:#2e6be6}}
*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;background:var(--bg);font-family:'Hiragino Kaku Gothic ProN','Yu Gothic',sans-serif;color:#fff;display:flex;align-items:center;justify-content:center;padding:24px}}
#gate{{position:fixed;inset:0;background:#0b1426;display:flex;align-items:center;justify-content:center;z-index:10}}
.box{{background:#fff;color:var(--ink);padding:28px 26px;border-radius:14px;max-width:340px;width:88%;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.4)}}
.box h1{{font-size:18px;margin:0 0 4px}}.box p{{font-size:12px;color:var(--muted);margin:0 0 16px;line-height:1.6}}
.box input{{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:8px;font-size:15px;margin-bottom:10px}}
.box button{{width:100%;padding:11px;border:0;border-radius:8px;background:var(--accent);color:#fff;font-size:15px;cursor:pointer}}
.err{{color:#b23b3b;font-size:12px;height:14px;margin-top:6px}}
#app{{display:none;max-width:680px;width:100%}}
.kicker{{color:#9fb1c8;font-size:12px;letter-spacing:.12em}}
h2{{font-size:26px;margin:6px 0 2px}}.sub{{color:#9fb1c8;font-size:13px;margin-bottom:22px;line-height:1.6}}
.card{{display:block;background:#13294a;border:1px solid #24446c;border-radius:12px;padding:18px 20px;margin-bottom:14px;text-decoration:none;color:#fff}}
.card:hover{{background:#183356}}
.card .t{{font-size:17px;font-weight:700}}.card .d{{font-size:12px;color:#9fb1c8;margin-top:4px;line-height:1.6}}
.tag{{display:inline-block;font-size:11px;padding:2px 8px;border-radius:10px;background:#070f1d;color:#9fb1c8;margin-left:8px}}
.foot{{color:#6b7c92;font-size:11px;margin-top:18px;line-height:1.7}}
</style></head><body>
<div id="gate"><form class="box" onsubmit="return unlock(event)">
<h1>Arkth 幹部代行サポート 資料</h1><p>新屋さん限定（議論用たたき台）<br>閲覧パスワードを入力してください</p>
<input id="pw" type="password" autocomplete="off" placeholder="パスワード" autofocus>
<button type="submit">開く</button><div class="err" id="err"></div></form></div>
<div id="app">
<div class="kicker">ARKTH &#215; SECOND ｜ 限定公開</div>
<h2>幹部代行サポート 仮案</h2>
<div class="sub">2026-07 ｜ 確定案ではなく、新屋さんと議論するためのたたき台。</div>
<a class="card" href="./deck.html"><div class="t">幹部代行サポート 仮案＋競合に勝つ戦略<span class="tag">全15枚</span></div><div class="d">現状と課題の整理／支援3テーマ（経営アジェンダ・リード・採用）／競合に勝つ戦略3観点（事業・採用・組織）／90日ロードマップ／論点</div></a>
<div class="foot">取り扱い：本資料は議論用のたたき台で限定公開（推測されにくいURL＋パスワード＋noindex。厳密なアクセス制御ではない）。数字は公開情報ベースで本人確認前のものを含む。戦略は仮案で、新屋さんと話して変える前提。</div>
</div>
<script>
function unlock(e){{e.preventDefault();if(document.getElementById('pw').value==='{password}'){{sessionStorage.setItem('ak_ok','1');document.getElementById('gate').style.display='none';document.getElementById('app').style.display='block'}}else{{document.getElementById('err').textContent='パスワードが違います'}}return false}}
if(sessionStorage.getItem('ak_ok')==='1'){{document.getElementById('gate').style.display='none';document.getElementById('app').style.display='block'}}
</script></body></html>"""


def main():
    ensure_pdf()
    n = render()
    with open(os.path.join(ROOT, "deck.html"), "w", encoding="utf-8") as f:
        f.write(DECK_HTML.format(title=DECK["title"], note=DECK["note"], n=n,
                                 key=DECK["key"], password=PASSWORD))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_HTML.format(password=PASSWORD))
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nDisallow: /\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    print(f"deck: {n} slides / index.html / deck.html / robots.txt / .nojekyll written")


if __name__ == "__main__":
    main()
