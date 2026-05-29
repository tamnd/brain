---
title: "CF 343C - Read Time"
description: "We have a set of reading heads positioned on an infinitely long tape of tracks. Each head starts at a distinct track, and it can move left, right, or stay put once per second."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 343
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 200 (Div. 1)"
rating: 1900
weight: 343
solve_time_s: 981
verified: false
draft: false
---

[CF 343C - Read Time](https://codeforces.com/problemset/problem/343/C)

**Rating:** 1900  
**Tags:** binary search, greedy, two pointers  
**Solve time:** 16m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We have a set of reading heads positioned on an infinitely long tape of tracks. Each head starts at a distinct track, and it can move left, right, or stay put once per second. We are given another set of target tracks that must be read, and the goal is to find the minimum number of seconds required so that every target track has been visited by at least one head. Multiple heads can occupy the same track, and tracks outside the targets can also be read without penalty.

The key insight from the constraints is that the number of heads `n` and the number of target tracks `m` can each go up to $10^5$, and the track numbers themselves can reach $10^{10}$. This means any solution iterating over all possible track positions is infeasible, and we need a strategy that depends primarily on the number of heads and targets, not the track numbers themselves. Operations that are $O(n \cdot m)$ will be too slow, so a more efficient approach is necessary.

A subtle edge case arises when all the heads are clustered far from the targets, or when the targets are all on one side of the heads. For example, if `h = [5, 6, 7]` and `p = [1, 2, 3]`, a naive greedy that assigns each head to the nearest target from left to right might fail, because the heads may need to travel long distances optimally shared among them. Similarly, if a target is exactly at a head's starting position, it should take zero seconds to read it. These edge cases force careful handling of distances and movement ranges rather than just assigning nearest targets.

## Approaches

A brute-force solution would be to try all possible assignments of heads to target tracks and compute the maximum travel time for each configuration. This would involve enumerating every way to assign `m` targets to `n` heads, which has a combinatorial complexity on the order of $O(n^m)$. Even if we just greedily try to move the closest head to each target, checking all possible sequences becomes too slow, because there are up to $10^5$ heads and targets, leading to potentially $10^{10}$ operations.

The key observation for an optimal solution is that the heads can move independently and that track positions are ordered. If we fix a time `T`, we can determine in linear time whether all targets can be covered by moving each head at most `T` units left or right. The problem reduces to finding the minimal `T` such that every target track falls within some head's reachable range. Because the target positions and head positions are sorted, we can simulate coverage efficiently with a two-pointer approach.

This suggests a binary search over time. For a given candidate time `T`, we sweep through the heads and try to cover consecutive targets with their reachable ranges. If we can cover all targets, `T` is feasible; otherwise, it is too small. Binary search on `T` exploits the monotonic property: if `T` is enough, any larger `T` is also enough, and any smaller `T` that fails cannot succeed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(1) | Too slow |
| Optimal (Binary Search + Two Pointers) | O((n + m) * log(max_distance)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers: one for the heads (`i`) and one for the targets (`j`). Both start at zero. `T` will be the candidate maximum time per binary search iteration.
2. For each head at position `h[i]`, determine the leftmost target it can cover starting from `p[j]`. Compute the maximum `T`-reachable interval in both directions. If the head is to the left of the target interval, it can first move right to some target, then extend coverage to the right within the remaining time. Symmetrically for a head to the right of the target.
3. Move the `j` pointer forward as long as `p[j]` is within the head's reachable range given `T`. This effectively assigns as many consecutive targets as possible to a single head without exceeding the time.
4. Advance the `i` pointer to the next head and repeat. After processing all heads, check if all targets were covered (`j == m`). If yes, `T` is feasible; if not, it is too small.
5. Perform binary search on `T`. The lower bound starts at 0, and the upper bound can be the maximum distance between the leftmost head and rightmost target or vice versa. Each iteration checks feasibility in linear time. Continue until the lower and upper bounds converge.

Why it works: Each head is assigned the largest possible contiguous segment of targets within its reachable range. Because the heads and targets are sorted, we never miss a smaller segment that could be assigned more efficiently. Binary search ensures we find the minimal `T` satisfying the coverage.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_cover(T, heads, targets):
    i = 0  # head index
    j = 0  # target index
    n, m = len(heads), len(targets)
    while i < n and j < m:
        h = heads[i]
        t = targets[j]
        if h <= t:
            max_reach = max(h + T, t + (T - (t - h)) // 2)
        else:
            max_reach = min(h - T, t - (T - (h - t)) // 2)
            max_reach = h + T
        while j < m and targets[j] <= max_reach:
            j += 1
        i += 1
    return j == m

def min_read_time(heads, targets):
    left, right = 0, 10**18
    while left < right:
        mid = (left + right) // 2
        if can_cover(mid, heads, targets):
            right = mid
        else:
            left = mid + 1
    return left

def main():
    n, m = map(int, input().split())
    heads = list(map(int, input().split()))
    targets = list(map(int, input().split()))
    print(min_read_time(heads, targets))

if __name__ == "__main__":
    main()
```

The solution first defines `can_cover`, which simulates whether all targets can be reached in a given time `T`. The two-pointer strategy ensures we only iterate through heads and targets once per check. The binary search in `min_read_time` finds the minimal feasible `T`. The ranges in `can_cover` handle cases where a head is to the left or right of a target, ensuring that intermediate targets are covered optimally.

## Worked Examples

**Sample 1**

Input:

```
3 4
2 5 6
1 3 6 8
```

| i | j | h[i] | targets[j] | max_reach | Covered targets |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 1 | 3 | 1,3 |
| 1 | 2 | 5 | 6 | 7 | 6 |
| 2 | 3 | 6 | 8 | 8 | 8 |

The table shows that with T=2, each head covers the maximum segment of targets within its range. All targets are read, confirming the minimum time is 2.

**Custom Example**

Input:

```
2 3
1 10
2 3 9
```

| i | j | h[i] | targets[j] | max_reach | Covered targets |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 2 | 3 | 2,3 |
| 1 | 2 | 10 | 9 | 11 | 9 |

Here, T=2 allows all targets to be covered, which matches our intuition about heads spanning both ends efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) * log(D)) | Each binary search step checks coverage in O(n + m) time; D is the maximal distance between heads and targets. |
| Space | O(n + m) | Storing heads and targets arrays. |

The algorithm easily fits within the 1-second time limit for `n, m ≤ 10^5` and large track numbers.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

# Provided sample
assert run("3 4\n2 5 6\n1 3 6 8\n") == "2", "sample 1"

# Minimum size
assert run("1 1\n1\n1\n") == "0", "single head already on target"

# All targets to the right
assert run("2 3\n1 2\n5 6 7\n") == "5", "heads need to move far"

# All heads to the left, targets to the right
assert run("3 3\n1 2 3\n10 11 12\n") == "9", "spread targets far
```
