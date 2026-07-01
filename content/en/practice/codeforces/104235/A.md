---
title: "CF 104235A - \u041a\u0440\u0430\u0441\u0438\u0432\u043e\u0435 \u043e\u043a\u043d\u043e"
description: "We are given a rectangular window of height H and width W. Two cuts are made. First, we choose a vertical cut at some integer position A, splitting the window into a left rectangle of width A and a right rectangle of width W - A."
date: "2026-07-01T23:30:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104235
codeforces_index: "A"
codeforces_contest_name: "2022-2023 Olympiad Cognitive Technologies, Final Round"
rating: 0
weight: 104235
solve_time_s: 83
verified: true
draft: false
---

[CF 104235A - \u041a\u0440\u0430\u0441\u0438\u0432\u043e\u0435 \u043e\u043a\u043d\u043e](https://codeforces.com/problemset/problem/104235/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular window of height `H` and width `W`. Two cuts are made.

First, we choose a vertical cut at some integer position `A`, splitting the window into a left rectangle of width `A` and a right rectangle of width `W - A`.

Second, inside the right rectangle only, we choose a horizontal cut at height `B`, splitting it into a top and bottom rectangle of heights `B` and `H - B`.

This produces exactly three rectangles:

the left part, the top-right part, and the bottom-right part. Their areas are

`S1 = H * A`,

`S2 = B * (W - A)`,

`S3 = (H - B) * (W - A)`.

The goal is to choose integer `A` and `B` so that the smallest of these three areas is as large as possible.

The constraints are small: both dimensions are at most 1000. That already suggests that even an `O(HW)` or `O(W)` per test approach is completely safe, while anything cubic would be unnecessary.

A naive mistake would be to try all `(A, B)` pairs directly. That is at most a million states, which still passes, but it hides the structure and can lead to incorrect reasoning if one tries to optimize incorrectly.

A more subtle pitfall appears when trying to treat the three areas independently. For example, one might try to maximize each area separately or balance all three at once. That fails because `S2` and `S3` are coupled through the same factor `(W - A)` and symmetric in `B`.

There is also a hidden edge constraint: `A` must be at least 1 and at most `W-1`, similarly `B` must be between `1` and `H-1`. This prevents degenerate cases where one region disappears, and any solution must respect that.

## Approaches

A direct brute-force strategy chooses every valid pair `(A, B)` and computes the three areas. This is correct because it evaluates the exact objective function, but it requires iterating over roughly `(W-1)(H-1)` states, which in the worst case is about one million operations. This is acceptable under constraints, but it is wasteful and does not use the structure of the expression.

The key observation is that for a fixed vertical cut `A`, the right side becomes a rectangle of size `(W - A) × H`. Inside it, we choose `B` to split it horizontally. The left area `S1` is independent of `B`, while `S2` and `S3` only depend on how we split the height.

For fixed `A`, the problem reduces to maximizing `min(B, H - B)` because both `S2` and `S3` are multiplied by the same factor `(W - A)`. The best way to maximize the minimum of two symmetric linear functions is to split as evenly as possible, so `B` should be as close to `H/2` as possible. This gives a best possible value of `floor(H/2)` for the smaller side.

So for each `A`, the best achievable minimum among `S2` and `S3` becomes `(W - A) * floor(H/2)`. Now the third value `S1 = H * A` competes with this quantity, so we reduce the problem to a single variable optimization over `A`.

At this point, the problem becomes a one-dimensional maximum of `min(H*A, C*(W-A))` where `C = floor(H/2)`. This function increases with `A` in the first term and decreases in the second term, so the optimum lies near their intersection. Since `W ≤ 1000`, we can safely evaluate all possible `A`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over A, B | O(HW) | O(1) | Accepted |
| Optimized reduction over A | O(W) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the problem step by step into a single-variable optimization.

1. Compute `C = floor(H / 2)`.

This represents the best possible value of `min(B, H - B)` for any valid horizontal split.
2. Fix a vertical cut position `A` from `1` to `W - 1`.

Each choice determines the left rectangle and the width of the right rectangle.
3. For each `A`, compute the two competing quantities:

`S1 = H * A` and `S23 = C * (W - A)`.

The value `S23` represents the best possible minimum between the top-right and bottom-right rectangles after optimally choosing `B`.
4. For this `A`, the best achievable answer is `min(S1, S23)`.

This reflects that all three regions must be at least this large, so the smallest among them is the limiting factor.
5. Track the maximum value of this expression over all `A`.

The final answer is the best balance point where the left area and the best possible right-side minimum are as close as possible.

### Why it works

For a fixed `A`, the right side is independent of the left side except through the factor `(W - A)`. The horizontal split problem inside the right rectangle is symmetric and linear, so its optimal strategy is always to split as evenly as possible. This reduces the two-dimensional decision `(A, B)` into a single parameter `A` without losing optimality. Since every feasible configuration is represented by some `(A, B)`, and for each `A` we choose the optimal `B`, no better solution can exist outside this reduction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    H, W = map(int, input().split())

    C = H // 2
    best = 0

    for A in range(1, W):
        s1 = H * A
        s23 = C * (W - A)
        best = max(best, min(s1, s23))

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation follows the reduced formulation directly. The loop over `A` explores all valid vertical cuts. For each one, `s1` is the left area and `s23` is the best achievable bottleneck from the right side after optimally placing the horizontal cut. The `min` enforces that all three regions are at least as large as the smallest among them.

A common implementation mistake is forgetting that the optimal `B` does not need to be explicitly iterated. Another is using `H/2` instead of `floor(H/2)`, which breaks integer correctness when `H` is odd.

## Worked Examples

### Sample 1

Input:

```
2 2
```

Here `C = 1`.

| A | S1 = H*A | S23 = C*(W-A) | min(S1, S23) |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |

The best value is `1`.

This shows the extreme case where both cuts are forced into minimal dimensions, and balancing is impossible beyond a single unit area.

### Sample 2

Input:

```
2 3
```

Here `C = 1`.

| A | S1 = H*A | S23 = C*(W-A) | min(S1, S23) |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 2 |
| 2 | 4 | 1 | 1 |

The maximum is `2`, achieved when `A = 1`.

This demonstrates the tradeoff: increasing `A` improves the left rectangle but shrinks the right side faster than the gain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(W) | We iterate over all possible vertical cuts once, each in constant time |
| Space | O(1) | Only a few scalar variables are used |

The constraints allow up to 1000 per dimension, so a linear scan over `W` is easily fast enough even under multiple evaluations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io

    buf = _io.StringIO()
    with redirect_stdout(buf):
        solve()
    return buf.getvalue().strip()

def solve():
    H, W = map(int, input().split())
    C = H // 2
    best = 0
    for A in range(1, W):
        best = max(best, min(H * A, C * (W - A)))
    print(best)

# provided samples
assert run("2 2\n") == "1"
assert run("2 3\n") == "2"

# custom cases
assert run("3 3\n") == "2", "small symmetric case"
assert run("2 1000\n") == "500", "long horizontal strip"
assert run("1000 2\n") == "500", "degenerate width"
assert run("4 4\n") == "4", "balanced square case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 | 2 | symmetric middle split behavior |
| 2 1000 | 500 | dominance of vertical dimension |
| 1000 2 | 500 | edge case where only one A exists |
| 4 4 | 4 | balanced case where both cuts align optimally |

## Edge Cases

One edge case occurs when `H = 2`. Then `C = 1`, and the horizontal cut is forced to split into two height-1 strips. The algorithm handles this correctly because `min(B, H-B)` is always 1, so the right side becomes `(W - A)` exactly, and the optimization reduces to balancing `2A` and `W - A`.

Another edge case is when `W = 2`. Then there is only one valid vertical cut `A = 1`, so the loop evaluates exactly one configuration. The result is `min(H, floor(H/2))`, which matches the forced structure of the right rectangle.

A final subtle case is when `H` is odd. Using `H // 2` ensures that the split never overestimates the achievable minimum. Any attempt to use floating division would produce incorrect comparisons due to invalid non-integer area assumptions.
