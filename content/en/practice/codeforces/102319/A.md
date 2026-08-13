---
title: "CF 102319A - Andrew and Efficient Change"
description: "We have a coin system containing n distinct denominations, including denomination 1. Andrew must pay separately for every amount in the consecutive interval [l, r]. For each amount, he wants the minimum possible number of coins whose values sum exactly to that amount."
date: "2026-08-14T04:49:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102319
codeforces_index: "A"
codeforces_contest_name: "UBC Summer Contest 2018"
rating: 0
weight: 102319
solve_time_s: 161
verified: true
draft: false
---

[CF 102319A - Andrew and Efficient Change](https://codeforces.com/problemset/problem/102319/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a coin system containing `n` distinct denominations, including denomination `1`. Andrew must pay separately for every amount in the consecutive interval `[l, r]`. For each amount, he wants the minimum possible number of coins whose values sum exactly to that amount.

We may introduce one additional denomination `c`, where `1 <= c <= r`. After adding it, every amount from `l` through `r` may use the new coin as many times as necessary. The objective is to minimize the sum of the minimum coin counts for all these amounts. If no new denomination improves the total, we print `0`. If several denominations give the same best total, any of them is valid. The official problem page gives the same two samples used below.

The interesting constraint is `r - l <= 50`. The absolute value of `r` can be 200000, so an algorithm that performs work proportional to `r` is reasonable, but doing that separately for every possible new denomination is not. There are at most 51 grocery amounts, while there can be as many as 200000 possible new denominations. The existing number of denominations is at most 420, so a standard dynamic program for the original coin system costs `O(nr)`, about 84 million elementary transitions in the largest case. A quadratic or cubic dependence on `r` is out of the question.

There are several edge cases that are easy to mishandle. If the requested interval consists of a single amount that is already an existing coin, no addition can improve it. For example, with

```
3
1 1
1 2 3
```

the correct output is `0`, because amount `1` already costs one coin and no payment can use fewer than one coin. A careless implementation that always chooses some candidate denomination might incorrectly print `1`.

The optimal new denomination can be smaller than `l`. For example,

```
1
100 150
1
```

has a very useful new coin of value `50`. Every amount from 100 through 150 can then be paid using two or three coins, whereas adding a coin near 100 would only make a small part of the interval cheap. Restricting candidates to `[l, r]` is consequently incorrect.

Another subtle case occurs when the new coin is larger than the interval width. Suppose `r-l=10` and we add a coin `c` larger than 10. A target can potentially use several copies of `c`, but for the purpose of finding the globally best denomination, we can replace those several copies by one coin whose value is their total. That replacement is still at most `r` and remains larger than the interval width. Missing this observation leads to an unnecessarily expensive candidate evaluation.

Finally, an existing denomination must not be treated as a new improvement. Adding a coin that is already present leaves every minimum unchanged. The algorithm simply skips such candidates.

## Approaches

A direct approach would consider every possible new denomination and solve the complete coin change problem again. For one fixed candidate `c`, we could run the usual dynamic program

`dp[x] = 1 + min(dp[x - coin])`

over all amounts up to `r`, now using the original denominations plus `c`. This is correct because the standard recurrence considers the last coin of an optimal representation.

However, this approach repeats almost the same computation for every candidate. There are up to `r` candidates, and each DP takes `O(nr)` time. In the worst case this becomes `O(nr²)`, roughly `420 * 200000²`, which is around 16.8 trillion transitions.

The key observation is that we do not actually need to recompute the original coin system. First compute `base[x]`, the minimum number of original coins needed for every `x <= r`. Then ask how adding a particular `c` changes those values.

For a small new coin, there are only a few possible denominations to inspect. More precisely, let

`W = r - l + 1`.

There are at most 51 amounts in the shopping interval, so `W <= 51`. For every candidate `c <= W`, we can compute the new DP in `O(r)` time using the recurrence

`new[x] = min(base[x], new[x-c] + 1)`.

There are only `W` such candidates, giving `O(rW)` time.

The much more useful observation handles every candidate `c > W`. Consider a representation of some target using `k >= 2` copies of the new coin. Those copies contribute value `kc`. Instead of adding denomination `c`, imagine adding denomination `kc`. Since `kc <= x <= r`, this is still an allowed new denomination. Since `c > W`, it is also a valid large candidate. The `k` coins have been replaced by one coin, so the resulting representation is no worse.

Thus, among all candidates larger than `W`, there is always a globally optimal candidate that is used at most once for every target. For a fixed such `c`, amount `x` can only improve from `base[x]` to

`min(base[x], base[x-c] + 1)`,

when `x >= c`. We only have `W` target amounts, so each large candidate takes `O(W)` time. There are at most `r` candidates, giving another `O(rW)` term.

The brute-force method works because dynamic programming completely solves one fixed coin system. It fails because it rebuilds that system for every candidate. The observation about the interval width lets us separate candidates into a small set of denominations that need a full DP and a large set where only one use of the new coin has to be considered.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nr²)` | `O(r)` | Too slow |
| Optimal | `O(nr + r(r-l+1))` | `O(r)` | Accepted |

## Algorithm Walkthrough

1. Read the existing denominations and compute `base[x]`, the minimum number of existing coins needed to form every amount `x` from `0` through `r`. The value `base[0]` is zero, and denomination `1` guarantees that every amount is reachable.
2. Compute the original total for all shopping amounts from `l` through `r`. This is the value that a new denomination must beat to be useful.
3. Let `W = r - l + 1`. For every candidate denomination `c` with `1 <= c <= W`, skip it if it already exists. Otherwise, build a temporary DP array from `0` through `r`. For amounts below `c`, the new coin cannot be used, so their value is exactly `base[x]`. For `x >= c`, the optimal solution either does not use the new coin or uses it at least once, giving the recurrence `min(base[x], new[x-c] + 1)`.
4. Sum the temporary DP values over `[l, r]`. If the sum is smaller than the best total seen so far, remember this candidate.
5. For every candidate `c > W`, again skip denominations that already exist. For each target `x` in `[l, r]`, consider either not using the new coin, costing `base[x]`, or using one copy of it, costing `base[x-c] + 1` when `x >= c`. Take the smaller value.
6. Keep the candidate producing the smallest total. If the smallest total is equal to the original total, output `0`; otherwise output the remembered denomination.

The central invariant is that `base[x]` is always the exact optimum using only the original denominations. For small candidates, the recurrence considers every possible use count of the new coin because `new[x-c]` already contains the best representation of `x-c`. For large candidates, any solution using multiple copies can be transformed into a solution using one copy of another legal large denomination, so considering only one new coin cannot exclude the globally optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data: str) -> str:
    it = iter(map(int, data.split()))
    n = next(it)
    l = next(it)
    r = next(it)

    coins = [next(it) for _ in range(n)]
    coin_set = set(coins)

    # Original minimum-coin DP.
    INF = r + 1
    base = [INF] * (r + 1)
    base[0] = 0

    # Unbounded coin change.
    for c in coins:
        if c > r:
            continue
        for x in range(c, r + 1):
            v = base[x - c] + 1
            if v < base[x]:
                base[x] = v

    width = r - l + 1
    original_total = sum(base[l:r + 1])

    best_total = original_total
    best_coin = 0

    # Small candidates: a full DP over [0, r] is affordable because
    # there are at most width <= 51 of them.
    for c in range(1, min(width, r) + 1):
        if c in coin_set:
            continue

        cur = base[:]

        for x in range(c, r + 1):
            v = cur[x - c] + 1
            if v < cur[x]:
                cur[x] = v

        total = sum(cur[l:r + 1])

        if total < best_total:
            best_total = total
            best_coin = c

    # Large candidates: c > width.
    # A globally optimal large candidate never needs to be used twice.
    for c in range(width + 1, r + 1):
        if c in coin_set:
            continue

        total = 0

        for x in range(l, r + 1):
            v = base[x]

            if x >= c:
                nv = base[x - c] + 1
                if nv < v:
                    v = nv

            total += v

        if total < best_total:
            best_total = total
            best_coin = c

    return str(best_coin)

def main():
    data = sys.stdin.buffer.read().decode()
    print(solve(data))

if __name__ == "__main__":
    main()
```

The first DP constructs `base`. Processing denominations one at a time and amounts in increasing order is the standard unbounded coin change recurrence, because after processing coin `c`, `base[x-c]` may already use any number of copies of `c`.

The small-candidate loop copies `base` and then relaxes every amount using the new denomination. Starting from `base` is equivalent to saying that the new coin may be used zero times. The forward traversal makes repeated uses available automatically.

The split uses `width`, not `r-l`, because there are exactly `r-l+1` shopping amounts. Using `r-l` here would create an off-by-one error when the interval has one amount.

For large candidates, `x-c` may be negative, so the code checks `x >= c` before indexing `base`. No other amount outside `[0,r]` is needed. Python integers also avoid any overflow concerns, although all relevant totals are much smaller than the limits of ordinary 64-bit integers.

A candidate already present in `coin_set` is skipped. Adding an existing denomination cannot improve the coin system, and processing it would only waste time.

## Worked Examples

The first official sample is

```
1
10 10
1
```

The original system contains only the one-valued coin, so amount 10 requires ten coins. The interval width is one, so candidate `1` is skipped because it already exists. Every candidate greater than one is handled by the large-candidate case.

| Candidate | Target | Original | With candidate | Total |
| --- | --- | --- | --- | --- |
| 10 | 10 | 10 | 1 | 1 |

The best candidate is `10`, so the output is `10`. This also demonstrates the single-target boundary case.

The second official sample is

```
3
10 15
1 5 10
```

The original minimum counts are as follows.

| Amount `x` | `base[x]` |
| --- | --- |
| 10 | 1 |
| 11 | 2 |
| 12 | 2 |
| 13 | 3 |
| 14 | 3 |
| 15 | 2 |

The original total is `13`. The interval contains six amounts, so `W=6`. Candidate `12` is a large candidate. It is not already present, and the one-use calculation gives the following values.

| Amount `x` | `base[x]` | `base[x-12]+1` | New minimum |
| --- | --- | --- | --- |
| 10 | 1 | unavailable | 1 |
| 11 | 2 | unavailable | 2 |
| 12 | 2 | 1 | 1 |
| 13 | 3 | 2 | 2 |
| 14 | 3 | 3 | 3 |
| 15 | 2 | 2 | 2 |

The new total is `11`, so denomination `12` improves the original system and is an optimal answer for the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nr + r(r-l+1))` | The original DP costs `O(nr)`. Small candidates cost `O(rW)` and large candidates cost `O(rW)`, where `W=r-l+1<=51`. |
| Space | `O(r)` | The original DP and one temporary DP each contain `r+1` values. |

With `r <= 200000`, `n <= 420`, and `W <= 51`, the expensive part is the single original coin-change DP. The candidate search depends on the width of the shopping interval rather than its absolute position, which is exactly why the `r-l <= 50` restriction makes the solution practical.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided sample 1
assert run("""\
1
10 10
1
""") == "10", "sample 1"

# Provided sample 2
assert run("""\
3
10 15
1 5 10
""") == "12", "sample 2"

# Minimum-size input. Amount 1 is already a one-coin payment,
# so no new denomination can improve it.
assert run("""\
1
1 1
1
""") == "0", "minimum-size case"

# All requested amounts are already denominations.
# Adding anything cannot make a payment cheaper than one coin.
assert run("""\
3
1 3
1 2 3
""") == "0", "no improvement"

# The optimal new denomination is smaller than l.
# Coin 50 makes every amount from 100 through 150 require at most 3 coins.
assert run("""\
1
100 150
1
""") == "50", "candidate below l"

# Boundary case where the best candidate is exactly r.
assert run("""\
2
10 10
1 5
""") == "10", "candidate at r"

# Maximum-size structural test. The existing denominations are 1..420.
# Adding 199950 gives one coin for 199950 and two coins for every
# following amount, reaching the lower bound of 101 total coins.
coins = " ".join(map(str, range(1, 421)))
assert run(f"""\
420
199950 200000
{coins}
""") == "199950", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1` | `0` | Minimum-size input and an already optimal one-coin payment |
| `3 / 1 3 / 1 2 3` | `0` | No possible improvement when every target already has a one-coin representation |
| `1 / 100 150 / 1` | `50` | The optimal denomination can be strictly smaller than `l` |
| `2 / 10 10 / 1 5` | `10` | Candidate exactly at the upper boundary `r` |
| `420 / 199950 200000 / 1..420` | `199950` | Maximum `n`, large `r`, and interval-width boundary |

## Edge Cases

The first edge case is an interval containing a single amount that is already a coin. For

```
3
1 1
1 2 3
```

the original cost of amount `1` is already one coin. Every legal payment of a positive amount needs at least one coin, so the original total is optimal. The DP computes `base[1]=1`, every candidate either leaves this value unchanged or is skipped because it already exists, and `best_coin` remains zero.

The second edge case is a useful new denomination smaller than the entire shopping interval. For

```
1
100 150
1
```

the candidate `50` is handled by the small-candidate loop because the interval contains 51 amounts. The temporary DP repeatedly applies `cur[x] = min(base[x], cur[x-50]+1)`. Amounts 100 through 150 can consequently use two or three 50-valued coins, with ones filling the remainder. A strategy restricted to candidates at least `l` would never discover this improvement.

The third edge case concerns multiple copies of a large new coin. Suppose the interval width is 10 and a candidate has value 20. If a target uses two copies, those two copies have total value 40. Since the target itself is at least 40, denomination 40 is also a legal candidate. Replacing two 20-valued coins by one 40-valued coin reduces the coin count. The same argument works for any number of copies. This is why the large-candidate loop only checks `base[x-c]+1`.

The fourth edge case is an existing denomination. If the candidate `c` belongs to the original set, adding it again changes nothing. The `coin_set` membership check removes such candidates before either evaluation path, preventing a zero improvement from being mistaken for a useful new denomination.

The final edge case is the right boundary of the candidate range. A new coin larger than `r` can never appear in a payment for an amount at most `r`, so the search stops at `r`. Conversely, `c=r` must be included. In the input

```
2
10 10
1 5
```

the new coin `10` changes the cost of the only target from two coins to one, so the correct answer is `10`. The loop uses `range(width + 1, r + 1)` for large candidates and includes this upper endpoint exactly.
