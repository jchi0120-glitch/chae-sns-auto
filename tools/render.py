"""채팀장 인스타 카드뉴스 렌더러 (1080x1350, 4:5)
사용: python3 render.py slides.json out_dir
slides.json = {"handle": "...", "slides": [{"body": "<html>"}, ...]}
"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright

FONT = "/tmp/fonts/package/dist/public/static"
CSS = f"""
@font-face{{font-family:P;src:url(file://{FONT}/Pretendard-Medium.otf);font-weight:500}}
@font-face{{font-family:P;src:url(file://{FONT}/Pretendard-Bold.otf);font-weight:700}}
@font-face{{font-family:P;src:url(file://{FONT}/Pretendard-ExtraBold.otf);font-weight:800}}
@font-face{{font-family:P;src:url(file://{FONT}/Pretendard-Black.otf);font-weight:900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;font-family:P,"Noto Sans CJK KR",sans-serif;color:#fff;letter-spacing:-0.02em;
 background:radial-gradient(900px 700px at 85% 0%,rgba(70,214,130,.18),transparent 60%),
 radial-gradient(800px 600px at 0% 100%,rgba(214,236,96,.08),transparent 60%),#0b0f17;
 position:relative;overflow:hidden}}
.top{{position:absolute;top:56px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:700;color:rgba(255,255,255,.55)}}
.page{{background:rgba(255,255,255,.08);border-radius:40px;padding:8px 22px}}
.foot{{position:absolute;bottom:56px;left:72px;right:72px;display:flex;justify-content:space-between;font-size:26px;font-weight:700;color:rgba(255,255,255,.45)}}
.foot b{{color:#46D682}}
.wrap{{position:absolute;top:150px;left:72px;right:72px;bottom:140px;display:flex;flex-direction:column;justify-content:center}}
.tag{{display:inline-block;align-self:flex-start;background:linear-gradient(90deg,#46D682,#D6EC60);color:#0f1a14;font-weight:900;font-size:30px;padding:12px 28px;border-radius:40px;margin-bottom:34px}}
h1{{font-size:84px;font-weight:900;line-height:1.18;margin-bottom:30px}}
h2{{font-size:66px;font-weight:900;line-height:1.22;margin-bottom:40px}}
.g{{background:linear-gradient(90deg,#46D682,#D6EC60);-webkit-background-clip:text;color:transparent}}
.sub{{font-size:38px;font-weight:700;line-height:1.5;color:rgba(255,255,255,.82)}}
.panel{{background:rgba(22,30,48,.88);border:2px solid rgba(255,255,255,.14);border-radius:28px;padding:34px 40px;margin-bottom:22px}}
.panel.hl{{border:4px solid #46D682}}
.panel .t{{font-size:40px;font-weight:900;margin-bottom:12px}}
.panel .d{{font-size:32px;font-weight:500;line-height:1.5;color:rgba(255,255,255,.8)}}
.pill{{display:inline-block;background:linear-gradient(180deg,#fff,#d9dce2);color:#111827;font-weight:900;border-radius:16px;padding:4px 16px}}
table{{width:100%;border-collapse:separate;border-spacing:0;font-size:29px;background:rgba(22,30,48,.88);border-radius:24px;overflow:hidden;border:2px solid rgba(255,255,255,.14)}}
th,td{{padding:19px 14px;text-align:center;border-bottom:1px solid rgba(255,255,255,.1);font-weight:700}}
th{{font-size:31px;font-weight:900;background:rgba(70,214,130,.16)}}
th.r{{color:#46D682}}
td:first-child{{color:rgba(255,255,255,.6);font-weight:800;text-align:left;padding-left:26px}}
tr:last-child td{{border-bottom:none}}
.row{{display:flex;align-items:center;gap:20px;background:rgba(22,30,48,.88);border:2px solid rgba(255,255,255,.14);border-radius:22px;padding:24px 30px;margin-bottom:16px;font-size:32px;font-weight:700}}
.row .s{{flex:1;line-height:1.35}}
.row .a{{background:linear-gradient(90deg,#46D682,#D6EC60);color:#0f1a14;font-weight:900;border-radius:30px;padding:10px 22px;font-size:29px;white-space:nowrap}}
.steps{{display:flex;flex-direction:column;gap:18px}}
.step{{display:flex;align-items:center;gap:28px;background:rgba(22,30,48,.88);border:2px solid rgba(255,255,255,.14);border-radius:24px;padding:28px 34px}}
.step .n{{width:78px;height:78px;border-radius:50%;background:linear-gradient(135deg,#46D682,#D6EC60);color:#0f1a14;font-weight:900;font-size:38px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.step .t{{font-size:42px;font-weight:900}}
.step .d{{font-size:29px;font-weight:500;color:rgba(255,255,255,.7);margin-top:6px}}
.two{{display:flex;gap:22px}}
.two .panel{{flex:1}}
.swipe{{margin-top:60px;font-size:32px;font-weight:800;color:#46D682}}
.btn{{display:inline-block;align-self:flex-start;background:linear-gradient(90deg,#46D682,#D6EC60);color:#0f1a14;font-weight:900;font-size:44px;padding:28px 48px;border-radius:60px;margin-top:40px;box-shadow:0 12px 30px rgba(70,214,130,.3)}}
.note{{font-size:25px;color:rgba(255,255,255,.45);margin-top:26px;font-weight:500}}
"""

def page(handle, i, n, body):
    return f"""<html><head><meta charset=utf-8><style>{CSS}</style></head><body>
<div class=top><span>{handle}</span><span class=page>{i}/{n}</span></div>
<div class=wrap>{body}</div>
<div class=foot><span><b>채팀장</b> 차량컨설턴트</span><span>14년차 · 누적출고 1,600대+</span></div>
</body></html>"""

def main(src, out):
    data = json.loads(pathlib.Path(src).read_text())
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    slides = data["slides"]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(slides, 1):
            f = out / "_tmp.html"; f.write_text(page(data["handle"], i, len(slides), s["body"]))
            pg.goto(f"file://{f.resolve()}"); pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(out / f"card_{i:02d}.jpg"), type="jpeg", quality=92)
        b.close()
    (out / "_tmp.html").unlink(missing_ok=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
