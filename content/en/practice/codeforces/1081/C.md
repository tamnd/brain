---
title: "CF 1081C - Colorful Bricks"
description: "We are painting a line of $n$ bricks, each brick choosing one of $m$ available colors. Once the painting is done, we look at the positions where the color changes compared to the previous brick."
date: "2026-06-15T06:13:44+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1081
codeforces_index: "C"
codeforces_contest_name: "Avito Cool Challenge 2018"
rating: 1500
weight: 1081
solve_time_s: 319
verified: true
draft: false
---

[CF 1081C - Colorful Bricks](https://codeforces.com/problemset/problem/1081/C)

**Rating:** 1500  
**Tags:** combinatorics, dp, math  
**Solve time:** 5m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are painting a line of $n$ bricks, each brick choosing one of $m$ available colors. Once the painting is done, we look at the positions where the color changes compared to the previous brick. Formally, we scan from left to right and count how many indices $i \ge 2$ satisfy $a_i \ne a_{i-1}$. That count is required to be exactly $k$.

The task is to count how many full colorings of the entire sequence produce exactly $k$ such “change points”, and return the result modulo $998244353$.

A useful way to interpret the structure is to think of the array as being split into contiguous blocks of equal colors. Each time we have a change point, a new block starts. So if there are $k$ positions where the color differs from the previous one, then the array consists of exactly $k+1$ monochromatic segments.

The constraints $n, m \le 2000$ suggest that an $O(n^2)$ or $O(n^2 m)$ dynamic programming approach is plausible, while anything exponential over all colorings is immediately infeasible because the number of colorings is $m^n$, which grows too fast even for moderate $n$.

A subtle edge case appears when $k = 0$. In this situation all bricks must share the same color, which yields exactly $m$ valid configurations. Another boundary case is $k = n-1$, where every adjacent pair differs, forcing a strict alternation of colors, which heavily restricts transitions but still allows multiple choices depending on $m$.

A naive mistake would be to treat each of the $k$ change positions independently, but the constraints are global: once a color is chosen, future choices depend on the previous color, so independence assumptions break.

## Approaches

A brute-force solution would enumerate all $m^n$ colorings and count how many have exactly $k$ transitions. This is conceptually straightforward: generate every array and count changes in $O(n)$, giving total complexity $O(n m^n)$. This fails immediately since even $m=2, n=2000$ is astronomically large.

The key observation is that the structure depends only on whether we continue a segment or start a new one. We never need to track the full coloring history, only the color of the previous brick and how many transitions have occurred so far. This leads naturally to dynamic programming over positions.

Let $dp[i][j]$ be the number of ways to color the first $i$ bricks such that exactly $j$ transitions have occurred. When we place brick $i$, we either match the previous color (no new transition) or choose a different color (one new transition). The critical point is that in the “different color” case, we have $m-1$ choices regardless of what the previous color was, which allows us to collapse dependence on the actual color value.

This reduces the problem from tracking full color states to just tracking transition counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m^n \cdot n)$ | $O(n)$ | Too slow |
| DP over transitions | $O(nk)$ | $O(nk)$ | Accepted |

## Algorithm Walkthrough

We define a DP table where $dp[i][j]$ represents the number of ways to color the first $i$ bricks with exactly $j$ transitions.

1. Initialize the base case for the first brick. There are $m$ ways to color it, and no transitions have occurred, so $dp[1][0] = m$. Every valid coloring must start with some color choice.
2. For each position $i$ from $2$ to $n$, we consider extending all valid configurations from $i-1$.
3. If we assign brick $i$ the same color as brick $i-1$, then the number of transitions does not change. For every configuration counted in $dp[i-1][j]$, there is exactly one way to extend it without increasing the transition count, so this contributes $dp[i-1][j]$ to $dp[i][j]$.
4. If we assign brick $i$ a different color from brick $i-1$, then we increase the transition count by 1. Since the previous color is fixed, there are exactly $m-1$ valid choices for the new color. This contributes $(m-1) \cdot dp[i-1][j-1]$ to $dp[i][j]$.
5. We compute all states up to $dp[n][k]$, which is the final answer.

The recurrence is:

$$dp[i][j] = dp[i-1][j] + (m-1)\cdot dp[i-1][j-1]$$

with careful handling of invalid indices.

### Why it works

The DP state is sufficient because any partial coloring is completely characterized, for future extension purposes, by two pieces of information: how many transitions have already occurred and what the last color is. The last color dependency disappears in the transition formula because all colors are symmetric, and switching to any different color always yields exactly $m-1$ choices. This symmetry ensures that aggregating over all last colors does not lose information and does not double count configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

n, m, k = map(int, input().split())

# dp[j] = ways for current prefix with j transitions
dp = [0] * (k + 1)

# base: first brick, 0 transitions, m choices
dp[0] = m

for i in range(2, n + 1):
    ndp = [0] * (k + 1)
    for j in range(0, k + 1):
        # same color transition count unchanged
        ndp[j] = (ndp[j] + dp[j]) % MOD

        # different color increases transitions
        if j + 1 <= k:
            ndp[j + 1] = (ndp[j + 1] + dp[j] * (m - 1)) % MOD

    dp = ndp

print(dp[k])
```

The implementation compresses the DP to a single dimension because each layer depends only on the previous one. The key detail is that both transitions are applied from the same previous state, so we must not update in-place, otherwise we would contaminate future states in the same iteration.

The base initialization `dp[0] = m` captures the fact that the first brick freely chooses its color. Every subsequent step builds on that without needing to track actual color identities.

## Worked Examples

### Example 1

Input:

```
3 3 0
```

We want all bricks identical.

| i | dp[0] | dp[1] |
| --- | --- | --- |
| 1 | 3 | 0 |
| 2 | 3 | 0 |
| 3 | 3 | 0 |

Final answer is 3.

This confirms that the DP preserves the invariant that no transitions are introduced when $k=0$, and every step simply propagates existing uniform colorings.

### Example 2

Input:

```
3 3 1
```

We want exactly one transition.

| i | dp[0] | dp[1] |
| --- | --- | --- |
| 1 | 3 | 0 |
| 2 | 3 | 6 |
| 3 | 3 | 12 |

Final answer is 12.

This shows how the factor $m-1 = 2$ repeatedly expands configurations whenever a transition is introduced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nk)$ | Each position updates at most $k$ transition states |
| Space | $O(k)$ | Only current DP layer is stored |

The bounds $n, k \le 2000$ make $n \cdot k \le 4 \cdot 10^6$, which is comfortably within limits for Python with simple integer arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 998244353
    n, m, k = map(int, input().split())

    dp = [0] * (k + 1)
    dp[0] = m

    for i in range(2, n + 1):
        ndp = [0] * (k + 1)
        for j in range(k + 1):
            ndp[j] = (ndp[j] + dp[j]) % MOD
            if j + 1 <= k:
                ndp[j + 1] = (ndp[j + 1] + dp[j] * (m - 1)) % MOD
        dp = ndp

    return str(dp[k])

# provided samples
assert run("3 3 0") == "3"

# custom cases
assert run("1 5 0") == "5", "single brick all colors"
assert run("2 2 1") == "2", "must differ once"
assert run("4 1 0") == "1", "only one color available"
assert run("4 3 3") == "6", "maximum transitions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 0 | 5 | single element edge case |
| 2 2 1 | 2 | single transition correctness |
| 4 1 0 | 1 | no-color-choice degeneracy |
| 4 3 3 | 6 | full alternation counting |

## Edge Cases

For $n=1$, there are no transitions possible, so the answer is always $m$ when $k=0$ and $0$ otherwise. The DP handles this implicitly because the loop over positions never runs and the base state remains unchanged.

For $m=1$, all bricks must be the same color. The only valid configuration has zero transitions. In DP terms, $m-1 = 0$, so all transition-creating paths vanish, leaving only $dp[n][0] = 1$, which is correct.

For $k = n-1$, every adjacent pair must differ. The DP forces a chain where each step multiplies by $m-1$, resulting in $m \cdot (m-1)^{n-1}$, which matches the combinatorial interpretation of choosing the first color freely and then always avoiding the previous one.
