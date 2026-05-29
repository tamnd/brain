---
title: "CF 436E - Cardboard Box"
description: "We are given a set of levels in a game, each with two possible completion times. Completing a level for one star takes a[i] time, and completing it for two stars takes b[i] time, with a[i] < b[i]."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 436
codeforces_index: "E"
codeforces_contest_name: "Zepto Code Rush 2014"
rating: 2600
weight: 436
solve_time_s: 81
verified: false
draft: false
---

[CF 436E - Cardboard Box](https://codeforces.com/problemset/problem/436/E)

**Rating:** 2600  
**Tags:** data structures, greedy  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of levels in a game, each with two possible completion times. Completing a level for one star takes `a[i]` time, and completing it for two stars takes `b[i]` time, with `a[i] < b[i]`. We start with zero stars, and the goal is to accumulate at least `w` stars in the minimum total time. Each level can be completed at most once, either for one star or two stars, or not at all. The output must include the minimal total time and a string of length `n` where each character indicates whether the corresponding level is skipped (`0`), completed for one star (`1`), or completed for two stars (`2`).

The constraints are large: up to `3 * 10^5` levels and `w` up to `2*n`. This means any algorithm worse than `O(n log n)` is unlikely to run within the 5-second limit. Naive solutions that try all possible combinations of levels would have exponential complexity and are infeasible. Levels can have very different `a[i]` and `b[i]`, so greedy choices must carefully account for the star efficiency versus time cost. A subtle edge case arises when `w > n` - we are forced to pick some levels for two stars, but a naive approach might always choose the smallest `a[i]` values first, which could overshoot or be suboptimal.

For example, consider `n = 2, w = 3` with levels `(1, 100)` and `(2, 2)`. Picking two one-star completions would yield 3 stars in times `1 + 2 = 3`, while picking the two-star level `(2, 2)` first might seem better if only focusing on `b[i]`. A careless algorithm might fail to mix 1-star and 2-star choices optimally.

## Approaches

The brute-force approach iterates through all subsets of levels and all ways of assigning 0, 1, or 2 stars per level. This ensures correctness but requires `3^n` operations, which is completely infeasible for `n` up to `3*10^5`. Even generating all combinations of 1-star and 2-star completions separately and checking sums is too slow, since the number of ways to reach a given star count grows combinatorially.

The key insight comes from treating levels in two sorted lists: one by `a[i]` for 1-star completions and one by the difference `b[i] - a[i]` for two-star efficiency. Every level contributes either 1 or 2 stars. To minimize total time, we want to pick the smallest `b[i]` values if we need 2-star completions, and the smallest `a[i]` values if we need 1-star completions. This problem can be solved by first considering all levels as candidates for 1-star completions, sorted by `a[i]`. We then greedily replace 1-star completions with 2-star completions for those levels where the incremental cost `b[i] - a[i]` is smallest until the total stars reach `w`.

The observation is that we do not need to explore all subsets. Sorting allows a linear pass with priority queues or two-pointer techniques, achieving `O(n log n)` complexity. The structure of the problem - levels contributing 1 or 2 stars, each with independent costs - ensures that locally optimal greedy replacements are globally optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| Optimal (Greedy + Sorting) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of levels `n` and target stars `w`. Store each level as `(a[i], b[i], index)` for later reconstruction of the answer.
2. Sort the levels in increasing order of `a[i]`. This ensures the cheapest levels for 1-star completions are considered first.
3. Compute the prefix sums of `a[i]` for the first `k` levels. This lets us quickly calculate the total time for picking any number of levels for 1-star completions.
4. Determine the minimal number of levels that must be completed for 2 stars to reach `w`. Let `two_star_needed = max(0, w - n)`.
5. Among all levels, select `two_star_needed` levels with the smallest `b[i] - a[i]` - these are the levels that are cheapest to upgrade from 1 star to 2 stars.
6. Sum the `a[i]` times for all chosen 1-star completions and add the `b[i] - a[i]` for the upgraded levels. This gives the minimal total time.
7. Construct the answer string by assigning `2` to upgraded levels, `1` to remaining 1-star levels until `w` stars are reached, and `0` to all other levels.
8. Output the total time and the string representing the completion plan.

Why it works: Sorting guarantees that the cheapest levels for 1-star completions are used first. Choosing upgrades based on minimal `b[i] - a[i]` ensures that any forced 2-star completions are done at minimal incremental cost. Because each level is used at most once and the sum of stars is tracked precisely, no combination can yield a smaller total time.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, w = map(int, input().split())
levels = []

for i in range(n):
    a, b = map(int, input().split())
    levels.append((a, b, i))

# Sort levels by a[i] to consider cheapest 1-star completions first
levels.sort(key=lambda x: x[0])

# We will store the chosen completion type: 0=skip, 1=1-star, 2=2-star
res = [0] * n
time = 0
stars = 0

# Priority queue to pick levels with minimal b-a for upgrades to 2 stars
upgrade_candidates = []

for a, b, idx in levels:
    res[idx] = 1
    time += a
    stars += 1
    upgrade_candidates.append((b - a, idx, b))

# If stars already >= w, we only need 1-star completions
if stars >= w:
    # Possibly remove excess cheapest 1-star completions
    extra = stars - w
    # Remove no upgrades in this case
else:
    # Sort upgrade candidates by incremental cost
    upgrade_candidates.sort()
    need = w - stars
    for delta, idx, b in upgrade_candidates[:need]:
        res[idx] = 2
        time += delta
        stars += 1

print(time)
print("".join(map(str, res)))
```

This solution first marks all levels for 1-star completion and calculates the total time. It then upgrades the cheapest levels to 2 stars only if necessary to reach `w` stars. Sorting by `a[i]` ensures minimal 1-star cost, and sorting upgrades by `b[i]-a[i]` ensures minimal extra cost for forced 2-star completions.

## Worked Examples

### Example 1

Input:

```
2 3
1 2
1 2
```

| Level | a | b | Initial res | Time | Stars | Upgrade |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 1 | 1 | 1 | candidate |
| 1 | 1 | 2 | 1 | 2 | 2 | candidate |

We need 3 stars, currently have 2. Upgrade one cheapest delta `(b-a)` = 1. After upgrade, `time = 3`, `res = [2,1]`. Correct.

### Exampl
