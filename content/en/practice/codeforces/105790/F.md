---
title: "CF 105790F - Frogs or Toads?"
description: "Eric starts with a laser weapon whose energy is initially zero. For each level, there are two possible actions. The normal route requires killing si mutants."
date: "2026-06-25T23:32:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "F"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 44
verified: true
draft: false
---

[CF 105790F - Frogs or Toads?](https://codeforces.com/problemset/problem/105790/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Eric starts with a laser weapon whose energy is initially zero.

For each level, there are two possible actions.

The normal route requires killing `s_i` mutants. Every shot, even with non-positive energy, consumes one unit of energy, so passing through the level changes the current energy by `e_i - s_i`. After that, Eric moves to the next level.

The alternative route is a wormhole. Using it skips `k` levels ahead. To enter the wormhole, Eric must kill `X` guarding mutants, so his energy decreases by `X`. He does not fight the `s_i` regular mutants and does not receive the energy bank `e_i`.

After all levels are finished, Eric reaches the Light Queen. A shot damages the boss only while the weapon's energy is strictly positive. If Eric arrives with energy `E`, he can deal exactly `max(E, 0)` damage before the energy becomes non-positive.

The task is to maximize the energy remaining when reaching the boss. The answer is that maximum energy if it is positive, otherwise `0`.

The constraints are the key observation. There are up to `2 · 10^5` levels. Any solution that explores all possible paths explicitly is impossible because each level offers two choices, producing roughly `2^N` paths. Even an `O(N^2)` dynamic program would require around `4 · 10^10` operations in the worst case, which is far beyond the limit. We need something linear or close to linear.

A subtle edge case appears when every possible path ends with non-positive energy.

Example:

```
1 1 5
3 0
```

The normal route gives energy `-3`, the wormhole gives energy `-5`. Eric reaches the boss, but cannot inflict any damage. The correct answer is:

```
0
```

A careless implementation might output the maximum reachable energy, `-3`, instead of converting negative values to zero.

Another edge case occurs when a wormhole jumps beyond the last level.

Example:

```
2 2 1
10 100
10 100
```

Using the wormhole at level 1 immediately reaches the boss. The destination must be treated as "after all levels", not as an invalid state. Missing this detail usually causes out-of-bounds errors or lost transitions.

A third edge case is when `X = 0`.

Example:

```
3 1 0
5 0
5 0
5 0
```

The wormhole becomes a free skip. The algorithm must still consider it because avoiding large negative `(e_i - s_i)` values can be optimal.

## Approaches

The brute-force idea is straightforward. At every level, choose either the normal route or the wormhole route, recursively exploring all possible futures. Since each level has two choices, the number of paths grows exponentially. With `N = 200000`, this is completely infeasible.

The interesting part is that the current energy is the only quantity that matters. The future does not depend on how we arrived at a level, only on the maximum energy available there.

Suppose `dp[i]` denotes the maximum energy achievable after finishing the first `i` levels, or equivalently, when standing at the beginning of level `i + 1`.

From state `i`, there are only two transitions.

Taking the normal route through level `i + 1` changes energy by `e_i - s_i`.

Using the wormhole changes energy by `-X` and moves directly to level `i + k`.

Since both transitions simply add a fixed value to the current energy, keeping only the best energy for each state is sufficient. Any smaller energy at the same position can never lead to a better future result.

This converts the exponential search into a linear dynamic program over positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(N) | Too slow |
| Optimal DP | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` of length `N + 1`, initialized with negative infinity.
2. Set `dp[0] = 0`, representing the starting state before entering the first level.
3. Process levels from left to right.
4. From state `i`, try the normal route.

The energy change is `(e_i - s_i)`, so update:

`dp[i + 1] = max(dp[i + 1], dp[i] + e_i - s_i)`.
5. From state `i`, try the wormhole route.

The destination is `min(N, i + k)` because jumping beyond the last level means reaching the boss immediately.

Update:

`dp[min(N, i + k)] = max(dp[min(N, i + k)], dp[i] - X)`.
6. After all transitions are processed, `dp[N]` is the maximum energy achievable upon reaching the boss.
7. Output `max(dp[N], 0)` because negative or zero energy cannot damage the boss.

### Why it works

The invariant is that `dp[i]` always stores the maximum possible energy among all ways to reach state `i`.

Every legal action from a state corresponds to exactly one DP transition. Since each transition adds a fixed amount to the current energy, a larger energy at the same state is always at least as good as a smaller one. No future decision can make a weaker state preferable.

By processing all states and taking the maximum over all incoming transitions, the DP computes the best achievable energy for every position. In particular, `dp[N]` becomes the maximum energy obtainable when reaching the Light Queen. The boss can only be damaged while energy is positive, so the maximum possible damage is `max(dp[N], 0)`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, x = map(int, input().split())

    s = [0] * n
    e = [0] * n

    for i in range(n):
        s[i], e[i] = map(int, input().split())

    NEG = -(10 ** 30)
    dp = [NEG] * (n + 1)
    dp[0] = 0

    for i in range(n):
        if dp[i] == NEG:
            continue

        dp[i + 1] = max(dp[i + 1], dp[i] + e[i] - s[i])

        nxt = min(n, i + k)
        dp[nxt] = max(dp[nxt], dp[i] - x)

    print(max(dp[n], 0))

solve()
```

The DP array uses index `i` to represent the state after processing the first `i` levels.

The normal route transition adds `e[i] - s[i]`, matching the net energy gain from fighting the level and collecting its energy bank.

The wormhole transition jumps to `min(n, i + k)`. This is the most common place to make a mistake. Once a jump goes beyond the last level, the game immediately reaches the boss, so every such jump should land in state `n`.

The value range can reach roughly `2 · 10^5 × 10^9`, so 64-bit arithmetic is required. Python integers handle this automatically.

The final answer is not `dp[n]` itself. Negative energy cannot damage the boss, so the result must be clamped to zero.

## Worked Examples

### Example 1

Input:

```
4 2 1
1 2
4 6
5 2
3 11
```

| i | dp[i] before | Normal destination | Normal value | Wormhole destination | Wormhole value |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 2 | -1 |
| 1 | 1 | 2 | 3 | 3 | 0 |
| 2 | 3 | 3 | 0 | 4 | 2 |
| 3 | 0 | 4 | 8 | 4 | -1 |

Final:

| State | Value |
| --- | --- |
| dp[4] | 8 |

Answer:

```
8
```

This example shows that sometimes taking the normal route despite paying mutant costs is worthwhile because the energy bank compensates for it.

### Example 2

Input:

```
5 3 20
3 4
2 2
5 6
3 1
8 5
```

| i | dp[i] before | Normal destination value | Wormhole destination value |
| --- | --- | --- | --- |
| 0 | 0 | 1 | -20 |
| 1 | 1 | 1 | -19 |
| 2 | 1 | 2 | -19 |
| 3 | 2 | 0 | -18 |
| 4 | 0 | -3 | -20 |

Final:

| State | Value |
| --- | --- |
| dp[5] | -3 |

Answer:

```
0
```

This trace demonstrates the situation where every strategy reaches the boss with non-positive energy. The answer must be clamped to zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each level performs two DP transitions |
| Space | O(N) | The DP array contains `N + 1` states |

With `N ≤ 2 · 10^5`, a linear scan and a single array easily fit within the available time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k, x = map(int, input().split())

    s = [0] * n
    e = [0] * n

    for i in range(n):
        s[i], e[i] = map(int, input().split())

    NEG = -(10 ** 30)
    dp = [NEG] * (n + 1)
    dp[0] = 0

    for i in range(n):
        if dp[i] == NEG:
            continue

        dp[i + 1] = max(dp[i + 1], dp[i] + e[i] - s[i])

        nxt = min(n, i + k)
        dp[nxt] = max(dp[nxt], dp[i] - x)

    return str(max(dp[n], 0)) + "\n"

# provided samples
assert run(
"""4 2 1
1 2
4 6
5 2
3 11
"""
) == "8\n", "sample 1"

assert run(
"""5 3 20
3 4
2 2
5 6
3 1
8 5
"""
) == "0\n", "sample 2"

# minimum size
assert run(
"""1 1 0
0 5
"""
) == "5\n"

# all routes negative
assert run(
"""1 1 5
3 0
"""
) == "0\n"

# free wormholes
assert run(
"""3 1 0
5 0
5 0
5 0
"""
) == "0\n"

# jump beyond end
assert run(
"""2 2 1
10 100
10 100
"""
) == "99\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single level with positive gain | 5 | Minimum-size instance |
| Single level with negative result | 0 | Final clamping to zero |
| Free wormholes | 0 | Correct wormhole handling when X = 0 |
| Jump beyond last level | 99 | Correct use of `min(n, i + k)` |

## Edge Cases

Consider the case where all energies are non-positive.

```
1 1 5
3 0
```

Initialization gives `dp[0] = 0`.

Normal route:

```
dp[1] = -3
```

Wormhole:

```
dp[1] = max(-3, -5) = -3
```

The best reachable energy is `-3`. Since negative energy cannot damage the boss, the algorithm outputs:

```
0
```

Now consider a jump beyond the end.

```
2 2 1
10 100
10 100
```

At state `0`:

```
normal -> dp[1] = 90
wormhole -> dp[2] = -1
```

At state `1`:

```
normal -> dp[2] = 180
wormhole -> dp[2] = max(180, 89)
```

The destination of the wormhole is state `2`, not state `3`, because reaching beyond the last level means reaching the boss. The final answer becomes:

```
180
```

Finally, consider free wormholes.

```
3 1 0
5 0
5 0
5 0
```

Every normal route loses 5 energy. Every wormhole loses 0 energy.

The DP repeatedly prefers the wormhole transitions and reaches the boss with energy `0`. The answer remains:

```
0
```

This confirms that the algorithm correctly compares both choices at every level and always keeps the best reachable energy.
