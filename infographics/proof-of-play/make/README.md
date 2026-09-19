# Proof of Play

Owner, 2026-09-19: "make a great visual about our new Proof of Play system
and how many chess players are in the world, how they could all earn to
play. Be convincing and the design must be extraordinary. Use our horse the
best you can."

Same house style as the countdown card, which is deliberate: one brand, one
grammar. 1080 x 1350 at 2x, ground #05070a, cyan for identity, gold for
what is being mined, Geist and Geist Mono, the whole knight and never a crop.
Fonts and mark are read from `../../countdown/make` rather than copied, so
the series cannot drift apart.

## Every number, and where it comes from

| Figure | Source |
|---|---|
| 605 million adults play chess regularly | YouGov survey commissioned by AGON for FIDE, 2012, and cited by FIDE in its own submission to the IOC |
| 1,879 grandmasters alive | FIDE title-holder summary, January 2026 |
| 268.6 million Chess.com members (July 2026) | Kept off the card on purpose: two numbers land, three blur |

Other estimates of the player population run from 200 million to a billion.
605 is the one FIDE stands behind, so it is the one printed, with the source
named on the card itself.

The punch line is arithmetic, not rhetoric: 1,879 / 1,000,000 is 1/532 of a
dot, so "every grandmaster alive fits inside one five-hundredth of a single
dot" is true and slightly understated.

## Why the chart is drawn this way

- A unit chart, because the job is to make an unfeelable number felt.
- 55 x 11 is exactly 605. The grid IS the statistic, with no partial row to
  explain away and no rounding to defend.
- Every dot is the same colour. A gradient across them would read as an
  encoding of something, and nothing is being encoded. The gold stays where
  the meaning is, in the numerals.

## What the card may not say

Nothing about price, nothing about earning money. The honest claim is the
one the contracts make and it is strong enough unaided: a decisive staked
game mints CHESS on every stake, win or lose. Note the wording — an earlier
draft said "for both players", which is true of a duel and false of a
Stockfish challenge, where the machine stakes nothing and mines nothing.

## Rebuild

    cd infographics/proof-of-play/make
    npm i playwright-core          # once; needs a Chromium on the machine
    python3 build.py               # writes proof-of-play.html
    node shoot.mjs                 # writes proof-of-play.png (2160 x 2700)
