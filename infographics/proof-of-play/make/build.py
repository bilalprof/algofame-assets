"""The Proof of Play card.

Owner, 2026-09-19: "make a great visual about our new Proof of Play system
and how many chess players are in the world, how they could all earn to
play. Be convincing and the design must be extraordinary. Use our horse the
best you can."

THE ARGUMENT, and every number in it was checked before it was drawn:

  605,000,000 adults play chess regularly. FIDE commissioned the YouGov
  survey behind that figure and cited it in its own submission to the IOC.
  Other estimates run from 200 million to a billion; 605 is the one FIDE
  stands behind, so it is the one we print, with the source on the card.

  1,879 people hold the grandmaster title, per FIDE's January 2026 title
  summary. That is 1,879 out of 605 million. Drawn at one dot per million,
  every grandmaster alive fits in one five-hundredth of a single dot
  (1,879 / 1,000,000 = 1/532, which is less than 1/500, so the claim is
  true and understated).

  268.6 million people have a Chess.com account (July 2026). Kept in
  reserve, not on the card: two numbers land, three blur.

THE FORM is a unit chart, because the job is to make an unfeelable number
felt, and 55 x 11 is exactly 605 — the grid IS the statistic, with no
partial row to explain away. Every dot is the same colour on purpose: a
gradient across them would look like an encoding of something, and nothing
is being encoded. The gold stays where the meaning is, in the numerals.

WHAT THE CARD MAY NOT SAY: nothing about price, nothing about earning
money. The honest claim is the one the contracts make — a decisive staked
game mints CHESS for BOTH players, on their own stake — and it is strong
enough without help.
"""
import base64, os

HERE = os.path.dirname(os.path.abspath(__file__))
# The series shares one set of fonts and one mark. They live with the
# countdown, which was the first card; duplicating three megabytes of
# binaries per folder is how a brand drifts.
SRC = os.path.join(HERE, '..', '..', 'countdown', 'make')
F = os.path.join(SRC, 'fonts')
def font(p): return base64.b64encode(open(p, 'rb').read()).decode()
knight = base64.b64encode(open(os.path.join(SRC, 'knight-full.png'), 'rb').read()).decode()

PLAYERS_M = 605          # dots, one per million
COLS, ROWS = 55, 11      # 55 * 11 = 605 exactly
dots = ''.join('<i></i>' for _ in range(PLAYERS_M))

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: G; font-weight: 400; src: url(data:font/woff2;base64,{font(F + "/Geist-Regular.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 500; src: url(data:font/woff2;base64,{font(F + "/Geist-Medium.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 600; src: url(data:font/woff2;base64,{font(F + "/Geist-SemiBold.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 700; src: url(data:font/woff2;base64,{font(F + "/Geist-Bold.woff2")}) format("woff2"); }}
@font-face {{ font-family: GM; font-weight: 500; src: url(data:font/woff2;base64,{font(F + "/GeistMono-Medium.woff2")}) format("woff2"); }}
html, body {{ margin: 0; background: #05070a; }}
.card {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; box-sizing: border-box; padding: 56px 64px 50px; color: #bcc6d0; font-family: G, system-ui, sans-serif; -webkit-font-smoothing: antialiased; display: flex; flex-direction: column;
  background: radial-gradient(70rem 50rem at 88% 22%, rgba(34,227,224,0.15), transparent 60%), radial-gradient(60rem 44rem at 6% 82%, rgba(230,200,138,0.11), transparent 60%), #05070a; }}
.brand {{ position: relative; display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 600; letter-spacing: -0.02em; color: #f2f6f8; }}
.brand img {{ height: 44px; width: auto; }}
.brand .c {{ color: #22e3e0; }}
.brand .tag {{ margin-left: auto; font-family: GM, monospace; font-size: 13px; letter-spacing: 0.16em; text-transform: uppercase; color: #e6c88a; border: 1px solid rgba(230,200,138,0.45); border-radius: 999px; padding: 8px 16px; background: rgba(5,7,10,0.62); }}

/* The knight is the co-hero and it paints ABOVE ordinary text, so every
   line it crosses is position: relative with a dark shadow behind it. */
.knight {{ position: absolute; right: 18px; top: 92px; height: 690px; width: auto;
  filter: drop-shadow(0 0 60px rgba(34,227,224,0.45)) drop-shadow(0 0 150px rgba(34,227,224,0.20)); }}

.eyebrow {{ position: relative; text-shadow: 0 0 8px rgba(5,7,10,1), 0 0 20px rgba(5,7,10,0.95); margin-top: 52px; font-family: GM, monospace; font-size: 19px; letter-spacing: 0.30em; text-transform: uppercase; color: #22e3e0; display: flex; align-items: center; gap: 14px; }}
.eyebrow i {{ display: inline-block; width: 10px; height: 10px; border-radius: 999px; background: #22e3e0; box-shadow: 0 0 16px rgba(34,227,224,0.9); }}

.thesis {{ position: relative; text-shadow: 0 2px 18px rgba(5,7,10,0.9); margin-top: 26px; max-width: 580px; font-size: 49px; line-height: 1.16; letter-spacing: -0.035em; font-weight: 600; white-space: nowrap; }}
.thesis .dim {{ color: #56616e; display: block; }}
.thesis .now {{ color: #f2f6f8; display: block; margin-top: 8px; }}
.thesis .gold {{ text-shadow: none; background: linear-gradient(180deg, #fff3cf 0%, #e6c88a 45%, #b8924e 100%); -webkit-background-clip: text; background-clip: text; color: transparent; filter: drop-shadow(0 2px 10px rgba(5,7,10,0.85)) drop-shadow(0 0 22px rgba(230,200,138,0.35)); }}
.under {{ position: relative; text-shadow: 0 2px 14px rgba(5,7,10,0.95); margin-top: 20px; max-width: 470px; font-size: 22px; line-height: 1.42; color: #bcc6d0; }}

/* The scale: one dot per million, 55 x 11 = 605, no partial row. */
.scale {{ margin-top: auto; padding-top: 16px; }}
.count {{ position: relative; display: flex; align-items: baseline; gap: 16px; }}
.count .n {{ font-size: 104px; font-weight: 700; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums;
  background: linear-gradient(180deg, #fff3cf 0%, #e6c88a 45%, #b8924e 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 0 34px rgba(230,200,138,0.32)); }}
.count .w {{ font-family: GM, monospace; font-size: 30px; letter-spacing: 0.20em; text-transform: uppercase; color: #e6c88a; }}
.src {{ margin-top: 10px; font-size: 19px; color: #838f9c; }}
/* The system itself, in the space the knight leaves. Three steps, because
   the whole claim is that there is no fourth one: no rig to buy, no stake
   to lock, no queue to join. */
.steps {{ position: relative; margin-top: 34px; max-width: 540px; display: flex; flex-direction: column; gap: 14px; }}
.step {{ display: flex; align-items: baseline; gap: 16px; text-shadow: 0 2px 14px rgba(5,7,10,0.95); }}
.step .k {{ font-family: GM, monospace; font-size: 16px; letter-spacing: 0.12em; color: #22e3e0; min-width: 34px; }}
.step .t {{ font-size: 23px; line-height: 1.3; color: #f2f6f8; }}
.step .t em {{ font-style: normal; color: #838f9c; }}
.field {{ margin-top: 22px; display: grid; grid-template-columns: repeat({COLS}, 1fr); gap: 8px 8px; }}
.field i {{ display: block; width: 100%; aspect-ratio: 1; border-radius: 999px; background: #354c5c; }}
.legend {{ margin-top: 16px; display: flex; align-items: center; gap: 10px; font-family: GM, monospace; font-size: 14px; letter-spacing: 0.10em; text-transform: uppercase; color: #56616e; }}
.legend b {{ display: inline-block; width: 11px; height: 11px; border-radius: 999px; background: #38505e; }}
.punch {{ margin-top: 26px; font-size: 27px; line-height: 1.34; letter-spacing: -0.02em; color: #f2f6f8; font-weight: 500; }}
.punch .g {{ color: #e6c88a; }}
.turn {{ margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.10); padding-top: 22px; font-size: 24px; line-height: 1.38; color: #bcc6d0; }}
.turn b {{ color: #f2f6f8; font-weight: 600; }}
.foot {{ margin-top: 22px; display: flex; align-items: baseline; justify-content: space-between; }}
.foot .z {{ font-size: 20px; font-weight: 600; color: #f2f6f8; }}
.foot .u {{ font-family: GM, monospace; font-size: 15px; color: #22e3e0; }}
</style></head><body>
<div class="card">
  <img class="knight" src="data:image/png;base64,{knight}" alt="">
  <div class="brand"><img src="data:image/png;base64,{knight}" alt=""><span>Algo<span class="c">Chess</span></span><span class="tag">Proof of Play</span></div>
  <div class="eyebrow"><i></i>A new way to mine</div>
  <div class="thesis">
    <span class="dim">Bitcoin proves work.</span>
    <span class="dim">Algorand proves stake.</span>
    <span class="now">AlgoChess proves <span class="gold">play</span>.</span>
  </div>
  <div class="under">No rigs, no capital, no lock-up. A board, a clock, and a game that reaches a result.</div>
  <div class="steps">
    <div class="step"><span class="k">01</span><span class="t">Sit down and stake what you like <em>from 1 ALGO</em></span></div>
    <div class="step"><span class="k">02</span><span class="t">Play until the game has a result</span></div>
    <div class="step"><span class="k">03</span><span class="t">The contract pays the winner and mints CHESS <em>on every stake</em></span></div>
  </div>

  <div class="scale">
    <div class="count">
      <span class="n">605</span><span class="w">million</span>
    </div>
    <div class="src">adults play chess regularly · FIDE, YouGov survey</div>
    <div class="field">{dots}</div>
    <div class="legend"><b></b>one dot is one million players</div>
    <div class="punch">All <span class="g">1,879</span> grandmasters alive fit inside one five-hundredth of a single dot. Almost nobody else has ever been paid to play.</div>
    <div class="turn">Proof of Play does not ask you to be one of them. <b>Win or lose, every decisive staked game mines CHESS on your own stake.</b></div>
    <div class="foot"><span class="z">The board is the only door in.</span><span class="u">algochess.org/token</span></div>
  </div>
</div>
</body></html>'''
open(os.path.join(HERE, 'proof-of-play.html'), 'w').write(html)
print('ok, dots:', PLAYERS_M, '=', COLS, 'x', ROWS)
