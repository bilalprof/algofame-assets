#!/usr/bin/env python3
"""Render 'The last mile' series cards in the First Principles visual system.

Geometry, colours and type sizes were measured off
series/first-principles/10-what-it-is-all-for.jpg (2400x2400).
"""
import base64
import html
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
# Inter is not vendored. Fetch it once:
#   curl -L -o /tmp/inter.zip https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip
#   unzip -q /tmp/inter.zip -d /tmp/inter
INTER = pathlib.Path(os.environ.get('INTER_TTF', '/tmp/inter/extras/ttf'))
LOGO = HERE / 'fame-logo.png'

TOTAL = 5
SERIES_LABEL = 'THE LAST MILE'
FOOTER_RIGHT = 'A five part series on the last mile'


def b64(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def font_face(name, weight, file):
    return (f"@font-face{{font-family:'{name}';font-weight:{weight};font-style:normal;"
            f"src:url({b64(INTER / file, 'font/ttf')}) format('truetype');}}")


def hexagon(w, h, fill, opacity=1.0, stroke=None, dot=False):
    """Flat-top hexagon matching the season-1 mark."""
    pts = '50,0 100,25 100,75 50,100 0,75 0,25'
    if stroke:
        body = f'<polygon points="{pts}" fill="none" stroke="{stroke}" stroke-width="1.4"/>'
    else:
        body = f'<polygon points="{pts}" fill="{fill}"/>'
    if dot:
        body += '<circle cx="50" cy="50" r="7.5" fill="#fff"/>'
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 100 100" '
            f'style="opacity:{opacity}" preserveAspectRatio="none">{body}</svg>')


def progress(active):
    dots = []
    for i in range(1, TOTAL + 1):
        if i == active:
            dots.append('<span class="dot on">' + hexagon(44, 48, 'url(#g)') + '</span>')
        else:
            dots.append('<span class="dot">' + hexagon(34, 38, '#ffffff', 0.30) + '</span>')
    return (f'<div class="dots">{"".join(dots)}'
            f'<span class="count">0{active} / 0{TOTAL}</span></div>')


def build(card):
    faces = ''.join([
        font_face('Inter', 400, 'Inter-Regular.ttf'),
        font_face('Inter', 500, 'Inter-Medium.ttf'),
        font_face('Inter', 600, 'Inter-SemiBold.ttf'),
        font_face('Inter', 700, 'Inter-Bold.ttf'),
    ])
    kicker_a, kicker_b = card['kicker']
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:2400px;height:2400px}}
body{{
  font-family:'Inter',sans-serif;
  background:
    radial-gradient(ellipse 92% 78% at 0% 0%, #401686 0%, rgba(64,22,134,0) 62%),
    radial-gradient(ellipse 72% 62% at 100% 100%, #06415f 0%, rgba(6,65,95,0) 58%),
    #0a0917;
  color:#fff;position:relative;overflow:hidden;
}}
.logo{{position:absolute;left:146px;top:130px;width:223px;height:73px}}
.series{{position:absolute;right:144px;top:152px;font-size:24px;font-weight:600;
  letter-spacing:.32em;color:rgba(255,255,255,.42)}}
.dots{{position:absolute;left:144px;top:252px;display:flex;align-items:center;gap:11px;height:48px}}
.dot{{display:flex;align-items:center;justify-content:center;width:44px;height:48px}}
.count{{margin-left:26px;font-size:26px;font-weight:700;letter-spacing:.18em;
  color:rgba(255,255,255,.45)}}
.head{{position:absolute;left:150px;top:360px;display:flex;align-items:baseline;gap:64px}}
.num{{font-size:184px;font-weight:700;line-height:.78;
  background:linear-gradient(180deg,#8a86ff 0%,#3ac2ff 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent}}
.title{{font-size:88px;font-weight:700;letter-spacing:-.015em;line-height:1}}
.stage{{position:absolute;left:144px;right:144px;top:830px;height:950px}}
.rule{{position:absolute;left:144px;right:144px;top:2028px;height:1px;
  background:rgba(255,255,255,.13)}}
.kicker{{position:absolute;left:144px;top:2062px;font-size:52px;font-weight:700;
  letter-spacing:-.01em}}
.kicker .b{{background:linear-gradient(90deg,#8a86ff 0%,#3ac2ff 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent}}
.f-left{{position:absolute;left:144px;top:2152px;font-size:34px;font-weight:700}}
.f-right{{position:absolute;right:144px;top:2154px;font-size:30px;font-weight:600;
  color:rgba(255,255,255,.32)}}
/* diagram idiom */
.lbl{{font-size:30px;font-weight:700;letter-spacing:.16em;color:rgba(255,255,255,.62);
  text-transform:uppercase;white-space:nowrap}}
.lbl.dim{{color:rgba(255,255,255,.34)}}
{card.get('css','')}
</style></head><body>
<svg width="0" height="0"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#8a86ff"/><stop offset="1" stop-color="#3ac2ff"/>
</linearGradient>
<linearGradient id="gh" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#8a86ff"/><stop offset="1" stop-color="#3ac2ff"/>
</linearGradient></defs></svg>
<img class="logo" src="{b64(LOGO,'image/png')}">
<div class="series">{SERIES_LABEL}</div>
{progress(card['n'])}
<div class="head"><div class="num">0{card['n']}</div><div class="title">{html.escape(card['title'])}</div></div>
<div class="stage">{card['stage']}</div>
<div class="rule"></div>
<div class="kicker">{html.escape(kicker_a)} <span class="b">{html.escape(kicker_b)}</span></div>
<div class="f-left">algofame.org</div>
<div class="f-right">{FOOTER_RIGHT}</div>
</body></html>"""


# ---------------------------------------------------------------- card 1
# Stage is 2112 wide (2400 minus the 144px margins), origin at x=144,y=830.
# Positions mirror the measured geometry of card 10 of season 1.
CARD1_CSS = """
.ghosthex{position:absolute;left:882px;top:10px}
.ghostcap{position:absolute;left:0;right:0;top:352px;text-align:center}
.hexL{position:absolute;left:402px;top:446px}
.hexR{position:absolute;left:1362px;top:446px}
.wire{position:absolute;left:672px;width:690px;top:592px;height:3px;
  background:linear-gradient(90deg,#8a86ff,#3ac2ff)}
.over{position:absolute;left:0;right:0;top:500px;text-align:center}
.under{position:absolute;left:0;right:0;top:672px;text-align:center}
.capL{position:absolute;left:187px;width:700px;top:790px;text-align:center}
.capR{position:absolute;left:1147px;width:700px;top:790px;text-align:center}
"""

CARD1_STAGE = f"""
<div class="ghosthex">{hexagon(264, 300, 'none', 1, 'rgba(255,255,255,.15)')}</div>
<div class="ghostcap"><span class="lbl dim">The three locks</span></div>
<div class="hexL">{hexagon(270, 296, 'url(#g)', dot=True)}</div>
<div class="hexR">{hexagon(270, 296, 'url(#g)', dot=True)}</div>
<div class="wire"></div>
<div class="over"><span class="lbl">0.9 to 1.9 percent, whole journey</span></div>
<div class="under"><span class="lbl dim">Fame takes nothing at the counter</span></div>
<div class="capL"><span class="lbl">A number on a ledger</span></div>
<div class="capR"><span class="lbl">Cash in her hand</span></div>
"""

# ---------------------------------------------------------------- card 2
CARD2_CSS = CARD1_CSS + """
.chips{position:absolute;left:672px;width:690px;top:498px;display:flex;
  justify-content:center;gap:14px}
.chip{border:1.4px solid rgba(255,255,255,.22);border-radius:999px;padding:12px 22px;
  font-size:24px;font-weight:700;letter-spacing:.12em;color:rgba(255,255,255,.70);
  text-transform:uppercase;white-space:nowrap}
"""

CARD2_STAGE = f"""
<div class="ghosthex">{hexagon(264, 300, 'none', 1, 'rgba(255,255,255,.15)')}</div>
<div class="ghostcap"><span class="lbl dim">The counter, tomorrow morning</span></div>
<div class="hexL">{hexagon(270, 296, 'url(#g)', dot=True)}</div>
<div class="hexR">{hexagon(270, 296, 'url(#g)', dot=True)}</div>
<div class="wire"></div>
<div class="chips"><span class="chip">One agent</span><span class="chip">One day</span>
  <span class="chip">One limit</span></div>
<div class="under"><span class="lbl dim">Revocable until it is used</span></div>
<div class="capL"><span class="lbl">A guardian</span></div>
<div class="capR"><span class="lbl">One withdrawal</span></div>
"""

# ---------------------------------------------------------------- card 3
CARD3_CSS = """
.cols{position:absolute;left:0;right:0;top:60px;display:flex;justify-content:center;gap:150px}
.col{width:840px;border:1.4px solid rgba(255,255,255,.13);border-radius:44px;
  padding:64px 60px 58px;display:flex;flex-direction:column;align-items:center;gap:36px}
.col.final{border-color:rgba(138,134,255,.42)}
.who{font-size:30px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;
  color:rgba(255,255,255,.42)}
.act{font-size:58px;font-weight:700;letter-spacing:-.01em;text-align:center;line-height:1.16}
.state{font-size:29px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.state.ok{color:#3ac2ff}
.state.no{color:rgba(255,255,255,.42)}
.note{font-size:28px;font-weight:500;line-height:1.45;color:rgba(255,255,255,.46);
  text-align:center}
"""

CARD3_STAGE = f"""
<div class="cols">
  <div class="col">
    <div class="who">A guardian can</div>
    {hexagon(150, 164, 'url(#g)', dot=True)}
    <div class="act">Cut off the agent<br>she is standing at</div>
    <div class="state ok">Reversible</div>
    <div class="note">The vault carries forward. The same four digits<br>work at any other shop tomorrow.</div>
  </div>
  <div class="col final">
    <div class="who">Only the member can</div>
    {hexagon(150, 164, 'url(#g)', dot=True)}
    <div class="act">End the<br>assisted tier</div>
    <div class="state no">Final</div>
    <div class="note">From her own session, and nowhere else.<br>Nobody can do this on her behalf.</div>
  </div>
</div>
"""

# ---------------------------------------------------------------- card 4
CARD4_CSS = """
.bars{position:absolute;left:60px;right:60px;top:120px;display:flex;flex-direction:column;gap:74px}
.bar .top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:26px}
.bar .name{font-size:36px;font-weight:700}
.bar .name span{font-weight:500;color:rgba(255,255,255,.40);font-size:31px}
.bar .val{font-size:36px;font-weight:700;letter-spacing:.02em}
.track{height:30px;border-radius:999px;background:rgba(255,255,255,.07)}
.fill{height:30px;border-radius:999px}
.them .val{color:#ff8a5c}
.them .fill{background:linear-gradient(90deg,#f97a4d,#e04a63)}
.us .val{color:#3ac2ff}
.us .fill{background:linear-gradient(90deg,#8a86ff,#3ac2ff)}
.src{position:absolute;left:60px;right:60px;top:760px;font-size:26px;font-weight:500;
  color:rgba(255,255,255,.30)}
"""


def bar(cls, name, sub, val, pct):
    return f"""<div class="bar {cls}"><div class="top">
      <div class="name">{name} <span>{sub}</span></div><div class="val">{val}</div></div>
      <div class="track"><div class="fill" style="width:{pct}%"></div></div></div>"""


CARD4_STAGE = f"""
<div class="bars">
  {bar('them', 'Sub-Saharan Africa average', '· all providers, World Bank', '8.78%', 100)}
  {bar('us', 'FAME, send plus cash-out at an agent', "· the agent's own fee", '0.9 to 1.9%', 21.6)}
  {bar('us', 'FAME, money that stays digital', '· circles, shops, re-sending', '0.50%', 5.7)}
</div>
<div class="src">Sending &euro;200 from Europe to Kenya or Tanzania. Bars to scale.
  Sources: World Bank Remittance Prices Worldwide Q3 2025, Monito, provider tariffs. Ranges, not live quotes.</div>
"""

# ---------------------------------------------------------------- card 5
CARD5_CSS = """
.hexA{position:absolute;left:222px;top:120px}
.hexB{position:absolute;left:222px;top:600px}
.hexC{position:absolute;left:1560px;top:360px}
.capA{position:absolute;left:-100px;width:874px;top:394px;text-align:center}
.capB{position:absolute;left:-100px;width:874px;top:874px;text-align:center;line-height:1.5}
.capC{position:absolute;left:1325px;width:700px;top:634px;text-align:center}
.join{position:absolute;left:452px;top:120px;width:1108px;height:770px}
"""

CARD5_STAGE = f"""
<div class="hexA">{hexagon(230, 252, 'url(#g)', dot=True)}</div>
<div class="hexB">{hexagon(230, 252, 'url(#g)', dot=True)}</div>
<div class="hexC">{hexagon(230, 252, 'url(#g)', dot=True)}</div>
<svg class="join" viewBox="0 0 1108 770" preserveAspectRatio="none">
  <path d="M0,126 C400,126 500,366 1108,366" fill="none" stroke="url(#gh)" stroke-width="3"/>
  <path d="M0,606 C400,606 500,366 1108,366" fill="none" stroke="url(#gh)" stroke-width="3"/>
</svg>
<div class="capA"><span class="lbl">A phone number</span></div>
<div class="capB"><span class="lbl">A FAME number,<br>for someone who owns no phone</span></div>
<div class="capC"><span class="lbl">One account</span></div>
"""

CARDS = [
    dict(n=1, title='The counter is the product',
         stage=CARD1_STAGE, css=CARD1_CSS,
         kicker=('The rails were never the hard part.', 'The counter is.'),
         out='01-the-counter-is-the-product.jpg'),
    dict(n=2, title='What an envelope approves',
         stage=CARD2_STAGE, css=CARD2_CSS,
         kicker=('It is not access.', 'It is one withdrawal.'),
         out='02-what-an-envelope-approves.jpg'),
    dict(n=3, title='Who can strand you',
         stage=CARD3_STAGE, css=CARD3_CSS,
         kicker=('A guardian is the person who can help you.', 'Never the one who can strand you.'),
         out='03-who-can-strand-you.jpg'),
    dict(n=4, title='Why the agent still charges',
         stage=CARD4_STAGE, css=CARD4_CSS,
         kicker=('We took our fee off the counter.', 'We did not pretend the counter is free.'),
         out='04-why-the-agent-still-charges.jpg'),
    dict(n=5, title='An account is a person',
         stage=CARD5_STAGE, css=CARD5_CSS,
         kicker=('A person who owns no phone', 'still owns an account.'),
         out='05-an-account-is-a-person.jpg'),
]


def render(card):
    tmp = HERE / 'card.html'
    tmp.write_text(build(card), encoding='utf-8')
    out = HERE / card['out'].replace('.jpg', '.png')
    subprocess.run([
        CHROME, '--headless', '--disable-gpu', '--no-sandbox',
        '--hide-scrollbars', '--force-device-scale-factor=1',
        '--window-size=2400,2400', f'--screenshot={out}', f'file://{tmp}',
    ], check=True, capture_output=True, timeout=180)
    from PIL import Image
    im = Image.open(out).convert('RGB')
    assert im.size == (2400, 2400), im.size
    dest = REPO / 'series/last-mile' / card['out']
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, quality=92, subsampling=0, optimize=True)
    print(f'  {dest.relative_to(REPO)}  {dest.stat().st_size//1024} KB')


if __name__ == '__main__':
    only = sys.argv[1:] and int(sys.argv[1])
    for c in CARDS:
        if only and c['n'] != only:
            continue
        render(c)
