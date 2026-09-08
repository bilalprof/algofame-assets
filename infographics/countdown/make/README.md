# The countdown card

One card a day until the CHESS mine opens (September 20, 2026). The owner
(2026-09-08): "the visual is stunning. remember the style and design for the
next days until launch." This folder is that memory: the generator, the
fonts and the mark, so the card of any day is rebuilt pixel for pixel.

## The style, in words

- 1080 x 1350 (4:5), rendered at 2x (2160 x 2700). Ground #05070a with a
  cyan glow (rgba(34,227,224,.14)) top right and a gold glow
  (rgba(230,200,138,.10)) bottom left.
- Geist for words, Geist Mono for numbers and eyebrows. Ink #f2f6f8 for
  titles, #bcc6d0 for body, #838f9c and #56616e for the quiet lines.
- Two accents only: cyan #22e3e0 is action and identity (eyebrow dot,
  the URL), gold #e6c88a is money (the number, the facts, the strip).
- The number of days is the hero: Geist Bold, 560px, letter-spacing
  -0.07em, gold gradient #fff3cf to #e6c88a to #b8924e, a soft gold glow.
  Under it "DAYS TO GO" in mono, tracked 0.42em.
- The knight (knight-full.png, the whole piece, never a crop) at the right,
  760px tall, with a cyan rim glow; it may overlap the number.
- Eyebrow above the number: "The mine opens · September 20", cyan dot.
- One sentence under the number: "Every staked game will mine CHESS.
  Nothing is sold. The board is the only door in." with "mine CHESS" in gold.
- Three glass facts: 1 : 1, 0, 20 M. Then the supply strip to scale
  (al-Suli half of everything, the striped sliver for the last fifteen),
  then the footer line and algochess.org/token.
- House rules: no em dash, no promise on price, no "rake" or "house",
  AlgoChess with two capitals, knight-full.png as the only mark.

## Rebuild the card for day N

    cd infographics/countdown/make
    npm i playwright-core            # once; needs a Chromium on the machine
    python3 build.py 9               # writes mine-9.html
    node shoot.mjs 9                 # writes mine-9.png (2160 x 2700)

`shoot.mjs` launches Chromium at the path in the file (set
`executablePath` to yours). The rendered series for 12 to 1 already sits
one folder up.
