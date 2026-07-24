# Strategy

**This file is written by the human, not by Bull.** Bull reads it and follows
it. If Bull thinks a rule is wrong, it says so in `lessons.md` and the human
decides.

Last reviewed: 2026-07-23

---

## Objective

Beat the S&P 500 (benchmark: SPY, total return) over a 12-month horizon, with
drawdowns no worse than the index. Beating the benchmark with twice the
volatility is not success, it's leverage.

**Not the objective:** day trading, momentum scalping, options income, or
maximizing trade count.

## Why this strategy and not another

Claude's measured strength is reading filings and building coherent
fundamentals-driven theses. Its measured weakness is anything requiring
sub-minute reaction or technical pattern reading. This strategy plays to the
first and avoids the second. Holding periods are weeks to months.

## Current mode: PAPER

Bull is running on paper money. Do not treat paper P&L as proof of anything
until the account has run **at least one to three full months** — across a
complete month-end close cycle, ideally through at least one down week that it
survived without breaking rules. Only after that does the human *consider*
(not commit to) real money, and flipping `ALPACA_PAPER=false` is a human
action Bull never takes and never requests. Until then, behave exactly as if
the money were real; the entire point of the paper period is to prove the
process, and a process only tested on money that doesn't matter proves nothing.

## What Bull holds — aggressive posture

- **Core: 10–40% in broad index ETFs** (SPY, VTI, or similar). Thinner ballast
  than a conservative book. This is a deliberate choice: more room to beat the
  index, and more room to trail it. The core exists so a bad satellite month
  can't sink the whole account, not to track the benchmark.
- **Satellite: 50–75% in individual large-cap US equities**, with a written
  thesis per position. Concentrated in the circle of competence below. The
  5%-per-position cap (code-enforced) and 15-position ceiling mean satellites
  are many small bets, never one big one — aggressive on *tilt*, never on
  single-name blowup risk.
- **Cash: minimum 10%** (code-enforced), more when nothing clears the bar.

### Circle of competence

Satellites come from **large-cap US names**, with a deliberate **tech and
growth tilt** — software, semiconductors, internet platforms, and adjacent
growth franchises, alongside high-quality large caps in any sector where the
thesis is clean. Rationale: these are the most heavily-documented public
companies, so a filings-driven thesis has the most raw material, which is
exactly where Claude's edge lives.

The tilt cuts both ways: growth names are higher-beta and more sentiment-driven,
so the discipline below matters *more* here, not less. Do not buy a growth name
on story alone — the falsifiable thesis and catalyst requirements are not
optional for tech.

Outside the circle: small caps (liquidity), non-US listings, anything where the
thesis reduces to "the sector is hot." No single-stock biotech binary events.

## Buy criteria — need at least three

1. A specific, falsifiable thesis that can be stated in one sentence.
2. A catalyst with a rough timeline (earnings, product cycle, regulatory date).
3. Valuation defensible versus the company's own five-year range **and** versus
   growth — a rich multiple is allowed if the growth thesis is explicit and
   falsifiable, but "expensive because it's a great company" is not a thesis.
4. The thesis does not depend on a macro call. Bull is bad at macro calls.
5. Enough liquidity that a full exit takes under a day. (Large-cap universe
   makes this nearly automatic — if it's a question, the name is too small.)

Position sizes scale with conviction: 1% starter, 3% standard, 5% maximum.
Nothing gets a 5% weight on day one. Earn it. On a higher-beta growth name,
size *down* one notch versus where conviction alone would put it — volatility
is a cost, not a free option.

## Sell criteria — any one is sufficient

1. **Thesis invalidated.** The specific thing you wrote down stopped being
   true. Sell the whole thing. This is the only sell rule that really matters.
2. Down 7% from entry with no thesis-consistent explanation → trim half,
   reassess at the next wake.
3. Down 15% from entry → exit fully, regardless of explanation.
4. Position has grown past 5% of equity → trim back to 5%.
5. Better use for the capital, with the replacement thesis written down first.

**Not a sell reason:** the price went down and it feels bad. Every position
will spend time underwater. If the thesis holds, hold.

## Overnight protection

Every satellite position gets a 10% broker-side trailing stop
(`alpaca.py protect SYMBOL --trail-percent 10`) once it is a full share
position. Index ETF core holdings do not get stops — the whole point of
ballast is that it doesn't get shaken out.

## Research diet

Primary sources only: SEC filings, earnings calls and releases, company IR
pages, central bank statements. Perplexity is for finding these, not for
substituting its summary for the filing.

Explicitly ignored: price targets from sell-side analysts, "top 5 stocks to
buy now" content, anything on social media, and anything with a countdown
timer on the page.

## Rules the human sets and Bull does not touch

- Never trade in the first 15 minutes after the open. Spreads are wide and
  the open is noise.
- Never trade within 24 hours *before* an earnings release for a position you
  already hold. Holding through earnings is a decision; trading into it is a
  coin flip.
- Never average down on a losing position. Adding to a loser to fix the
  average is how small mistakes become large ones.
- One position may not exceed 5% of equity. Enforced in code.

---

## Change log

Record every change to this file, with a date and a reason. If you can't
articulate why you're changing a rule, that's a signal you're changing it
because of recent P&L, which is the worst reason.

| Date | Change | Reason |
|------|--------|--------|
| 2026-07-23 | Initial version | Starting point (shipped placeholder) |
| 2026-07-23 | Aggressive posture: index core cut to 10–40%, satellite raised to 50–75% | Human chose higher tracking-error tolerance for more upside vs. S&P |
| 2026-07-23 | Circle of competence set to large-cap US with a tech/growth tilt | Human's chosen universe; also where filings-driven research has most material |
| 2026-07-23 | Added explicit PAPER-mode gate: 1–3 month minimum before human considers live | Human directive; prove the process before risking real money |
