# AlgoChess — public assets

Press and social assets for **[algochess.org](https://algochess.org)** — chess played
for real ALGO, with every stake held and paid out by a smart contract on Algorand
MainNet.

Free to use when writing about AlgoChess. Please don't restyle the mark.

## launch/

| File | Size | Use |
|---|---|---|
| `x-launch-1600x900.png` | 1600×900 | Launch card — "You've won thousands of games. You were paid for none of them." |
| `x-onchain-proof-1600x900.png` | 1600×900 | Proof card — the game written into its own payout transaction |

Both cards show a real MainNet duel settled on 25 August 2026: 20 ALGO escrowed,
18.0449 ALGO to the winner, 2.0000 ALGO rake, released by the contract seven
minutes after checkmate. The moves are stored in the settlement transaction
itself and can be read on any Algorand explorer:

`allo.info/tx/4IXCEK45D7UNVDJKWLGUVVJKBIQJHMWPV43NSLWMILKHXHBJIDNA`

## brand/

| File | Use |
|---|---|
| `knight.png` | The mark on a transparent ground — always the whole piece, never a crop |
| `knight-on-white.png` | The mark on white, for light backgrounds |
| `icon-512.png` | App icon |
| `x-header-1500x500.jpg` | X / Twitter header. The bottom-left is dark and empty on purpose — the profile picture lands there |

**Colours** — ground `#05070a` · cyan `#22e3e0` · gold `#e6c88a` · ink `#f2f6f8`

## Contracts

Stakes are held by two Algorand MainNet applications, not by a company wallet:

- **EscrowDuel** `3677535924` — player-versus-player stakes
- **HouseChallenge** `3677535991` — challenges against the engine
