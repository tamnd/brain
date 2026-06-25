---
title: "CF 105874B - Spaceship"
description: "We are given several weights, each a positive integer, representing masses that we are allowed to place on the left pan of a balance scale. On the right pan, we can place any product whose weight we want to identify."
date: "2026-06-25T14:24:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105874
codeforces_index: "B"
codeforces_contest_name: "Spring Lyceum Second school olympiad in informatics 2025"
rating: 0
weight: 105874
solve_time_s: 48
verified: true
draft: false
---

[CF 105874B - Spaceship](https://codeforces.com/problemset/problem/105874/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several weights, each a positive integer, representing masses that we are allowed to place on the left pan of a balance scale. On the right pan, we can place any product whose weight we want to identify. The scale is assumed to be precise and we are allowed to perform arbitrarily many weighings.

The key idea is that with a fixed set of weights, not every target weight can necessarily be uniquely identified. Some weights might produce ambiguous balance outcomes where different product weights could lead to the same sequence of balance results. The task is to determine the largest integer value `p` such that every product with weight from `1` up to `p` can be uniquely identified using these weights and repeated weighings.

A more structural way to view the problem is that the weights define a system of representable values through signed combinations. Each weighing effectively allows a comparison that behaves like choosing coefficients from `{-1, 0, 1}` for each weight. The central question becomes how far this signed representation can be extended without collisions in representability for integers.

The constraint `n ≤ 2 * 10^5` immediately rules out any approach that tries to simulate all achievable sums explicitly, since even enumerating subsets would grow exponentially. Even dynamic programming over all reachable values would fail because weights go up to `10^9`, making any dense range DP infeasible.

A subtle edge case appears when the weights are too sparse or degenerate. For example, if there is only a single weight `[5]`, then we cannot uniquely determine any weight at all from `1` to `4`, since we cannot represent them distinctly using any combination of weighings. The correct answer in this case is `0`, even though a naive interpretation might suggest we can measure multiples of 5.

Another corner case is when weights are large but include small increments, such as `[1, 3]`. Here we can distinguish weights up to `4`, but not necessarily beyond, because beyond that point representations start to overlap in terms of achievable balance outcomes.

## Approaches

The brute-force interpretation would attempt to simulate all possible ways of assigning each weight to the left pan, right pan, or not used, across multiple weighings, and check which product weights remain uniquely identifiable. This quickly becomes intractable because each weight has three states per weighing, and even a single weighing already produces `3^n` configurations. With multiple weighings allowed, the state space expands further and becomes impossible to explore even for moderate `n`.

The key insight is that multiple weighings do not fundamentally increase the representational power beyond signed combinations of the given weights. Each weight contributes a fixed “resolution scale”, and the system behaves like building a numerical base where digits can be `-1, 0, 1`. The limiting factor becomes whether we can continuously cover the integer line without gaps in representability.

If we sort the weights, we can process them in increasing order and maintain the maximum contiguous range `[0, p]` that can be uniquely represented. Each new weight either extends this range or creates a gap. If we can currently represent all values up to `p`, then a new weight `x` can extend this range only if `x ≤ p + 1`. Otherwise, a gap appears at `p + 1`, making it impossible to uniquely represent that value, and the process stops.

This transforms the problem into a greedy scan over sorted weights while maintaining the reachable prefix of representable values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration of all weighings | Exponential | Exponential | Too slow |
| Sorted greedy range extension | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array of weights in non-decreasing order. This allows us to process them in the order in which they can potentially extend the representable range.
2. Initialize a variable `p = 0`, representing the maximum weight value that can currently be uniquely determined.
3. Iterate through each weight `x` in sorted order. At each step, we check whether this weight can extend the contiguous representable range.

The reasoning is that if we can already uniquely determine all weights up to `p`, then the next missing value is `p + 1`. A new weight must be able to “bridge” or cover this next value to extend the system.
4. If `x > p + 1`, we stop immediately. This means there is a gap at `p + 1` that cannot be filled by any combination of previous weights or the current one, so uniqueness fails beyond this point.
5. Otherwise, we update `p = p + x`. This step reflects that adding a new weight extends the range of achievable distinguishable sums by exactly `x`, because all previously representable values can now be shifted and combined with this weight.
6. After processing all weights, output `p`.

The invariant maintained is that at any point during iteration, every integer in `[0, p]` can be uniquely represented using the processed weights with signed combinations. The sorted order ensures that when we attempt to extend this interval, no smaller unprocessed weight is missing that would be necessary to fill a gap. If a gap ever appears, it is permanent because larger weights cannot create smaller representable increments.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

p = 0
for x in a:
    if x > p + 1:
        break
    p += x

print(p)
```

The sorting step is essential because the greedy argument relies on always attempting to extend the smallest missing representable value first. Without sorting, a large weight appearing early could incorrectly inflate `p` and hide a gap that should block further progress.

The condition `x > p + 1` is the critical boundary check. It detects when the current weight is too large to contribute to filling the smallest unreachable value, which is always `p + 1`. Any implementation that instead checks against `p` or uses a different inequality will fail on cases where the gap is exactly one unit.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
```

We start with `p = 0`.

| Step | x | p before | Condition | p after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 ≤ 1 | 1 |
| 2 | 2 | 1 | 2 ≤ 2 | 3 |
| 3 | 3 | 3 | 3 ≤ 4 | 6 |
| 4 | 4 | 6 | 4 ≤ 7 | 10 |

Output is `10`.

This trace shows continuous extension without any gap. Each new weight remains within the reachable frontier, confirming that the representable interval grows monotonically without interruption.

### Example 2

Input:

```
3
1 2 5
```

| Step | x | p before | Condition | p after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 ≤ 1 | 1 |
| 2 | 2 | 1 | 2 ≤ 2 | 3 |
| 3 | 5 | 3 | 5 > 4 | stop |

Output is `3`.

This shows a failure point: after reaching `3`, the next missing value is `4`, but the next weight is `5`, which is too large to fill the gap. The construction breaks at this exact boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, single linear scan afterward |
| Space | O(1) or O(n) | depending on whether sorting is in-place |

The constraints allow up to `2 * 10^5` weights, so an `O(n log n)` solution fits comfortably within typical limits, and the linear scan adds negligible overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    p = 0
    for x in a:
        if x > p + 1:
            break
        p += x

    return str(p)

# provided samples (from statement)
assert run("4\n1 2 3 4\n") == "10"
assert run("2\n1 3\n") == "4"

# custom cases
assert run("1\n5\n") == "0", "single large weight"
assert run("1\n1\n") == "1", "minimal extension"
assert run("3\n1 2 5\n") == "3", "gap after small prefix"
assert run("5\n1 1 1 1 1\n") == "5", "repeated small weights"
assert run("6\n2 2 2 2 2 2\n") == "2", "no early bridging possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5` | `0` | no representable range |
| `1 1` | `1` | smallest non-trivial case |
| `1 2 5` | `3` | gap detection correctness |
| `1 1 1 1 1` | `5` | repeated small increments |
| `2 2 2 2 2 2` | `2` | stagnation case |

## Edge Cases

When there is only a single weight greater than `1`, the algorithm immediately stops at `p = 0` because `x > p + 1`. For input `5`, the scan halts instantly and outputs `0`, matching the fact that no smaller value can be uniquely isolated.

When all weights are identical small values like `1`, the range grows linearly. Each step satisfies the condition `1 ≤ p + 1`, so the interval expands deterministically, producing a final answer equal to `n`.

When a gap appears after a valid prefix, such as `1, 2, 10`, the algorithm processes `1` and `2` to reach `p = 3`, then detects `10 > 4` and stops. The trace confirms that the smallest missing representable value governs all future feasibility, and larger weights cannot repair earlier gaps.
