# The launch card

Owner, 2026-09-20: "make a great post and picture to celebrate the launch
of CHESS today."

Two states, because a card is a claim with a timestamp and the mine opened
at 17:00 UTC:

    python3 build.py        ->  launch-today.png   hero 17:00, "opens today"
    python3 build.py live   ->  launch-live.png    hero OPEN, "the mine is open"

Post the first in the morning, the second when the bell actually rings. A
card that says OPEN before 17:00 is simply untrue, and launch day is the
one day when every word is read closely.

## The style, and what changed from the countdown

Same brand grammar: 1080 x 1350 at 2x, ground #05070a, cyan for identity,
gold for what is mined, Geist and Geist Mono, the whole knight and never a
crop. Fonts and mark are read from `../../countdown/make`, not copied.

What changed is the staging. The countdown kept the knight at the right
edge and made a falling number the hero. Here the knight is CENTRED and
800px tall, the stage rather than a margin ornament, and the hero sits on
top of it: the hour, then the word. Everything that crosses the piece is
`position: relative; z-index: 2` with a dark text-shadow, because an
absolutely positioned image paints above ordinary text and will otherwise
swallow the headline. Verified at full resolution that the gold letters
pass in front of the ear, not behind it.

## Every figure, read off the chain before it was drawn

ChessDistributor 3693252995, CHESS ASA 3693253069, Algorand MainNet.

| Figure | Where it comes from |
|---|---|
| 20,000,000 CHESS total | the asset's own total supply, 6 decimals |
| 10,000,000 in epoch I | `poolRemaining`, al-Suli, half of everything |
| zero premine | the distributor held all 20,000,000 and no other account held a unit |
| 1 ALGO stakes 1 CHESS | epoch 0 rate, and both sides of a duel mine on their own stake, win or lose |

"Win or lose, on your own stake" is the precise claim: in a duel both
players mine, against Stockfish the challenger mines whether they win or
lose, and only a draw mines nothing. Nothing about price appears anywhere.
