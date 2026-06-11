---
title: "CF 1162A - Zoning Restrictions Again"
description: "We have a street with n building positions. Every position can contain a house whose height is an integer between 0 and h. The profit from a house of height a is a², so taller houses are always better. The city imposes m zoning rules."
date: "2026-06-12T02:23:56+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1162
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 557 (Div. 2) [based on Forethought Future Cup - Final Round]"
rating: 800
weight: 1162
solve_time_s: 79
verified: true
draft: false
---

[CF 1162A - Zoning Restrictions Again](https://codeforces.com/problemset/problem/1162/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a street with `n` building positions. Every position can contain a house whose height is an integer between `0` and `h`.

The profit from a house of height `a` is `a²`, so taller houses are always better. The city imposes `m` zoning rules. Each rule covers a segment of positions `[l, r]` and says that the tallest house inside that segment cannot exceed some value `x`.

The task is to choose a height for every position so that all restrictions are satisfied and the total profit, the sum of squares of all heights, is as large as possible.

The constraints are very small. Both `n` and `m` are at most `50`. Even an algorithm that performs work proportional to every restriction times every position is completely safe. An `O(nm)` or `O(n²m)` solution runs instantly.

The main challenge is understanding how the range restrictions affect individual houses. A restriction says that the maximum height inside a range cannot exceed `x`. That means every house inside that range must also be at most `x`. If even one house were taller than `x`, the maximum of the range would exceed `x` and the restriction would be violated.

A common mistake is to treat a restriction as applying only to one position.

Consider:

```
3 10 1
1 3 5
```

Every house lies inside the restricted range, so every height must be at most `5`.

The optimal heights are:

```
[5, 5, 5]
```

Profit:

```
25 + 25 + 25 = 75
```

A careless interpretation might allow heights such as `[10, 10, 10]`, which clearly violate the restriction.

Another easy mistake is forgetting that multiple restrictions can overlap.

Example:

```
3 10 2
1 2 7
2 3 4
```

Position `2` belongs to both ranges. Its height must satisfy both limits, so its effective maximum is:

```
min(7, 4) = 4
```

The optimal heights become:

```
[7, 4, 4]
```

Ignoring one of the restrictions would produce an invalid answer.

A final subtle point is that some positions may never appear in any restriction.

Example:

```
3 10 1
2 2 3
```

Position `1` and position `3` are unrestricted except for the global limit `h = 10`, so they should remain at height `10`.

The optimal heights are:

```
[10, 3, 10]
```

Profit:

```
100 + 9 + 100 = 209
```

## Approaches

A brute-force idea is to try every possible assignment of heights and keep the best valid one. Each position has up to `h + 1` choices, so there are `(h + 1)^n` possible configurations.

With `n = 50` and `h = 50`, this is roughly:

```
51^50
```

which is astronomically large and completely impossible.

The key observation is that every restriction directly translates into upper bounds on individual positions.

Suppose a restriction says:

```
l = 2, r = 5, x = 7
```

Since the maximum height in that interval must not exceed `7`, every position from `2` through `5` must individually be at most `7`.

This means we can think of each position independently. Start by assuming every position can reach height `h`. Then process each restriction and reduce the allowed height of every covered position to:

```
current_limit = min(current_limit, x)
```

After all restrictions are processed, each position has an effective maximum height.

Now consider the objective function. The profit contributed by one position is:

```
a²
```

which strictly increases as `a` increases for nonnegative heights.

Since positions no longer interact, the best choice for each position is simply its largest allowed height.

The entire problem reduces to computing the final maximum height allowed at every position and summing their squares.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((h+1)^n) | O(n) | Too slow |
| Optimal | O(nm) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array `height` of length `n` and initialize every entry to `h`.
2. Process each restriction `(l, r, x)`.
3. For every position inside the interval `[l, r]`, replace its current limit with:

```
min(current_limit, x)
```

This accumulates all restrictions affecting that position.
4. After all restrictions have been processed, each entry of `height` stores the largest legal height for that position.
5. Compute:

```
answer = Σ height[i]²
```
6. Output the resulting sum.

### Why it works

A restriction on a range says that no house inside that range may exceed `x`. Applying `min(current_limit, x)` to every covered position records exactly this requirement.

After all restrictions are processed, the value stored for a position is the smallest upper bound imposed on it by any restriction covering that position, or `h` if none cover it.

The profit function is increasing with height because all heights are nonnegative and profit equals `a²`. Raising a house never decreases profit. Consequently, for every position, the optimal choice is its maximum legal height. Choosing anything smaller only reduces profit and cannot help satisfy any additional constraint because all constraints have already been encoded into the per-position limits.

Thus the algorithm constructs the unique profit-maximizing configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, h, m = map(int, input().split())

height = [h] * n

for _ in range(m):
    l, r, x = map(int, input().split())
    for i in range(l - 1, r):
        height[i] = min(height[i], x)

answer = sum(v * v for v in height)
print(answer)
```

The array `height` stores the current maximum allowed height for every position.

Initially every position can reach height `h`, so the array is filled with `h`.

Each restriction is processed immediately. Because the input uses one-based indexing while Python lists use zero-based indexing, the interval `[l, r]` becomes:

```
range(l - 1, r)
```

For every covered position we keep the minimum limit seen so far.

Once all restrictions have been applied, every position already contains its optimal height. The final loop computes the sum of squares.

No special handling is required for overlapping intervals because repeated `min` operations naturally combine all restrictions. Integer overflow is also irrelevant because the maximum possible answer is:

```
50 × 50² = 125000
```

which easily fits in Python integers.

## Worked Examples

### Sample 1

Input:

```
3 3 3
1 1 1
2 2 3
3 3 2
```

Initial state:

| Step | Height Array |
| --- | --- |
| Start | [3, 3, 3] |

After each restriction:

| Restriction | Height Array |
| --- | --- |
| (1,1,1) | [1, 3, 3] |
| (2,2,3) | [1, 3, 3] |
| (3,3,2) | [1, 3, 2] |

Profit computation:

| Position | Height | Contribution |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 9 |
| 3 | 2 | 4 |

Total:

```
1 + 9 + 4 = 14
```

This example shows that each restriction directly lowers the allowed height of the positions it covers.

### Sample 2

Input:

```
4 10 2
2 3 8
3 4 7
```

Initial state:

| Step | Height Array |
| --- | --- |
| Start | [10, 10, 10, 10] |

After each restriction:

| Restriction | Height Array |
| --- | --- |
| (2,3,8) | [10, 8, 8, 10] |
| (3,4,7) | [10, 8, 7, 7] |

Profit computation:

| Position | Height | Contribution |
| --- | --- | --- |
| 1 | 10 | 100 |
| 2 | 8 | 64 |
| 3 | 7 | 49 |
| 4 | 7 | 49 |

Total:

```
100 + 64 + 49 + 49 = 262
```

This trace demonstrates how overlapping restrictions combine through the minimum operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each restriction may update up to n positions |
| Space | O(n) | Stores the height limit for every position |

With `n ≤ 50` and `m ≤ 50`, the worst-case work is only about `2500` updates. This is far below the limits and runs essentially instantly.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, h, m = map(int, input().split())

    height = [h] * n

    for _ in range(m):
        l, r, x = map(int, input().split())
        for i in range(l - 1, r):
            height[i] = min(height[i], x)

    return str(sum(v * v for v in height))

# provided samples
assert run(
"""3 3 3
1 1 1
2 2 3
3 3 2
"""
) == "14", "sample 1"

assert run(
"""4 10 2
2 3 8
3 4 7
"""
) == "262", "sample 2"

# minimum size
assert run(
"""1 5 0
"""
) == "25", "single position"

# full-range restriction
assert run(
"""3 10 1
1 3 5
"""
) == "75", "all positions limited"

# overlapping restrictions
assert run(
"""3 10 2
1 2 7
2 3 4
"""
) == "81", "minimum of overlapping limits"

# unrestricted positions remain at h
assert run(
"""3 10 1
2 2 3
"""
) == "209", "positions outside intervals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 0` | `25` | Minimum-size instance |
| Full-range restriction | `75` | Range limit applies to every position |
| Overlapping restrictions | `81` | Minimum of all applicable limits is used |
| Single restricted position | `209` | Uncovered positions remain at height `h` |

## Edge Cases

### Overlapping restrictions

Input:

```
3 10 2
1 2 7
2 3 4
```

Processing gives:

```
[10,10,10]
→ [7,7,10]
→ [7,4,4]
```

Position `2` receives both restrictions and keeps the smaller value `4`. The final profit is:

```
49 + 16 + 16 = 81
```

The algorithm handles this automatically through repeated `min` operations.

### Restriction covering the entire street

Input:

```
3 10 1
1 3 5
```

Processing gives:

```
[10,10,10]
→ [5,5,5]
```

Profit:

```
25 + 25 + 25 = 75
```

Every position belongs to the restricted interval, so every position receives the same cap.

### Unrestricted positions

Input:

```
3 10 1
2 2 3
```

Processing gives:

```
[10,10,10]
→ [10,3,10]
```

Positions `1` and `3` never appear in any interval, so they retain their original limit `h = 10`.

Profit:

```
100 + 9 + 100 = 209
```

The initialization with `h` guarantees that positions untouched by restrictions automatically receive the largest possible legal height.
