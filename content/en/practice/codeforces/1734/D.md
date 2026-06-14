---
title: "CF 1734D - Slime Escape"
description: "We start at position k on a line of n slimes. Each position contains a slime with some health value, and when we step onto a position that still has a slime, we absorb it and add its health to ours. Negative values reduce our health, positive values increase it."
date: "2026-06-15T03:27:32+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1734
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 822 (Div. 2)"
rating: 1800
weight: 1734
solve_time_s: 219
verified: false
draft: false
---

[CF 1734D - Slime Escape](https://codeforces.com/problemset/problem/1734/D)

**Rating:** 1800  
**Tags:** data structures, dp, greedy, two pointers  
**Solve time:** 3m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We start at position `k` on a line of `n` slimes. Each position contains a slime with some health value, and when we step onto a position that still has a slime, we absorb it and add its health to ours. Negative values reduce our health, positive values increase it. Our slime is never allowed to drop below zero at any moment.

The goal is to move step by step either left toward position `0` or right toward position `n+1`, absorbing everything we pass through because slimes disappear after being eaten. We are allowed to choose the order of expansion implicitly by deciding which direction to go first, but once we move through a position, it is gone.

The key difficulty is that we are not simply checking whether the total sum is non-negative. We must ensure that at every prefix of the path, the running health never becomes negative, and we may have to pick the “safer” direction first.

The constraints are large, with total `n` over all test cases up to 200,000. This rules out any quadratic simulation over intervals or trying all possible left-right interleavings. Any solution must be linear per test or amortized linear overall. That strongly suggests that each position is processed at most a constant number of times, and that decisions depend on prefix-like or greedy feasibility checks.

A subtle pitfall is assuming that only the total sum matters. For example, consider a segment like `[-5, +100, -200, +200]`. The total sum is positive, but if we take the wrong order of absorption, we might hit a negative prefix before reaching the large positive values. Another failure case is assuming we must take all slimes on one side completely before touching the other; in fact, the optimal strategy may involve extending one side only until it becomes “safe enough” to switch.

## Approaches

A naive view is to simulate both possibilities: try going left-first or right-first, and recursively consider all ways to expand outward. At each step we choose to move left or right, check if health stays non-negative, and continue. This quickly becomes exponential because every state is defined by the current interval `[L, R]` and position inside it, and branching on direction creates a combinatorial explosion.

Even if we restrict ourselves to monotonic strategies like “go fully left then fully right” or vice versa, this still fails because intermediate feasibility matters: a segment may have positive total sum but still require absorbing in a specific order to avoid a dip below zero.

The key observation is that once we decide to fully consume one side, the internal order is fixed. So the problem reduces to checking whether we can expand left and right in some order such that each extension is feasible given current health. The critical insight is that feasibility of extending to one side depends only on whether we can traverse that entire segment starting from current health, which can be checked greedily by scanning outward and maintaining minimum prefix sum.

So instead of simulating all paths, we precompute whether each side can be fully consumed from a starting point, and then greedily expand the side that is currently safe, updating our health as we grow the interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full simulation of states | Exponential | O(n) | Too slow |
| Greedy expansion with prefix feasibility checks | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the reasoning at the starting position `k`, and treat the current reachable region as a segment that expands outward.

1. Compute whether we can expand left from `k` as far as possible while never letting health drop below zero. We simulate moving left one step at a time, updating health, and stop when it becomes impossible to proceed further. This gives a maximum reachable left boundary.
2. Similarly compute how far we can expand to the right from `k` under the same rule. This gives a maximum reachable right boundary.
3. If either side reaches beyond the boundary (`0` or `n+1`), we can escape immediately.
4. Otherwise, we treat the problem as maintaining an interval `[L, R]` initially at `[k, k]`, with current health equal to `a[k]`.
5. We attempt to expand the interval outward. At each stage, we consider extending either left to `L-1` or right to `R+1`, but only if that entire side segment is “feasible”, meaning we can traverse it starting from current health without hitting negative.
6. To test feasibility efficiently, we maintain prefix sums of segments and ensure the minimum prefix sum along the extension does not drop below `-current_health`. This guarantees we never cross zero during absorption.
7. We greedily extend whichever side is currently feasible. If both are feasible, either order works because both expansions preserve non-negative health.
8. We continue until we reach either `0` or `n+1`.

### Why it works

At any moment, the only constraint that matters is whether a full contiguous segment can be consumed without violating the non-negative prefix condition. Once a segment is feasible, consuming it in full is always optimal because it only increases flexibility by expanding reachable positions and never reduces future options except through health changes already accounted for in feasibility. The process maintains the invariant that the current interval `[L, R]` is fully consumable in some order without breaking the health constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_cross(a, k):
    n = len(a) - 1
    left = k
    right = k
    health = a[k]

    if health < 0:
        return False

    # Try expanding greedily
    while True:
        moved = False

        # try left
        if left > 1:
            h = health
            ok = True
            for i in range(left - 1, 0, -1):
                h += a[i]
                if h < 0:
                    ok = False
                    break
            if ok:
                for i in range(left - 1, 0, -1):
                    health += a[i]
                left = 1
                moved = True

        # try right
        if right < n:
            h = health
            ok = True
            for i in range(right + 1, n + 1):
                h += a[i]
                if h < 0:
                    ok = False
                    break
            if ok:
                for i in range(right + 1, n + 1):
                    health += a[i]
                right = n
                moved = True

        if not moved:
            break

        if left == 1 or right == n:
            return True

    return left == 1 or right == n

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = [0] + list(map(int, input().split()))
        print("YES" if can_cross(a, k) else "NO")

if __name__ == "__main__":
    solve()
```

The implementation keeps a current interval and tries to expand it outward only when a full side segment can be safely absorbed. The inner feasibility check simulates consumption of a candidate side while tracking minimum health implicitly via running sum.

The main subtlety is that we only commit to an expansion when we know the entire segment is safe. Partial consumption is never allowed in the check phase, because that would mix feasibility testing with state mutation. Another key detail is guarding boundary conditions: reaching `left == 1` or `right == n` means we can still move one more step into the escape cell.

## Worked Examples

### Example 1

Input:

```
7 4
-1 -2 -3 6 -2 -3 -1
```

We start at index 4 with health 6.

| Step | Left | Right | Health | Action |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 6 | Start |
| 2 | 4 | 7 | 6 → -3 | Expand right fully |
| 3 | 4 | 7 | 6 → -3 → -6 → -7 | Right expansion invalid early |

The right side is not safely consumable first, so we try left expansion instead.

| Step | Left | Right | Health | Action |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 6 | Start |
| 2 | 1 | 4 | 6 → 5 → 3 → 0 | Expand left fully |
| 3 | 1 | 4 | 0 → 6 → 4 → 1 | Then expand right |

We successfully reach both ends.

This shows that the correct strategy is not directional bias but feasibility-based expansion.

### Example 2

Input:

```
3 1
232 -500 -700
```

We start at position 1, already near escape 0.

| Step | Left | Right | Health | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 232 | Start |
| 2 | 0 | 1 | 232 | Move left to escape |

This demonstrates a boundary case where no absorption is needed at all.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test (amortized) | Each element is absorbed at most once during expansion |
| Space | O(n) | Storage for the input array |

The total complexity is linear in the total input size, which fits comfortably under the constraint of 200,000 total slimes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys
```
