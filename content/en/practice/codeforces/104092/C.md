---
title: "CF 104092C - \u0414\u0432\u043e\u0440\u0435\u0446 (\u0442\u0438\u043f\u043e\u0432\u043e\u0439)"
description: "Each palace has exactly n floors. The floors are numbered from the top, starting at 1. For the floor with index i, its base must be a square with integer side length. The area of that square cannot exceed i, and among all valid squares we always choose the largest possible one."
date: "2026-07-02T02:25:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104092
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2021-2022 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104092
solve_time_s: 41
verified: true
draft: false
---

[CF 104092C - \u0414\u0432\u043e\u0440\u0435\u0446 (\u0442\u0438\u043f\u043e\u0432\u043e\u0439)](https://codeforces.com/problemset/problem/104092/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

Each palace has exactly `n` floors. The floors are numbered from the top, starting at `1`.

For the floor with index `i`, its base must be a square with integer side length. The area of that square cannot exceed `i`, and among all valid squares we always choose the largest possible one.

If the side length is `s`, then `s² ≤ i`, so the chosen side is simply

$$s=\lfloor\sqrt{i}\rfloor.$$

The perimeter of that floor is

$$4\lfloor\sqrt{i}\rfloor.$$

We must compute the total perimeter of all floors in all three identical palaces. The required answer is

$$3\cdot4\sum_{i=1}^{n}\lfloor\sqrt{i}\rfloor
=12\sum_{i=1}^{n}\lfloor\sqrt{i}\rfloor
\pmod{10^9+7}.$$

The number of test cases reaches `10^4`, while `n` itself may be as large as `10^18`. A direct loop over every floor is immediately impossible. Even a single test case with `10^18` iterations is completely infeasible. The algorithm must run in roughly logarithmic or square root time.

A subtle point is that `n` is far beyond the range where floating point square roots remain exact. For example, values close to `10^18` cannot safely use `int(n ** 0.5)`, because rounding errors may produce the wrong integer square root. The correct implementation must use integer arithmetic.

Another easy mistake is handling the final incomplete interval. Consider

```
1
5
```

Here

$$\lfloor\sqrt{i}\rfloor=(1,1,1,2,2),$$

whose sum is `7`. Treating every block as having full length would incorrectly count the interval corresponding to `2` as containing three numbers instead of only two.

The smallest input also deserves attention.

```
1
1
```

The only floor has side length `1`, perimeter `4`, and three palaces give `12`. Forgetting the factor of three or starting the indexing from zero produces an incorrect answer.

## Approaches

The most direct solution evaluates every floor independently. For each `i` from `1` to `n`, compute `⌊√i⌋`, multiply by four, accumulate the result, and finally multiply by three. This is obviously correct because it follows the definition exactly.

Unfortunately, this requires `n` square root computations. With `n` as large as `10^18`, the running time is completely unrealistic.

The key observation is that `⌊√i⌋` changes very rarely. If

$$\lfloor\sqrt{i}\rfloor=k,$$

then `i` must satisfy

$$k^2\le i<(k+1)^2.$$

Every value inside this interval contributes the same number `k`.

Instead of processing numbers one by one, we process entire intervals. Let

$$m=\lfloor\sqrt n\rfloor.$$

For every `k<m`, the interval

$$[k^2,(k+1)^2-1]$$

is complete and has length

$$(k+1)^2-k^2=2k+1.$$

Its total contribution is

$$k(2k+1).$$

The last interval may be incomplete. It starts at `m²` and ends at `n`, contributing

$$m(n-m^2+1).$$

The remaining task is computing

$$\sum_{k=1}^{m-1}k(2k+1),$$

which expands into

$$2\sum k^2+\sum k.$$

Both sums have well known closed formulas, so every test case becomes an `O(1)` computation after obtaining the integer square root.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n)` | `O(1)` | Too slow |
| Optimal | `O(1)` arithmetic plus integer square root | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `n`.
2. Compute the integer square root `m = isqrt(n)`. This is the largest integer satisfying `m² ≤ n`.
3. Every complete interval corresponds to values `k = 1 ... m-1`. Compute

$$\sum_{k=1}^{m-1}k=\frac{(m-1)m}{2}$$

and

$$\sum_{k=1}^{m-1}k^2=\frac{(m-1)m(2m-1)}{6}.$$
4. Use these formulas to obtain

$$\sum_{k=1}^{m-1}k(2k+1)
=2\sum k^2+\sum k.$$

Every complete block contributes exactly its constant square root multiplied by its length.
5. Compute the contribution of the final partial block:

$$m(n-m^2+1).$$

This covers every remaining integer from `m²` through `n`.
6. Add both contributions together.
7. Multiply the result by `12`, because every floor contributes four times its side length and there are three identical palaces.
8. Output the result modulo `10^9+7`.

### Why it works

The crucial invariant is that every integer belongs to exactly one interval

$$[k^2,(k+1)^2-1].$$

Inside such an interval,

$$\lfloor\sqrt{i}\rfloor=k$$

for every value of `i`. The algorithm replaces many identical additions by one multiplication of the common value and the interval length. Since the intervals partition the entire range from `1` to `n`, every floor is counted exactly once with exactly the correct side length.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

MOD = 10 ** 9 + 7

t = int(input())

for _ in range(t):
    n = int(input())

    m = isqrt(n)
    x = m - 1

    sum1 = x * (x + 1) // 2
    sum2 = x * (x + 1) * (2 * x*
```
