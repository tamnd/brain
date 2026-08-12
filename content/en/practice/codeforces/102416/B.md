---
title: "CF 102416B - Efficient market"
description: "We have m companies and n future days. For every company, we know its stock price on every day. The input stores one company per row, so each row contains that company's prices from day 1 through day n. We start with d pounds before the first known day."
date: "2026-08-12T20:41:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102416
codeforces_index: "B"
codeforces_contest_name: "Edinburgh Competition 2019"
rating: 0
weight: 102416
solve_time_s: 148
verified: true
draft: false
---

[CF 102416B - Efficient market](https://codeforces.com/problemset/problem/102416/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `m` companies and `n` future days. For every company, we know its stock price on every day. The input stores one company per row, so each row contains that company's prices from day 1 through day `n`.

We start with `d` pounds before the first known day. During a day, prices do not change, and we may perform any number of trades. Since the sample itself requires investing a non-integer number of shares, we can treat our money as continuously divisible: if we have `x` pounds and a stock costs `p`, we can put all `x` pounds into `x / p` shares. At the end of day `n`, we want the largest possible cash value.

The crucial consequence of unlimited same-day trading is that we do not need to remember a complicated portfolio. Suppose we have `x` pounds at the beginning of a transition from day `i` to day `i+1`, and company `j` costs `p` on day `i` and `q` on day `i+1`. Investing everything in that company changes our wealth from `x` to `x * q / p`. The best company is simply the one with the largest ratio `q / p`. Keeping the money as cash is also an option, with ratio `1`.

The number of days is at most 50 and the number of companies is at most 1000. An `O(nm)` algorithm performs at most about 50,000 ratio comparisons, which is comfortably within the one-second limit. A strategy that tries every possible sequence of company choices grows exponentially with `n`, so even the relatively small bound of 50 days makes such enumeration impossible. The input itself contains only `nm <= 50,000` prices, so storing the complete matrix is inexpensive.

There are several cases where a careless implementation can silently fail. First, when there is only one day, there is no price transition at all. For example,

```
1 1 25.00
7.50
```

has answer `25.00`. There is no opportunity to turn the initial money into a larger amount, because the final day is also the first observed day. An implementation that blindly applies one transition would be performing an operation that does not exist.

Second, we are not required to invest. Consider

```
2 1 100.00
5.00 4.00
```

The only stock loses value, so the correct answer is `100.00`. A solution that always buys the stock would incorrectly obtain `80.00`. The cash asset effectively contributes a multiplier of `1`, so every daily multiplier must be at least `1`.

Third, the best company can change from one day to the next. For example,

```
3 2 10.00
1.00 10.00 1.00
1.00 1.00 10.00
```

The first transition is best through company 1, multiplying the money by `10`. The second transition is best through company 2, multiplying it by another `10`, giving `100.00`. A solution that chooses one company for the entire period would miss this possibility.

## Approaches

A direct brute-force strategy can try every possible stock choice for every transition between consecutive days. For each complete sequence, we multiply the current amount by the corresponding price ratio and keep the largest result. We also need the option of staying in cash, so each transition has at most `m + 1` choices.

This brute force is correct because every candidate sequence describes a possible way of investing the current wealth during each day-to-day interval. The problem is the number of sequences. There are `(m + 1)^(n - 1)` of them, and evaluating one sequence takes `O(n)` work. In the worst case this is `O(n(m + 1)^(n - 1))`. With `n = 50` and `m = 1000`, that is roughly `49 * 1001^49`, around `5 * 10^148` basic operations, which is completely infeasible.

The observation that removes the exponential factor is that different transitions do not interfere with one another. Once we reach a particular day with `x` pounds, every possible previous history has been summarized by that single number. For the next transition, the only question is which asset gives the largest multiplier from today's price to tomorrow's price. Since unlimited same-day transactions let us sell the old holding and immediately buy the new one, changing companies costs nothing beyond their listed prices.

For company `j`, the multiplier from day `i` to day `i+1` is

`price[i+1][j] / price[i][j]`.

We take the maximum of this ratio over all companies and over `1` for cash. We then multiply the current wealth by that maximum. Repeating this independently for all `n - 1` transitions gives the optimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n(m+1)^(n-1))` | `O(n)` | Too slow |
| Optimal | `O(nm)` | `O(nm)` | Accepted |

## Algorithm Walkthrough

1. Read the number of days `n`, the number of companies `m`, and the initial amount `d`. Store the `m` price rows because each transition needs the price of every company on two consecutive days.
2. Set the current amount of money to `d`. Before processing any transition, this is exactly the amount available at the beginning of day 1.
3. For every pair of consecutive days `i` and `i + 1`, examine every company. If its prices are `p = price[i][j]` and `q = price[i+1][j]`, calculate the multiplier `q / p`.
4. Start the best multiplier for the transition at `1.0`. This represents leaving all money as cash. Replace it whenever a stock offers a larger multiplier.
5. Multiply the current amount by the best multiplier. This gives the maximum amount that can be available at the next day, because all money can be converted into the best-performing asset for this particular transition.
6. After processing the final transition, print the resulting amount with two digits after the decimal point. When `n = 1`, the loop has zero iterations, so the original amount is printed unchanged.

### Why it works

Maintain the invariant that `money` is the maximum amount of cash that can be available at the current day after using all profitable opportunities up to that day. Consider the next transition. Any money available now can either remain as cash, preserving a multiplier of `1`, or be converted entirely into one company's stock. If company `j` is chosen, every pound becomes `price[i+1][j] / price[i][j]` pounds on the next day. Because arbitrary same-day transactions are allowed, any previous stock can be sold and the entire portfolio can be moved into whichever company has the largest ratio. Thus the best possible next-day wealth is exactly `money * max(1, max_j(price[i+1][j] / price[i][j]))`. The invariant is preserved at every transition, so after the last day the computed amount is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, money = input().split()
    n = int(n)
    m = int(m)
    money = float(money)

    prices = [list(map(float, input().split())) for _ in range(m)]

    for day in range(n - 1):
        best_ratio = 1.0

        for company in range(m):
            ratio = prices[company][day + 1] / prices[company][day]
            if ratio > best_ratio:
                best_ratio = ratio

        money *= best_ratio

    print(f"{money:.2f}")

if __name__ == "__main__":
    solve()
```

The first three values are parsed from the first line, with `n` and `m` converted to integers and the initial capital converted to a floating-point number. The prices are stored as `prices[company][day]`, matching the row-oriented input directly.

The outer loop runs from day `0` through day `n - 2`. This corresponds to exactly the `n - 1` transitions between consecutive days. Using `range(n - 1)` is also what makes the `n = 1` case work automatically, since there are then no transitions.

For each transition, `best_ratio` starts at `1.0`, not at `0`. This represents the option of doing nothing and keeping the money in cash. Since every stock price is positive, division by a price is always safe.

The ratio is calculated before updating `money`, so every company is compared using the same starting capital for that transition. Updating the amount only after all companies have been examined is equivalent to selecting the best company and investing the whole amount in it.

Python's floating-point arithmetic is sufficient here because the required output tolerance is `0.01`, while the answer is guaranteed to be at most `10^9`. Python also has no fixed-width integer overflow issue, although this solution does not need large integers anyway. Formatting with `:.2f` produces the required two decimal places.

## Worked Examples

### Sample 1

The input is

```
4 2 10.00
1.02 1.00 1.00 1.00
4.37 4.81 5.32 6.06
```

The two rows are the price histories of the two companies.

| Transition | Company 1 ratio | Company 2 ratio | Best multiplier | Money |
| --- | --- | --- | --- | --- |
| Day 1 → 2 | `1.00 / 1.02 ≈ 0.9804` | `4.81 / 4.37 ≈ 1.1007` | `1.1007` | `11.007` |
| Day 2 → 3 | `1.00 / 1.00 = 1` | `5.32 / 4.81 ≈ 1.1060` | `1.1060` | `12.174` |
| Day 3 → 4 | `1.00 / 1.00 = 1` | `6.06 / 5.32 ≈ 1.1391` | `1.1391` | `13.873` |

The final value rounds to `13.87`. The trace also demonstrates why the actual number of shares does not need to be stored. After every transition, the entire current wealth can be treated as cash again, then reinvested optimally for the next transition.

### Constructed Example 2

Consider

```
3 2 10.00
1.00 10.00 1.00
1.00 1.00 10.00
```

| Transition | Company 1 ratio | Company 2 ratio | Best multiplier | Money |
| --- | --- | --- | --- | --- |
| Day 1 → 2 | `10 / 1 = 10` | `1 / 1 = 1` | `10` | `100` |
| Day 2 → 3 | `1 / 10 = 0.1` | `10 / 1 = 10` | `10` | `1000` |

The answer is `1000.00`. The optimal strategy changes companies between the two transitions. This confirms that the algorithm does not commit to one stock for the whole period.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nm)` | There are `n - 1` transitions, and every transition checks all `m` companies. |
| Space | `O(nm)` | The complete price matrix contains `m * n` floating-point values. |

With at most 50 days and 1000 companies, the algorithm performs fewer than 50,000 ratio calculations. The price matrix also contains at most 50,000 values, so both the running time and memory usage are easily within the one-second and 256 MB limits.

## Test Cases

```python
# The following test harness reuses the same solve() logic.
import sys
import io

def solve():
    n, m, money = input().split()
    n = int(n)
    m = int(m)
    money = float(money)

    prices = [list(map(float, input().split())) for _ in range(m)]

    for day in range(n - 1):
        best_ratio = 1.0

        for company in range(m):
            ratio = prices[company][day + 1] / prices[company][day]
            if ratio > best_ratio:
                best_ratio = ratio

        money *= best_ratio

    print(f"{money:.2f}")

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """4 2 10.00
1.02 1.00 1.00 1.00
4.37 4.81 5.32 6.06
"""
) == "13.87", "sample 1"

# Minimum-size input, no transitions and zero initial money
assert run(
    """1 1 0.00
10.00
"""
) == "0.00", "minimum size and zero capital"

# All prices equal, so the amount never changes
assert run(
    """3 2 123.45
5.55 5.55 5.55
2.00 2.00 2.00
"""
) == "123.45", "all prices equal"

# Falling stock, so keeping cash is better than investing
assert run(
    """2 1 100.00
5.00 4.00
"""
) == "100.00", "cash must be an available choice"

# The best company changes between transitions
assert run(
    """3 2 10.00
1.00 10.00 1.00
1.00 1.00 10.00
"""
) == "1000.00", "company switching"

# Maximum dimensions with equal prices
max_case = ["50 1000 1000000.00"]
max_case.extend(["1.00 " * 49 + "1.00"] * 1000)
assert run("\n".join(max_case) + "\n") == "1000000.00", "maximum dimensions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0.00` with one price | `0.00` | Minimum dimensions and the absence of any transition |
| Three days with all prices unchanged | `123.45` | A multiplier of exactly `1` leaves wealth unchanged |
| One stock falling from `5.00` to `4.00` | `100.00` | The algorithm must be allowed to keep cash |
| Two stocks with alternating best returns | `1000.00` | The optimal company can change every day |
| `n = 50`, `m = 1000`, all prices `1.00` | `1000000.00` | Maximum input dimensions and performance |

## Edge Cases

When there is only one day, there is no investment interval. For

```
1 1 25.00
7.50
```

the loop over `range(n - 1)` becomes `range(0)`, so `money` remains `25.00` and the output is `25.00`. This avoids the common off-by-one mistake of comparing day 1 with a nonexistent day 2.

When every available stock loses value, cash must beat all of them. For

```
2 1 100.00
5.00 4.00
```

the only stock has ratio `4 / 5 = 0.8`, while cash has ratio `1`. The algorithm initializes `best_ratio` to `1.0`, so the transition leaves the wealth at `100.00`. A greedy implementation that always buys the best stock, without considering cash, would incorrectly reduce the capital.

When the optimal company changes, the algorithm deliberately reevaluates all companies after every transition. In

```
3 2 10.00
1.00 10.00 1.00
1.00 1.00 10.00
```

the first transition chooses company 1 and multiplies the money by `10`. The resulting `100.00` is then treated as the available capital for the second transition, where company 2 has ratio `10`. The final value is `1000.00`. The previous choice does not restrict the next one because same-day selling and buying are unrestricted.

If all prices are equal, every stock ratio is exactly `1`, so the capital never changes. For

```
3 2 123.45
5.55 5.55 5.55
2.00 2.00 2.00
```

every transition has best multiplier `1`, producing `123.45` throughout. This also checks that the algorithm does not create artificial profit from repeated same-day transactions.

Finally, zero initial capital is harmless even when profitable opportunities exist. For

```
2 1 0.00
1.00 10.00
```

the stock offers a multiplier of `10`, but `0 * 10` is still `0`. The answer is `0.00`. The algorithm computes the optimal multiplier independently of the amount of capital, then applies it to the current wealth, so this boundary case requires no special handling.
