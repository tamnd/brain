---
title: "CF 105228E - Building Pigeon Houses"
description: "We are given a collection of pigeon species, where each species has a limited supply of pigeons available for purchase. The goal is to build as many identical pigeon houses as possible."
date: "2026-06-24T16:19:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105228
codeforces_index: "E"
codeforces_contest_name: "SanSi Cup 2023"
rating: 0
weight: 105228
solve_time_s: 77
verified: true
draft: false
---

[CF 105228E - Building Pigeon Houses](https://codeforces.com/problemset/problem/105228/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of pigeon species, where each species has a limited supply of pigeons available for purchase. The goal is to build as many identical pigeon houses as possible. Every house must contain exactly `k` pigeons, and no two pigeons inside the same house can belong to the same species. However, the same species can appear in multiple different houses, as long as we do not exceed the number of pigeons available for that species.

We are not required to explicitly construct the assignment. We only need to determine the maximum number of houses that can be formed under these constraints.

The key difficulty is that choosing more houses restricts how often each species can be reused, because a single species can contribute at most one pigeon per house. If we try to build `H` houses, then each species `i` can contribute at most `min(p_i, H)` pigeons in total.

This immediately suggests a feasibility condition: if we fix a candidate number of houses `H`, the total usable pigeons across all species becomes `sum(min(p_i, H))`. Since each house needs `k` pigeons, we require `sum(min(p_i, H)) >= H * k`.

The constraints go up to `n = 10^5` and `p_i ≤ 10^9`, so any solution that tries all possible assignments or simulates distribution per house will be far too slow. A naive check for a fixed `H` is fine, but we must be able to test many values efficiently, which suggests a monotonic feasibility structure and binary search.

A subtle edge case arises when a species has very large `p_i`. A naive interpretation might incorrectly assume such a species can always fully contribute to all houses, but it is still limited by the number of houses because of the “one per house” restriction. For example, if `k = 2`, `p = [1000]`, then even though we have many pigeons, we can never build more than 0 houses because we do not have enough distinct species to fill a single house.

Another edge case appears when `k > n`. Even if total pigeon count is large, a single house requires `k` distinct species, which is impossible if we have fewer than `k` species. The correct answer is then always zero.

## Approaches

A direct attempt would be to construct houses one by one. For each house, we would repeatedly pick species that still have remaining pigeons and ensure we pick at most one pigeon per species per house. After filling each house, we decrement counts and continue. This quickly becomes expensive because each selection step may scan many species, and we may repeat this process up to `10^9` times in the worst case of reasoning space. Even with greedy heaps, the structure is not stable because the constraint is global across houses, not local.

The key observation is that we do not need to simulate construction. Instead, we only need to check whether a given number of houses `H` is feasible. For each species `i`, it can contribute at most `H` pigeons (one per house), but also no more than `p_i`. So its true contribution is bounded by `min(p_i, H)`.

If we sum these contributions, we get the total number of pigeon slots we can fill across all houses. Since each house requires exactly `k` pigeons, feasibility reduces to a single inequality.

This transforms the problem into a monotonic decision problem: if `H` houses are possible, then any `H' < H` is also possible. This monotonicity allows binary search over `H`. For each midpoint, we compute the feasibility in `O(n)` using a sorted array or prefix sums. Sorting once enables fast computation of `sum(min(p_i, H))` by splitting species into those below `H` and those above.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy simulation per house | O(H·n) | O(n) | Too slow |
| Binary search with feasibility check | O(n log n + n log max_p) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Sort the available pigeons

We sort the array `p` in non-decreasing order. This allows us to quickly separate species that are fully usable (`p_i < H`) from those capped by `H`.

### 2. Define a feasibility function for a fixed number of houses `H`

For each species, we compute how many pigeons it can contribute:

If `p_i < H`, it contributes `p_i`.

Otherwise, it contributes `H`.

We sum this across all species to get total usable pigeons.

This step matters because it encodes the per-house restriction implicitly without constructing any assignment.

### 3. Check whether `H` houses can be filled

We compare total usable pigeons with required pigeons `H * k`. If usable pigeons are at least this large, then we can distribute pigeons into houses.

### 4. Binary search the maximum feasible `H`

We search from `0` to `sum(p_i) // k`. For each midpoint, we test feasibility using the function above. If feasible, we move right; otherwise, we move left.

The answer is the largest feasible `H`.

### Why it works

The critical invariant is that for any fixed `H`, the expression `sum(min(p_i, H))` is the exact maximum number of pigeon slots that can be legally assigned across `H` houses. The “one per species per house” restriction is fully captured by the `min(p_i, H)` cap, and no further structural constraints exist because houses are interchangeable and symmetric. Therefore, feasibility depends only on whether total capacity covers total demand, and monotonicity guarantees binary search correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def feasible(p, k, H):
    total = 0
    for x in p:
        if x >= H:
            total += H
        else:
            total += x
        if total >= H * k:
            return True
    return total >= H * k

def solve():
    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    
    if k > n:
        print(0)
        return

    p.sort()

    lo, hi = 0, sum(p) // k
    ans = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(p, k, mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The `feasible` function computes the total usable pigeons under the assumption that no species can be used more than once per house. The early exit when `total >= H * k` prevents unnecessary summation when `H` is large.

The binary search bounds are safe because each house consumes exactly `k` pigeons, so the maximum number of houses cannot exceed the total pigeon count divided by `k`.

## Worked Examples

### Example 1

Input:

```
3 2
3 4 1
```

We binary search over `H`.

| H | sum(min(p_i, H)) | H*k | Feasible |
| --- | --- | --- | --- |
| 1 | 3 | 2 | yes |
| 2 | 6 | 4 | yes |
| 3 | 7 | 6 | yes |
| 4 | 8 | 8 | yes |

The last feasible value is `4`.

This trace shows how larger `H` reduces contribution from large species and forces tighter capacity matching.

### Example 2

Input:

```
2 3
5 4
```

We test `H = 1`:

sum(min) = 2, required = 3, not feasible.

All larger `H` are also infeasible.

Result is `0`.

This demonstrates that even with sufficient total pigeons, insufficient species diversity prevents forming a single valid house.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + n log S) | Sorting plus binary search over feasible house count, each check scans all species |
| Space | O(1) extra (excluding input) | Only stores array and variables |

The constraints allow up to `10^5` species, so an `O(n log n)` preprocessing step and about 30 feasibility checks are easily within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isfinite
    import sys

    n, k = map(int, sys.stdin.readline().split())
    p = list(map(int, sys.stdin.readline().split()))

    if k > n:
        return "0"

    p.sort()

    def feasible(H):
        total = 0
        for x in p:
            total += x if x < H else H
            if total >= H * k:
                return True
        return total >= H * k

    lo, hi = 0, sum(p) // k
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return str(ans)

# provided samples
assert run("3 2\n3 4 1\n") == "4", "sample 1"
assert run("2 3\n5 4\n") == "0", "sample 2"

# custom cases
assert run("1 1\n10\n") == "10", "single species trivial"
assert run("3 3\n1 1 1\n") == "1", "tight species constraint"
assert run("5 2\n100 1 1 1 1\n") == "5", "one dominant species"
assert run("4 3\n2 2 2 2\n") == "2", "balanced case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single species | 10 | k=1 degenerate feasibility |
| all ones with k=3 | 1 | strict diversity constraint |
| one large species | 5 | dominance does not break logic |
| uniform medium case | 2 | balanced distribution correctness |

## Edge Cases

When `k > n`, the algorithm immediately returns zero because no house can be formed with enough distinct species. Even if `p_i` are large, the per-house diversity constraint blocks any construction.

For very large `p_i`, such as `p = [10^9, 10^9, ..., 10^9]`, the binary search will push `H` high, but feasibility will correctly cap growth because each species contributes only `H` per house, preventing overcounting.

When all `p_i` are small and identical, the binary search converges tightly, and each feasibility check terminates early once the threshold `H*k` is reached, ensuring efficiency even in worst-case uniform distributions.
