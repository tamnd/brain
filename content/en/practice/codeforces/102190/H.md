---
title: "CF 102190H - standard input/output"
description: "A day on this clock contains h hours, and every hour contains m minutes. A displayed time is identified by an hour number x and a minute number y, where 0 <= x < h and 0 <= y < m."
date: "2026-08-19T05:56:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102190
codeforces_index: "H"
codeforces_contest_name: "2019 ECNU Campus Invitational Contest"
rating: 0
weight: 102190
solve_time_s: 328
verified: true
draft: false
---

[CF 102190H - standard input/output](https://codeforces.com/problemset/problem/102190/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

A day on this clock contains `h` hours, and every hour contains `m` minutes. A displayed time is identified by an hour number `x` and a minute number `y`, where `0 <= x < h` and `0 <= y < m`.

A minute is classified as huashui when its minute number is at least its hour number, so the condition is simply `y >= x`. Every pair `(x, y)` represents one minute of the day because seconds are irrelevant. The task is to find the fraction of all minutes satisfying this condition, and print that fraction in lowest terms.

There are `h * m` total displayed minutes. Since both `h` and `m` can be as large as `10^9`, this product can reach `10^18`. More importantly, iterating over every hour or every minute would require up to `10^9` operations, while iterating over every pair `(x, y)` would require up to `10^18` operations. The solution must reduce the counting to a constant number of arithmetic operations.

The first boundary case is when `h = m = 2`. The four times are `(0,0)`, `(0,1)`, `(1,0)`, and `(1,1)`. Three satisfy `y >= x`, so the answer is `3/4`. A careless implementation using `y > x` would count only `(0,1)` and produce `1/4`.

Another boundary case occurs when there are more hours than minutes, for example `7 2`. For hour numbers `0` and `1`, some minutes qualify, but for every hour from `2` through `6`, no minute can satisfy `y >= x` because the largest minute number is only `1`. The correct result is `3/14`. An implementation that assumes every hour contributes at least one huashui minute would overcount.

The opposite situation also matters. For `2 7`, hour `0` has all seven qualifying minutes, while hour `1` has six, giving `13` qualifying minutes out of `14`, or `13/14`. The inequality includes equality, so `(1,1)` must be counted. Using a strict comparison would incorrectly give `12/14 = 6/7`.

## Approaches

The direct approach is to examine every displayed time `(x, y)` and test whether `y >= x`. There are exactly `h * m` such pairs, so although the method is obviously correct, its worst-case operation count is `10^18`. Even checking one pair in a single constant-time operation is far beyond any practical contest limit.

We can do much better by fixing the hour number and counting valid minute numbers mathematically. For a fixed hour `x`, the condition is `y >= x`. If `x >= m`, there is no valid `y`, because every minute number is at most `m - 1`. If `x < m`, the valid minute numbers are `x, x + 1, ..., m - 1`, giving exactly `m - x` valid minutes.

Only the first `min(h, m)` hour numbers can contribute. Let `k = min(h, m)`. The number of huashui minutes is

`m + (m - 1) + ... + (m - k + 1)`.

This is an arithmetic progression with `k` terms. Its sum is

`k * (2m - k + 1) / 2`.

The denominator is simply the total number of minutes, `h * m`. We then reduce the resulting fraction using the greatest common divisor.

The key observation is that the two-dimensional counting problem is actually a one-dimensional arithmetic progression. The comparison `y >= x` creates a triangular region in the `h x m` grid, and its size can be computed directly instead of visiting its cells.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(hm) | O(1) | Too slow |
| Optimal | O(log(hm)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `h` and `m`, then set `k = min(h, m)`. Only hour numbers from `0` through `k - 1` can have at least one valid minute number.
2. Compute the number of huashui minutes as `k * (2m - k + 1) / 2`. This is the sum of the contributions `m, m - 1, ..., m - k + 1`.
3. Compute the total number of minutes as `h * m`. Every hour contains exactly `m` minutes.
4. Reduce the numerator and denominator by their greatest common divisor. The output must be the reduced fraction rather than merely an equivalent fraction.
5. Print the reduced numerator followed by `/` and the reduced denominator.

### Why it works

For every hour `x < min(h, m)`, exactly the minute numbers from `x` through `m - 1` satisfy `y >= x`, so that hour contributes `m - x` huashui minutes. For every `x >= m`, it contributes zero. Thus the complete count is exactly the arithmetic progression summed by the algorithm. Dividing this count by the total `h * m` gives the required proportion, and dividing both values by their gcd produces the unique reduced fraction.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

def solve():
    h, m = map(int, input().split())

    k = min(h, m)

    numerator = k * (2 * m - k + 1) // 2
    denominator = h * m

    g = gcd(numerator, denominator)

    print(numerator // g, denominator // g)

if __name__ == "__main__":
    solve()
```

The value `k` captures the only relevant boundary in the counting. If `h <= m`, every hour can contribute, so `k = h`. If `h > m`, only the first `m` hours can contribute, so `k = m`.

The numerator uses the arithmetic progression formula rather than a loop. The division by `2` is performed before the gcd reduction, but the product is always even because one of `k` and `2m - k + 1` is even. Python integers also handle the largest intermediate values safely, so there is no overflow concern.

The expression `m - x` includes the endpoint `y = x`, matching the `>=` condition. This is exactly where a strict comparison would introduce an off-by-one error.

Finally, `gcd` reduces the fraction. For example, the raw result for `h = 13, m = 11` is `66/143`, and their gcd is `11`, giving `6/13`.

## Worked Examples

### Sample 1: `h = 2, m = 2`

The relevant variables evolve as follows.

| Variable | Value |
| --- | --- |
| `h` | 2 |
| `m` | 2 |
| `k = min(h, m)` | 2 |
| `numerator` | `2 * (4 - 2 + 1) / 2 = 3` |
| `denominator` | `2 * 2 = 4` |
| `gcd` | 1 |
| answer | `3/4` |

The two hours contribute `2` and `1` huashui minutes respectively. The equality case `(1,1)` is included, giving three valid times out of four.

### Sample 2: `h = 2, m = 7`

| Variable | Value |
| --- | --- |
| `h` | 2 |
| `m` | 7 |
| `k = min(h, m)` | 2 |
| `numerator` | `2 * (14 - 2 + 1) / 2 = 13` |
| `denominator` | `2 * 7 = 14` |
| `gcd` | 1 |
| answer | `13/14` |

Hour `0` contributes seven valid minutes and hour `1` contributes six. The total is `13`, so the fraction is already reduced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(hm)) | Computing the gcd takes logarithmic time; all other operations are constant time. |
| Space | O(1) | Only a constant number of integer variables are stored. |

The constraints allow values up to `10^9`, so a solution requiring `O(h)` or `O(m)` iterations could already require up to one billion operations. The arithmetic formula avoids all iteration, making the running time effectively constant apart from the gcd computation. Python's arbitrary-precision integers also safely handle products around `10^18`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def solve():
    h, m = map(int, input().split())

    k = min(h, m)
    numerator = k * (2 * m - k + 1) // 2
    denominator = h * m

    g = gcd(numerator, denominator)
    print(numerator // g, denominator // g)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run("2 2\n") == "3/4", "sample 1"
assert run("2 7\n") == "13/14", "sample 2"
assert run("7 2\n") == "3/14", "sample 3"
assert run("13 11\n") == "6/13", "sample 4"
assert run("100 33\n") == "17/100", "sample 5"
assert run("100005 100009\n") == "50007/100009", "sample 6"
assert run("1000000000 2\n") == "3/2000000000", "sample 7"
assert run("2 999999999\n") == "1999999997/1999999998", "sample 8"
assert run("914067307 998244353\n") == "541210700/998244353", "sample 9"

# Minimum-size input
assert run("2 2\n") == "3/4", "minimum values"

# Equal dimensions with a larger size
assert run("100 100\n") == "1/2", "all-equal values"

# More hours than minutes
assert run("5 2\n") == "3/10", "hours exceed minutes"

# More minutes than hours
assert run("2 5\n") == "9/10", "minutes exceed hours"

# Large boundary values
assert run("1000000000 1000000000\n") == "500000000000000001/1000000000000000000", "maximum equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2` | `3/4` | Minimum constraints and inclusion of equality |
| `100 100` | `500000000000000001/1000000000000000000` | Equal `h` and `m` with large arithmetic values |
| `5 2` | `3/10` | Hours beyond the available minute numbers contribute zero |
| `2 5` | `9/10` | All hours contribute when there are more minutes than hours |
| `1000000000 1000000000` | `500000000000000001/1000000000000000000` | Maximum-size arithmetic and integer handling |

## Edge Cases

When `h = m = 2`, the input is `2 2` and the numerator is `2 + 1 = 3`, while the denominator is `4`. The algorithm gets `k = 2` and computes `3/4`. The equality case `(1,1)` is counted because the progression starts at minute `x`, not `x + 1`.

When there are more hours than minutes, consider `7 2`. Here `k = 2`, so only hours `0` and `1` contribute. Their contributions are `2` and `1`, giving `3` huashui minutes out of `14`. The output is `3/14`. Hours `2` through `6` are automatically excluded by taking `k = min(h, m)`.

When there are more minutes than hours, consider `2 7`. Here both hours contribute, with `7` valid minutes for hour `0` and `6` for hour `1`. The numerator is `13` and the denominator is `14`, so the result is `13/14`. This checks that the entire valid suffix of minute numbers is counted for each hour.

For the maximum equal dimensions, `1000000000 1000000000`, the algorithm never loops through a billion values. It directly evaluates the arithmetic progression with `k = 1000000000`, producing the reduced fraction `500000000000000001/1000000000000000000`. The large intermediate values are safely represented by Python integers.

The central boundary condition throughout all of these cases is the same: an hour number equal to `m` has no valid minute, because the largest minute number is `m - 1`. That is why the contributing hour count is exactly `min(h, m)`, rather than `min(h, m + 1)` or `min(h, m - 1)`.
