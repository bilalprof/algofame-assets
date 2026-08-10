# The last mile — LinkedIn copy

Five cards, one per remaining kit day of the week, posted to the FAME company
page at 15:00 UTC. Written for the operator audience: agent networks, corridor
partners, financial-inclusion teams, funders. Register is deliberately not the
member-facing one used on X and Facebook.

Card URLs resolve from `main` once this branch is merged.

---

## 01 · The counter is the product — Mon 10 Aug

![card](https://raw.githubusercontent.com/bilalprof/algofame-assets/main/series/last-mile/01-the-counter-is-the-product.jpg)

Most of a cross-border payment is solved. The part that is not is the last
hundred metres.

Moving value between two ledgers is close to free and close to instant. Turning
it into cash in somebody's hand, in a town with no branch, is where the cost,
the failure and the queueing actually live. That is the product. Everything
upstream is plumbing.

So we built for the counter first. A cash-out is three independent locks rather
than one password. It can be cancelled mid-flight with nothing moved and no fee
taken. A guardian can pre-approve exactly one withdrawal and revoke it until the
moment it is used.

FAME takes 0.5 percent to send and nothing at all at the counter. The agent
charges their own fee, which puts the whole journey at 0.9 to 1.9 percent
against a regional average of 8.78.

We are looking for agent networks and corridor partners who already know the
last mile is the hard part.

algofame.org

---

## 02 · What an envelope approves — Tue 11 Aug

![card](https://raw.githubusercontent.com/bilalprof/algofame-assets/main/series/last-mile/02-what-an-envelope-approves.jpg)

A recovery code and a withdrawal approval are not the same object, and treating
them as one is how people get robbed by their own families.

In FAME a guardian holds two distinct powers. A recovery code returns somebody
to their account. An envelope pre-approves one cash withdrawal: one agent, one
day, one limit. It is revocable right up until the moment it is used, and once
used it is spent.

The distinction matters because the person collecting cash often cannot read the
screen, is standing in front of an agent who can, and has family several time
zones away. An approval that works twice is an approval somebody else can spend.

We also rebuilt the guardian screen to lead with whoever is waiting at a counter
right now, above everything else. Someone standing in a queue should not be at
the bottom of a list.

algofame.org

---

## 03 · Who can strand you — Wed 12 Aug

![card](https://raw.githubusercontent.com/bilalprof/algofame-assets/main/series/last-mile/03-who-can-strand-you.jpg)

Every assisted-access design eventually has to answer one question: who can take
somebody's money away from them?

In FAME a guardian can cut off the agent a member is standing at, unilaterally,
without being asked. Nothing is lost when they do. The vault carries forward and
the same four digits work at any other shop the next morning. It is a safe power
to hand out precisely because it is reversible.

Ending the assisted tier is a different kind of act. For someone without a
smartphone it means losing access to their money until they get one, so only the
member can do it, from their own session. No guardian, no agent, no support
ticket.

The rule we hold to: a guardian is the person who can help you, never the person
who can strand you. If a permission cannot be handed out safely, it does not get
handed out.

algofame.org

---

## 04 · Why the agent still charges — Thu 13 Aug

![card](https://raw.githubusercontent.com/bilalprof/algofame-assets/main/series/last-mile/04-why-the-agent-still-charges.jpg)

Sending 200 euros from Europe to Kenya or Tanzania costs 8.78 percent on the
World Bank's all-provider average. The family receives about 182 of your 200.

Our fee is 0.5 percent to send and zero at the counter. That does not make the
journey free, and we are not going to claim it does. The agent handing over cash
is running a business with real float, real risk and real rent, and they charge
their own fee. End to end, a FAME send plus a full cash-out lands between 0.9
and 1.9 percent. Money that stays digital stays at 0.5.

We moved off a flat ten-cent fee for a reason worth stating plainly: a flat fee
sounds fair until somebody sends one dollar and pays a tenth of it. A share of
what is sent, with a one cent minimum, is the honest shape.

Sources: World Bank Remittance Prices Worldwide Q3 2025, Monito, provider
tariffs. Ranges, not live quotes.

algofame.org

---

## 05 · An account is a person — Fri 14 Aug

![card](https://raw.githubusercontent.com/bilalprof/algofame-assets/main/series/last-mile/05-an-account-is-a-person.jpg)

A large share of the people who most need to receive money do not own the phone
the money is supposed to arrive on.

So in FAME an account belongs to a person, not a handset. If someone has a phone
number, you send to it. If they own no phone at all, they have a FAME number,
and it goes in the same field. The sender is never asked which kind it is.

This is what makes the assisted tier coherent rather than a workaround. A mother
with no device still holds an account, a vault, a PIN and guardians of her own.
She is not a row inside somebody else's wallet.

It has been true in the code since launch. Our own website was the last place
still implying a phone number was required, and that is fixed.

That closes this five part series on the last mile.

algofame.org
