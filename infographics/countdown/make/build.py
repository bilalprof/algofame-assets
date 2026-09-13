import base64, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, 'fonts')
def font(p): return base64.b64encode(open(p, 'rb').read()).decode()
knight = base64.b64encode(open(os.path.join(HERE, 'knight-full.png'), 'rb').read()).decode()
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 12

# the supply, to scale: twenty pools halving, the striped sliver for the last fifteen
segs = ''.join(
    f'<div style="flex: {50 / 2 ** i} 1 0px; background: {c}"></div>'
    for i, c in enumerate(['#f5dda2', '#e3c489', '#d1ab70', '#bf9257', '#b08948']))
segs += '<div style="flex: 3.125 1 0px; background: repeating-linear-gradient(135deg,#8a6a35 0 4px,#6b532a 4px 8px)"></div>'

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: G; font-weight: 400; src: url(data:font/woff2;base64,{font(F + "/Geist-Regular.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 500; src: url(data:font/woff2;base64,{font(F + "/Geist-Medium.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 600; src: url(data:font/woff2;base64,{font(F + "/Geist-SemiBold.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 700; src: url(data:font/woff2;base64,{font(F + "/Geist-Bold.woff2")}) format("woff2"); }}
@font-face {{ font-family: GM; font-weight: 500; src: url(data:font/woff2;base64,{font(F + "/GeistMono-Medium.woff2")}) format("woff2"); }}
html, body {{ margin: 0; background: #05070a; }}
.card {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; box-sizing: border-box; padding: 56px 64px 52px; color: #bcc6d0; font-family: G, system-ui, sans-serif; -webkit-font-smoothing: antialiased; display: flex; flex-direction: column;
  background: radial-gradient(70rem 50rem at 85% 30%, rgba(34,227,224,0.14), transparent 60%), radial-gradient(60rem 44rem at 10% 70%, rgba(230,200,138,0.10), transparent 60%), #05070a; }}
.brand {{ display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 600; letter-spacing: -0.02em; color: #f2f6f8; }}
.brand img {{ height: 44px; width: auto; }}
.brand .c {{ color: #22e3e0; }}
.brand .tag {{ margin-left: auto; font-family: GM, monospace; font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; color: #e6c88a; border: 1px solid rgba(230,200,138,0.45); border-radius: 999px; padding: 8px 16px; }}
.knight {{ position: absolute; right: -12px; top: 120px; height: 820px; width: auto; filter: drop-shadow(0 0 60px rgba(34,227,224,0.45)) drop-shadow(0 0 140px rgba(34,227,224,0.18)); }}
.eyebrow {{ position: relative; margin-top: 64px; font-family: GM, monospace; font-size: 22px; letter-spacing: 0.32em; text-transform: uppercase; color: #22e3e0; display: flex; align-items: center; gap: 14px; }}
.eyebrow i {{ display: inline-block; width: 10px; height: 10px; border-radius: 999px; background: #22e3e0; box-shadow: 0 0 16px rgba(34,227,224,0.9); }}
.big {{ position: relative; margin: -30px 0 0 -14px; font-size: 560px; line-height: 0.9; font-weight: 700; letter-spacing: -0.07em; font-variant-numeric: tabular-nums;
  background: linear-gradient(180deg, #fff3cf 0%, #e6c88a 42%, #b8924e 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 0 40px rgba(230,200,138,0.35)); }}
.days {{ margin-top: -18px; font-family: GM, monospace; font-size: 34px; letter-spacing: 0.42em; text-transform: uppercase; color: #f2f6f8; }}
.days span {{ color: #838f9c; }}
h1 {{ position: relative; margin: 36px 0 0; max-width: 500px; font-size: 54px; line-height: 1.04; letter-spacing: -0.035em; font-weight: 600; color: #f2f6f8; text-wrap: balance; }}
h1 .gold {{ color: #e6c88a; }}
.facts {{ margin-top: 34px; display: flex; gap: 14px; }}
.fact {{ flex: 1 1 0; border-radius: 14px; border: 1px solid rgba(255,255,255,0.09); background: linear-gradient(180deg, rgba(143,154,164,0.09), rgba(143,154,164,0.03)); box-shadow: inset 0 1px 0 rgba(255,255,255,0.12); padding: 18px 20px; display: flex; flex-direction: column; gap: 6px; }}
.fact .n {{ font-family: GM, monospace; font-size: 30px; color: #e6c88a; line-height: 1; letter-spacing: -0.02em; }}
.fact .n.c {{ color: #7ffdf8; }}
.fact .l {{ font-size: 15px; line-height: 1.35; color: #bcc6d0; }}
.strip {{ margin-top: auto; display: flex; flex-direction: column; gap: 10px; }}
.strip .bar {{ display: flex; height: 30px; gap: 2px; border-radius: 8px; overflow: hidden; }}
.strip .cap {{ display: flex; justify-content: space-between; font-family: GM, monospace; font-size: 13px; letter-spacing: 0.1em; text-transform: uppercase; color: #56616e; }}
.foot {{ margin-top: 26px; display: flex; align-items: baseline; justify-content: space-between; }}
.foot .z {{ font-size: 20px; font-weight: 600; color: #f2f6f8; }}
.foot .z span {{ color: #e6c88a; }}
.foot .u {{ font-family: GM, monospace; font-size: 15px; color: #22e3e0; }}
</style></head><body>
<div class="card">
  <img class="knight" src="data:image/png;base64,{knight}" alt="">
  <div class="brand"><img src="data:image/png;base64,{knight}" alt=""><span>Algo<span class="c">Chess</span></span><span class="tag">The CHESS token · not live yet</span></div>
  <div class="eyebrow"><i></i>The mine opens · September 20</div>
  <div class="big">{DAYS}</div>
  <div class="days">{'day' if DAYS == 1 else 'days'} <span>to go</span></div>
  <h1>Every staked game will <span class="gold">mine CHESS</span>. Nothing is sold. The board is the only door in.</h1>
  <div class="facts">
    <div class="fact"><span class="n">1 : 1</span><span class="l">Stake 1 ALGO, mine 1 CHESS. Duel or Stockfish, every decisive game.</span></div>
    <div class="fact"><span class="n c">0</span><span class="l">Zero premine, zero sale. On day one nobody owns a coin.</span></div>
    <div class="fact"><span class="n">20 M</span><span class="l">Twenty epochs named for the masters. When Fischer's last coin is mined, the story ends.</span></div>
  </div>
  <div class="strip">
    <div class="bar">{segs}</div>
    <div class="cap"><span>al-Suli · half of everything</span><span>Lucena · Ruy Lopez · Greco · Philidor · fifteen more</span></div>
  </div>
  <div class="foot"><span class="z">Be at the table when it opens. <span>Every coin goes to the player who mined it.</span></span><span class="u">algochess.org/token</span></div>
</div>
</body></html>'''
open(f'mine-{DAYS}.html', 'w').write(html)
print('ok', DAYS)
