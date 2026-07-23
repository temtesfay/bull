# Strategy

**This file is written by the human, not by Bull.** Bull reads it and follows
it. If Bull thinks a rule is wrong, it says so in `lessons.md` and the human
decides.

Last reviewed: [DATE — update this when you change anything]

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

## What Bull holds

- Core: 40–60% in broad index ETFs (SPY, VTI, or similar). This is ballast.
- Satellite: individual large- and mid-cap US equities with a written thesis.
- Cash: minimum 10%, more when nothing looks good.

## Buy criteria — need at least three

1. A specific, falsifiable thesis that can be stated in one sentence.
2. A catalyst with a rough timeline (earnings, product cycle, regulatory date).
3. Valuation not obviously stretched versus the company's own five-year range.
4. The thesis does not depend on a macro call. Bull is bad at macro calls.
5. Enough liquidity that a full exit takes under a day.

Position sizes scale with conviction: 1% starter, 3% standard, 5% maximum.
Nothing gets a 5% weight on day one. Earn it.

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
|      | Initial version | Starting point |
