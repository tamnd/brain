---
title: "CF 102416C - Quick coffee"
description: "We need to make exactly d dollars of change. The available coin denominations are every integer from a through some upper bound b, inclusive, and we may use any denomination any number of times."
date: "2026-08-12T20:49:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102416
codeforces_index: "C"
codeforces_contest_name: "Edinburgh Competition 2019"
rating: 0
weight: 102416
solve_time_s: 152
verified: true
draft: false
---

[CF 102416C - Quick coffee](https://codeforces.com/problemset/problem/102416/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to make exactly `d` dollars of change. The available coin denominations are every integer from `a` through some upper bound `b`, inclusive, and we may use any denomination any number of times. The task is to find the smallest possible `b` for which `d` can be represented as a sum of these coins.

The input contains `a` and `d`, with `1 <= a <= d <= 10^9`. Since the values can reach one billion, an algorithm that checks a linear number of possible values is far too expensive for the 1 second limit. We need to reduce the problem to constant-time arithmetic rather than trying candidate values one by one.

The first boundary case is `a = d`. The only way to make `d` is to use the coin of value `d`, so the answer must be `d`. For example, `10 10` gives `10`. A careless approach that assumes at least two coins are needed could incorrectly return a smaller value.

Another small case is `a = 1`. For example, `1 7` has answer `1`, because the coin of value `1` alone can make every positive amount. A search that starts from `a + 1` would miss this immediately.

The case where `d` is divisible by `a` also matters. For `6 18`, three coins of value `6` already make the target, so `b = 6`. A solution based on rounding `d / floor(d / a)` incorrectly with floating-point arithmetic could introduce precision problems at large values, so integer ceiling division is preferable.

## Approaches

A direct approach is to try every possible upper denomination `b`, starting at `a`. For each candidate, we could determine whether `d` can be formed using coins from `a` through `b`. This is correct because we inspect the candidates in increasing order, so the first feasible one is necessarily the minimum.

The problem is that `b` can be as large as `d`, and `d` can be `10^9`. In the worst case this means checking roughly `10^9` candidates. Even if each candidate could be tested in constant time, that is about one billion operations, which is nowhere near appropriate for a 1 second time limit.

The useful observation comes from fixing the number of coins rather than fixing the largest denomination. Suppose we use exactly `k` coins. The smallest possible sum is `ka`, because every coin is at least `a`. The largest possible sum is `kb`, because every coin is at most `b`.

More importantly, because every denomination between `a` and `b` exists, every integer sum between `ka` and `kb` is achievable. Thus `d` can be formed with exactly `k` coins precisely when

`ka <= d <= kb`.

The first inequality gives `k <= floor(d / a)`. Let

`q = floor(d / a)`.

If we can use at most `q` coins, then choosing `q` coins gives us the largest possible flexibility on the lower bound, because `qa <= d`. We only need `b` large enough that `q` coins can reach `d`, which means

`qb >= d`.

Therefore the smallest possible `b` is

`ceil(d / q)`,

where `q = floor(d / a)`.

There is no reason to consider fewer than `q` coins. If `k < q`, then `ceil(d / k) >= ceil(d / q)`, so requiring fewer coins can only make the necessary maximum denomination larger or equal. The brute-force search over possible `b` has consequently been reduced to two integer divisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d - a + 1) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `a` and `d`. These are the minimum available coin value and the target amount.
2. Compute `q = d // a`. This is the maximum number of coins of value at least `a` that can possibly fit into a sum of `d`.
3. Compute the smallest denomination bound that lets `q` coins reach `d`. We need `q * b >= d`, so use integer ceiling division:

`b = (d + q - 1) // q`.
4. Print `b`. Since `q` is the largest feasible number of coins, this value is the smallest possible upper denomination.

### Why it works

Let `q = floor(d / a)`. Since `qa <= d`, using `q` coins does not exceed the target when all of them have value `a`. We need those `q` coins to be capable of reaching `d`, which requires `qb >= d`.

Because the available denominations form the complete integer interval from `a` to `b`, every sum between `qa` and `qb` is achievable by exactly `q` coins. Thus `b = ceil(d / q)` is sufficient.

For any smaller number of coins `k < q`, reaching `d` would require `b >= ceil(d / k)`. Since `k < q`, we have `ceil(d / k) >= ceil(d / q)`. Hence no smaller `b` can work with fewer coins. The computed value is both feasible and minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, d = map(int, input().split())

q = d // a
b = (d + q - 1) // q

print(b)
```

The value `q` is computed with integer division, so it is exactly `floor(d / a)`. Since `a <= d`, `q` is always at least `1`, which makes the subsequent division safe.

The expression `(d + q - 1) // q` performs ceiling division without floating-point arithmetic. This matters because the input can contain values up to `10^9`, and integer arithmetic gives an exact result with no rounding concerns.

Python integers also have arbitrary precision, so there is no integer overflow issue. In languages with fixed-width integer types, the same formula is still safe for these constraints with standard 64-bit integers.

## Worked Examples

For the first sample, `a = 19` and `d = 60`.

| Variable | Value | Reason |
| --- | --- | --- |
| `a` | 19 | Minimum coin |
| `d` | 60 | Target amount |
| `q = d // a` | 3 | At most three coins can be used |
| `b = ceil(d / q)` | 20 | Three coins of maximum value 20 can reach 60 |
| Answer | 20 | Minimum valid upper denomination |

With coins `19` and `20`, the target is simply `20 + 20 + 20 = 60`. With only denomination `19`, the possible sums around the target do not include `60`, because three coins give `57` and four coins give `76`. Thus `20` is exactly the first feasible upper bound.

For the second sample, `a = 100` and `d = 914`.

| Variable | Value | Reason |
| --- | --- | --- |
| `a` | 100 | Minimum coin |
| `d` | 914 | Target amount |
| `q = d // a` | 9 | At most nine coins can be used |
| `b = ceil(d / q)` | 102 | Nine coins need maximum denomination at least 102 |
| Answer | 102 | Minimum valid upper denomination |

With denominations from `100` through `102`, nine coins can make `914`. Start with nine `100` coins for `900`, then increase the value of seven of those coins by `2`, giving `102 + 102 + 102 + 102 + 102 + 102 + 102 + 100 + 100 = 914`. With `b = 101`, nine coins have maximum total value `909`, so that bound is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs a constant number of integer operations. |
| Space | O(1) | Only a few integer variables are stored. |

The constraints allow values up to `10^9`, which makes any search proportional to the target potentially reach one billion iterations. The constant-time solution avoids that entirely and easily fits within the 1 second and 256 MB limits.

## Test Cases

```python
import sys
import io

def solve(data: str) -> str:
    a, d = map(int, data.split())

    q = d // a
    b = (d + q - 1) // q

    return str(b)

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided samples
assert run("19 60") == "20", "sample 1"
assert run("100 914") == "102", "sample 2"

# Minimum-size input
assert run("1 1") == "1", "minimum values"

# Same minimum and target
assert run("10 10") == "10", "a equals d"

# Divisible case
assert run("6 18") == "6", "d is divisible by a"

# Small boundary case
assert run("3 10") == "5", "ceil(10 / floor(10 / 3)) = 5"

# Large values
assert run("500000000 1000000000") == "500000000", "large divisible case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum possible input and `q = 1` |
| `10 10` | `10` | Boundary where the minimum coin equals the target |
| `6 18` | `6` | Exact divisibility and ceiling division |
| `3 10` | `5` | Non-divisible case that catches rounding errors |
| `500000000 1000000000` | `500000000` | Large values and constant-time arithmetic |

## Edge Cases

For `a = d`, consider `10 10`. The calculation gives `q = 10 // 10 = 1`, followed by `b = ceil(10 / 1) = 10`. The result is correct because the only available denomination that can make the target is `10` itself. The algorithm does not accidentally assume that multiple coins are required.

For `a = 1`, consider `1 7`. We obtain `q = 7`, so `b = ceil(7 / 7) = 1`. This says that the single denomination `1` is enough. Indeed, seven coins of value `1` make the target exactly. This case also confirms that the answer can equal the smallest possible input value `a`.

For an exactly divisible target, consider `6 18`. Here `q = 18 // 6 = 3`, and `b = ceil(18 / 3) = 6`. Three coins of value `6` make `18`, so no larger denomination is necessary. The calculation lands exactly on `a`, which is the smallest possible answer.

For a non-divisible target, consider `3 10`. We have `q = 10 // 3 = 3`. Three coins must reach `10`, so the maximum denomination must satisfy `3b >= 10`, giving `b = 4`. The actual formula yields `(10 + 3 - 1) // 3 = 12 // 3 = 4`, not `3`. With denominations `3` and `4`, the target is `3 + 3 + 4 = 10`. This is the kind of case that exposes an incorrect use of ordinary floor division.

Finally, consider the maximum target `a = 500000000`, `d = 1000000000`. We get `q = 2`, and `b = ceil(1000000000 / 2) = 500000000`. Two coins of value `500000000` make the target exactly. The computation remains constant-time even at the largest input scale.
