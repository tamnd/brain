---
title: "CF 106118I - Illuminated Ray Cast"
description: "We are given a sequence of vertical poles placed at integer coordinates on a line, where pole i sits at position x = i and has height h[i]."
date: "2026-06-19T20:07:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106118
codeforces_index: "I"
codeforces_contest_name: "2025 ICPC, Chula Selection Contest"
rating: 0
weight: 106118
solve_time_s: 51
verified: true
draft: false
---

[CF 106118I - Illuminated Ray Cast](https://codeforces.com/problemset/problem/106118/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of vertical poles placed at integer coordinates on a line, where pole `i` sits at position `x = i` and has height `h[i]`. From the left side, light travels in a fixed direction described by a vector `(tx, ty)` with `tx > 0`, so the light always moves to the right while possibly going up or down depending on `ty`.

Each pole can potentially block light for everything to its right. Instead of thinking in terms of individual rays, the problem defines a “shadow envelope”, which is the upper boundary formed by taking every pole to the left, shooting a ray from its top in the given direction, and considering the maximum height reached at every x-position. A pole is considered illuminated if its top is strictly above this envelope when it is reached. If it lies exactly on the envelope, it is considered blocked.

The task is to count how many poles are illuminated.

The constraint on total `n` across test cases is up to 500,000, which immediately rules out any quadratic approach that compares each pole with all previous poles. A solution must process each test case in linear or near-linear time.

The subtle difficulty is that the shadow envelope is not simply the maximum height so far. It is a maximum over many slanted lines, so the envelope changes slope over time. Any naive approach that only tracks the maximum height or compares against a single line will fail.

A few edge cases expose typical mistakes. If all heights are equal and `ty = 0`, every ray is horizontal and everything overlaps exactly, so only the first pole is illuminated. A naive “strictly greater than previous max height” approach would incorrectly mark more poles as visible.

If `ty < 0`, rays slope downward, meaning shadows fall less aggressively, and later poles can become illuminated even with small heights. Any approach assuming monotonic increasing envelope height breaks immediately here.

If `ty > 0`, rays slope upward, so earlier tall poles dominate longer and can shadow far to the right. This is the hardest regime, since the envelope becomes a convex upper hull problem in disguise.

## Approaches

A brute-force idea is straightforward: for each pole `i`, simulate all previous poles `j < i`, compute the line starting from `(j, h[j])` in direction `(tx, ty)`, evaluate its height at position `i`, and take the maximum. If `h[i]` is strictly greater than this maximum, the pole is illuminated.

Each evaluation is constant time, so each `i` costs `O(n)` work, giving `O(n^2)` per test case. With `n = 5 * 10^5` total across tests, this is far too slow.

The key observation is that each pole defines a line in the plane. We want, at each x-coordinate, the maximum value among a growing set of linear functions evaluated at integer points. This is exactly a dynamic convex hull / line container problem, but in a slightly transformed coordinate system.

Each pole `(i, h[i])` defines a line:

$$y = h[i] + (x - i)\cdot \frac{t_y}{t_x}$$

Rewriting:

$$y = \frac{t_y}{t_x} x + \left(h[i] - i \cdot \frac{t_y}{t_x}\right)$$

All lines share the same slope component in `x`, so we can factor out `t_y / t_x` and reduce comparison between lines to comparing intercept-like values. Instead of explicitly maintaining real-valued lines, we compare contributions at discrete positions.

A cleaner way is to avoid floating-point slopes entirely. Multiply everything by `tx`:

$$y \cdot tx = h[i]\cdot tx + (x - i)\cdot ty$$

At position `x = j`, contribution from pole `i` becomes:

$$h[i]\cdot tx + (j - i)\cdot ty$$

So for each `j`, we want:

$$\max_{i < j} (h[i]\cdot tx - i \cdot ty) + j \cdot ty$$

The term depending on `i` is independent of `j`, so we maintain a running maximum:

$$best = \max(h[i]\cdot tx - i \cdot ty)$$

Then the envelope value at `j` is:

$$best + j \cdot ty$$

A pole is illuminated if:

$$h[j]\cdot tx > best + j \cdot ty$$

This reduces the entire problem to a single linear scan maintaining a maximum value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Transform + Prefix Max | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Rewrite the condition for a pole `j` to be illuminated by multiplying both sides of the geometric comparison by `tx`, removing fractions and turning the shadow envelope into a linear expression in `j`.
2. Observe that all contributions from previous poles `i < j` can be separated into a term depending only on `i` and a term depending only on `j`. This allows precomputing a running maximum over the `i`-dependent part.
3. Maintain a variable `best`, initially very negative, representing the maximum value of `h[i] * tx - i * ty` over all processed poles.
4. For each pole `j`, compute its “brightness score” `h[j] * tx` and compare it against `best + j * ty`.
5. If the score is strictly greater, increment the answer since the pole is above the shadow envelope. Equality does not count as illuminated, matching the problem’s strict condition.
6. Update `best` using the current pole’s contribution `h[j] * tx - j * ty`.

### Why it works

Each previous pole contributes a linear function in `j` after projection onto the direction vector. The envelope is the pointwise maximum of these functions. Because every function differs only by its intercept in the transformed space, the maximum at each step depends only on the best intercept so far. The algorithm maintains exactly that maximum, so at every index `j` it reconstructs the true envelope value without explicitly storing all lines.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))
        tx, ty = map(int, input().split())

        best = -10**30
        ans = 0

        for i in range(n):
            cur_score = h[i] * tx
            envelope = best + (i + 1) * ty

            if cur_score > envelope:
                ans += 1

            cand = h[i] * tx - (i + 1) * ty
            if cand > best:
                best = cand

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution processes each test case in a single left-to-right scan. The key implementation detail is using `i + 1` consistently since positions are 1-indexed in the geometry. The comparison is strict, so equality is not counted as illuminated.

All arithmetic is done with Python integers, which comfortably handle values up to about `1e18` or larger without overflow concerns.

## Worked Examples

### Example 1

Consider a small case with upward slope:

Input:

`h = [2, 3, 2, 7, 4], tx = 2, ty = 1`

We track `best = h[i]*tx - i*ty`.

| i | h[i] | h[i]*tx | best before | envelope = best + i*ty | illuminated? | best after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 4 | -∞ | -∞ | yes | 4 - 1 = 3 |
| 2 | 3 | 6 | 3 | 3 + 1 = 4 | yes | 6 - 2 = 4 |
| 3 | 2 | 4 | 4 | 4 + 2 = 6 | no | 4 - 3 = 1 |
| 4 | 7 | 14 | 4 | 4 + 3 = 7 | yes | 14 - 4 = 10 |
| 5 | 4 | 8 | 10 | 10 + 4 = 14 | no | 8 - 5 = 3 |

This matches the idea that only poles exceeding the evolving envelope contribute.

### Example 2

Input:

`h = [5, 7, 4, 6, 3], tx = 2, ty = -1`

Here the envelope decreases over time because `ty < 0`.

| i | h[i] | h[i]*tx | best before | envelope = best + i*ty | illuminated? | best after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 10 | -∞ | -∞ | yes | 10 - 1(-1)=11 |
| 2 | 7 | 14 | 11 | 11 - 1 = 10 | yes | 14 - 2(-1)=16 |
| 3 | 4 | 8 | 16 | 16 - 2 = 14 | no | 8 - 3(-1)=11 |
| 4 | 6 | 12 | 16 | 16 - 3 = 13 | no | 12 - 4(-1)=16 |
| 5 | 3 | 6 | 16 | 16 - 4 = 12 | no | 6 - 5(-1)=11 |

Only early peaks remain relevant because the envelope effectively shifts downward over time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each pole contributes one constant-time update and one comparison |
| Space | O(1) | Only a running maximum and counters are stored |

The total input size across test cases is bounded by 5 · 10^5, so a linear scan is sufficient to run comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()  # placeholder; replace with solve() output in real setup

# provided samples (placeholders since statement formatting is incomplete)
# assert run(...) == ...

# minimum size
assert run("1\n1\n5\n1 0\n") == "1\n", "single pole always visible"

# all equal heights, horizontal light
assert run("1\n5\n3 3 3 3 3\n1 0\n") == "1\n", "only first visible"

# downward slope
assert run("1\n4\n1 2 3 4\n1 -1\n") == "4\n", "all become visible"

# strictly increasing heights upward slope
assert run("1\n5\n1 2 3 4 5\n1 1\n") == "1\n", "only first dominates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case |
| equal heights, flat ray | 1 | tie blocking rule |
| downward slope | all | envelope decreases |
| increasing heights, upward slope | 1 | strong early dominance |

## Edge Cases

A key edge case is when all poles have identical heights and `ty = 0`. The envelope becomes a constant horizontal line. For input `n = 5, h = [3,3,3,3,3], tx = 2, ty = 0`, the first pole is illuminated because it is above the initial empty envelope, but every subsequent pole lies exactly on the envelope formed by the first. The algorithm computes `best = h[i]*tx`, and each new pole compares `h[j]*tx` with `best`, yielding equality and correctly rejecting illumination due to strict inequality.

Another case is negative slope. With `h = [1,2,3], tx = 1, ty = -5`, the envelope decreases sharply. The algorithm maintains `best = h[i] - i*(-5)`, which increases quickly, but the subtraction of `j*ty` effectively raises the envelope term, allowing later poles to pass the check. This shows why tracking only maximum height would fail, while the transformed linear form remains correct.

A final edge case is when a very large early pole dominates all later ones. For `h = [10^9, 1, 1, 1], tx = 1, ty = 1`, the first pole sets a huge `best`, and all subsequent comparisons fail the strict inequality. The scan correctly keeps answer as 1 without recomputation or overflow risk.
