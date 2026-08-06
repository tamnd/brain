---
title: "CF 102536H - Maggie and Dana's Mass Supper"
description: "The grid is a rectangle where the valid cells form a diagonal corridor. The corridor has width l - w + 1, and every row shifts the corridor one position to the right. A path only moves right or down, so the problem is counting monotone paths that never leave this diagonal strip."
date: "2026-08-06T20:28:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "H"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 94
verified: true
draft: false
---

[CF 102536H - Maggie and Dana's Mass Supper](https://codeforces.com/problemset/problem/102536/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid is a rectangle where the valid cells form a diagonal corridor. The corridor has width `l - w + 1`, and every row shifts the corridor one position to the right. A path only moves right or down, so the problem is counting monotone paths that never leave this diagonal strip.

A direct dynamic programming solution would store the number of ways to reach every cell. That would require processing about `l * w` cells, which is far too large because `l` can reach `5 * 10^6` and `w` can reach `5 * 10^5`.

The useful observation is that the corridor condition can be transformed into a one-dimensional walk. Let the current value be:

```
column - row
```

A right move increases this value by one and a down move decreases it by one. The start value is `0`, the final value is `l - w`, and the path is valid exactly when this value stays between `0` and `l - w`.

This turns the problem into counting walks in a bounded strip.

## Approaches

The brute force solution uses dynamic programming on the grid. For every open cell, it adds the number of ways from the cell above and the cell on the left. It is correct because every valid path reaches a cell from exactly one of those two directions. However, the number of cells can be around `2.5 * 10^12`, so this approach is impossible.

The key observation is that the one-dimensional walk has two forbidden boundaries. The reflection principle lets us count the invalid walks by reflecting every path that crosses a boundary. The result is an alternating sum of ordinary binomial coefficients.

Let:

```
n = l + w - 2
d = l - w
```

The answer becomes:

```
sum over k:
C(n, l - 1 + k(d + 2)) - C(n, l + k(d + 2))
```

Only indices between `0` and `n` matter, so the sum has a small number of terms when `d` is large, and when `d` is small the step size is small but the number of terms is still manageable.

The modulus `104857601` is prime, so factorials and inverse factorials allow every binomial coefficient to be computed in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(lw) | O(lw) | Too slow |
| Reflection + Binomial | O(l + w) | O(l + w) | Accepted |

## Algorithm Walkthrough

1. Compute `n = l + w - 2` and `step = l - w + 2`. The value `step` is the distance between consecutive reflected copies of the path.
2. Precompute factorials and inverse factorials up to `n`. Since the modulus is prime, every binomial coefficient can be obtained as:

```
C(n, k) = fact[n] * invfact[k] * invfact[n-k]
```

1. Add all terms of the form `C(n, l - 1 + k * step)` that are inside the range `[0, n]`.
2. Subtract all terms of the form `C(n, l + k * step)` that are inside the range `[0, n]`.
3. Normalize the result modulo `104857601`.

Why it works: every invalid path is paired with exactly one reflected path. The first family of binomial coefficients counts unrestricted paths, while the second family removes paths that cross the upper or lower forbidden boundary. The alternating sum leaves only paths that stay completely inside the corridor.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 104857601

def solve():
    l, w = map(int, input().split())

    n = l + w - 2
    step = l - w + 2

    fact = array('I', [1]) * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i - 1] * i) % MOD

    invfact = array('I', [1]) * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = (invfact[i] * i) % MOD

    def comb(k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    ans = 0

    x = l - 1
    while x >= 0:
        ans += comb(x)
        x -= step

    x = l - 1 + step
    while x <= n:
        ans += comb(x)
        x += step

    x = l
    while x >= 0:
        ans -= comb(x)
        x -= step

    x = l + step
    while x <= n:
        ans -= comb(x)
        x += step

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The factorial arrays use `array('I')` instead of normal Python lists because the maximum `n` is close to `5.5 * 10^6`, and Python integer objects would consume much more memory.

The four loops generate the positive and negative reflection terms separately. Starting from both directions is necessary because reflected paths can correspond to negative values of `k` as well as positive ones.

The modular inverse uses Fermat's little theorem, which is valid because `104857601` is prime.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(l + w) | Factorial preparation dominates, and the reflection sum contains far fewer terms |
| Space | O(l + w) | Two arrays store factorial and inverse factorial values |

The maximum factorial size is about `5.5 million`, so the memory usage stays well below the limit. The solution avoids any dependence on the number of cells in the original grid.

## Worked Example

For `l = 7`, `w = 5`:

```
n = 10
step = 4
```

The positive terms are:

| k | Index | Value |
| --- | --- | --- |
| 0 | 6 | C(10,6) |
| -1 | 2 | C(10,2) |

The negative terms are:

| k | Index | Value |
| --- | --- | --- |
| 0 | 7 | C(10,7) |
| -1 | 3 | C(10,3) |

The result is:

```
C(10,6) + C(10,2) - C(10,7) - C(10,3)
= 210 + 45 - 120 - 120
= 16
```

which matches the sample output.
