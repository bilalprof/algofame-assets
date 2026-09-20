"""The launch card, in two states.

Owner, 2026-09-20: "make a great post and picture to celebrate the launch
of CHESS today."

TWO STATES, because a card is a claim with a timestamp and the mine opens
at 17:00 UTC:

    python3 build.py         ->  launch-today.png   "opens today, 17:00 UTC"
    python3 build.py live    ->  launch-live.png    "the mine is open"

Post the first this morning, the second when the bell actually rings. A
card saying OPEN before 17:00 is simply untrue, and this is the one day of
the project where every word will be read closely.

Every figure was read off the chain before it was drawn (ChessDistributor
3693252995, CHESS ASA 3693253069, both on Algorand MainNet):

    total supply      20,000,000 CHESS   (asset total, 6 decimals)
    epoch I pool      10,000,000 CHESS   (poolRemaining, half of everything)
    premine                        0     (the distributor holds all of it,
                                          nobody else holds a single unit)
    opening rate      1 ALGO staked mines 1 CHESS, and BOTH sides of a duel
                      mine on their own stake, win or lose

THE STYLE is the series style, one brand and one grammar: 1080 x 1350 at
2x, ground #05070a, cyan for identity, gold for what is mined, Geist and
Geist Mono, the whole knight and never a crop. What changes is the focal
point. The countdown's hero was a number falling to zero; this one's is the
hour itself, and then the word OPEN.
"""
import base64, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'countdown', 'make')
F = os.path.join(SRC, 'fonts')
def font(p): return base64.b64encode(open(p, 'rb').read()).decode()
knight = base64.b64encode(open(os.path.join(SRC, 'knight-full.png'), 'rb').read()).decode()

LIVE = len(sys.argv) > 1 and sys.argv[1] == 'live'

EYEBROW  = 'Live now · Algorand MainNet' if LIVE else 'Launch day · 20 September 2026'
HERO     = 'OPEN' if LIVE else '17:00'
HERO_SUB = 'Epoch I · al-Suli' if LIVE else 'UTC · today'
HEAD     = ('The CHESS mine is <span class="gold">open</span>.'
            if LIVE else 'The CHESS mine opens <span class="gold">today</span>.')
LINE     = ('Every decisive staked game is now mining CHESS, for both sides, on their own stake.'
            if LIVE else 'Twenty million coins. None for sale. One door in, and it is the board.')
CTA      = 'Sit down and mine the first of them.' if LIVE else 'Be at a board when the bell rings.'
NAME     = 'launch-live' if LIVE else 'launch-today'

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: G; font-weight: 400; src: url(data:font/woff2;base64,{font(F + "/Geist-Regular.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 500; src: url(data:font/woff2;base64,{font(F + "/Geist-Medium.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 600; src: url(data:font/woff2;base64,{font(F + "/Geist-SemiBold.woff2")}) format("woff2"); }}
@font-face {{ font-family: G; font-weight: 700; src: url(data:font/woff2;base64,{font(F + "/Geist-Bold.woff2")}) format("woff2"); }}
@font-face {{ font-family: GM; font-weight: 500; src: url(data:font/woff2;base64,{font(F + "/GeistMono-Medium.woff2")}) format("woff2"); }}
html, body {{ margin: 0; background: #05070a; }}
.card {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; box-sizing: border-box; padding: 56px 64px 50px; color: #bcc6d0; font-family: G, system-ui, sans-serif; -webkit-font-smoothing: antialiased; display: flex; flex-direction: column;
  background: radial-gradient(64rem 46rem at 50% 44%, rgba(34,227,224,0.17), transparent 62%), radial-gradient(56rem 40rem at 12% 88%, rgba(230,200,138,0.13), transparent 60%), #05070a; }}
.brand {{ position: relative; z-index: 2; display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 600; letter-spacing: -0.02em; color: #f2f6f8; }}
.brand img {{ height: 44px; width: auto; }}
.brand .c {{ color: #22e3e0; }}
.brand .tag {{ margin-left: auto; font-family: GM, monospace; font-size: 13px; letter-spacing: 0.16em; text-transform: uppercase; color: #e6c88a; border: 1px solid rgba(230,200,138,0.45); border-radius: 999px; padding: 8px 16px; background: rgba(5,7,10,0.62); }}

/* The knight is the stage, not a margin ornament: centred, tall, and every
   line that crosses it is position: relative with a dark shadow behind. */
.knight {{ position: absolute; left: 50%; transform: translateX(-46%); top: 210px; height: 800px; width: auto;
  filter: drop-shadow(0 0 70px rgba(34,227,224,0.50)) drop-shadow(0 0 190px rgba(34,227,224,0.22)); }}

.eyebrow {{ position: relative; z-index: 2; text-shadow: 0 0 10px rgba(5,7,10,1), 0 0 22px rgba(5,7,10,0.95); margin-top: 44px; font-family: GM, monospace; font-size: 20px; letter-spacing: 0.30em; text-transform: uppercase; color: #22e3e0; display: flex; align-items: center; gap: 14px; }}
.eyebrow i {{ display: inline-block; width: 10px; height: 10px; border-radius: 999px; background: #22e3e0; box-shadow: 0 0 18px rgba(34,227,224,1); }}

.hero {{ position: relative; z-index: 2; margin-top: 14px; font-size: {230 if LIVE else 210}px; line-height: 1; font-weight: 700; letter-spacing: -0.055em; font-variant-numeric: tabular-nums;
  background: linear-gradient(180deg, #fff6dd 0%, #e6c88a 44%, #b8924e 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 0 46px rgba(230,200,138,0.45)); text-shadow: 0 6px 40px rgba(5,7,10,0.9); }}
.herosub {{ position: relative; z-index: 2; text-shadow: 0 0 10px rgba(5,7,10,1), 0 2px 16px rgba(5,7,10,0.95); margin-top: 2px; font-family: GM, monospace; font-size: 27px; letter-spacing: 0.26em; text-transform: uppercase; color: #f2f6f8; }}

.spacer {{ flex: 1 1 auto; }}

.head {{ position: relative; z-index: 2; text-shadow: 0 2px 20px rgba(5,7,10,0.95), 0 0 46px rgba(5,7,10,0.85); font-size: 62px; line-height: 1.04; letter-spacing: -0.04em; font-weight: 600; color: #f2f6f8; max-width: 900px; }}
.head .gold {{ background: linear-gradient(180deg, #fff3cf 0%, #e6c88a 45%, #b8924e 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.line {{ position: relative; z-index: 2; text-shadow: 0 2px 16px rgba(5,7,10,0.95); margin-top: 18px; font-size: 25px; line-height: 1.4; color: #bcc6d0; max-width: 820px; }}

.facts {{ position: relative; z-index: 2; margin-top: 30px; display: flex; gap: 14px; }}
.fact {{ flex: 1 1 0; border-radius: 14px; border: 1px solid rgba(255,255,255,0.10); background: linear-gradient(180deg, rgba(143,154,164,0.10), rgba(143,154,164,0.03)); box-shadow: inset 0 1px 0 rgba(255,255,255,0.12); padding: 18px 20px; display: flex; flex-direction: column; gap: 6px; backdrop-filter: blur(6px); }}
.fact .n {{ font-family: GM, monospace; font-size: 29px; color: #e6c88a; line-height: 1; letter-spacing: -0.02em; }}
.fact .n.c {{ color: #7ffdf8; }}
.fact .l {{ font-size: 15px; line-height: 1.35; color: #bcc6d0; }}

.foot {{ position: relative; z-index: 2; margin-top: 26px; display: flex; align-items: baseline; justify-content: space-between; }}
.foot .z {{ font-size: 20px; font-weight: 600; color: #f2f6f8; }}
.foot .u {{ font-family: GM, monospace; font-size: 15px; color: #22e3e0; }}
</style></head><body>
<div class="card">
  <img class="knight" src="data:image/png;base64,{knight}" alt="">
  <div class="brand"><img src="data:image/png;base64,{knight}" alt=""><span>Algo<span class="c">Chess</span></span><span class="tag">{'The CHESS token · live' if LIVE else 'The CHESS token · today'}</span></div>
  <div class="eyebrow"><i></i>{EYEBROW}</div>
  <div class="hero">{HERO}</div>
  <div class="herosub">{HERO_SUB}</div>
  <div class="spacer"></div>
  <div class="head">{HEAD}</div>
  <div class="line">{LINE}</div>
  <div class="facts">
    <div class="fact"><span class="n">1 : 1</span><span class="l">Stake 1 ALGO, mine 1 CHESS. Win or lose, on your own stake.</span></div>
    <div class="fact"><span class="n c">0</span><span class="l">No premine, no sale, no allocation. Nobody was handed a coin.</span></div>
    <div class="fact"><span class="n">10 M</span><span class="l">Epoch I, al-Suli: half of all the CHESS there will ever be.</span></div>
  </div>
  <div class="foot"><span class="z">{CTA}</span><span class="u">algochess.org/token</span></div>
</div>
</body></html>'''
open(os.path.join(HERE, NAME + '.html'), 'w').write(html)
print('ok', NAME)
